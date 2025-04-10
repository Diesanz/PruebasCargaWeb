import pymysql

def get_connection():
    try:
        """
        Establece una conexión con la base de datos MariaDB utilizando los parámetros proporcionados.
                
        return: Devuelve un objeto de tipo conexión a la base de datos si la conexión es exitosa.
                Si ocurre un error, devuelve None.
        """
        connection = pymysql.connect(
            host= "localhost",
            port= int(3306),
            database= "Carga_web",
            user= "user_pr",
            password= "Grupo6esi",
            charset='utf8mb4',  # Evita problemas de encoding
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        print("Error al conectarse a la base de datos:" + str(e))
        return None


def select_db(query, args=(), one=False):
    """Función destinada a realizar consultas SELECT en la base de datos.

    Keyword arguments:
    query -- consulta SQL que se ejecuta en la base de datos.
    args -- parámetros que se deben sustituir en la consulta SQL (por defecto es una tupla vacía).
    one -- si es True, devuelve solo un resultado (el primer elemento) en lugar de una lista de resultados.

    Return:
    Si 'one' es True, devuelve un solo valor. Si 'one' es False, devuelve una lista de resultados.
    """
    
    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(query, args)
            result = cursor.fetchall()

            if one:  # En caso de que solo se devuelva un solo resultado (por ejemplo, un usuario o un producto)
                return result[0]
            else:
                return result  # Devuelve una lista de resultados

    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
    finally:
        if connection: 
            # Si la conexión es válida, se cierra la conexión
            connection.close()


def execute_db(query, args=()):
    """Función destinada a ejecutar consultas que modifican la base de datos (INSERT, UPDATE, DELETE).

    Keyword arguments:
    query -- consulta SQL que se ejecuta en la base de datos.
    args -- parámetros que se deben sustituir en la consulta SQL (por defecto es una tupla vacía).

    Return:
    No devuelve nada, pero se realiza un commit en la base de datos para aplicar cambios.
    """
    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(query, args)
            connection.commit()  # Realiza el commit para asegurar que los cambios se guarden
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
    finally:
        if connection: 
            # Si la conexión es válida, se cierra la conexión
            connection.close()
