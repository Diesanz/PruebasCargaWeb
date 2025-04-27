import pymysql

class Conexion:
    """
    Clase que gestiona la conexión y operaciones con una base de datos MySQL utilizando pymysql.
    """

    def __init__(self, host="localhost", port=3306, database="Carga_web", user="user_pr", password="Grupo6esi"):
        """
        Inicializa la configuración de conexión con los parámetros dados.

        Parámetros:
        - host (str): Dirección del servidor MySQL (por defecto: localhost)
        - port (int): Puerto del servidor MySQL (por defecto: 3306)
        - database (str): Nombre de la base de datos a la que conectarse
        - user (str): Nombre del usuario con permisos en la base de datos
        - password (str): Contraseña del usuario

        Inicializa:
        - self.connection_params (dict): Diccionario con los parámetros de conexión
        - self.connection (pymysql.Connection | None): Objeto de conexión
        """
        self.connection_params = {
            "host": host,
            "port": port,
            "database": database,
            "user": user,
            "password": password,
            "charset": 'utf8mb4',
            "cursorclass": pymysql.cursors.DictCursor
        }
        self.connection = None

    def get_connection(self):
        """
        Establece una conexión con la base de datos utilizando los parámetros definidos.

        Return:
        - pymysql.Connection: Objeto de conexión activo si la conexión es exitosa
        - None: Si ocurre un error al conectar

        Excepciones:
        - pymysql.MySQLError: Captura errores de conexión y los imprime
        """
        try:
            self.connection = pymysql.connect(**self.connection_params)
            return self.connection
        except pymysql.MySQLError as e:
            print("Error al conectarse a la base de datos:" + str(e))
            self.connection = None
            return self.connection

    def close_connection(self):
        """
        Cierra la conexión activa con la base de datos si existe.
        """
        if self.connection:
            self.connection.close()
            self.connection = None

    def select_db(self, query: str, args: tuple = (), one: bool = False):
        """
        Ejecuta una consulta SELECT en la base de datos.

        Parámetros:
        - query (str): Consulta SQL que se va a ejecutar (de tipo SELECT)
        - args (tuple): Tupla de argumentos para la consulta parametrizada
        - one (bool): Si es True devuelve solo un registro; si es False, todos los registros

        Return:
        - dict | list[dict] | None: Resultado de la consulta (uno o varios diccionarios)

        Excepciones:
        - Exception: Captura errores en la ejecución de la consulta y los imprime
        """
        if not self.connection:
            self.get_connection()

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, args)
                result = cursor.fetchone() if one else cursor.fetchall() #si es fetchone devuelven forma de json!!!!!
                return result
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            self.close_connection()

    def execute_db(self, query: str, args: tuple = ()):
        """
        Ejecuta una consulta de modificación (INSERT, UPDATE, DELETE) en la base de datos.

        Parámetros:
        - query (str): Consulta SQL a ejecutar
        - args (tuple): Tupla con los valores a insertar en la consulta

        Return:
        - bool: True si la operación fue exitosa, False si ocurrió algún error

        Excepciones:
        - Exception: Captura errores en la ejecución y los imprime
        """
        if not self.connection:
            self.get_connection()

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, args)
                self.connection.commit()
                return True
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return False
        finally:
            self.close_connection()

    def procedure(self, procedimiento: str, args: tuple = ()):
        """
        Ejecuta un procedimiento almacenado y devuelve el resultado esperado.

        Parámetros:
        - procedimiento (str): Nombre del procedimiento almacenado a ejecutar
        - args (tuple): Argumentos necesarios para el procedimiento

        Return:
        - int | bool: Retorna el 'id' del usuario si se obtiene correctamente,
                      o False si hubo un error en la ejecución

        Excepciones:
        - Exception: Captura errores en la ejecución del procedimiento
        """
        if not self.connection:
            self.get_connection()

        id_usuario = None

        try:
            with self.connection.cursor() as cursor:
                cursor.callproc(procedimiento, args)
                result = cursor.fetchall()
                if result:
                    id_usuario = result[0]['id']  # Se espera que el procedimiento devuelva una fila con la clave 'id'
                self.connection.commit()
                return id_usuario
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return False
        finally:
            self.close_connection()
