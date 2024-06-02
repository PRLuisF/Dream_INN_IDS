from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/habitaciones')
def tipos_habitaciones():
    return render_template('habitaciones.html')

@app.route('/introduction')
def intro():
    return render_template('introduction.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/contact')
def contact():
    return render_template('cancelacion.html')

@app.route('/detalles')
def details():
    return render_template('room-details.html')

if __name__ == '__main__':
    app.run(debug=True)
