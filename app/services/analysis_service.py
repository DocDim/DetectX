import json
import os
from datetime import datetime
from app.engine import DetectXEngine

class AnalysisService:
    def __init__(self):
        self.engine = DetectXEngine()
        # Chemin vers la base de données des cas enregistrés
        self.db_path = os.path.join('app', 'data', 'analyses_history.json')
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        """Crée le fichier JSON de la base de données s'il n'existe pas."""
        if not os.path.exists(self.db_path):
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def get_all_symptoms(self):
        """
        Extrait les noms uniques de symptômes depuis la base de connaissances 
        pondérée pour l'autocomplétion.
        """
        symptoms_set = set()
        for syndrome in self.engine.syndromes:
            for critere_obj in syndrome.get('criteres', []):
                # Correction : critere_obj est un dict {"nom": "...", "poids": X}
                nom_symptome = critere_obj.get('nom', '')
                if nom_symptome:
                    symptoms_set.add(nom_symptome.strip().lower())
        return sorted(list(symptoms_set))

    def run_analysis(self, symptoms):
        """Exécute l'analyse pondérée via le moteur DetectX."""
        return self.engine.analyze(symptoms)

    def save_to_json(self, record):
        """Gère la persistance des données avec sécurité contre la corruption."""
        os.makedirs('data', exist_ok=True)
        history = []
        
        # Lecture sécurisée
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content: # Vérifie que le fichier n'est pas vide
                        history = json.loads(content)
            except (json.JSONDecodeError, IOError) as e:
                print(f"⚠️ Warning: Base de données corrompue ou vide, réinitialisation... ({e})")
                history = []
        
        # Ajout et sauvegarde
        history.append(record)
        try:
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Erreur critique lors de l'écriture : {e}")

    def get_history(self):
        """Récupère tous les cas enregistrés."""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def get_dashboard_stats(self):
        """Calcule les agrégats statistiques pour le tableau de bord."""
        cases = self.get_history()
        total_cases = len(cases)
        
        if total_cases == 0:
            return {
                "total_cases": 0,
                "critical_count": 0,
                "districts_count": 0,
                "avg_score": 0,
                "disease_distribution": {}
            }

        critical_count = 0
        districts = set()
        total_scores = 0
        disease_counts = {}

        for case in cases:
            # Metadata
            districts.add(case.get('metadata', {}).get('district', 'Inconnu'))
            
            # Résultats
            results = case.get('results', [])
            if results:
                main_result = results[0]  # Le plus probable
                score = main_result.get('score', 0)
                total_scores += score
                if score >= 50:
                    critical_count += 1
                
                # Distribution
                disease_name = main_result.get('maladie')
                disease_counts[disease_name] = disease_counts.get(disease_name, 0) + 1

        return {
            "total_cases": total_cases,
            "critical_count": critical_count,
            "districts_count": len(districts),
            "avg_score": round(total_scores / total_cases) if total_cases > 0 else 0,
            "disease_distribution": disease_counts
        }