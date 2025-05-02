from flask import Flask, request, jsonify, Blueprint, render_template, redirect, url_for, flash, make_response
from app.db.conexiondb import Conexion
from app.models.Producto import Producto
from app.schemas.Producto import producto_schema

producto = Blueprint('producto', __name__, url_prefix="/api")

#Método que se encarga de obtener los productos de la base de datos
def get_produtosdb():
    conn = Conexion()
    query = "SELECT * FROM Producto" 
    productos = conn.select_db(query)
    
    return productos

#Método que se encarga de obtener el producto de la base de datos según su identificador
def obtener_producto_por_id(id):
    conn = Conexion()
    query = "SELECT * FROM Producto p WHERE p.id=%s" 
    producto = conn.select_db(query, (id,))

    if producto:
        return producto[0]
    return None  

#Endpoint encargado de mostrar la lista de productos
@producto.route('/productos', methods=['GET'])
def api_index():
    return render_template("platos.html", productos = get_produtosdb()) # Renderiza el template para /api

#Endpoint encargado de mostrar los detalles de un producto seleccionado
@producto.route('/productos/<int:id>')
def producto_detalle(id):
    producto = obtener_producto_por_id(id)
    
    if producto:
        return render_template('detallesProducto.html', producto=producto)
    else:
        return "Producto no encontrado", 404

