from app import create_app
from flask import render_template, redirect, url_for

# Crear la aplicación usando la función de fábrica
app = create_app()
@app.route('/')
def hello_world():
    return redirect(url_for('api_index'))  # Referencia la función api_index en el blueprint api

# Ruta de la API
@app.route('/api')
def api_index():
    return render_template("index.html")  # Renderiza el template para /api

#esto quitalo y ponlo como un get de su controlador
@app.get('/platos')
def platos():
    return render_template('platos.html')

if __name__ == '__main__':
    app.run(debug=True)



