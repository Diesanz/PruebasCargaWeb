
from datetime import date

def pedido_schema(pedido, items: list) -> dict:
    return{
        "id": int(pedido["id"]) or None,
        "usuario_id": int(pedido["usuario_id"]), 
        "fecha": pedido["fecha"].date(),
        "estado": str(pedido["estado"]),
        "items": items,
        "precio_total": float(pedido["precio_total"]) or None
    }