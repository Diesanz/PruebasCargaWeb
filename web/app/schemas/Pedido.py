from datetime import date

def pedido_schema(pedido, items: list) -> dict:
    """Convierte un pedido en un diccionario con los atributos correspondientes.

    Args:
        pedido: El pedido, que se espera sea un diccionario con los datos del pedido.
        items: Una lista de ítems asociados al pedido.

    Returns:
        dict: Un diccionario con los atributos del pedido, como el usuario, la fecha, el estado y los ítems.
    """
    return {
        "id": int(pedido["id"]) or None,  # Convierte el id en un entero, si es None lo establece como None
        "usuario_id": int(pedido["usuario_id"]),  # Convierte el usuario_id en un entero
        "fecha": pedido["fecha"].date(),  # Convierte la fecha a un objeto de tipo date
        "estado": str(pedido["estado"]),  # Convierte el estado a cadena de texto
        "items": items  # La lista de ítems ya validada
    }
