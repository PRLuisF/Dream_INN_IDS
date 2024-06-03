from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://root@localhost:3305/dreaminn_db")
# nota: la base de datos MySQL debe correr en el puerto 3305 (configurar el puerto de XAMPP, en mysql config)
    

if __name__ == "__main__":
    app.run("127.0.0.1", port = 5000, debug = True)