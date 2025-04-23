from app import create_app
from flask import render_template

# Crear la aplicación usando la función de fábrica
app = create_app()

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.get('/login')
def login():
    return render_template('inicioSesion.html')

@app.get('/registro')
def registro():
    return render_template('registroUsuario.html')

@app.get('/carrito')
def carrito():
    return render_template('carrito.html')

@app.get('/platos')
def platos():
    return render_template('platos.html')

if __name__ == '__main__':
    app.run(debug=True)



