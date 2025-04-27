from pydantic import BaseModel
from typing import Optional

class Producto(BaseModel):
    id: Optional[int] = None
    nombre: str
    descripcion: str
    precio: float
    stock: int
    tipo: str
    imagen_url: str

    # Método para convertir el objeto en una tupla
    def to_tuple(self):
        return (self.id, self.nombre, self.descripcion, self.precio, self.stock, self.tipo, self.imagen_url)
