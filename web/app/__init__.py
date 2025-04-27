from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.secret_key = 'clave-super-secreta-123'
    
    # Importas el Blueprint de autentificar
    from .routes.autentificar import autentificar_usuarios
    from .routes.carritoController import carrito

    app.register_blueprint(autentificar_usuarios)
    app.register_blueprint(carrito)

    return app