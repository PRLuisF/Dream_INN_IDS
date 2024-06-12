from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/habitaciones')
def habitaciones():
    habitaciones = requests.get("http://localhost:5000/habitaciones")
    if habitaciones.status_code == 200:
        respuesta_hab = habitaciones.json()
    
    elif habitaciones.status_code == 500:
        return render_template("500.html")

    return render_template('habitaciones.html', habitaciones=respuesta_hab)

@app.route('/about') 
def about():
    return render_template('about.html')

@app.route('/reserva', methods = ["GET", "POST"])
def hacer_reserva():
    if request.method == "POST":
        """
        nombre = request.form.get('id_nombre')
        apellido = request.form.get('id_apellido')
        email = request.form.get('id_email')
        habitacion = request.form.get('id_habitacion')
        fecha = request.form.get('fecha')
        noches = request.form.get('id_noches')

        Falta integrar con API para verificar los datos y
        subirlos a la base de datos.
        """
        return render_template('mensaje_de_confirmacion.html', mensaje="La reserva se ha realizado exitosamente", id_reserva="1") #"1" es un placeholder, el ID debería generarse incrementativamente al guardar la reserva en la base de datos.
    return render_template('reserva.html')

@app.route('/cancelar-reserva', methods = ["GET", "POST"])
def cancelar_reserva():
    if request.method == "POST":
        nreserva = request.form.get('id_reserva')
        respuesta = requests.delete(f"http://127.0.0.1:5000/cancelar-reserva/{nreserva}")
        if respuesta.status_code == 202:
            return render_template('mensaje_de_confirmacion.html', mensaje="La reserva se ha cancelado exitosamente", id_reserva=nreserva)
        elif respuesta.status_code == 404:
            return render_template('cancelacion.html', mensaje="No se encontró ninguna reserva con el número ingresado")
    return render_template('cancelacion.html')

@app.route('/detalles')
def detalle_habitacion():
    return render_template('room-details.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run("127.0.0.1", port = 8080, debug = True)
