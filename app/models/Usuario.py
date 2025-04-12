from pydantic import BaseModel

class Usuario(BaseModel):
    id: int | None
    nombre: str
    dni: str
    email: str
    domicilio: str

    # Método para convertir el objeto en una tupla
    def to_tuple(self):
        return ( self.nombre, self.dni, self.email, self.domicilio)

class UsuarioDB(Usuario):
    fechaCreacion: str | None
    password: str

    # Sobrescribir el método to_tuple para incluir los nuevos atributos
    def to_tuple(self):
        return (self.id, self.nombre, self.dni, self.email, self.domicilio, self.fechaCreacion, self.password)
