
def usuario_schema(usuario) -> dict:
    return{
        "id": int(usuario["id"]) or None,
        "nombre": usuario["nombre"],
        "dni": usuario["dni"],
        "email": usuario["email"],
        "domicilio": usuario["domicilio"]
    }

def usuario_schema_db(usuario) -> dict:
    return{
        "id": int(usuario["id"]) or  None,
        "nombre": usuario["nombre"],
        "dni": usuario["dni"],
        "email": usuario["email"],
        "domicilio": usuario["domicilio"],
        "fecha_creacion": usuario["fecha_creacion"] | None,
        "password": usuario["password"]
    }