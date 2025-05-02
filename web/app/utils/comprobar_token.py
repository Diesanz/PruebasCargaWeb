from flask import request, jsonify,url_for, redirect, make_response
from functools import wraps
import jwt

SECRET = 'mi_clave_secreta' 
ALGORITHM = 'HS256'

def verificar_token(f):
    """
    Decorador que protege rutas requeridas para usuarios autenticados.
    Verifica la validez de un token JWT almacenado en una cookie llamada 'authToken'.

    Si el token es válido, extrae el `usuario_id` y lo pasa como primer argumento
    a la función decorada.

    - Si el token ha expirado, borra la cookie y redirige al login.
    - Si el token es inválido, devuelve un error JSON 401.
    - Si no hay token, redirige al login.

    Args:
        f (function): Función de vista (endpoint) que requiere autenticación.

    Returns:
        function: Función decorada que incluye verificación del token.
    """
    
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('authToken')  # Obtener el token de la cookie
        
        if token:
            try:
                # Intentar decodificar el token
                token_decode = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
                usuario_id = token_decode['id']
                
                # Llamar a la función original si el token es válido
                return f(usuario_id, *args, **kwargs)
            
            except jwt.ExpiredSignatureError:
                # Si el token ha expirado, borra la cookie y redirige al login
                resp = make_response(redirect(url_for('autentificar.login')))  # Redirige al login
                resp.set_cookie('authToken', '', expires=0)  # Borra el token de la cookie
                return resp  # Retorna la respuesta con la cookie borrada y redirección
            except jwt.InvalidTokenError:
                # Si el token es inválido, puedes devolver un error o redirigir
                return jsonify({"message": "Token inválido"}), 401
        else:
            # Si no hay token, redirige al login
            return redirect(url_for('autentificar.login'))
    
    return wrapper
