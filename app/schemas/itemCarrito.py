
def item_carrito_schema(item) -> dict:
    return {
        "producto_id": int(item["producto_id"]),
        "nombre": item["nombre"],
        "cantidad": int(item["cantidad"]),
        "precio": float(item["precio_unitario"]),
    }

def item_carrito_schema_db(item) -> dict:
    return {
        "producto_id": int(item["producto_id"]),
        "carrito_id": int(item["carrito_id"]),
        "nombre": item["nombre"],
        "cantidad": int(item["cantidad"]),
        "precio": float(item["precio_unitario"]),
    }


