# Proyecto Tienda Online

Este es un proyecto de tienda online, donde se gestionan productos, usuarios, y pedidos. Se ha desarrollado utilizando **Flask** y un entorno virtual para la gestión de dependencias.

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
     * **Corrección:** El nombre de la carpeta del entorno virtual es `env_pruebas`, por lo que la ruta para activar debe coincidir.

   - En sistemas **Linux/macOS**:
     ```bash
     python3 -m venv env_pruebas
     source env_pruebas/bin/activate
     ```
     * **Corrección:** Para mantener la consistencia, te recomiendo usar el mismo nombre para el entorno virtual en ambos sistemas: `env_pruebas`.

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
	
