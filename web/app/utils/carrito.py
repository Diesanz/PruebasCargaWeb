from app.models.Carrito import Carrito
from app.db.conexiondb import Conexion
from app.models.Carrito import Carrito
from app.models.itemCarrito import ItemCarrito, ItemCarritoDB
from app.schemas.Carrito import carrito_schema
from app.schemas.itemCarrito import item_carrito_schema



def get_carrito_items_usuario(usuario_id: str) -> Carrito:
    """
    Obtiene el objeto `Carrito` completo, incluyendo todos los ítems agregados por el usuario.

    Args:
        usuario_id (str): ID del usuario.

    Returns:
        Carrito: Objeto `Carrito` con su información y los productos contenidos.
    """
    
    query_db = "SELECT * FROM Carrito WHERE usuario_id = %s"
    conn = Conexion()
    carrito = conn.select_db(query_db, (usuario_id,), one=True)

    #obtner los items
    query_db_items = "SELECT * FROM CarritoItem WHERE carrito_id = %s"
    conn = Conexion()
    items = conn.select_db(query_db_items, (carrito['id'],), one=False)
    
    lista_items = [ItemCarrito(**item_carrito_schema(i)) for i in items]
   
    return Carrito(**carrito_schema(carrito, lista_items))