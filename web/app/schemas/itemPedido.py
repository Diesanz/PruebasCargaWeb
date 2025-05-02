from app.schemas.Producto import producto_schema

#Método para la validación de un producto del pedido
def item_pedido_schema(item) -> dict:
    return {
        "pedido_id": int(item["pedido_id"]),
        "producto": producto_schema(item),
        "cantidad": int(item["cantidad"]),
    }

#Método para la validación de un producto del pedido
def item_pedido_schema_db(item) -> dict:
    return {
        "pedido_id": int(item["pedido_id"]),
        "producto_id": int(item["producto_id"]),
        "cantidad": int(item["cantidad"]),
        "precio": float(item["precio"]),
    }
