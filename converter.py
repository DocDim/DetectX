import csv
import json

def csv_to_rules_json(csv_file_path, json_file_path):
    syndromes = []
    
    # Utilisation de 'latin-1' ou 'cp1252' pour supporter les caractères accentués français d'Excel
    try:
        with open(csv_file_path, mode='r', encoding='cp1252') as csvfile:
            # On définit le délimiteur (souvent ';' dans les CSV Excel français)
            reader = list(csv.reader(csvfile, delimiter=','))
            
            if not reader:
                print("Le fichier est vide.")
                return

            header = reader[0]
            syndrome_names = [name.strip() for name in header[1:] if name.strip()] 

            disease_map = {name: {"id": f"S{i+1:03}", "nom": name, "criteres": []} 
                          for i, name in enumerate(syndrome_names)}

            for row in reader[1:]:
                if not row or not row[0]: continue
                
                symptome = row[0].strip()
                for i, presence in enumerate(row[1:]):
                    if i < len(syndrome_names):
                        if presence.strip().upper() == 'X':
                            current_syndrome = syndrome_names[i]
                            disease_map[current_syndrome]["criteres"].append(symptome)

            syndromes = list(disease_map.values())

    except FileNotFoundError:
        print(f"Erreur : Le fichier {csv_file_path} est introuvable.")
        return
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        return

    output_data = {
        "metadata": {
            "project": "Detect-X",
            "version": "1.1",
            "description": "Règles extraites avec support des caractères spéciaux"
        },
        "syndromes": syndromes
    }

    with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(output_data, jsonfile, indent=4, ensure_ascii=False)
    
    print(f"Conversion réussie ! Fichier généré : {json_file_path}")

# IMPORTANT : Assurez-vous d'utiliser le nom exact du fichier CSV, pas le .xlsx
csv_to_rules_json('rules.csv', 'rules.json')