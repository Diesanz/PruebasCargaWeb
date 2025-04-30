from flask import Flask, request, jsonify, Blueprint, render_template, redirect, url_for, flash, make_response
from app.db.conexiondb import Conexion
from app.models.Producto import Producto
from app.schemas.Producto import producto_schema

producto = Blueprint('producto', __name__, url_prefix="/api")

def get_produtosdb():
    conn = Conexion()
    query = "SELECT * FROM Producto" 
    productos = conn.select_db(query)
    
    productos_obj = [Producto(**producto_schema(p)) for p in productos] #validamos datos y tipamos
    
    return productos

@producto.route('/productos', methods=['GET'])
def api_index():
    return render_template("platos.html", productos = get_produtosdb()) # Renderiza el template para /api

@producto.route('/detalles/<int:id>')
def producto_detalle(id):
    producto = obtener_producto_por_id(id)
    if producto:
        return render_template('detallesProducto.html', producto=producto)
    else:
        return "Producto no encontrado", 404

def obtener_producto_por_id(id):
    conn = Conexion()
    query = "SELECT * FROM Producto p WHERE p.id=%s" 
    producto = conn.select_db(query, (id,))
    if producto:
        return producto[0]
    return None  