from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta

app = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://root@localhost:3305/dreaminn_db")
#nota: la base de datos MySQL debe correr en el puerto 3305 (configurar el puerto de XAMPP, en mysql config)
    


@app.route("/generar-reserva", methods = ["POST"])
def generar_reserva():
    """Genera un nuevo registro en la tabla Reserva_Especifica con los datos en formato JSON pasados por el body de la
    request (nombre, apellido, email, fecha_ingreso, cantidad_noches, cantidad_personas, habitacion)
    Nota: para que la tabla tome correctamente la fecha, se debe ingresar en formato YYYY-MM-DD."""

    datos_body = request.get_json()
    with engine.connect() as conn:
        validacion1 = text(f"SELECT cantidad_personas FROM habitaciones WHERE habitacion = {datos_body['habitacion']};")
        validacion2 = text(f"SELECT fecha_ingreso, cantidad_noches, habitacion FROM reservas;")
        query = text(f"INSERT INTO reservas (nombre, apellido, email, fecha_ingreso, cantidad_noches, cantidad_personas, habitacion) VALUES ('{datos_body['nombre']}', '{datos_body['apellido']}', '{datos_body['email']}', '{datos_body['fecha_ingreso']}', '{datos_body['cantidad_noches']}', '{datos_body['cantidad_personas']}', '{datos_body['habitacion']}');")

        try:
            res_validacion1 = conn.execute(validacion1)
            res_validacion2 = conn.execute(validacion2)

            # verificar que cantidad de personas sea correcta
            if res_validacion1.first().cantidad_personas < datos_body["cantidad_personas"]:
                return jsonify({"mensaje": "Error: la cantidad de personas supera la capacidad de la habitacion"}), 400
            
            # verificar que fechas no se solapen
            elif res_validacion2.rowcount != 0:
                fecha_ingreso = datetime.strptime(datos_body["fecha_ingreso"], "%Y-%m-%d")
                cant_noches = timedelta(days = datos_body["cantidad_noches"])

                for fil in res_validacion2:
                    fecha_reserva = datetime(fil.fecha_ingreso.year, fil.fecha_ingreso.month, fil.fecha_ingreso.day)
                    noches_reserva = timedelta(days = fil.cantidad_noches)

                    if fecha_reserva <= fecha_ingreso < fecha_reserva + noches_reserva and fil.habitacion == datos_body["habitacion"]:
                        return jsonify({"mensaje": "Error: la habitacion esta ocupada en esas fechas."}), 400
                    elif fecha_reserva < fecha_ingreso + cant_noches <= fecha_reserva + noches_reserva and fil.habitacion == datos_body["habitacion"]:
                        return jsonify({"mensaje": "Error: la habitacion esta ocupada en esas fechas."}), 400

            # guardar reserva    
            conn.execute(query)
            conn.commit()

            # obtener id de reserva para devolverlo en el json
            query_id = text(f"SELECT id FROM reservas WHERE habitacion = {datos_body['habitacion']} AND fecha_ingreso = '{datos_body['fecha_ingreso']}' AND cantidad_noches = {datos_body['cantidad_noches']};")
            id = conn.execute(query_id)
            id = id.first().id

        except SQLAlchemyError as error:
            return jsonify({"mensaje": f"Error {error.__cause__}"}), 500
        
        return jsonify({"mensaje": "La reserva se ha creado correctamente", "id_reserva": id}), 201

        
@app.route("/cancelar-reserva/<id>", methods=['DELETE'])
def cancelar_reserva(id):
    conn = engine.connect()
    validation_query = f"SELECT * FROM reservas WHERE id = {id};"
    try:
        val_result = conn.execute(text(validation_query))
        if val_result.rowcount != 0:
            query1 = f"DELETE FROM reservas WHERE id = {id};"
            resultado1 = conn.execute(text(query1))
            conn.commit()
            conn.close()
            return jsonify({"message": "La reserva se ha cancelado correctamente"}), 202
        else:
            conn.close()
            return jsonify({"message": "No existe la reserva de tal ID"}), 404
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))



@app.route("/habitaciones", methods=["GET"])
def mostrar_habitaciones():
    """
    Se conecta a la base de datos dreaminn, y hace una consulta en la cual devuelve las habitaciones que no estan ocupadas
    """
    conn = engine.connect()
    query = "SELECT * FROM habitaciones;"
    try:
        habs = conn.execute(text(query))
        conn.close()
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))

    datos = []
    for dato in habs:
        hab = {}
        hab['habitacion'] = dato.habitacion
        hab['cantidad_personas'] = dato.cantidad_personas
        hab['precio'] = dato.precio
        hab['descripcion'] = dato.descripcion
        hab['categoria'] = dato.categoria
        datos.append(hab)
    
    return jsonify(datos), 200


@app.route('/agregar-habitacion', methods=['POST'])
def incorporar_habitacion():
    conn = engine.connect()
    nueva_hab = request.get_json()
    query = f"""INSERT INTO habitaciones VALUES
                ({nueva_hab["habitacion"]}, {nueva_hab["cantidad_personas"]}, {nueva_hab["precio"]}, '{nueva_hab["descripcion"]}', '{nueva_hab["categoria"]}');"""
    try:
        resultado = conn.execute(text(query))
        conn.commit()
        conn.close()
        return jsonify({"message": "Se ha incorporado correctamente la nueva habitacion a la base de datos"}), 201
    except SQLAlchemyError as err:
        return jsonify({"message": "Se ha producido un error " + str(err.__cause__)})
    

@app.route('/modificar/<habitacion>', methods = ['PATCH'])
def update_habitacion(habitacion):
    conn = engine.connect()
    mod_data = request.get_json()

    query = f"UPDATE habitaciones SET "
    for columna,dato in mod_data.items():
        if type(dato) == str:
            query += f"{columna} = '{dato}',"
        else:
            query += f"{columna} = {dato} ,"
    query = query[:-1]
    query += f"WHERE habitacion = {habitacion};"
 
    query_validation = f"SELECT * FROM habitaciones WHERE habitacion = {habitacion};"
    try:
        val_result = conn.execute(text(query_validation))
        if val_result.rowcount!=0:
            result = conn.execute(text(query))
            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify({'message': "La habitacion no existe"}), 404
    except SQLAlchemyError as err:
        return jsonify({'message': str(err.__cause__)})
    return jsonify({'message': 'La habitacion se ha modificado correctamente'}), 200


@app.route('/eliminar/<habitacion>', methods = ['DELETE'])
def eliminar_habitacion(habitacion):
    conn = engine.connect()

    query = f"DELETE from habitaciones WHERE habitacion = {habitacion}"
    
    validation_query = f"SELECT * FROM habitaciones WHERE habitacion = {habitacion}"
    try:
        val_result = conn.execute(text(validation_query))
        if val_result.rowcount != 0 :
            result = conn.execute(text(query))
            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify({"message": "La habitacion no existe"}), 404
    except SQLAlchemyError as err:
        jsonify(str(err.__cause__))
    return jsonify({'message': 'La habitacion se elimino correctamente'}), 202


if __name__ == "__main__":
    app.run("127.0.0.1", port = 5000, debug = True)
