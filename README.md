# Detect-X | Aide à la Décision Clinique & Surveillance SIMR

**Detect-X** est une solution logicielle conçue pour renforcer la surveillance épidémiologique au Cameroun. Elle permet aux professionnels de santé d'identifier rapidement les cas suspects de pathologies prioritaires en s'appuyant sur les protocoles officiels de la **Surveillance Intégrée des Maladies et la Riposte (SIMR)**.

## 🌟 Fonctionnalités

* **Analyse Clinique Pondérée** : Calcul d'un score de suspicion basé sur l'importance clinique des symptômes (Signes majeurs vs signes mineurs).
* **Base SIMR Complète** : Couvre 23 pathologies incluant le Choléra, les Fièvres Hémorragiques (Ebola, Marbourg), la Rougeole, et la Poliomyélite.
* **Tableau de Bord Dynamique** : Visualisation des agrégats statistiques, alertes critiques et répartition par district de santé.
* **Gestion de l'Historique** : Archivage persistant des consultations avec filtres avancés (Code patient, District, Date).
* **Importation Massive** : Module d'import CSV avec barre de progression pour le traitement de larges cohortes de données.

## 🛠️ Architecture du Projet

D'après l'arborescence actuelle du système :

```text
DETECTX/
├── app/
│   ├── data/
│   │   ├── dict_patologies_weighted.json  # Base de connaissances (Critères & Poids)
│   │   └── analyses_history.json          # Base de données NoSQL des cas
│   ├── services/
│   │   └── analysis_service.py            # Logique métier et calculs stats
│   ├── templates/
│   │   ├── dashboard.html                 # Interface de suivi épidémiologique
│   │   └── index.html                     # Interface de diagnostic individuel
│   ├── engine.py                          # Moteur de règles de calcul (Scoring)
│   ├── routes.py                          # API Rest et gestion des flux
│   └── models.py                          # Définitions des structures de données
├── static/                                # Ressources CSS, JS et Images
├── run.py                                 # Point d'entrée de l'application Flask
└── requirements.txt                       # Dépendances (Flask, Pandas, etc.)
```

## 🚀 Installation Rapide

1.  **Installation des dépendances** :
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configuration des données** :
    Vérifiez que le fichier `dict_patologies_weighted.json` est présent dans `app/data/`.

3.  **Lancement** :
    ```bash
    python run.py
    ```

## 📊 Méthodologie de Calcul

Le moteur de règles utilise une pondération rigoureuse :
* **Poids 3** : Signe pathognomonique ou majeur (définit le cas).
* **Poids 2** : Signe important (fortement évocateur).
* **Poids 1** : Signe mineur ou général (commun à plusieurs pathologies).

$$Score = \left( \frac{\sum \text{Poids des signes détectés}}{\sum \text{Poids totaux de la maladie}} \right) \times 100$$

## ⚖️ Conformité et Éthique

L'application intègre un **Avis de non-responsabilité** (Disclaimer) obligatoire à chaque session. Detect-X est un outil de **support à la réflexion clinique** et ne remplace jamais le diagnostic final d'un médecin ou la confirmation biologique en laboratoire.

---
*Projet développé par Tchifou M. Dieffi.*
