from flask import Flask
from config import Config

def create_app(config_class=Config):
    """
    Usine de création de l'application (Application Factory).
    Initialise Flask avec la configuration personnalisée.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Importation des routes et du moteur ici pour éviter les imports circulaires
    with app.app_context():
        from app import routes
        
    return app