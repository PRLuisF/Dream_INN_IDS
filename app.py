<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for
import requests
=======
from flask import Flask, render_template, request
>>>>>>> development

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/habitaciones')
def habitaciones():
<<<<<<< HEAD
    habitaciones = requests.get("http://localhost:5000/habitaciones")
    if habitaciones.status_code == 200:
        respuesta_hab = habitaciones.json()
    
    elif habitaciones.status_code == 500:
        return render_template("500.html")

    return render_template('habitaciones.html', habitaciones=respuesta_hab)
=======
    return render_template('habitaciones.html')
>>>>>>> development

@app.route('/about') 
def about():
    return render_template('about.html')

@app.route('/reserva', methods = ["GET", "POST"])
def hacer_reserva():
    if request.method == "POST":
<<<<<<< HEAD
=======
        """
>>>>>>> development
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        habitacion = request.form.get('habitacion')
<<<<<<< HEAD
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


=======
        personas = request.form.get('cant_personas')
        fecha = request.form.get('fecha')
        noches = request.form.get('cant_noches')

        Falta integrar con API para verificar los datos y
        subirlos a la base de datos.
        """
        return render_template('mensaje_de_confirmacion.html', mensaje="La reserva se ha realizado exitosamente", id_reserva="1") #"1" es un placeholder, el ID debería generarse incrementativamente al guardar la reserva en la base de datos.
    return render_template('reserva.html')

>>>>>>> development
@app.route('/cancelar-reserva', methods = ["GET", "POST"])
def cancelar_reserva():
    if request.method == "POST":
        nreserva = request.form.get('id_reserva')
<<<<<<< HEAD
        respuesta = requests.delete(f"http://127.0.0.1:5000/cancelar-reserva/{nreserva}")
        if respuesta.status_code == 202:
            return render_template('mensaje_de_confirmacion.html', mensaje="La reserva se ha cancelado exitosamente", id_reserva=nreserva)
        elif respuesta.status_code == 404:
=======
        reservas = {1,2,3,4,5,6,7} #cuando se integra con la api se cambia por la request correspondiente
        if int(nreserva) in reservas: #cuando se integra con la api se cambia al estado de la request 
            return render_template('mensaje_de_confirmacion.html', mensaje="La reserva se ha cancelado exitosamente", id_reserva=nreserva)
        else:
>>>>>>> development
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
