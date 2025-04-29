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
#esto quitalo y ponlo como un get de su controlador
# class Plato:

#     def __init__(self, id, nombre, descripcion, precio, stock, imagen_url):
#         self.id = id
#         self.nombre = nombre
#         self.descripcion = descripcion
#         self.precio = precio
#         self.stock = stock
#         self.imagen_url = imagen_url

# @app.get('/platos')
# def platos():

#     return render_template('platos.html')
 
#     platos = [
#         Plato(1, 'Ensalada de Pavo y Pina','1 lechuga. 200 gramos de pechuga de pavo asada. 200 gramos de queso feta. 90 gramos de cebollitas encurtidas. 1 lata de maíz dulce. 6 rodajas de piña, con su jugo. 1 zanahoria', 10.5, 10, '../static/img/ensaladaPavoPina.jpg'),
#         Plato(2, 'Pasta carbonara','400 g de spaghetti Garofalo. 200 g de panceta curada de cerdo. 50 g de queso Parmigiano Reggiano. 3 yemas y 1 huevo entero', 9.8, 80, '../static/img/pastacarbonara.jpg'),
#         Plato(3, 'Guisantes con Jamon y Sepia','3 dientes de ajo. 50 g de aceite de oliva. 300 g de sepia limpia. 90 - 100 g de jamón curado en dados. 100 g de vino blanco. 500 g de guisantes congelados', 11.2, 60, '../static/img/guisantesconjamonysepia.jpg') 
#     ]

#     return render_template('platos.html', platos=platos)

if __name__ == '__main__':
    app.run(debug=True)



