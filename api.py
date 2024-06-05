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



@app.route("/Habitaciones_Particulares", methods=["GET"])
def mostrar_habitaciones() -> dict:
    """
    Se conecta a la base de datos dreaminn, y hace una consulta en la cual devuelve las habitaciones que no estan ocupadas
    """
    conn = engine.connect()
    query = "SELECT * FROM Habitaciones_Particulares WHERE estado = 0;"
    try:
        habs = conn.execute(text(query))
        conn.close()
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))

    datos = []
    for dato in habs:
        print(dato)
        hab = {}
        hab['id'] = dato[0]
        hab['tipo'] = dato[1]
        hab['estado'] = dato[2]
        datos.append(hab)
    
    return jsonify(datos), 200



@app.route("/Tipo_Habitaciones", methods = ['GET'])
def mostrar_tipos():

    conn = engine.connect()
    query = "SELECT * FROM Tipo_Habitaciones;"
    try:
        tipos = conn.execute(text(query))
        conn.close() 
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))
    
    datos = []
    for dato in tipos:
        informacion = {}
        informacion['tipo_habitacion'] = dato.tipo_habitacion
        informacion['descripcion'] = dato.descripcion
        informacion['precio'] = dato.precio
        datos.append(informacion)

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



if __name__ == "__main__":
    app.run("127.0.0.1", port = 5000, debug = True)