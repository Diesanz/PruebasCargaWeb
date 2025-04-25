from flask import request, jsonify,url_for, redirect
from functools import wraps
import jwt

SECRET = 'mi_clave_secreta' 
ALGORITHM = 'HS256'

def verificar_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Obtener el token desde las cookies
        token = request.cookies.get('authToken')  # Obtener el token de la cookie
        
        if token:
            try:
                # Verificar el token
                token_decode = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
                usuario_id = token_decode['id']
                
                # Permitir acceso si es válido y pasa el id de usuario
                return f(usuario_id, *args, **kwargs)
            
            except jwt.ExpiredSignatureError:
                return jsonify({"message": "Token expirado."}), 401
            except jwt.InvalidTokenError:
                return jsonify({"message": "Token inválido."}), 401
        else:
            return redirect(url_for('autentificar.login'))
    return wrapper