from app.schemas.Producto import producto_schema

def item_pedido_schema(item) -> dict:
    """Convierte un ítem de pedido en un diccionario, con un esquema específico para el producto.

    Args:
        item: El ítem del pedido, que se espera sea un diccionario con los datos del ítem.

    Returns:
        dict: Un diccionario con los atributos del ítem del pedido, incluyendo el producto.
    """
    return {
        "pedido_id": int(item["pedido_id"]),
        "producto": producto_schema(item),  # Usa producto_schema para obtener el producto
        "cantidad": int(item["cantidad"]),
    }
def item_pedido_schema_db(item) -> dict:
    """Convierte un ítem de pedido en un diccionario para la base de datos.

    Args:
        item: El ítem del pedido, que se espera sea un diccionario con los datos del ítem.

    Returns:
        dict: Un diccionario con los atributos del ítem para la base de datos, incluyendo el `pedido_id` y `producto_id`.
    """
    return {
        "pedido_id": int(item["pedido_id"]),
        "producto_id": int(item["producto_id"]),
        "cantidad": int(item["cantidad"]),
        "precio": float(item["precio"]),
    }
