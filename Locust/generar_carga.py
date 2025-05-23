from locust import HttpUser, task, between
import random, json, string, os


# === Archivo de persistencia ===
ARCHIVO_PRODUCTOS = "productos_cache.json"

# === Funciones auxiliares ===
def generar_usuario():
    """Genera un usuario con datos aleatorios

    Return: dict con datos del usuario
    """
    nombre = ''.join(random.choices(string.ascii_lowercase, k=10))
    return {
        "nombre": nombre,
        "dni": ''.join(random.choices(string.digits, k=8)),
        "email": nombre + "@gmail.com",
        "domicilio": "Calle 123",
        "password": "1234"
    }

def cargar_json(path):
    """Carga un archivo JSON completo

    Keyword arguments:
    path -- ruta del archivo
    Return: objeto JSON o lista vacía
    """
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

# === Clase principal de usuario ===
class MiUsuario(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        """Se ejecuta al iniciar cada usuario de prueba

        Return: None
        """
        self.usuario = generar_usuario()
        self.autenticado = False
        self.productos_disponibles = cargar_json(ARCHIVO_PRODUCTOS)
        self.lista_pedidos = []
        self.login = False

        with self.client.post("/api/registro", data=self.usuario, catch_response=True) as response:
            if response.status_code == 200 and "redirect_url" in response.json():
                print("✅ Usuario registrado exitosamente")
                response.success()
            else:
                response.failure(f"❌ Error al registrar: {response.status_code} - {response.text}")
        
    def manejar_redireccion(self, response, mensaje_ok):
        """Gestiona respuestas HTTP, chequeando redirecciones y errores

        Keyword arguments:
        response -- respuesta HTTP
        mensaje_ok -- mensaje a mostrar si es exitosa
        Return: True si OK y False redirección válida, o si error
        """
        if response.status_code == 200:
            print(mensaje_ok)
            return True
        elif response.status_code in [301, 302, 303, 307, 308]:
            print("❌ Redirigido por problemas con el token")
            return False
        elif response.status_code == 401:
            print("❌ No autorizado: token inválido o ausente (401)")
            return False
        else:
            print(f"❌ Error inesperado ({response.status_code})")
            return False
        
    @task(2)
    def intentar_login(self):
        """Tarea para login con usuario registrado aleatorio

        Return: None
        """
        if self.login is False:
            with self.client.post("/api/login", data={
                "email": self.usuario["email"],
                "password": self.usuario["password"]
            }, catch_response=True) as response:
                if response.status_code == 200:
                    self.login = True
                    print(f"🔐 Login exitoso{self.lista_pedidos}")
                    return True
                else:
                    self.login = False
                    print("❌ Login fallido")
                    return False

    @task(1)
    def register_get(self):
        """Tarea para solicitar la página de registro vía GET

        Return: None
        """
        self.client.get("/api/registro")

    @task(1)
    def login_get(self):
        """Tarea para solicitar la página de login vía GET

        Return: None
        """
        self.client.get("/api/login")

    @task(2)
    def menu(self):
        """Tarea para obtener el menú vía GET

        Return: None
        """
        self.client.get("/api/menu")
    
    @task(2)
    def get_productos(self):
        """Tarea para obtener la lista de productos vía GET

        Return: None
        """
        response = self.client.get("/api/productos")
        if response.status_code == 200:
            print("✅ Muestreo de productos exitoso")
        else:
            print(f"❌ Error en el muestreo: {response.status_code}")

    @task(1)
    def get_producto_por_id(self):
        """Tarea para obtener un producto aleatorio por ID vía GET

        Return: None
        """
        if not self.productos_disponibles:
            return

        producto = random.choice(self.productos_disponibles)
        response = self.client.get(f"/api/productos/{producto['id']}")
        if response.status_code == 200:
            print(f"✅ Producto {producto['id']} obtenido")
        else:
            print(f"❌ Error al obtener producto {producto['id']}: {response.status_code}")

    @task(3)
    def agregar_producto_carrito(self):
        """Tarea para agregar un producto aleatorio al carrito vía POST

        Return: None
        """
        if not self.productos_disponibles:
            print("⚠️ No hay productos disponibles.")
            return

        producto = random.choice(self.productos_disponibles)
        data = {"id_producto": producto["id"]}

        with self.client.post("/api/carrito/agregar", json=data, allow_redirects=False, catch_response=True) as response:
            if self.manejar_redireccion(response, "✅ Producto añadido al carrito"):
                response.success()
            else:
                response.failure(f"❌ Fallo al agregar producto al carrito {response.status_code}")

    @task(2)
    def checkout(self):
        """Tarea para realizar checkout y vaciar carrito

        Return: None
        """
        with self.client.post("/api/checkout", allow_redirects=False, catch_response=True) as response:
            try:
                if response.status_code == 200:
                    data = response.json()
                    if 'id_pedido' in data:
                        id_pedido = data.get("id_pedido")
                        self.lista_pedidos.append(id_pedido)
                        print("✅ Pedido creado con ID:", id_pedido)
                        response.success()
                        
                    elif 'redirect_url' in data:
                        print("⚠️ Sin items de carrito")
                        response.success()
                    else:
                        response.failure("Respuesta 200 sin 'id_pedido'")
                else:
                    if self.manejar_redireccion(response, ""):
                        response.success()
                    else:
                        response.failure(f"❌ Fallo en checkout {response.status_code}")
            except ValueError as e:
                response.failure(f"❌ Error al parsear JSON: {str(e)}")

    
    @task(1)
    def get_carrito(self):
        """Tarea para obtener el carrito vía GET

        Return: None
        """
        with self.client.get("/api/carrito", allow_redirects=False, catch_response=True) as response:
            if self.manejar_redireccion(response, "✅ El carrito se muestra correctamente"):
                response.success()
            else:
                response.failure(f"❌ Fallo al obtener el carrito {response.status_code}")

    @task(1)
    def delete_carrito(self):
        """Tarea para vaciar el carrito vía DELETE

        Return: None
        """
        with self.client.delete("/api/carrito/vaciar", allow_redirects=False, catch_response=True) as response:
            if self.manejar_redireccion(response, "✅ El carrito se vacia correctamente"):
                response.success()
            else:
                response.failure(f"❌ Fallo al vaciar el carrito {response.status_code}")
    
    @task(1)
    def get_pedidos(self):
        """Tarea para obtener la lista de pedidos vía GET

        Return: None
        """
        if self.lista_pedidos: #ya que en los pedidos a la hora de cargarlos se usa paginación, para no sobrecargar la db.
                            # con esto se simula como un usuario va a ir accediendo a sus diferentes páginas de pedidos.
            num_ped = len(self.lista_pedidos)
            paginas = (num_ped // 4) + (1 if num_ped % 4 > 0 else 0)
            pagina_rand = random.randint(1,paginas)
            url = f"/api/pedidos?page={pagina_rand}"
        else:
            url = "/api/pedidos"

        with self.client.get(url, allow_redirects=False, catch_response=True) as response:
            if self.manejar_redireccion(response, "✅ Los pedidos se muestran correctamente"):
                response.success()
            else:
                response.failure(f"❌ Fallo al obtener pedidos {response.status_code}")

    @task(1)
    def get_un_pedido(self):
        """Tarea para obtener un pedido aleatorio de la lista vía GET

        Return: None
        """
        if not self.lista_pedidos:
            print("⚠️ No hay pedidos en la lista para consultar.")
            return

        id_random = random.choice(self.lista_pedidos)

        with self.client.get(f"/api/pedidos/{id_random}", catch_response=True) as response:
            if self.manejar_redireccion(response, f"✅ Se ha accedido al pedido {id_random}"):
                response.success()
            else:
                response.failure(f"❌ Error al consultar pedido {response.status_code}")

    @task(2)
    def actualizar_producto_put(self):
        """Tarea para actualizar producto completo vía PUT

        Return: None
        """
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

        with self.client.put(f"/api/productos/{producto['id']}", data=data, catch_response= True) as response:
            if self.manejar_redireccion(response, f"✅ Producto {producto['id']} actualizado completamente (PUT)"):
                response.success()
            else:
                response.failure(f"❌ Error al actualizar producto {producto['id']} con PUT: {response.status_code}")

    @task(2)
    def actualizar_tipo_patch(self):
        """Tarea para actualizar solo el tipo del producto vía PATCH

        Return: None
        """
        if not self.productos_disponibles:
            return

        producto = random.choice(self.productos_disponibles)
        tipo_actual = producto.get("tipo", "Vegano")
        nuevo_tipo = random.choice([t for t in ["Vegano", "Proteico", "Equilibrado"] if t != tipo_actual])
        data = {"tipo": nuevo_tipo}

        with self.client.patch(f"/api/productos/{producto['id']}", json=data, catch_response= True) as response:
            if self.manejar_redireccion(response, f"✅ Tipo del producto {producto['id']} actualizado a '{nuevo_tipo}'"):
                response.success()
            else:
                response.failure(f"❌ Error al actualizar tipo del producto {producto['id']}: {response.status_code}")

    @task(1)
    def cerrar_sesion(self):
        """Tarea para cerrar sesión vía GET

        Return: None
        """
        with self.client.get("/api/logout", allow_redirects=False, catch_response=True) as response:
            if self.manejar_redireccion(response, "✅ Cierre de sesión correcto"):
                self.login = False
                response.success()
            else:
                response.failure(f"❌ Fallo al cerrar sesión {response.status_code} ")
   