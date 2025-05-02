def usuario_schema(usuario) -> dict:
    """Convierte un diccionario de datos de un usuario en un formato adecuado para el modelo Usuario.

    Args:
        usuario: Diccionario con los datos del usuario, como el resultado de una consulta SQL.

    Returns:
        dict: Un diccionario con los atributos del usuario, con los valores convertidos al tipo correcto.
    """
    return {
        "id": int(usuario["id"]) or None,  # Convierte el id a entero o asigna None si está vacío
        "nombre": usuario["nombre"],  # El nombre del usuario, sin cambios
        "dni": usuario["dni"],  # DNI del usuario, sin cambios
        "email": usuario["email"],  # Correo electrónico del usuario, sin cambios
        "domicilio": usuario["domicilio"]  # Domicilio del usuario, sin cambios
    }

def usuario_schema_db(usuario) -> dict:
    """Convierte un diccionario de datos de un usuario con más información (como fecha de creación y contraseña) 
    en un formato adecuado para el modelo UsuarioDB.

    Args:
        usuario: Diccionario con los datos del usuario, como el resultado de una consulta SQL.

    Returns:
        dict: Un diccionario con los atributos del usuario, con los valores convertidos al tipo correcto.
    """
    return {
        "id": int(usuario["id"]) or None,  # Convierte el id a entero o asigna None si está vacío
        "nombre": usuario["nombre"],  # El nombre del usuario, sin cambios
        "dni": usuario["dni"],  # DNI del usuario, sin cambios
        "email": usuario["email"],  # Correo electrónico del usuario, sin cambios
        "domicilio": usuario["domicilio"],  # Domicilio del usuario, sin cambios
        "fecha_creacion": usuario["fechaCreacion"] or None,  # Fecha de creación, asigna None si está vacía
        "password": usuario["password"]  # Contraseña del usuario, sin cambios
    }
