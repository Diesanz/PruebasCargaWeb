from flask import Flask, request, jsonify, Blueprint, render_template, redirect, url_for, flash
from datetime import datetime, timedelta
from app.models.Carrito import Carrito
from app.models.itemCarrito import ItemCarrito, ItemCarritoDB
from app.models.Pedido import Pedido
from app.models.itemPedido import ItemPedido, ItemPedidoDB
from app.schemas.Carrito import carrito_schema
from app.schemas.itemCarrito import item_carrito_schema
from app.schemas.Pedido import pedido_schema
from app.schemas.itemPedido import item_pedido_schema, item_pedido_schema_db
from app.db.conexiondb import Conexion
from app.utils.comprobar_token import verificar_token #importar el decorador del token
from app.utils.carrito import get_id_carrito_usuario, get_carrito_items_usuario
from time import sleep

pedido = Blueprint('pedidoController', __name__, url_prefix="/api")

def crear_pedido(usuario_id: int):
    query = "INSERT INTO Pedido (usuario_id, estado) VALUES (%s, %s)"
    conn = Conexion()
    id = conn.execute_db(query, (usuario_id,"Pendiente",),return_last_id=True)
    conn.close_connection()
    return id

def get_join_items_productos(pedido_id: int):
    query = "SELECT p.* FROM PedidoItem as i JOIN Producto as p WHERE i.pedido_id = %s"

def get_pedidos_items(usuario_id: int):
    query = "SELECT * FROM Pedido WHERE usuario_id = %s"
    conn = Conexion()
    pedidos = conn.select_db(query, (usuario_id))

    lista_pedidos_items = []
    for i in pedidos:
        query_items = "SELECT * FROM PedidoItem WHERE pedido_id = %s"
        conn = Conexion()
        item_results = conn.select_db(query_items, (i['id'],))

        items_formateados = [ItemPedidoDB(**item_pedido_schema_db(item)) for item in item_results]
        
        lista_pedidos_items.append(Pedido(**pedido_schema(i, items_formateados)))

    return lista_pedidos_items

@pedido.route('/pedidos', methods=['GET'])
@verificar_token
def get_pedidos_usuario(usuario_id):
    pedidos = get_pedidos_items(usuario_id)
    for p in pedidos:
        p.getTotalPedido()
        print(p.precio_total)

@pedido.route('/checkout', methods=['POST'])
@verificar_token
def procesar_comprar(usuario_id):
    sleep(2)
    carrito = get_carrito_items_usuario(usuario_id)

    if not carrito:
        print("No se encontró carrito para el usuario.")
    
    if not carrito.items:
        return redirect(url_for('carritoController.get_items_carrito'))

    # 1. Crear el pedido
    id_pedido = crear_pedido(usuario_id)
    if not id_pedido:
        print("No se pudo crear el pedido.")
        
    # 2. Crear los items del pedido
    obj_items_pedido = [
        ItemPedidoDB(pedido_id=id_pedido, producto_id=i.producto_id, cantidad=i.cantidad, precio=i.precio).to_tuple()
        for i in carrito.items
    ]
    
    for item in obj_items_pedido:
        conn = Conexion()
        query = "INSERT into PedidoItem (pedido_id, producto_id, cantidad, precio) VALUES (%s, %s, %s, %s)"
        bien = conn.execute_db(query, (item))

    return jsonify({"message": "Pedido realizado exitosamente"}), 200