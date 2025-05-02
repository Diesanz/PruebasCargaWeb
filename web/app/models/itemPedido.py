from pydantic import BaseModel
from typing import Optional, List
from app.models.Producto import Producto

# Modelo para un ítem dentro del pedido
class ItemPedido(BaseModel):
    producto: Producto
    cantidad: int
    pedido_id: int

    # Método para calcular el precio total del producto
    def subtotal(self):
        return self.producto.precio * self.cantidad

    # Método para convertir el objeto en una tupla
    def to_tuple(self):
        return (self.producto.id, self.cantidad)

class ItemPedidoDB(BaseModel):
    id: Optional[int]=None
    producto_id: int
    pedido_id: Optional[int]=None
    cantidad: int
    precio: float

    # Método para convertir el objeto en una tupla
    def to_tuple(self):
        return (self.pedido_id, self.producto_id, self.cantidad, self.precio)
    
    # Método para calcular el precio total del producto
    def subtotal(self):
        return self.precio * self.cantidad