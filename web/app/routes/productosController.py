from flask import Flask, request, jsonify, Blueprint, render_template, redirect, url_for, flash, make_response
from app.db.conexiondb import Conexion
from app.models.Producto import Producto
from app.schemas.Producto import producto_schema

producto = Blueprint('producto', __name__, url_prefix="/api")

#Método que se encarga de obtener los productos de la base de datos
def get_produtosdb():
    """
    Obtiene todos los productos disponibles en la base de datos.

    Returns:
        list[dict]: Lista de instacions de objeto Producto.
    """

    conn = Conexion()
    query = "SELECT * FROM Producto" 
    productos = conn.select_db(query)
    conn.close_connection()
    
    return [Producto(**producto_schema(p)) for p in productos]

#Método que se encarga de obtener el producto de la base de datos según su identificador
def obtener_producto_por_id(id):
    """
    Obtiene los detalles de un producto a partir de su identificador único.

    Args:
        id (int): ID del producto a buscar.

    Returns:
        dict or None: Producto con sus datos si existe si no existe devuelve None.
    """

    conn = Conexion()
    query = "SELECT * FROM Producto p WHERE p.id=%s" 
    producto = conn.select_db(query, (id,), one=True)
    conn.close_connection()

    return Producto(**producto_schema(producto)) if producto else None 

#Endpoint encargado de mostrar la lista de productos
@producto.route('/productos', methods=['GET'])
def api_index():
    """
    Renderiza la vista con el listado de todos los productos disponibles.

    Returns:
        HTML: Página renderizada con la lista de productos.
    """
    return render_template("platos.html", productos = get_produtosdb()) # Renderiza el template para /api

#Endpoint encargado de mostrar los detalles de un producto seleccionado
@producto.route('/productos/<int:id>')
def producto_detalle(id: int):
    """
    Renderiza la vista con los detalles de un producto específico.

    Args:
        id (int): ID del producto a visualizar.

    Returns:
        HTML or Tuple: Página renderizada con los detalles del producto si existe,
        o una respuesta 404 si no se encuentra.
    """

    producto = obtener_producto_por_id(id)
    
    if isinstance(producto, Producto):
        return render_template('detallesProducto.html', producto=producto)
    else:
        return "Producto no encontrado", 404

