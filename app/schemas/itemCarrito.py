
def item_carrito_schema(item, objeto = False) -> dict: #Si es true accede a los parametros como si fuera un objeto y si es false accede como si fuera un json
    if objeto:
        return {
            "producto_id": int(item.producto_id),
            "nombre": item.nombre,
            "cantidad": int(item.cantidad),
            "precio": float(item.precio),
        }
    else:
        # Si item no es un objeto de tipo ItemCarrito, asume que es un diccionario
        return {
            "producto_id": int(item["producto_id"]),
            "nombre": item["nombre"],
            "cantidad": int(item["cantidad"]),
            "precio": float(item["precio"]),
        }

def item_carrito_schema_db(item) -> dict:
    return {
        "producto_id": int(item["producto_id"]),
        "carrito_id": int(item["carrito_id"]),
        "nombre": item["nombre"],
        "cantidad": int(item["cantidad"]),
        "precio": float(item["precio"]),
    }


