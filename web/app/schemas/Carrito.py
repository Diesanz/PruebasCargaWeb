from app.schemas.itemCarrito import item_carrito_schema

def carrito_schema(carrito, items: list) -> dict:
    """Convierte los datos del carrito de la compra a un diccionario.

    Esta función toma un objeto `carrito` (que generalmente es un registro de la base de datos) 
    y una lista de `items` (que son los productos dentro del carrito), 
    y los convierte a un diccionario con claves específicas para ser utilizado en otros procesos (ej. responder una API).

    Args:
        carrito (dict): Un diccionario que representa los datos del carrito de la compra. 
                         Se espera que tenga las claves 'id' y 'usuario_id'.
        items (list): Una lista de ítems (productos) dentro del carrito. Cada ítem puede ser un objeto 
                      que sigue el esquema de `item_carrito_schema`.

    Returns:
        dict: Un diccionario con la estructura del carrito, con el formato adecuado para su uso.
    """
    
    return {
        "id": int(carrito["id"]) or None,  # Convierte el 'id' del carrito a entero, o 'None' si es inválido.
        "usuario_id": int(carrito["usuario_id"]),  # Convierte el 'usuario_id' a entero.
        "items": items  # Los ítems del carrito se pasan tal cual, ya que han sido procesados por `item_carrito_schema`.
    }
