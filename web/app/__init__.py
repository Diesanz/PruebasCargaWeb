from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.secret_key = 'clave-super-secreta-123'
    
    # Importas el Blueprint de autentificar
    from .routes.autentificar import autentificar_usuarios
    from .routes.carritoController import carrito
    from .routes.menuController import menu
    from .routes.pedidoController import pedido
    from .routes.productosController import producto

    app.register_blueprint(autentificar_usuarios)
    app.register_blueprint(carrito)
    app.register_blueprint(menu)
    app.register_blueprint(pedido)
    app.register_blueprint(producto)

    return app