import os
from flask import Flask
from config import DevelopmentConfig, ProductionConfig

def create_app():
    app = Flask(__name__)
    
    # Determine if dev/prod based on FLASK_DEBUG
    if os.getenv('FLASK_DEBUG') == '1':
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(ProductionConfig)

    from .routes import main
    app.register_blueprint(main)
    
    return app