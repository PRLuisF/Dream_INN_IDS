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

if __name__ == "__main__":
    app.run("127.0.0.1", port = 5000, debug = True)
