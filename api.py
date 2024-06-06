from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://root@localhost:3305/dreaminn_db")
#nota: la base de datos MySQL debe correr en el puerto 3305 (configurar el puerto de XAMPP, en mysql config)
    


@app.route("/generar_reserva", methods = ["POST"])
def generar_reserva():
    """Genera un nuevo registro en la tabla Reserva_Especifica con los datos en formato JSON pasados por el body de la
    request (nombre, email, tipo_habitacion, numero_habitacion, fecha_entrada, fecha_salida). Cambia el estado de la habitación
    a true en la tabla Habitaciones_Particulares, y devuelve un JSON con claves: mensaje, id_reserva.
    Nota: para que la tabla tome correctamente la fecha, se debe ingresar en formato YYYY-MM-DD."""

    reserva = request.get_json()
    with engine.connect() as conexion:

        validacion = text(f"SELECT * FROM Reserva_Especifica WHERE numero_habitacion = {reserva['numero_habitacion']};")

        try:
            val_resultado = conexion.execute(validacion)

            if val_resultado.rowcount != 0:            # si ya hay una reserva a ese número de habitación, no se puede reservar
                return jsonify({"mensaje": f"La habitacion {reserva['numero_habitacion']} ya esta ocupada"}), 400
            
            # agregar reserva
            query = text(f"INSERT INTO Reserva_Especifica (nombre, email, tipo_habitacion, numero_habitacion, fecha_entrada, fecha_salida) VALUES ('{reserva['nombre']}', '{reserva['email']}', '{reserva['tipo_habitacion']}', {reserva['numero_habitacion']}, '{reserva['fecha_entrada']}', '{reserva['fecha_salida']}');")
            conexion.execute(query)
            conexion.commit()

            # obtener id de reserva
            query_id = text(f"SELECT id FROM Reserva_Especifica WHERE numero_habitacion = {reserva['numero_habitacion']};")
            res_id = conexion.execute(query_id)
            id = res_id.fetchone().id

            # cambiar estado de habitación a true (ocupado)
            query_estado_habitacion = text(f"UPDATE Habitaciones_Particulares SET estado = true WHERE numero_habitacion = {reserva['numero_habitacion']};")
            conexion.execute(query_estado_habitacion)
            conexion.commit()

            # devolver mensaje de éxito e id
            return jsonify({"mensaje": "La reserva se ha realizado con exito", "id_reserva": id}), 201

        except SQLAlchemyError as error:
            return jsonify({"mensaje": f"Se ha producido un error: {error}"}), 500



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
    

@app.route('/modificar/<habitacion>', methods = ['PATCH'])
def update_habitacion(habitacion):
    conn = engine.connect()
    mod_data = request.get_json()

    query = f"UPDATE habitaciones SET cantidad_personas = {mod_data['cantidad_personas']}, precio = {mod_data['precio']}, descripcion = '{mod_data['descripcion']}', categoria = '{mod_data['categoria']}' WHERE habitacion = {habitacion}"
 
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



if __name__ == "__main__":
    app.run("127.0.0.1", port = 5000, debug = True)
