from pydantic import BaseModel
from typing import Optional, List

# Modelo para un ítem dentro del carrito
class ItemCarrito(BaseModel):
    """Representa un artículo dentro del carrito de compras.

    Atributos:
        producto_id (int): Identificador único del producto.
        nombre (str): Nombre del producto.
        cantidad (int): Cantidad del producto en el carrito.
        precio (float): Precio unitario del producto.

    Métodos:
        subtotal(): Calcula el total para ese artículo (cantidad * precio).
        to_tuple(): Convierte el objeto en una tupla, útil para la base de datos.
    """
    
    producto_id: int  # Identificador del producto en el carrito.
    nombre: str  # Nombre del producto.
    cantidad: int  # Cantidad de productos en el carrito.
    precio: float  # Precio unitario del producto.

    def subtotal(self):
        """Calcula el precio total de este artículo (cantidad * precio).

        Returns:
            float: El total del artículo (cantidad * precio).
        """
        return self.cantidad * self.precio  # Multiplica la cantidad por el precio unitario

    def to_tuple(self):
        """Convierte el objeto `ItemCarrito` en una tupla.

        Esta tupla puede ser usada para almacenar la información del artículo en una base de datos.

        Returns:
            tuple: Tupla con la información del artículo (producto_id, nombre, cantidad, precio).
        """
        return (self.producto_id, self.nombre, self.cantidad, self.precio)  # Retorna los valores como tupla

# Modelo para un ítem dentro del carrito, con el campo adicional para identificar el carrito en la base de datos
class ItemCarritoDB(ItemCarrito):
    """Representa un ítem dentro del carrito, con un campo adicional `carrito_id`.

    Atributos:
        carrito_id (int): Identificador único del carrito al que pertenece este artículo.

    Métodos:
        to_tuple(): Convierte el objeto en una tupla, útil para la base de datos, con el campo `carrito_id`.
    """
    
    carrito_id: int  # Identificador del carrito al que pertenece este artículo.

    def to_tuple(self):
        """Convierte el objeto `ItemCarritoDB` en una tupla, incluyendo el carrito_id.

        Esta tupla es útil para almacenar los datos del ítem en la base de datos, considerando su relación con el carrito.

        Returns:
            tuple: Tupla con la información del artículo, incluyendo carrito_id (carrito_id, producto_id, nombre, cantidad, precio).
        """
        return (self.carrito_id, self.producto_id, self.nombre, self.cantidad, self.precio)  # Incluye carrito_id en la tupla
