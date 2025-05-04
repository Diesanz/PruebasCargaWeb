from pydantic import BaseModel
from typing import Optional, List
from app.models.Producto import Producto

# Modelo para un ítem dentro del pedido, con información para la base de datos
class ItemPedido(BaseModel):
    """Representa un artículo dentro de un pedido, con información para ser almacenada en la base de datos.

    Atributos:
        id (Optional[int]): Identificador único del ítem (si está presente).
        producto_id (int): Identificador del producto que se está pidiendo.
        pedido_id (Optional[int]): Identificador del pedido al que pertenece este ítem.
        cantidad (int): La cantidad de producto en el pedido.
        precio (float): El precio unitario del producto.

    Métodos:
        to_tuple(): Convierte el objeto en una tupla, útil para operaciones con la base de datos.
        subtotal(): Calcula el precio total del artículo (cantidad * precio).
    """
    
    id: Optional[int] = None  # Identificador único del ítem, opcional si se genera automáticamente
    producto_id: int  # Identificador del producto en la base de datos
    pedido_id: Optional[int] = None  # Identificador del pedido al que pertenece el ítem, opcional si se genera posteriormente
    cantidad: int  # La cantidad del producto en el pedido
    precio: float  # El precio unitario del producto

    def to_tuple(self):
        """Convierte el objeto `ItemPedidoDB` en una tupla, incluyendo la relación con el pedido y producto.

        Esta tupla es útil para almacenar la información del ítem en la base de datos.

        Returns:
            tuple: Tupla con el `pedido_id`, `producto_id`, `cantidad`, y `precio`.
        """
        return (self.pedido_id, self.producto_id, self.cantidad, self.precio)  # Retorna los datos como tupla

    def subtotal(self):
        """Calcula el precio total de este artículo (cantidad * precio).

        Returns:
            float: El precio total de este ítem (cantidad * precio).
        """
        return round(self.precio * self.cantidad, 2)  # Multiplica el precio unitario por la cantidad
