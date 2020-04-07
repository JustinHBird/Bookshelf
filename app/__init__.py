from flask import current_app, Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # Register Blueprints
    from .routes import bp
    app.register_blueprint(bp)

    # Test route to make sure the app is running:
    @app.route('/hello')
    def hello():
        return ('Hello, World')
    
    return app



