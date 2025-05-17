from locust import HttpUser, task, between
import random, json, string, os

# === Archivos de persistencia ===
ARCHIVO_USUARIOS = "usuarios_registrados.json"
ARCHIVO_PRODUCTOS = "productos_cache.json"

# === Funciones auxiliares ===
def generar_usuario():
    nombre = ''.join(random.choices(string.ascii_lowercase, k=10))
    return {
        "nombre": nombre,
        "dni": ''.join(random.choices(string.digits, k=8)),
        "email": nombre + "@gmail.com",
        "domicilio": "Calle 123",
        "password": "1234"
    }

def cargar_json_lines(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return [json.loads(line.strip()) for line in f if line.strip()]
    return []

def guardar_json_line(path, data):
    with open(path, "a") as f:
        f.write(json.dumps(data) + "\n")

def cargar_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

# === Clase principal de usuario ===
class MiUsuario(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.usuario = generar_usuario()
        self.usuarios_registrados = cargar_json_lines(ARCHIVO_USUARIOS)
        self.autenticado = False
        self.productos_disponibles = cargar_json(ARCHIVO_PRODUCTOS)
        self.lista_pedidos = []

    def manejar_redireccion(self, response, mensaje_ok):
        if response.status_code == 200:
            print(mensaje_ok)
            response.success()
        elif response.status_code in [301, 302, 303, 307, 308]:
            print("❌ Redirigido")
            response.success()
        elif response.status_code == 401:
            response.failure("❌ No autorizado: token inválido o ausente (401)")
        else:
            response.failure(f"❌ Error inesperado ({response.status_code})")

    @task(2)
    def registro_post(self):
        response = self.client.post("/api/registro", data=self.usuario)
        if response.status_code == 200 and "redirect_url" in response.json():
            print("✅ Usuario registrado exitosamente")
            guardar_json_line(ARCHIVO_USUARIOS, self.usuario)
            self.usuarios_registrados.append(self.usuario)
        else:
            print(f"❌ Error al registrar: {response.status_code} - {response.text}")

    @task(2)
    def login_post(self):
        if not self.usuarios_registrados:
            return
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
            print("⚠️ No hay productos disponibles.")
            return

        producto = random.choice(self.productos_disponibles)
        data = {"id_producto": producto["id"]}

        with self.client.post("/api/carrito/agregar", json=data, allow_redirects=False, catch_response=True) as response:
            self.manejar_redireccion(response, "✅ Producto añadido al carrito")

    @task(1)
    def get_productos(self):
        response = self.client.get("/api/productos")
        if response.status_code == 200:
            print("✅ Muestreo de productos exitoso")
        else:
            print(f"❌ Error en el muestreo: {response.status_code}")

    @task(2)
    def get_producto_por_id(self):
        if not self.productos_disponibles:
            return
        producto = random.choice(self.productos_disponibles)
        response = self.client.get(f"/api/productos/{producto['id']}")
        if response.status_code == 200:
            print(f"✅ Producto {producto['id']} obtenido")
        else:
            print(f"❌ Error al obtener producto {producto['id']}: {response.status_code}")

    @task(3)
    def get_un_pedido(self):
        if not self.lista_pedidos:
            print("⚠️ No hay pedidos en la lista para consultar.")
            return
        id_random = random.choice(self.lista_pedidos)
        with self.client.get(f"/api/pedidos/{id_random}", catch_response=True) as response:
            self.manejar_redireccion(response, f"✅ Se ha accedido al pedido {id_random}")

    @task(2)
    def checkout(self):
        with self.client.post("/api/checkout", allow_redirects=False, catch_response=True) as response: #caso especial 
            try:
                if response.status_code == 200:
                    data = response.json()
                    id_pedido = data.get("id_pedido")
                    if id_pedido:
                        self.lista_pedidos.append(id_pedido)
                        print("✅ Pedido creado con ID:", id_pedido)
                        #borrar los items del carrito, esta tarear se hace de manera manual pero se necesita de un frontend por eso se simul asi en locust
                        response.success()
                        with self.client.delete("/api/carrito/vaciar", json=data, allow_redirects=False, catch_response=True) as response:
                            self.manejar_redireccion(response, "✅ Carrito vaciado")
                    else:
                        response.failure("Respuesta 200 sin 'id_pedido'")
                elif response.status_code == 402:
                    data = response.json()
                    print(f"Sin items de carrito: {data.get('redirect_url', 'No redirect_url')}")
                    response.success()
                else:
                    self.manejar_redireccion(response, "")
            except ValueError as e:
                response.failure(f"❌ Error al parsear JSON: {str(e)}")

    @task(2)
    def actualizar_producto_put(self):
        if not self.productos_disponibles:
            return

        producto = random.choice(self.productos_disponibles)
        nuevo_nombre = producto["nombre"] + random.choice([" Plus", " Premium", " Especial"])
        nueva_descripcion = (producto.get("descripcion") or "") + " (editado)"
        data = {
            "nombre": nuevo_nombre,
            "descripcion": nueva_descripcion,
            "precio": round(random.uniform(5.0, 20.0), 2),
            "stock": random.randint(1, 100),
            "tipo": random.choice(["Vegano", "Proteico", "Equilibrado"])
        }

        response = self.client.put(f"/api/productos/{producto['id']}", data=data)
        if response.status_code == 200:
            print(f"✅ Producto {producto['id']} actualizado completamente (PUT)")
        else:
            print(f"❌ Error al actualizar producto {producto['id']} con PUT: {response.status_code}")

    @task(2)
    def actualizar_tipo_patch(self):
        if not self.productos_disponibles:
            return

        producto = random.choice(self.productos_disponibles)
        tipo_actual = producto.get("tipo", "Vegano")
        nuevo_tipo = random.choice([t for t in ["Vegano", "Proteico", "Equilibrado"] if t != tipo_actual])
        data = {"tipo": nuevo_tipo}

        response = self.client.patch(f"/api/productos/{producto['id']}", json=data)
        if response.status_code == 200:
            producto["tipo"] = nuevo_tipo
            print(f"✅ Tipo del producto {producto['id']} actualizado a '{nuevo_tipo}'")
        else:
            print(f"❌ Error al actualizar tipo del producto {producto['id']}: {response.status_code}")
    
    @task(1)
    def get_carrito(self):
        response = self.client.get("/api/carrito")
        if response.status_code == 200:
            print("✅ El carrito se muestra correctamente")
        else:
            print(f"❌ Error al mostrar el carrito: {response.status_code}")

    @task(1)
    def delete_carrito(self):
        response = self.client.delete("/api/carrito/vaciar")
        if response.status_code == 200:
            print("✅ El carrito se vacia correctamente")
        else:
            print(f"❌ Error al vaciar el carrito: {response.status_code}")

    @task(1)
    def get_pedidos(self):
        response = self.client.get("/api/pedidos")
        if response.status_code == 200:
            print("✅ Los pedidos se muestran correctamente")
        else:
            print(f"❌ Error al mostrar los pedidos: {response.status_code}")
