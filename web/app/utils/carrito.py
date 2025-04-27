from app.models.Carrito import Carrito
from app.db.conexiondb import Conexion
from app.models.Carrito import Carrito
from app.models.itemCarrito import ItemCarrito, ItemCarritoDB
from app.schemas.Carrito import carrito_schema
from app.schemas.itemCarrito import item_carrito_schema

def get_id_carrito_usuario(usuario_id: str):
    query_db = "SELECT id FROM Carrito WHERE usuario_id = %s"
    conn = Conexion()
    id_carrito = conn.select_db(query_db, (usuario_id,), one=True)

    if not id_carrito:
        return jsonify({"error": "Carrito no encontrado para el usuario."}), 404 

    return id_carrito['id']

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