from pydantic import BaseModel
from datetime import date
from typing import Optional, List, Union
from app.models.itemPedido import ItemPedido, ItemPedidoDB

class Pedido(BaseModel):
    id: Optional[int] = None
    usuario_id: int
    fecha: date
    estado: str
    items: Optional[List[Union[ItemPedido, ItemPedidoDB]]] = None 
    precio_total: Optional[float] = None

    # Método para convertir el objeto en una tupla
    def to_tuple(self):
        return (self.usuario_id, self.fecha, self.estado, self.items)
    
    def getTotalPedido(self):
        sumaTotal = 0.0
        for item in self.items:
            sumaTotal += item.subtotal()

        self.precio_total = sumaTotal
        return round(self.precio_total, 2)
    
