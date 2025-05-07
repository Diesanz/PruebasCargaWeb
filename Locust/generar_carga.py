from locust import HttpUser, task, between
import random, json
import string
import time

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

class MiUsuario(HttpUser):
    wait_time = between(1, 2)  # Espera entre 1 y 2 segundos entre tareas

    
    def on_start(self):
        # Genera un usuario aleatorio
        self.usuario = generar_usuario()
        
        start = time.perf_counter()
        # Realiza la solicitud de registro
        response = self.client.post("/api/registro", data={
            "nombre": self.usuario['nombre'],
            "dni":  self.usuario['dni'],  
            "email":  self.usuario['email'],
            "domicilio": self.usuario['domicilio'],
            "password": self.usuario['password']
        })

        if response.status_code == 200:
            print("Usuario registrado exitosamente")
            print("Tiempo en crear usuario procedimiento:", time.perf_counter() - start)
            with open("usuarios_registrados.json", "a") as f:
                f.write(json.dumps(self.usuario) + "\n")
        else:
            print("Error al registrar el usuario ")

    @task
    def login(self):
        # Si ya se registraron usuarios previamente, intentar hacer login con los datos 
        if self.usuario:

            response = self.client.post("/api/login", data={
                "email": self.usuario['email'],
                "password": self.usuario['password']
            })

            # Verifica si el login fue exitoso
            if response.status_code == 200:
                print(f"Login exitoso")
            else:
                print(f"Error al hacer login")


        self.stop()