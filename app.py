from app import create_app

# Création de l'instance de l'application
app = create_app()

if __name__ == '__main__':
    # Lancement du serveur sur le port 5000
    # debug=True permet de voir les modifications en temps réel
    app.run(debug=True)