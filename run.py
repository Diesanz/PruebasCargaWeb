from app import create_app
from flask import render_template

# Crear la aplicación usando la función de fábrica
app = create_app()

@app.route('/')
def hello_world():
    return (app.template_folder)

@app.get('/login')
def login():
    return render_template('inicioSesion.html')

@app.get('/registro')
def registro():
    return render_template('registroUsuario.html')


if __name__ == '__main__':
    app.run(debug=True)



