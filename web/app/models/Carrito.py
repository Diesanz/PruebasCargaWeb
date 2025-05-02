from pydantic import BaseModel
from typing import Optional, List
from app.models.itemCarrito import ItemCarrito

class Carrito(BaseModel):
    id: Optional[int]=None
    usuario_id: int
    #estado: str
    items: Optional[List[ItemCarrito]] = None

    # Método para convertir el objeto en una tupla
    def to_tuple(self):
        return (self.id, self.usuario_id, self.items)
    
    # Método para calcular el total de precio del carrito
    def getTotalCarrito(self):
        sumaTotal = 0.0
        for item in self.items:
            sumaTotal += item.subtotal()
        return round(sumaTotal, 2)
    
    # Método para vaciar el carrito
    def vaciarCarrito(self):
        self.items = []

