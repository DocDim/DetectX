import json
import os

class DetectXEngine:
    def __init__(self):
        # Utilisation du fichier de connaissances avec poids (Standard OMS/SIMR)
        # self.dict_path = os.path.join('app', 'data', 'dict_patologies_weighted.json')
        # SI votre dossier 'data' est à la RACINE du projet, utilisez plutôt :
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.dict_path = os.path.join(os.path.dirname(base_dir), 'engineData', 'dict_patologies_weighted.json')
        self.syndromes = self._load_dict()

    def _load_dict(self):
        """
        Charge les définitions de cas cliniques et les poids associés 
        depuis la base de connaissances.
        """
        try:
            if not os.path.exists(self.dict_path):
                print(f"Erreur : {self.dict_path} est introuvable.")
                return []
            with open(self.dict_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement de la base SIMR : {e}")
            return []

    def analyze(self, user_symptoms):
        """
        Calcule le score de suspicion en fonction de l'importance clinique (poids).
        Standard SIMR / OMS.
        """
        results = []
        # Normalisation des entrées pour la comparaison
        user_symptoms = [s.strip().lower() for s in user_symptoms]

        for disease in self.syndromes:
            # 1. Calculer le dénominateur (Somme de tous les poids possibles)
            total_possible_weight = sum(critere['poids'] for critere in disease['criteres'])
            
            detected_weight = 0
            matched_symptoms = []

            # 2. Calculer le numérateur (Somme des poids des signes présents)
            for critere in disease['criteres']:
                nom_critere = critere['nom'].lower()
                
                if nom_critere in user_symptoms:
                    detected_weight += critere['poids']
                    matched_symptoms.append(critere['nom'])

            # 3. Générer le résultat si une correspondance existe
            if detected_weight > 0:
                score = round((detected_weight / total_possible_weight) * 100)
                
                results.append({
                    "maladie": disease['maladie'],
                    "definition": disease.get('definition_cas', 'N/A'), #
                    "score": score,
                    "symptomes_detectes": matched_symptoms,
                    "seuil_alerte": disease.get('seuil_alerte', 'N/A') #
                })

        # Tri par pertinence (score le plus élevé)
        return sorted(results, key=lambda x: x['score'], reverse=True)