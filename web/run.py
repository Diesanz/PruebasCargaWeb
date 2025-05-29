from app import create_app
from flask import render_template, redirect, url_for

# Crear la aplicación usando la función de fábrica
app = create_app()

@app.route('/')
def hello_world():
    return redirect(url_for('menu.api_index'))    # Referencia la función api_index en el blueprint api

def sumar_dias(fecha, dias):
    from datetime import timedelta
    return fecha + timedelta(days=dias)

app.jinja_env.filters['suma_dias'] = sumar_dias

if __name__ == '__main__':
    app.run(host='10.0.31.22', debug=False)



