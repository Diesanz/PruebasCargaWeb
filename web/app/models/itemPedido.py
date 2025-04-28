from pydantic import BaseModel
from typing import Optional, List
from app.models.Producto import Producto

# Modelo para un ítem dentro del pedido
class ItemPedido(BaseModel):
    producto: Producto
    cantidad: int
    pedido_id: int

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def to_tuple(self):
        return (self.producto.id, self.cantidad)

class ItemPedidoDB(BaseModel):
    id: Optional[int]=None
    producto_id: int
    pedido_id: Optional[int]=None
    cantidad: int
    precio: float

    def to_tuple(self):
        return (self.pedido_id, self.producto_id, self.cantidad, self.precio)
    
    def subtotal(self):
        return self.precio * self.cantidad