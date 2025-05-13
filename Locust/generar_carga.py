from locust import HttpUser, task, between
import random, json, string, os

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

    @task(3)
    def agregar_al_carrito(self):
        #Si no hay productos en la cache, nada
        if not self.productos_disponibles:
            return

        if self.autenticado:
            #Elige un producto random para agregarlo al carrito
            producto = random.choice(self.productos_disponibles)
            producto_id = producto["id"]
            response = self.client.post("/api/carrito/agregar")

            if response.status_code == 200:
                print(f"🛒 Producto {producto_id} añadido al carrito")
            else:
                print(f"❌ Error al añadir al carrito el producto {producto_id}: {response.status_code}")