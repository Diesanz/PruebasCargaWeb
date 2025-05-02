#Método para la validación de un usuario
def usuario_schema(usuario) -> dict:
    return{
        "id": int(usuario["id"]) or None,
        "nombre": usuario["nombre"],
        "dni": usuario["dni"],
        "email": usuario["email"],
        "domicilio": usuario["domicilio"]
    }

#Método para la validación de un usuario
def usuario_schema_db(usuario) -> dict:
    return{
        "id": int(usuario["id"]) or  None,
        "nombre": usuario["nombre"],
        "dni": usuario["dni"],
        "email": usuario["email"],
        "domicilio": usuario["domicilio"],
        "fecha_creacion": usuario["fechaCreacion"] or None,
        "password": usuario["password"]
    }