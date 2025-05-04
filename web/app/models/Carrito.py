from pydantic import BaseModel
from typing import Optional, List
from app.models.itemCarrito import ItemCarrito

class Carrito(BaseModel):
    """Representa el carrito de compras de un usuario en la tienda.

    Atributos:
        id (int, opcional): Identificador único del carrito. Si es `None`, el carrito no ha sido guardado en la base de datos.
        usuario_id (int): El identificador del usuario propietario del carrito.
        items (List[ItemCarrito]): Lista de los artículos (productos) en el carrito. Inicializada como lista vacía por defecto.

    Métodos:
        to_tuple(): Convierte el objeto `Carrito` en una tupla para ser usado en operaciones de base de datos.
        getTotalCarrito(): Calcula el total del carrito sumando los subtotales de cada artículo.
        vaciarCarrito(): Vacía el carrito eliminando todos los artículos.
    """

    id: Optional[int]=None
    usuario_id: int
    #estado: str
    items: Optional[List[ItemCarrito]] = None

    def to_tuple(self):
        """Convierte el objeto `Carrito` en una tupla.

        Este método es útil cuando se necesita insertar el carrito en una base de datos o pasar su información
        de una manera que sea compatible con las operaciones de bases de datos.

        Returns:
            tuple: Tupla con los valores del carrito, lista de items incluida.
        """
        return (self.id, self.usuario_id, self.items)
    
    def getTotalCarrito(self):
        """Calcula el total del carrito.

        Suma los subtotales de todos los artículos en el carrito y devuelve el resultado redondeado a 2 decimales.

        Returns:
            float: Total de todos los artículos del carrito.
        """
        sumaTotal = 0.0
        for item in self.items:
            sumaTotal += item.subtotal()
            
        return round(sumaTotal, 2)
    
