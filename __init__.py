import os
from flask import Flask
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
	SECRET_KEY = None
	STRIPE_SECRET_KEY = None
	STRIPE_PUBLISHABLE_KEY = None
	STRIPE_PRICE_ID = None

class DevelopmentConfig(Config):
	SECRET_KEY = os.getenv('SECRET_KEY_DEV')
	STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY_DEV')
	STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY_DEV')
	STRIPE_PRICE_ID = os.getenv('STRIPE_PRICE_ID_DEV')

class ProductionConfig(Config):
	SECRET_KEY = os.getenv('SECRET_KEY_PROD')
	STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY_PROD')
	STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY_PROD')
	STRIPE_PRICE_ID = os.getenv('STRIPE_PRICE_ID_PROD')

def create_app():
	app = Flask(__name__)

	env = os.getenv('ENVIRONMENT', 'development')

	if env == 'production':
		app.config.from_object(ProductionConfig)
	else:
		app.config.from_object(DevelopmentConfig)

	from .routes import main
	app.register_blueprint(main)

	return app