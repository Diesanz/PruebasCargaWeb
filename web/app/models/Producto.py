from pydantic import BaseModel
from typing import Optional

class Producto(BaseModel):
    """Representa un producto disponible en la tienda.

    Atributos:
        id (Optional[int]): Identificador único del producto, opcional si se genera automáticamente.
        nombre (str): Nombre del producto.
        descripcion (str): Descripción del producto.
        precio (float): Precio del producto.
        stock (int): Cantidad disponible del producto en inventario.
        tipo (str): Tipo o categoría del producto (e.g., 'Comida', 'Bebida').
        imagen_url (str): URL de la imagen del producto.

    Métodos:
        to_tuple(): Convierte el objeto `Producto` en una tupla para ser almacenado o manipulado en la base de datos.
    """
    
    id: Optional[int] = None  # Identificador único del producto, opcional si se genera automáticamente
    nombre: str  # Nombre del producto
    descripcion: str  # Descripción detallada del producto
    precio: float  # Precio del producto
    stock: int  # Cantidad disponible en inventario
    tipo: str  # Tipo o categoría del producto (e.g., 'Comida', 'Bebida')
    imagen_url: str  # URL de la imagen asociada al producto

    def to_tuple(self):
        """Convierte el objeto `Producto` en una tupla, útil para ser almacenado en la base de datos.

        Returns:
            tuple: Tupla con los valores del producto (id, nombre, descripcion, precio, stock, tipo, imagen_url).
        """
        return (self.id, self.nombre, self.descripcion, self.precio, self.stock, self.tipo, self.imagen_url)
