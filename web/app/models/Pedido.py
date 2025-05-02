from pydantic import BaseModel
from datetime import date
from typing import Optional, List, Union
from app.models.itemPedido import ItemPedido, ItemPedidoDB

class Pedido(BaseModel):
    """Representa un pedido realizado por un usuario.

    Atributos:
        id (Optional[int]): Identificador único del pedido, opcional si se genera automáticamente.
        usuario_id (int): Identificador del usuario que realizó el pedido.
        fecha (date): Fecha en que se realizó el pedido.
        estado (str): Estado del pedido (e.g., 'Pendiente', 'Enviado', 'Cancelado').
        items (Optional[List[Union[ItemPedido, ItemPedidoDB]]]): Lista de artículos en el pedido, que pueden ser instancias de `ItemPedido` o `ItemPedidoDB`.
        precio_total (Optional[float]): El precio total calculado del pedido, opcional.

    Métodos:
        to_tuple(): Convierte el objeto `Pedido` en una tupla, útil para operaciones con la base de datos.
        getTotalPedido(): Calcula el precio total del pedido sumando el precio de todos los artículos en el pedido.
    """
    
    id: Optional[int] = None  # Identificador único del pedido, opcional
    usuario_id: int  # Identificador del usuario que realizó el pedido
    fecha: date  # Fecha de creación del pedido
    estado: str  # Estado del pedido (e.g., 'Pendiente', 'Enviado', etc.)
    items: Optional[List[Union[ItemPedido, ItemPedidoDB]]] = None  # Lista de artículos en el pedido
    precio_total: Optional[float] = None  # Precio total del pedido, calculado a partir de los ítems

    def to_tuple(self):
        """Convierte el objeto `Pedido` en una tupla, útil para ser almacenado en la base de datos.

        Returns:
            tuple: Tupla con los valores del pedido (usuario_id, fecha, estado, items).
        """
        return (self.usuario_id, self.fecha, self.estado, self.items)  # Devuelve los datos principales del pedido como tupla

    def getTotalPedido(self):
        """Calcula el precio total del pedido sumando el precio de todos los artículos.

        Esta función recorre la lista de ítems del pedido, sumando el subtotal de cada uno para obtener el total.

        Returns:
            float: El precio total calculado del pedido, redondeado a dos decimales.
        """
        sumaTotal = 0.0  # Inicializamos el total en 0.0
        for item in self.items:
            sumaTotal += item.subtotal()  # Sumamos el subtotal de cada ítem al total
        
        self.precio_total = round(sumaTotal, 2)  # Asignamos el precio total calculado al atributo precio_total
        return round(self.precio_total, 2)  # Retornamos el precio total redondeado a dos decimales
