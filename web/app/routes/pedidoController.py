from flask import Flask, request, jsonify, Blueprint, render_template, redirect, url_for, flash
from datetime import datetime, timedelta
from app.models.Carrito import Carrito
from app.models.itemCarrito import ItemCarrito, ItemCarritoDB
from app.models.Pedido import Pedido
from app.models.itemPedido import ItemPedido, ItemPedidoDB
from app.models.Producto import Producto
from app.schemas.Carrito import carrito_schema
from app.schemas.itemCarrito import item_carrito_schema
from app.schemas.Pedido import pedido_schema
from app.schemas.itemPedido import item_pedido_schema, item_pedido_schema_db
from app.schemas.Producto import producto_schema
from app.db.conexiondb import Conexion
from app.utils.comprobar_token import verificar_token #importar el decorador del token
from app.utils.carrito import get_carrito_items_usuario
from time import sleep

pedido = Blueprint('pedidoController', __name__, url_prefix="/api")

#Método que crea un pedido al usuario
def crear_pedido(usuario_id: int):
    """
    Crea un nuevo pedido con estado 'Pendiente' para el usuario especificado.

    Args:
        usuario_id (int): ID del usuario que realiza el pedido.

    Returns:
        int: ID del nuevo pedido creado.
    """

    query = "INSERT INTO Pedido (usuario_id, estado) VALUES (%s, %s)"
    conn = Conexion()
    id = conn.execute_db(query, (usuario_id,"Pendiente",),return_last_id=True)
    conn.close_connection()
    return id

#Método que muestra el numero total de pedidos de un usuario
def get_total_pedidos(usuario_id: int):
    """
    Obtiene el número total de pedidos realizados por un usuario.

    Args:
        usuario_id (int): ID del usuario.

    Returns:
        int: Total de pedidos realizados por el usuario.
    """

    query_total = "SELECT COUNT(*) as num FROM Pedido WHERE usuario_id = %s"
    conn = Conexion()
    total_pedidos = conn.select_db(query_total, (usuario_id,))

    return total_pedidos [0]["num"]

#Método que muetsra la lista de productos de los pedidos
def get_pedidos_items(usuario_id: int, page:int):
    """
    Obtiene los pedidos paginados de un usuario, junto con los productos de cada pedido.

    Args:
        usuario_id (int): ID del usuario.
        page (int): Número de página actual.

    Returns:
        dict: Contiene:
            - 'lista_i': Lista de objetos Pedido con sus items.
            - 'page': Página actual.
            - 'total_pages': Total de páginas de pedidos.
    """

    items_por_pagina = 4  # Número de productos por página
    # Cálculo para obtener los pedidos de la página actual
    offset = (page - 1) * items_por_pagina  # Determina el punto de inicio de los pedidos

    # Obtén los pedidos paginados de la base de datos
    query = "SELECT * FROM Pedido WHERE usuario_id = %s LIMIT %s OFFSET %s"
    conn = Conexion()
    pedidos = conn.select_db(query, (usuario_id, items_por_pagina, offset))

    lista_pedidos_items = []
    for i in pedidos:
        #get_join_items_productos(i['id'])
        query_items = "SELECT * FROM PedidoItem WHERE pedido_id = %s"
        conn = Conexion()
        item_results = conn.select_db(query_items, (i['id'],))

        items_formateados = [ItemPedidoDB(**item_pedido_schema_db(item)) for item in item_results]

        p = Pedido(**pedido_schema(i, items_formateados))
        p.getTotalPedido()

        lista_pedidos_items.append(p)

    total_paginas = (get_total_pedidos(usuario_id) // items_por_pagina) + (1 if get_total_pedidos(usuario_id) % items_por_pagina > 0 else 0)

    return {
        'lista_i': lista_pedidos_items,
        'page': page,
        'total_pages': total_paginas
    }

#Endpoint que se encarga de mostrar los detalles de un pedido especifico
@pedido.route('/pedidos/<int:id>', methods=['GET'])
@verificar_token
def get_join_items_productos(usuario_id: int, id: int):
    """
    Muestra los detalles de un pedido específico, incluyendo los productos del pedido.

    Args:
        usuario_id (int): ID del usuario autenticado.
        id (int): ID del pedido a mostrar.

    Returns:
        HTML: Renderiza la plantilla 'unPedido.html' con los items del pedido.
    """
    query = "SELECT * FROM PedidoItem as i JOIN Producto as p ON i.producto_id = p.id WHERE i.pedido_id = %s"
    conn = Conexion()
    items_productos = conn.select_db(query, (id,))
    
    lista_items_productos =  []
    for i in items_productos:
        lista_items_productos.append(item_pedido_schema(i))

    return render_template('unPedido.html', items = lista_items_productos) #devuelve una lista de items y estos items con iformación de sus productos

#Endpoint que se encarga de mostrar el histrial de pedidos de un usuario
@pedido.route('/pedidos', methods=['GET'])
@verificar_token
def get_pedidos_usuario(usuario_id):
    """
    Muestra el historial de pedidos del usuario autenticado, con paginación.

    Args:
        usuario_id (int): ID del usuario autenticado.

    Returns:
        HTML: Renderiza la plantilla 'pedidos.html' con la información paginada.
    """

    # Obtén la página actual de la URL (por defecto la página 1)
    page = request.args.get('page', 1, type=int)

    pedidos = get_pedidos_items(usuario_id, page)
    print(f'pedidos{pedidos}')

    return render_template('pedidos.html', pedidos = pedidos)

#Endpoint que simula la compra y el registro de la venta de productos
@pedido.route('/checkout', methods=['POST'])
@verificar_token
def procesar_comprar(usuario_id):
    """
    Procesa el checkout del carrito actual del usuario autenticado, generando un pedido y registrando los productos comprados.

    Args:
        usuario_id (int): ID del usuario autenticado.

    Returns:
        Response: JSON con mensaje de confirmación o redirección en caso de error.
    """
    
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