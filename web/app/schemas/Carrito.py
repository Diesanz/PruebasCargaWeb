from app.schemas.itemCarrito import item_carrito_schema

#Método para la validación de un carrito de la compra
def carrito_schema(carrito, items: list) -> dict:
    return{
        "id": int(carrito["id"]) or None,
        "usuario_id": int(carrito["usuario_id"]), 
        "items": items
    }