from flask import Flask, request, jsonify, Blueprint
from app.models.Usuario import Usuario, UsuarioDB
from app.schemas.Usuario import usuario_schema
from app.db.conexiondb import get_connection, close_connection, select_db, execute_db

autentificar_usuarios = Blueprint('autentificar', __name__)

def search_usuario(busqueda:str, valor:str) -> Usuario:
    query_db = f"SELECT * FROM Usuario WHERE {busqueda} = %s"
    users = select_db(query_db, (valor,), conn=get_connection(), one=True)

    return Usuario(**usuario_schema(users)) if users else None

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