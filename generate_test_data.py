import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Configuration
PATHOLOGIES_SIMR = {
    "Choléra": ["diarrhée aqueuse profuse", "vomissements", "déshydratation sévère", "selles en eau de riz"],
    "Méningite": ["fièvre brutale", "céphalées", "raideur de la nuque", "photophobie"],
    "Fièvre Jaune": ["fièvre", "ictère (jaunisse)", "douleurs lombaires", "ictère dans les 14 jours"],
    "Rougeole": ["fièvre", "éruption maculo-papuleuse", "toux", "conjonctivite"],
    "Poliomyélite (PFA)": ["paralysie flasque aiguë", "diminution du tonus", "apparition brutale"]
}

SYMPTOMES_BENINS = ["fatigue légère", "rhume", "douleur légère au bras", "petite toux", "stress", "insomnie"]

districts = ["Yaoundé I", "Douala IV", "Bafoussam", "Garoua", "Maroua", "Bertoua"]
fosas = ["CMA", "Hôpital de District", "Centre de Santé", "Dispensaire"]

def generate_data(n=100, suspects_count=30):
    data = []
    start_date = datetime(2026, 1, 1)

    for i in range(n):
        is_suspect = i < suspects_count
        date_random = start_date + timedelta(days=random.randint(0, 80))
        
        # Sélection des symptômes
        if is_suspect:
            # On pioche une maladie et on prend 2 à 4 de ses critères
            maladie = random.choice(list(PATHOLOGIES_SIMR.keys()))
            symptomes_liste = random.sample(PATHOLOGIES_SIMR[maladie], random.randint(2, len(PATHOLOGIES_SIMR[maladie])))
        else:
            # Symptômes aléatoires qui ne matchent pas les définitions de cas
            symptomes_liste = random.sample(SYMPTOMES_BENINS, random.randint(1, 3))

        patient = {
            "district": random.choice(districts),
            "fosa": random.choice(fosas),
            "date": date_random.strftime("%Y-%m-%d"),
            "code": f"PAT-{1000 + i}",
            "sexe": random.choice(["M", "F"]),
            "age": random.randint(1, 75),
            "symptomes": ",".join(symptomes_liste)
        }
        data.append(patient)

    # Mélanger pour ne pas avoir tous les suspects au début
    random.shuffle(data)
    return pd.DataFrame(data)

# Génération et sauvegarde
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(os.path.dirname(base_dir), 'DetectX', 'tests', 'test_patients_100.csv')

df_test = generate_data(100, 30)
df_test.to_csv(file_path, index=False, encoding='utf-8-sig')

print("✅ Fichier 'test_patients_100.csv' généré avec succès.")
print(f"📊 Total: 100 | Suspects: 30 | Sains: 70")