from flask import Flask, request, jsonify, Blueprint, render_template, redirect, url_for, flash
from datetime import datetime, timedelta
from app.models.Carrito import Carrito
from app.models.itemCarrito import ItemCarrito, ItemCarritoDB
from app.schemas.Carrito import carrito_schema
from app.schemas.itemCarrito import item_carrito_schema
from app.db.conexiondb import Conexion
from app.utils.comprobar_token import verificar_token #importar el decorador del token

carrito = Blueprint('carritoController', __name__, url_prefix="/api/carrito")

#añadir funcion getProducto

def get_id_carrito_usuario(usuario_id: str):
    query_db = "SELECT id FROM Carrito WHERE usuario_id = %s"
    conn = Conexion()
    id_carrito = conn.select_db(query_db, (usuario_id,), one=True)

    return id_carrito['id']

@carrito.route('/agregar', methods=['POST'])
@verificar_token
def add_item_carrito(usuario_id):
    """
    Agrega un producto al carrito del usuario.

    - Se recibe un JSON con el id del producto.
    - Se obtiene el producto desde la base de datos.
    - Se agrega o actualiza el ítem en el carrito del usuario.
    """

    # Paso 1: Obtener los datos del cuerpo de la solicitud (el JSON)
    data = request.get_json()
    id_producto = data.get('id_producto')  # El ID del producto a agregar

    if not id_producto:
        return jsonify({"error": "El id_producto es obligatorio."}), 400

    # Paso 2: Consultar la base de datos para obtener el producto
    query_db = "SELECT nombre, precio FROM Producto WHERE id = %s"
    conn = Conexion()
    producto = conn.select_db(query_db, (id_producto,), one=True)

    if not producto:
        return jsonify({"error": "Producto no encontrado."}), 404

    # Extraemos los datos del producto
    nombre = producto['nombre']
    precio = producto['precio']

    # Paso 3: Obtener el ID del carrito del usuario
    id_carrito = get_id_carrito_usuario(usuario_id)

    if not id_carrito:
        return jsonify({"error": "Carrito no encontrado para el usuario."}), 404 #sustituir por un pocedimiento qaue se encarge de todo

    # Paso 4: Verificar si el producto ya existe en el carrito
    query_check = "SELECT cantidad FROM CarritoItem WHERE carrito_id = %s AND producto_id = %s"
    item_existente = conn.select_db(query_check, (id_carrito, id_producto), one=True)

    if item_existente:
        # Si el producto ya está en el carrito, se actualiza la cantidad
        nueva_cantidad = item_existente['cantidad'] + 1
        query_update = "UPDATE CarritoItem SET cantidad = %s WHERE carrito_id = %s AND producto_id = %s"
        conn.execute_db(query_update, (nueva_cantidad, id_carrito, id_producto))
        message = "Producto actualizado en el carrito."
    else:
        # Si el producto no está en el carrito, se agrega un nuevo ítem
        query_insert = "INSERT INTO CarritoItem (carrito_id, producto_id, nombre, cantidad, precio) VALUES (%s, %s, %s, %s, %s)"
        conn.execute_db(query_insert, (id_carrito, id_producto, nombre, 1, precio))
        message = "Producto agregado al carrito exitosamente."

    # Crear el objeto de ItemCarritoDB y devolver el resultado
    item_carrito_db = ItemCarritoDB(
        producto_id=id_producto,
        nombre=nombre,
        cantidad=1,
        precio=precio,
        carrito_id=id_carrito
    )

    # Devolver el ítem agregado o actualizado como una respuesta JSON
    return jsonify({
        "message": message,
        "item": item_carrito_db.dict()  # Devuelve los datos del ítem recién agregado o actualizado
    }), 200


