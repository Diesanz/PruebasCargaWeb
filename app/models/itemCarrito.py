from pydantic import BaseModel
from typing import Optional, List

# Modelo para un ítem dentro del carrito
class ItemCarrito(BaseModel):
    producto_id: int
    nombre: str
    cantidad: int
    precio: float

    def subtotal(self):
        return self.cantidad * self.precio

    def to_tuple(self):
        return (self.producto_id, self.nombre, self.cantidad, self.precio)

class ItemCarritoDB(ItemCarrito):
    carrito_id: int

    def to_tuple(self):
        return (self.carrito_id, self.producto_id, self.nombre, self.cantidad, self.precio)