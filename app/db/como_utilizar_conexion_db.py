from conexiondb import get_connection, close_connection, select_db, execute_db

def user_list(conn=None):
    query_db = "SELECT id, nombre FROM Usuario"
    users = select_db(query_db, conn=conn)
    return users

def add_user(conn=None):
    nombre = "Juan"
    email = "f@fetchall"
    contraseña_hash = "2345"  

    query = "INSERT INTO Usuario (nombre, email, contraseña_hash) VALUES (%s, %s, %s)"
    execute_db(query, (nombre, email, contraseña_hash), conn=conn)
    
    return f"✅ Usuario '{nombre}' agregado exitosamente!"


def update_user(id, new_name):
    query = "UPDATE users SET name = %s WHERE id = %s"
    execute_db(query, (new_name, id))
    return f"El usuario con ID {id} ha sido actualizado con el nuevo nombre {new_name}"

def delete_user(id):
    query = "DELETE FROM users WHERE id = %s"
    execute_db(query, (id,))
    return f"El usuario con ID {id} ha sido eliminado."

if __name__ == '__main__':
    conn = get_connection()
    if conn:
        users=user_list(conn)
        print(f'Usuarios {users}')
        add_user(conn)

        close_connection(conn)