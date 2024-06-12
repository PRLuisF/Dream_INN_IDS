from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/habitaciones')
def habitaciones():
    habitaciones = requests.get("http://localhost:5000/habitaciones").json()
    return render_template('habitaciones.html', habitaciones=habitaciones)

@app.route('/about') 
def about():
    return render_template('about.html')

@app.route('/reserva', methods = ["GET", "POST"])
def hacer_reserva():
    if request.method == "POST":
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        habitacion = request.form.get('habitacion')
        fecha = request.form.get('fecha')
        noches = request.form.get('cant_noches')
        cantidad_personas = request.form.get('cant_personas')

        if nombre and apellido and email and habitacion and fecha and noches and cantidad_personas:
            habitacion = int(habitacion)
            noches = int(noches)
            cantidad_personas = int(cantidad_personas)

            datos = {"nombre": nombre, "apellido": apellido, "email": email, "habitacion": habitacion, "fecha_ingreso": fecha,
                     "cantidad_noches": noches, "cantidad_personas": cantidad_personas}
            request_api = requests.post("http://localhost:5000/generar-reserva", json = datos)

            if request_api.status_code == 400:
                return render_template('reserva.html', mensaje = "La cantidad de personas ingresada supera la capacidad de la habitación.")
            if request_api.status_code == 409:
                return render_template('reserva.html', mensaje = "La fecha ingresada no se encuentra disponible.")
            if request_api.status_code == 500:
                return redirect(url_for('internal_server_error'))
            if request_api.status_code == 201:
                request_api = request_api.json()
                id = request_api["id_reserva"]
                return render_template('mensaje_de_confirmacion.html', mensaje="La reserva se ha realizado exitosamente", id_reserva=id)

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
