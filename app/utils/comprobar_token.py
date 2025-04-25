from flask import request, jsonify
from functools import wraps
import jwt

SECRET = 'mi_clave_secreta' 
ALGORITHM = 'HS256'

def verificar_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')  # Obtener el token del header
        if token:
            try:
                token = token.split(" ")[1]  # Eliminar 'Bearer' del token
                token_decode = jwt.decode(token, SECRET, algorithms=[ALGORITHM])  # Verificar el token
                usuario_id = token_decode['id']
                return f(usuario_id,*args, **kwargs)  # Permitir acceso si es válido y devuelve el id de usuario
            except jwt.ExpiredSignatureError:
                return jsonify({"message": "Token expirado."}), 401
            except jwt.InvalidTokenError:
                return jsonify({"message": "Token inválido."}), 401
        else:
            return jsonify({"message": "Token no proporcionado."}), 401
    
    return wrapper