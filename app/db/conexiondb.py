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
    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(query, args)
            result = cursor.fetchall()

            if one:
                return result[0]
            else:
                return result

    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
    finally:
        if connection: 
            #si la conexión es válida se cierra conexión
            connection.close()

def execute_db(query, args=(), one=False):
    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(query, args)
            connection.commit()
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
    finally:
        if connection: 
            #si la conexión es válida se cierra conexión
            connection.close()