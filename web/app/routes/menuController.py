from flask import Blueprint, render_template, redirect, url_for
from app.db.conexiondb import Conexion
from app.models.Producto import Producto
from app.schemas.Producto import producto_schema
import random

menu = Blueprint('menu', __name__, url_prefix="/api/menu")

def get_id_random_productos():
    """
    Genera una lista de 4 IDs aleatorios de productos.

    Returns:
        list[int]: Lista con 4 IDs únicos dentro del rango de 1 a 13 (inclusive).
    """
    return random.sample(range(1, 14), 4)

#Método que obtiene cuatro productos para mostrar en la pagina web
def get_produtos(ids=None):
    """
    Obtiene una lista de objetos Producto a partir de una lista de IDs.

    Si no se proporcionan IDs, se generan aleatoriamente mediante `get_id_random_productos`.

    Args:
        ids (list[int], optional): Lista de IDs de productos a recuperar. 
                                   Si no se proporciona, se generan aleatoriamente.

    Returns:
        list[Producto]: Lista de productos obtenidos desde la base de datos.
    """
    if ids is None:
        ids = get_id_random_productos()  # Genera los IDs si no se pasan como parámetro
    
    conn = Conexion()
    query = "SELECT * FROM Producto WHERE id IN %s" 
    productos = conn.select_db(query, (tuple(ids),))  # Pasa los IDs como una tupla
    
    productos_obj = [Producto(**producto_schema(p)) for p in productos] # Validamos datos y tipamos
    
    return productos_obj

#Endpoint que devuelve la información principal de la página web
@menu.route('/', methods=['GET'])
def api_index():
    """
    Renderiza la página principal con una selección aleatoria de productos.

    Returns:
        HTML: Página 'index.html' con los productos pasados como contexto.
    """
    return render_template("index.html", productos = get_produtos()) # Renderiza el template para /api