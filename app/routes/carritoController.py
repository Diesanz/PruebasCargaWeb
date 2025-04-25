from flask import Flask, request, jsonify, Blueprint, render_template, redirect, url_for, flash
from datetime import datetime, timedelta
from app.models.Carrito import Carrito
from app.models.itemCarrito import ItemCarrito, ItemCarritoDB
from app.schemas.Carrito import carrito_schema
from app.schemas.itemCarrito import item_carrito_schema
from app.db.conexiondb import Conexion
from app.utils.comprobar_token import verificar_token #importar el decorador del token

carrito = Blueprint('carritoController', __name__, url_prefix="/api/carrito")

def get_id_carrito_usuario(usuario_id: str):
    query_db = "SELECT id FROM Carrito WHERE usuario_id = %s"
    conn = Conexion()
    id_carrito = conn.select_db(query_db, (usuario_id,), one=True)

    if not id_carrito:
        return jsonify({"error": "Carrito no encontrado para el usuario."}), 404 

    return id_carrito['id']

def get_datos_producto(id_producto: str): #cambiar esto para que devuelva un objeto
    query_db = "SELECT nombre, precio FROM Producto WHERE id = %s"
    conn = Conexion()
    producto = conn.select_db(query_db, (id_producto,), one=True)

    if not producto:
        return jsonify({"error": "Producto no encontrado."}), 404

    return producto

def get_carrito_items_usuario(usuario_id: str) -> Carrito:
    query_db = "SELECT * FROM Carrito WHERE usuario_id = %s"
    conn = Conexion()
    carrito = conn.select_db(query_db, (usuario_id,), one=True)
    
    #obtner los items
    query_db_items = "SELECT * FROM CarritoItem WHERE carrito_id = %s"
    conn = Conexion()
    items = conn.select_db(query_db_items, (carrito['id'],), one=False)
    
    lista_items = [ItemCarrito(**item_carrito_schema(i)) for i in items]
   
    return Carrito(**carrito_schema(carrito, lista_items))

@carrito.route('/', methods=['GET'])
@verificar_token
def get_items_carrito(usuario_id):
    carrito = get_carrito_items_usuario(usuario_id)
    if isinstance(carrito, Carrito):
        # Obtener el total del carrito
        total_carrito = carrito.getTotalCarrito()

        # Convertir los ítems a JSON usando el esquema
        items_json = [item_carrito_schema(item, True) for item in carrito.items] #indicar que se van a para al schema objetos

        # Crear el objeto de respuesta con el total y los ítems
        response_data = {
            "total": total_carrito,  # Total con dos decimales
            "items": items_json  # Lista de ítems convertidos con el esquema
        }

        return jsonify(response_data)
    
    return jsonify({"error": "Carrito no encontrado"}), 404

@carrito.route('/vaciar', methods=['DELETE'])
@verificar_token
def delete_items_carrito(usuario_id):
    carrito = get_carrito_items_usuario(usuario_id)
    
    if isinstance(carrito, Carrito):
        carrito_id = carrito.id

        # Conexión a la base de datos y eliminación de los ítems
        conn = Conexion()
        query_db = "DELETE FROM CarritoItem WHERE carrito_id = %s"
        borrado_exitoso = conn.execute_db(query_db, (carrito_id,))

        if borrado_exitoso:
            return jsonify({"message": "Carrito vaciado exitosamente"}), 200

    return jsonify({"error": "No se encontró el carrito del usuario"}), 404


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
    producto = get_datos_producto(id_producto)

    item_carrito_db = ItemCarritoDB(
        producto_id=id_producto,
        nombre=producto['nombre'],
        cantidad=1,
        precio=producto['precio'],
        carrito_id=get_id_carrito_usuario(usuario_id)
    )

    # Paso 3: Añadir item al carrito o actualizar su cantidad
    conn = Conexion()
    success_id=conn.procedure('AddOrUpdateItemCarrito', item_carrito_db.to_tuple())

    # Devolver el ítem agregado o actualizado como una respuesta JSON
    return jsonify({
        "message": "Item añadido al carrito",
        "item": item_carrito_db.dict()  # Devuelve los datos del ítem recién agregado o actualizado
    }), 200


