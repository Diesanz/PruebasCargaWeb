"""
Un diccionario de datos (como el resultado de una consulta SQL) y transformarlo para que coincida con el formato esperado por el objeto de tu modelo.
Por ejemplo, si la consulta SQL devuelve claves que no coinciden directamente con los atributos del modelo Producto, 
puedes reestructurarlas para asegurarte de que coincidan antes de crear el objeto. 
Esto permite usar el modelo de una forma más flexible y no tener que preocuparte por las diferencias de nombres de claves.
"""
def producto_schema(producto) -> dict:
    return {
        "id": int(producto["id"]) if producto["id"] else None,
        "nombre": producto["nombre"],
        "descripcion": producto["descripcion"],
        "precio": float(producto["precio"]),
        "stock": int(producto["stock"]),
        "tipo": producto["tipo"],
        "imagen_url": producto["imagen_url"]
    }
