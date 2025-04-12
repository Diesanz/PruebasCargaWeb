from flask import request, jsonify
import jwt

SECRET = 'mi_clave_secreta' 
ALGORITHM = 'HS256'

def verificar_token(f):
    def wraps(*args, **kwargs):
        token = request.headers.get('Authorization')  # Obtener el token del header
        if token:
            try:
                print(token)
                token = token.split(" ")[1]  # Eliminar 'Bearer' del token
                print(token)
                jwt.decode(token, SECRET, algorithms=[ALGORITHM])  # Verificar el token
                return f(*args, **kwargs)  # Permitir acceso si es válido
            except jwt.ExpiredSignatureError:
                return jsonify({"message": "Token expirado."}), 401
            except jwt.InvalidTokenError:
                return jsonify({"message": "Token inválido."}), 401
        else:
            return jsonify({"message": "Token no proporcionado."}), 401
    
    return wraps