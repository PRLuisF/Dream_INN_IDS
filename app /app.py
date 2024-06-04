from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/habitaciones')
def tipos_habitaciones():
    return render_template('habitaciones.html')

@app.route('/about') 
def about():
    return render_template('about.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/cancelar-reserva')
def cancerlar_reserva():
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
    app.run(debug=True)
