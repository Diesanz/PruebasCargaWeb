from pydantic import BaseModel
from typing import Optional

class Usuario(BaseModel):
    """Representa a un usuario en el sistema.

    Atributos:
        id (Optional[int]): Identificador único del usuario, opcional si se genera automáticamente.
        nombre (str): Nombre del usuario.
        dni (str): Documento Nacional de Identidad del usuario, utilizado para identificación.
        email (str): Correo electrónico del usuario.
        domicilio (str): Dirección de residencia del usuario.

    Métodos:
        to_tuple(): Convierte el objeto `Usuario` en una tupla para ser almacenado o manipulado en la base de datos.
    """
    
    id: Optional[int] = None  # Identificador único del usuario, opcional si se genera automáticamente
    nombre: str  # Nombre del usuario
    dni: str  # DNI o documento de identificación del usuario
    email: str  # Correo electrónico del usuario
    domicilio: str  # Dirección de residencia del usuario

    def to_tuple(self):
        """Convierte el objeto `Usuario` en una tupla, útil para ser almacenado en la base de datos.

        Returns:
            tuple: Tupla con los valores del usuario (nombre, dni, email, domicilio).
        """
        return (self.nombre, self.dni, self.email, self.domicilio)

class UsuarioDB(Usuario):
    """Extiende la clase `Usuario` para incluir atributos adicionales específicos de la base de datos.

    Atributos:
        fechaCreacion (Optional[str]): Fecha de creación del usuario en el sistema, opcional.
        password (str): Contraseña del usuario, utilizada para autenticación.

    Métodos:
        to_tuple(): Sobrescribe el método `to_tuple` para incluir los nuevos atributos `password` y `fechaCreacion`.
    """
    
    fechaCreacion: Optional[str] = None  # Fecha de creación del usuario, opcional
    password: str  # Contraseña del usuario para autenticación

    def to_tuple(self):
        """Sobrescribe el método `to_tuple` para incluir los nuevos atributos `password` y `fechaCreacion`.

        Returns:
            tuple: Tupla con los valores del usuario (nombre, dni, email, domicilio, password).
        """
        return (self.nombre, self.dni, self.email, self.domicilio, self.password)
