from locust import HttpUser, task, between
import random, json, string, os, hashlib

# Ruta del archivo donde se almacenan los usuarios registrados
ARCHIVO_USUARIOS = "usuarios_registrados.json"

# Ruta del archivo donde se almacenan los productos
ARCHIVO_PRODUCTOS = "productos_cache.json"

# Función para generar datos aleatorios de usuario
def generar_usuario():
    nombre = ''.join(random.choices(string.ascii_lowercase, k=10))
    return {
        "nombre": nombre,
        "dni": ''.join(random.choices(string.digits, k=8)),  
        "email": nombre + "@gmail.com",
        "domicilio": "Calle 123",
        "password": "1234"
    }

# Cargar usuarios ya registrados del archivo (si existe)
def cargar_usuarios():
    if os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, "r") as f:
            return [json.loads(line.strip()) for line in f if line.strip()]
    return []

# Guardar nuevo usuario en el archivo
def guardar_usuario(usuario):
    with open(ARCHIVO_USUARIOS, "a") as f:
        f.write(json.dumps(usuario) + "\n")

def cargar_productos():
    if os.path.exists(ARCHIVO_PRODUCTOS):
        with open(ARCHIVO_PRODUCTOS, "r") as f:
            return json.load(f)
    return []

class MiUsuario(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        # Generar un usuario nuevo y almacenarlo localmente
        self.usuario = generar_usuario()
        self.usuarios_registrados = cargar_usuarios()
        self.autenticado = False
        # Crea una lista donde se almacenan los productos de la web
        self.productos_disponibles = cargar_productos()
        self.lista_pedidos = list()
        self.lista_pedidos = list()

    @task(2)
    def registro_post(self):
        response = self.client.post("/api/registro", data=self.usuario)
        
        if response.status_code == 200 and "redirect_url" in response.json():
            print("✅ Usuario registrado exitosamente")
            guardar_usuario(self.usuario)
            self.usuarios_registrados.append(self.usuario)
        else:
            print(f"❌ Error al registrar: {response.status_code} - {response.text}")

    @task(2)
    def login_post(self):
        if not self.usuarios_registrados:
            return  # Nada que logear aún

        usuario_random = random.choice(self.usuarios_registrados)
        response = self.client.post("/api/login", data={
            "email": usuario_random["email"],
            "password": usuario_random["password"]
        })

        if response.status_code == 200:
            self.autenticado = True
            print("✅ Login exitoso")
        else:
            print(f"❌ Error en login: {response.status_code}")

    @task(1)
    def register_get(self):
        self.client.get("/api/registro")

    @task(1)
    def login_get(self):
        self.client.get("/api/login")

    @task(1)
    def menu(self):
        self.client.get("/api/menu")

    @task(3)
    def agregar_producto_carrito(self):

        if not self.productos_disponibles:
            return 
        
        if self.autenticado:
            producto = random.choice(self.productos_disponibles)
            producto_id = producto["id"]
            # Datos que se enviarán en la solicitud POST
            data = {
                "id_producto": producto_id # Aquí pones el ID del producto que deseas agregar
            }

        if not self.productos_disponibles:
            return 
        
        if self.autenticado:
            producto = random.choice(self.productos_disponibles)
            producto_id = producto["id"]
            # Datos que se enviarán en la solicitud POST
            data = {
                "id_producto": producto_id # Aquí pones el ID del producto que deseas agregar
            }

            # Hacemos la solicitud POST al endpoint /agregar
            response = self.client.post(
                f"/api/carrito/agregar", 
                json=data
            )
            # Hacemos la solicitud POST al endpoint /agregar
            response = self.client.post(
                f"/api/carrito/agregar", 
                json=data
            )

            if response.status_code == 200:
                print("✅ Producto añadido")
            else:
                print(f"❌ Error al añadir producto")
        
            if response.status_code == 200:
                print("✅ Producto añadido")
            else:
                print(f"❌ Error al añadir producto")
        
    @task(1)
    def get_productos(self):
        response = self.client.get("/api/productos")

        if response.status_code == 200:
            print("✅ Muestreo de productos exitoso")
        else:
            print(f"❌ Error en el muestreo: {response.status_code}")
    
    @task(2)
    def get_producto_por_id(self):
        #Si no hay productos en la cache, nada
        if not self.productos_disponibles:
            return

        #Elige un producto random para ver sus detalles
        producto = random.choice(self.productos_disponibles)
        producto_id = producto["id"]
        response = self.client.get(f"/api/productos/{producto_id}")

        if response.status_code == 200:
            print(f"✅ Producto {producto_id} obtenido")
        else:
            print(f"❌ Error al obtener producto {producto_id}: {response.status_code}")

    @task(2)
    def checkout(self):
        response = self.client.post("/api/checkout")

        # Siempre intentamos parsear la respuesta como JSON, ya que el backend siempre devuelve JSON
        try:
            data = response.json()
        except ValueError:
            print(f"❌ Respuesta no es JSON válido - Código: {response.status_code}")
            return

        if response.status_code == 200:
            id_pedido = data.get("id_pedido")
            if id_pedido:
                self.lista_pedidos.append(id_pedido)
                print("✅ Pedido creado con ID:", id_pedido)
            else:
                print("⚠️ Respuesta 200 pero sin ID de pedido")
        elif response.status_code == 401:
            redirect_url = data.get("redirect_url")
            if redirect_url:
                print(f"🔒 No autorizado. Redirigiendo a: {redirect_url}")
            else:
                print("🔒 No autorizado sin URL de redirección")
        else:
            print(f"❌ Error inesperado ({response.status_code}): {data}")


    @task(2)
    def get_un_pedido(self):
        if self.lista_pedidos:
            id_random = random.choice(self.lista_pedidos)
            response = self.client.get(f"/api/pedidos/{id_random}")
            if response.status_code == 200:
                print(f"Se ha accedido al pedido {id_random}")
            else:
                print(f"Problema al acceder al pedido {id_random}")

    @task(2)
    def checkout(self):
        
        #esta funcion actua como un usuario de verdad, presiona el endpoint pero si no hay token de autentificación salta el Valueerror
        #para quitar esto se puede hacer como en otras funciones y meterlo dentro de un if self.autenticado:, esto ya no generara errores en locust pero no queremos eso ya que un usauio de verdad generaria un error
        # al presionmar ekl boton y no estar autenticado
        #Añadir el bloque try en las demas que los necesiten y quitar el self.autenticado

        response = self.client.post("/api/checkout")

        # Siempre intentamos parsear la respuesta como JSON, ya que el backend siempre devuelve JSON
        try:
            data = response.json()
        except ValueError:
            print(f"❌ Usuario no autenticado - Código: {response.status_code}")
            return

        if response.status_code == 200:
            id_pedido = data.get("id_pedido")
            if id_pedido:
                self.lista_pedidos.append(id_pedido)
                print("✅ Pedido creado con ID:", id_pedido)
            else:
                print("Respuesta 200 pero sin ID de pedido") # en este entorno este caso no se da 
        elif response.status_code == 402:
            redirect_url = data.get("redirect_url")
            if redirect_url:
                print(f"Sin items de carrito: {redirect_url}")
            else:
                print("Sin items de carrito")
        else:
            print(f"❌ Error inesperado ({response.status_code}): {data}")


    @task(2)
    def get_un_pedido(self):
        if self.lista_pedidos:
            id_random = random.choice(self.lista_pedidos)
            response = self.client.get(f"/api/pedidos/{id_random}")
            if response.status_code == 200:
                print(f"Se ha accedido al pedido {id_random}")
            else:
                print(f"Problema al acceder al pedido {id_random}")

