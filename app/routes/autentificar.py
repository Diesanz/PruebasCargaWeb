from flask import Flask, request, jsonify, Blueprint, render_template, redirect, url_for, flash, make_response
import jwt
from datetime import datetime, timedelta
from app.models.Usuario import Usuario, UsuarioDB
from app.schemas.Usuario import usuario_schema, usuario_schema_db
from app.db.conexiondb import Conexion
from app.utils.comprobar_token import verificar_token #importar el decorador del token

autentificar_usuarios = Blueprint('autentificar', __name__, url_prefix="/api") #blueprint para el controladoir (añadir en init.py)

SECRET = 'mi_clave_secreta'  
ALGORITHM = 'HS256'  # Algoritmo de firma por defecto

def search_usuario(busqueda:str, valor:str) -> Usuario:
    conn = Conexion()
    query_db = f"SELECT * FROM Usuario WHERE {busqueda} = %s"
    user = conn.select_db(query_db, (valor,), one=True)

    return Usuario(**usuario_schema(user)) if user else None

def search_usuario_db(email:str) -> UsuarioDB:
    conn = Conexion()
    query_db = "SELECT * FROM Usuario WHERE email = %s"
    user = conn.select_db(query_db, (email,), one=True)

    return UsuarioDB(**usuario_schema_db(user)) if user else None

# Función para verificar si el token es válido (solo para el login)
def verificar_token_login():
    token = request.cookies.get('authToken')
    if token:
        try:
            token_decode = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
            return token_decode  # Token válido, devuelve la decodificación
        except jwt.ExpiredSignatureError:
            return None  # Token expirado
        except jwt.InvalidTokenError:
            return None  # Token inválido
    return None  # No hay token

#Endpoit para obtener el html del login y del registro
@autentificar_usuarios.route('/login', methods=['GET'])
def login():
    # Verificar si el usuario ya está autenticado
    if verificar_token_login():
        # Si el token es válido, redirigir a la página principal o cualquier otra página
        return redirect('/api')  # Cambia '/' por la página a la que deseas redirigir
    else:
        # Si no hay token o el token es inválido, mostrar la página de inicio de sesión
        return render_template('inicioSesion.html')

@autentificar_usuarios.route('/registro', methods=['GET'])
def registro():
    return render_template('registroUsuario.html')

#Endpoint para registrar un nuevo Usuario
@autentificar_usuarios.route('/registro', methods=['POST'])
def registro_post():
    """
    Endpoint para registrar un nuevo usuario en el sistema.

    Este endpoint recibe los datos del formulario (nombre, dni, email, domicilio, y password)
    para crear un nuevo usuario. Si el DNI o el email ya están registrados en el sistema,
    se devuelve un error con un mensaje de flash. Después de registrar el usuario, se crea 
    un carrito de compras asociado al nuevo usuario.

    Los pasos incluyen:
    1. Verificar si el DNI o el email ya están en uso.
    2. Crear un nuevo usuario en la base de datos utilizando el procedimiento `CreateUser`.
    3. Crear un carrito asociado al nuevo usuario.

    Method:
    POST

    Request Form Parameters:
    - nombre (str): Nombre del usuario.
    - dni (str): DNI del usuario.
    - email (str): Correo electrónico del usuario.
    - domicilio (str): Dirección del usuario.
    - password (str): Contraseña del usuario.

    Response:
    - Si el usuario se registra correctamente y se crea el carrito: Redirige al login.
    - Si ocurre un error al registrar el usuario o al crear el carrito: Devuelve un mensaje de error con código 500.
    - Si el usuario ya existe con el mismo DNI o email: Se muestra un mensaje de error con flash y se redirige al registro.

    Return:
    - Redirección al login si el registro y carrito se crean correctamente.
    - Respuesta JSON con error 500 si hubo un fallo en el proceso de registro.
    """

    nombre = request.form.get('nombre')
    dni = request.form.get('dni')
    email = request.form.get('email')
    domicilio = request.form.get('domicilio')
    password = request.form.get('password')

    if type(search_usuario("dni", email)) == Usuario or type(search_usuario("email", email)) == Usuario:
        #return jsonify({"message": "El usuario con este DNI  o email ya existe."}), 400
        flash("El usuario con este DNI o email ya existe.")
        return redirect(url_for('autentificar.registro'))
    
    usuario = UsuarioDB(nombre=nombre, dni=dni, email=email, domicilio=domicilio, password=password)
    
    conn = Conexion()
    success_id=conn.procedure('CreateUser', usuario.to_tuple()) #Añade un usurio mediante procedimiento, ya que con este mismo se puede obtener el id para insertarlo en el carrito
    
    if success_id:
        query = "INSERT INTO Carrito (usuario_id) VALUES (%s)" #Crea el carrito para ese usuario

        conn = Conexion()
        success_execution=conn.execute_db(query, success_id)
        
        if success_execution:
            return redirect(url_for('autentificar.login'))
    
    return jsonify({"message": "Hubo un error al registrar el usuario."}), 500

#Endpoint para el login de Usuarios
@autentificar_usuarios.route('/login', methods=['POST'])
def login_post():
    """
    Endpoint para autenticar a un usuario y generar un token de autenticación.

    Este endpoint recibe el correo electrónico y la contraseña del usuario, verifica si los 
    datos son correctos y, si lo son, genera un token de autenticación JWT. El token es válido 
    por 1 minuto, y se envía como parte de la respuesta para que el usuario pueda realizar 
    peticiones autenticadas.

    Method:
    POST

    Request Form Parameters:
    - email (str): Correo electrónico del usuario.
    - password (str): Contraseña del usuario.

    Response:
    - Si las credenciales son correctas: Devuelve un token JWT para el usuario autenticado.
    - Si las credenciales son incorrectas: Devuelve un error con código 401 y mensaje de "Email o contraseña incorrectas."

    Return:
    - JSON con el token de autenticación y el tipo de token si las credenciales son correctas.
    - JSON con el mensaje de error y el código 401 si las credenciales son incorrectas.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    usuario_db = search_usuario_db(email)

    if type(usuario_db) != UsuarioDB or usuario_db.password != password: #comprobación de credenciales (falta hacer el hash)
        #flash("Email o contraseña incorrectas.")
        return jsonify({"error": "Email o contraseña incorrectas."}), 401

    #Creación de un token de autentificación
    expire = datetime.utcnow() + timedelta(minutes=40) #establecer un tiempo de expiración
    token = jwt.encode({"email": email, "id": usuario_db.id, "exp": expire}, SECRET, algorithm=ALGORITHM)

    resp = make_response(jsonify({"message": "Autenticado exitosamente."}), 200)
    resp.set_cookie('authToken', token, httponly=True, secure=True,  samesite='Strict')

    return resp

@autentificar_usuarios.route('/logout')
def logout():
    token = request.cookies.get('authToken')
    if token:
        resp = make_response(redirect(url_for('autentificar.login')))
        resp.set_cookie('authToken', '', expires=0)  # Borra la cookie
        return resp

@autentificar_usuarios.route('/me', methods=['GET'])
@verificar_token
def me():
    return jsonify({"message": "ruta disponible"}), 200