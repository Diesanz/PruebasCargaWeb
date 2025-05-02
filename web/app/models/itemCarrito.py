from pydantic import BaseModel
from typing import Optional, List

# Modelo para un ítem dentro del carrito
class ItemCarrito(BaseModel):
    producto_id: int
    nombre: str
    cantidad: int
    precio: float

    # Método para calcular el precio total del producto
    def subtotal(self):
        return self.cantidad * self.precio

    # Método para convertir el objeto en una tupla
    def to_tuple(self):
        return (self.producto_id, self.nombre, self.cantidad, self.precio)

class ItemCarritoDB(ItemCarrito):
    carrito_id: int

    # Método para convertir el objeto en una tupla
    def to_tuple(self):
        return (self.carrito_id, self.producto_id, self.nombre, self.cantidad, self.precio)