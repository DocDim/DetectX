import os

class Config:
    # Chemin de base du projet (E:\DevProjet\DetectX)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Chemin vers le fichier des règles JSON 
    RULES_FILE_PATH = os.path.join(BASE_DIR, 'data', 'rules.json')
    
    # Dossier pour les téléchargements CSV 
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'data', 'uploads')
    
    # Clé secrète pour la sécurité des sessions (utile pour Flask) 
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'detectx-dev-key-2026'

    # Configuration de l'analyse
    DEBUG = True