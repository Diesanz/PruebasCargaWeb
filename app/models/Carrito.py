from pydantic import BaseModel
from typing import Optional, List
from app.models.itemCarrito import ItemCarrito

class Carrito(BaseModel):
    id: Optional[int]=None
    usuario_id: int
    #estado: str
    items: List[ItemCarrito]

    # Método para convertir el objeto en una tupla
    def to_tuple(self):
        return (self.id, self.usuario_id, self.items)
    
    def getTotalCarrito(self):
        sumaTotal = 0.0
        for item in self.items:
            sumaTotal += item.subtotal()
    
    def vaciarCarrito(self):
        self.items = []

