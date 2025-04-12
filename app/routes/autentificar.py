from flask import Flask, request, jsonify, Blueprint
import jwt
from datetime import datetime, timedelta
from app.models.Usuario import Usuario, UsuarioDB
from app.schemas.Usuario import usuario_schema, usuario_schema_db
from app.db.conexiondb import get_connection, close_connection, select_db, execute_db
from app.utils.comprobar_token import verificar_token #importar el decorador del token

autentificar_usuarios = Blueprint('autentificar', __name__)

SECRET = 'mi_clave_secreta'  
ALGORITHM = 'HS256'  # Algoritmo de firma por defecto

def search_usuario(busqueda:str, valor:str) -> Usuario:
    query_db = f"SELECT * FROM Usuario WHERE {busqueda} = %s"
    user = select_db(query_db, (valor,), conn=get_connection(), one=True)

    return Usuario(**usuario_schema(user)) if user else None

def search_usuario_db(email:str) -> UsuarioDB:
    query_db = "SELECT * FROM Usuario WHERE email = %s"
    user = select_db(query_db, (email,), conn=get_connection(), one=True)

    return UsuarioDB(**usuario_schema_db(user)) if user else None

#Endpoint para registrar un nuevo Usuario
@autentificar_usuarios.route('/registro', methods=['POST'])
def registro_post():
    nombre = request.form.get('nombre')
    dni = request.form.get('dni')
    email = request.form.get('email')
    domicilio = request.form.get('domicilio')
    password = request.form.get('password')

    if type(search_usuario("dni", email)) == Usuario or type(search_usuario("email", email)) == Usuario:
        return jsonify({"message": "El usuario con este DNI  o email ya existe."}), 400
        #return render_template('registroUsuario.html', error="El usuario con este DNI ya existe.")
    
    usuario = UsuarioDB(nombre=nombre, dni=dni, email=email, domicilio=domicilio, password=password)
    
    query = "INSERT INTO Usuario (nombre,dni,email,domicilio,password) VALUES (%s, %s, %s, %s, %s)"
    success=execute_db(query, usuario.to_tuple(), conn=get_connection())
    
    if success:
        return jsonify({"message": "El suario fue creado"}), 200
    else:
        return jsonify({"message": "Hubo un error al registrar el usuario."}), 500

#Endpoint para el login de Usuarios
@autentificar_usuarios.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    usuario_db = search_usuario_db(email)

    if type(usuario_db) != UsuarioDB or usuario_db.password != password:
        return jsonify({"message": "Email o contraseña incorrecto."}), 400

    #Creación de un token de autentificación
    expire = datetime.utcnow() + timedelta(minutes=1) #establecer un tiempo de expiración
    token = jwt.encode({"email": email, "id": usuario_db.id, "exp": expire}, SECRET, algorithm=ALGORITHM)

    return jsonify({"token": token, "token_type":"bearer"}), 200 #añadir el token en la sesion mediante javascript


@autentificar_usuarios.route('/me', methods=['GET'])
@verificar_token
def me():
    return jsonify({"message": "ruta disponibleee"}), 200