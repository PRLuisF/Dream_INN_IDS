from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/habitaciones')
def habitaciones():
    return render_template('habitaciones.html')

@app.route('/about') 
def about():
    return render_template('about.html')

@app.route('/reserva', methods = ["GET", "POST"])
def hacer_reserva():
    if request.method == "POST":
        """
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        habitacion = request.form.get('habitacion')
        personas = request.form.get('cant_personas')
        fecha = request.form.get('fecha')
        noches = request.form.get('cant_noches')

        Falta integrar con API para verificar los datos y
        subirlos a la base de datos.
        """
        return render_template('mensaje_de_confirmacion.html', mensaje="La reserva se ha realizado exitosamente", id_reserva="1") #"1" es un placeholder, el ID debería generarse incrementativamente al guardar la reserva en la base de datos.
    return render_template('reserva.html')

@app.route('/cancelar-reserva', methods = ["GET", "POST"])
def cancelar_reserva():
    if request.method == "POST":
        nreserva = request.form.get('id_reserva')
        reservas = {1,2,3,4,5,6,7} #cuando se integra con la api se cambia por la request correspondiente
        if int(nreserva) in reservas: #cuando se integra con la api se cambia al estado de la request 
            return render_template('mensaje_de_confirmacion.html', mensaje="La reserva se ha cancelado exitosamente", id_reserva=nreserva)
        else:
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
