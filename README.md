# Proyecto Pruebas de carga spbre una página web

El objetivo principal es realizar pruebas de carga para evaluar el rendimiento de un servidor web, utilizando Locust para simular tráfico concurrente.

Para ello, se ha desarrollado una página web con Flask, sobre la cual se ejecutan distintas pruebas de carga con Locust para recoger datos relevantes del rendimiento.

Además, se monitoriza el sistema mediante Grafana, apoyándonos en el trabajo realizado en la práctica anterior, para obtener métricas del sistema y métricas de negocio que ayuden a interpretar los resultados.

Finalmente, se analizarán los datos recogidos para identificar posibles cuellos de botella y evaluar la escalabilidad del servidor bajo diferentes niveles de carga.

Esta práctica permite afianzar conocimientos sobre pruebas de rendimiento, monitorización y análisis de sistemas, así como comprender la importancia de estas herramientas en entornos de producción donde la disponibilidad y la capacidad de respuesta del servidor son factores críticos.

## Requisitos

Antes de empezar, asegúrate de tener los siguientes requisitos:

- Python 3.x
- pip (gestor de paquetes de Python)

## Configuración del entorno

### 1. **Crear y activar el entorno virtual**:

   - En sistemas **Windows**:
     ```bash
     python -m venv env_pruebas
     .\env_pruebas\Scripts\activate
     ```
     
   - En sistemas **Linux/macOS**:
     ```bash
     python3 -m venv env_pruebas
     source env_pruebas/bin/activate
     ```

### 1.2. **Activar entorno de manera rápida**
  - Con el fin de activar el entorno de una manera fácil se ha **creado** un alias dentro de `~/.bashrc` llamado `entorno`:
    ```bash
    alias entorno='source /home/usuario/esi/PruebasCargaWeb/env_pruebas/bin/activate'
    ```
  - De esta forma solo con introducir el comando `entorno` desde cualquier parte, se pueden utilizar las diferentes librerias instaladas y ejecutar la aplicación.
  - Para desactivar el entorno solo hace falta introducir el comando `deactivate` en la terminal.

### 2. **Instalar las dependencias**:

   Una vez el entorno virtual esté activo, instala las dependencias del proyecto con el siguiente comando:

   ```bash
   pip install -r requirements.txt
   ```
### 3. **Ejecutar la api**:
  ```bash
  python run.py
  ```
### 4. **Volcado de base de datos**:
```bash
mysqldump -u user_pr -p Carga_web Usuario Producto Carrito CarritoItem Pedido PedidoItem > carga_web_dump.sql
mysqldump -u user_pr -p --routines --no-create-info Carga_web >> carga_web_dump.sql
```
### Para más información revisar el documento Latex
