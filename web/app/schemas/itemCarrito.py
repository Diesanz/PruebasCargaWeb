def item_carrito_schema(item, objeto=False) -> dict:
    """Convierte un ítem de carrito en un diccionario, dependiendo de si es un objeto o un diccionario.

    Args:
        item: El ítem del carrito, que puede ser un objeto de tipo `ItemCarrito` o un diccionario.
        objeto (bool, optional): Si es `True`, se asume que `item` es un objeto; si es `False`, es un diccionario.

    Returns:
        dict: Un diccionario con los atributos del ítem del carrito.
    """
    if objeto:
        # Si item es un objeto (probablemente una instancia de ItemCarrito)
        return {
            "producto_id": int(item.producto_id),
            "nombre": item.nombre,
            "cantidad": int(item.cantidad),
            "precio": float(item.precio),
        }
    else:
        # Si item es un diccionario (ejemplo: de base de datos o JSON)
        return {
            "producto_id": int(item["producto_id"]),
            "nombre": item["nombre"],
            "cantidad": int(item["cantidad"]),
            "precio": float(item["precio"]),
        }
