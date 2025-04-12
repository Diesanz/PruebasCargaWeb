from flask import Flask, request, jsonify, Blueprint
from app.models.Usuario import Usuario
from app.schemas.Usuario import usuario_schema
from app.db.conexiondb import get_connection, close_connection, select_db, execute_db

autentificar_usuarios = Blueprint('autentificar', __name__)

def search_usuario(dni:str) -> Usuario:
    query_db = "SELECT * FROM Usuario WHERE dni = %s"
    users = select_db(query_db, (dni,), conn=get_connection(), one=True)

    return Usuario(**usuario_schema(users)) if users else None

#Endpoint para registrar un nuevo Usuario
@autentificar_usuarios.route('/registro', methods=['POST'])
def registro_post():
    nombre = request.form.get('nombre')
    dni = request.form.get('dni')
    email = request.form.get('email')
    domicilio = request.form.get('domicilio')
    password = request.form.get('password')

    if type(search_usuario(dni)) == Usuario:
        return jsonify({"message": "El usuario con este DNI ya existe."}), 400
        #return render_template('registroUsuario.html', error="El usuario con este DNI ya existe.")
    
    