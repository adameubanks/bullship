from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    app.secret_key = Config.STRIPE_SECRET_KEY

    from .routes import main
    app.register_blueprint(main)

    return app
