from flask import render_template, request, jsonify, send_file, current_app as app
from app.services.analysis_service import AnalysisService
from werkzeug.utils import secure_filename
import pandas as pd
import io
import os

# Initialisation unique du service pour toute l'application
service = AnalysisService()

@app.route('/')
def index():
    """Affiche l'interface de saisie individuelle."""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard_page():
    """Affiche la page du tableau de bord et de l'historique."""
    return render_template('dashboard.html')

@app.route('/get_symptoms', methods=['GET'])
def get_symptoms():
    """Récupère la liste des symptômes pour l'autocomplétion via le service."""
    return jsonify({"success": True, "symptoms": service.get_all_symptoms()})

@app.route('/analyze', methods=['POST'])
def analyze():
    """Calcule les scores de suspicion sans enregistrer immédiatement."""
    data = request.get_json()
    symptoms = data.get('symptoms', [])
    if not symptoms:
        return jsonify({"success": False, "message": "Aucun symptôme fourni"}), 400
    
    results = service.run_analysis(symptoms)
    return jsonify({"success": True, "results": results})

@app.route('/save_case', methods=['POST'])
def save_case():
    """Enregistre un dossier patient dans la base de données JSON."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Données manquantes"}), 400
    
    success = service.save_to_json(data)
    return jsonify({"success": success})

@app.route('/get_history', methods=['GET'])
def get_history():
    try:
        # Paramètres de pagination
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Nouveaux paramètres de filtrage
        f_code = request.args.get('code', '').lower()
        f_district = request.args.get('district', '').lower()
        f_date = request.args.get('date', '')

        all_history = service.get_history()

        # Application des filtres
        filtered_history = []
        for case in all_history:
            meta = case.get('metadata', {})
            
            match_code = f_code in str(meta.get('patient_code', '')).lower()
            match_district = f_district in str(meta.get('district', '')).lower()
            match_date = (f_date == meta.get('date')) if f_date else True

            if match_code and match_district and match_date:
                filtered_history.append(case)

        # Tri par date décroissante
        filtered_history.sort(key=lambda x: x.get('metadata', {}).get('date', ''), reverse=True)

        # Pagination sur la liste filtrée
        total_items = len(filtered_history)
        total_pages = (total_items + per_page - 1) // per_page if total_items > 0 else 1
        
        start = (page - 1) * per_page
        end = start + per_page
        
        return jsonify({
            "success": True, 
            "history": filtered_history[start:end],
            "total_pages": total_pages,
            "current_page": page,
            "total_items": total_items
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    
    
@app.route('/get_dashboard_stats', methods=['GET'])
def get_dashboard_stats():
    """Récupère les agrégats statistiques pour les graphiques et compteurs."""
    stats = service.get_dashboard_stats()
    return jsonify({"success": True, **stats})

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    """Traite un import massif de données via fichier CSV."""
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "Aucun fichier détecté"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": "Nom de fichier vide"}), 400

    if file and file.filename.endswith('.csv'):
        try:
            # Lecture du flux CSV
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            df = pd.read_csv(stream)
            
            for _, row in df.iterrows():
                # On suppose que les symptômes sont séparés par des virgules dans le CSV
                raw_symptoms = str(row.get('symptomes', ''))
                symptoms = [s.strip() for s in raw_symptoms.split(',') if s.strip()]
                
                if symptoms:
                    results = service.run_analysis(symptoms)
                    
                    record = {
                        "metadata": {
                            "district": row.get('district'),
                            "fosa": row.get('fosa'),
                            "date": row.get('date'),
                            "patient_code": row.get('code'),
                            "sexe": row.get('sexe'),
                            "age": row.get('age')
                        },
                        "symptoms_input": symptoms,
                        "results": results
                    }
                    service.save_to_json(record)
                
            return jsonify({"success": True, "count": len(df)})
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500
            
    return jsonify({"success": False, "message": "Format CSV requis"}), 400

@app.route('/export_report', methods=['POST'])
def export_report():
    """Génère un export CSV des résultats d'analyse actuels pour téléchargement."""
    data = request.get_json()
    results = data.get('results', [])
    if not results:
        return jsonify({"success": False, "message": "Aucune donnée à exporter"}), 400
        
    df = pd.DataFrame(results)
    
    # Utilisation de BytesIO pour générer le fichier en mémoire
    output = io.BytesIO()
    # encoding utf-8-sig pour assurer la compatibilité avec Excel (gestion des accents)
    df.to_csv(output, index=False, encoding='utf-8-sig')
    output.seek(0)
    
    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name='DetectX_SIMR_Rapport.csv'
    )

