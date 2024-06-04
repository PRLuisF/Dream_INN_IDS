from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://root@localhost:3305/dreaminn_db")
#nota: la base de datos MySQL debe correr en el puerto 3305 (configurar el puerto de XAMPP, en mysql config)
    
@app.route("/Habitaciones_Particulares", methods=["GET"])
def mostrar_habitaciones() -> dict:
    """
    Se conecta a la base de datos dreaminn, y hace una consulta en la cual devuelve las habitaciones que no estan ocupadas
    """
    conn = engine.connect()
    query = "SELECT * FROM Habitaciones_Particulares WHERE estado = 1;"
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

@app.route("/cancelar-reserva/<id>", methods=['DELETE','PATCH'])
def cancelar_reserva(id):
    conn = engine.connect()
    validation_query = f"SELECT * FROM Reserva_Especifica WHERE id = {id};"
    try:
        val_result = conn.execute(text(validation_query))
        if val_result.rowcount != 0:
            row = val_result.fetchone()
            n_habitacion = row.numero_habitacion
            query1 = f"DELETE FROM Reserva_Especifica WHERE id = {id};"
            query2 = f"UPDATE Habitaciones_Particulares SET estado = false WHERE numero_habitacion = '{n_habitacion}';"
            resultado1 = conn.execute(text(query1))
            resultado2 = conn.execute(text(query2))
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
