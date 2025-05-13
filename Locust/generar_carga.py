from locust import HttpUser, task, between
import random, json, string, os, hashlib

# Ruta del archivo donde se almacenan los usuarios registrados
ARCHIVO_USUARIOS = "usuarios_registrados.json"

def hash_sha256(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

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

class MiUsuario(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        # Generar un usuario nuevo y almacenarlo localmente
        self.usuario = generar_usuario()
        self.usuarios_registrados = cargar_usuarios()

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
    def agregar_producto_carrito(self):
        # Datos que se enviarán en la solicitud POST
        data = {
            "id_producto": 10 # Aquí pones el ID del producto que deseas agregar
        }

        # Hacemos la solicitud POST al endpoint /agregar
        response = self.client.post(
            f"/api/carrito/agregar", 
            json=data
        )

        if response.status_code == 200:
            print("✅ Producto añadido")
        else:
            print(f"❌ Error al añadir producto")
