from flask import Flask, request, jsonify, Blueprint, render_template, redirect, url_for, flash
from datetime import datetime, timedelta
from app.models.Carrito import Carrito
from app.models.itemCarrito import ItemCarrito, ItemCarritoDB
from app.schemas.Carrito import carrito_schema
from app.schemas.itemCarrito import item_carrito_schema
from app.db.conexiondb import Conexion
from app.utils.comprobar_token import verificar_token #importar el decorador del token
from app.utils.carrito import get_carrito_items_usuario

carrito = Blueprint('carritoController', __name__, url_prefix="/api/carrito")

def get_id_carrito_usuario(usuario_id: str):
    """
    Obtiene el ID del carrito asociado a un usuario específico.

    Args:
        usuario_id (str): ID del usuario.

    Returns:
        int or Tuple: ID del carrito si existe, o una respuesta JSON con error 404 si no se encuentra.
    """
    
    query_db = "SELECT id FROM Carrito WHERE usuario_id = %s"
    conn = Conexion()
    id_carrito = conn.select_db(query_db, (usuario_id,), one=True)
    conn.close_connection()

    if not id_carrito:
        return jsonify({"error": "Carrito no encontrado para el usuario."}), 404 

    return id_carrito['id']

def get_datos_producto(id_producto: str): #cambiar esto para que devuelva un objeto
    """
    Obtiene los datos de un producto desde la base de datos a partir de su ID.

    Args:
        id_producto (str): Identificador único del producto.

    Returns:
        tuple | Response: Tupla con los datos del producto (nombre, precio) si existe,
        o una respuesta JSON con error 404 si no se encuentra.
    """

    query_db = "SELECT nombre, precio FROM Producto WHERE id = %s"
    conn = Conexion()
    producto = conn.select_db(query_db, (id_producto,), one=True)
    conn.close_connection()

    if not producto:
        return jsonify({"error": "Producto no encontrado."}), 404

    return producto


@carrito.route('/', methods=['GET'])
@verificar_token
def get_items_carrito(usuario_id):
    """
    Muestra los productos actuales en el carrito del usuario autenticado.

    Args:
        usuario_id (int): ID del usuario autenticado extraído del token.

    Returns:
        Response: Renderiza la plantilla del carrito con los productos y el total si existe,
        o la plantilla de inicio con un mensaje de error si el carrito no fue encontrado.
    """

    carrito = get_carrito_items_usuario(usuario_id)
    if isinstance(carrito, Carrito):
        total_carrito = carrito.getTotalCarrito()
        items_json = [item_carrito_schema(item, True) for item in carrito.items]
        
        return render_template("carrito.html", items=items_json, total=total_carrito)

    return render_template("index.html", error="Carrito no encontrado", items=[], total=0)

#Endpoint encargado de vaciar el carrito del usuario
@carrito.route('/vaciar', methods=['DELETE'])
@verificar_token
def delete_items_carrito(usuario_id):
    """
    Elimina (vacía) todos los productos del carrito del usuario autenticado.

    Args:
        usuario_id (int): ID del usuario autenticado extraído del token.

    Returns:
        Response: 
            - JSON con mensaje de éxito si se vació el carrito correctamente (HTTP 200).
            - JSON con mensaje de error si no se encontró el carrito (HTTP 404).
    """
    carrito = get_carrito_items_usuario(usuario_id)
    
    if isinstance(carrito, Carrito):
        carrito_id = carrito.id

        # Conexión a la base de datos y eliminación de los ítems
        conn = Conexion()
        query_db = "DELETE FROM CarritoItem WHERE carrito_id = %s"
        borrado_exitoso = conn.execute_db(query_db, (carrito_id,))
        conn.close_connection()

        if borrado_exitoso:
            return jsonify({"message": "Carrito vaciado exitosamente"}), 200

    return jsonify({"error": "No se encontró el carrito del usuario"}), 404

#Endpoint encargado de agregar un producto al carrito
@carrito.route('/agregar', methods=['POST'])
@verificar_token
def add_item_carrito(usuario_id):
    
    """
    Agrega un producto al carrito del usuario autenticado.

    Este endpoint espera un JSON con el campo 'id_producto'. Luego:
    - Busca el producto en la base de datos.
    - Si existe, crea un objeto del ítem del carrito.
    - Llama a un procedimiento almacenado para añadir o actualizar el producto en el carrito.

    Args:
        usuario_id (int): ID del usuario autenticado.

    Returns:
        Response: 
            - JSON con el ítem añadido o actualizado (HTTP 200).
            - JSON con mensaje de error si falta el ID del producto (HTTP 400).
    """

    # Paso 1: Obtener los datos del cuerpo de la solicitud (el JSON)
    data = request.get_json()
    id_producto = data.get('id_producto')  # El ID del producto a agregar

    if not id_producto:
        return jsonify({"error": "El id_producto es obligatorio."}), 400

    # Paso 2: Consultar la base de datos para obtener el producto
    producto = get_datos_producto(id_producto)

    item_carrito_db = ItemCarritoDB(
        producto_id=id_producto,
        cantidad=1,
        carrito_id=get_id_carrito_usuario(usuario_id)
    )

    # Paso 3: Añadir item al carrito o actualizar su cantidad
    conn = Conexion()
    success_id=conn.procedure('AddOrUpdateItemCarrito', item_carrito_db.to_tuple())
    conn.close_connection()
    
    # Devolver el ítem agregado o actualizado como una respuesta JSON
    return jsonify({
        "message": "Item añadido al carrito",
        "item": item_carrito_db.dict()  # Devuelve los datos del ítem recién agregado o actualizado
    }), 200