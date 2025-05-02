def producto_schema(producto) -> dict:
    """Convierte un diccionario de datos (como el resultado de una consulta SQL) en un formato adecuado para el modelo Producto.

    Args:
        producto: Diccionario con los datos del producto, como el resultado de una consulta SQL.

    Returns:
        dict: Un diccionario con los atributos del producto, con los valores convertidos al tipo correcto.
    """
    return {
        "id": int(producto["id"]) if producto["id"] else None,  # Convierte el id a int, o None si es vacío
        "nombre": producto["nombre"],  # El nombre del producto, sin cambios
        "descripcion": producto["descripcion"],  # Descripción del producto, sin cambios
        "precio": float(producto["precio"]),  # Convierte el precio a float
        "stock": int(producto["stock"]),  # Convierte el stock a int
        "tipo": producto["tipo"],  # Tipo del producto, sin cambios
        "imagen_url": producto["imagen_url"]  # URL de la imagen del producto, sin cambios
    }
