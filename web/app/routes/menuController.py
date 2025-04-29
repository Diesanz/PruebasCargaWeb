
from flask import Blueprint, render_template, redirect, url_for
from app.db.conexiondb import Conexion
from app.models.Producto import Producto
from app.schemas.Producto import producto_schema
import random

menu = Blueprint('menu', __name__, url_prefix="/api/menu")

def get_id_random_productos():
    return random.sample(range(1, 14), 4)

#cambiar para trabajar con objetos
def get_produtos(ids=None):
    if ids is None:
        ids = get_id_random_productos()  # Genera los IDs si no se pasan como parámetro
    
    conn = Conexion()
    query = "SELECT * FROM Producto WHERE id IN %s" 
    productos = conn.select_db(query, (tuple(ids),))  # Pasa los IDs como una tupla
    
    productos_obj = [Producto(**producto_schema(p)) for p in productos] #validamos datos y tipamos
    
    return productos_obj

@menu.route('/', methods=['GET'])
def api_index():
    return render_template("index.html", productos = get_produtos()) # Renderiza el template para /api
