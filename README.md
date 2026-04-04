# Detect-X | Clinical Decision Support & IDSR Surveillance

**Detect-X** is a software solution designed to strengthen epidemiological surveillance. It assists healthcare professionals in the rapid identification of suspected cases for priority diseases, based on the official case definitions of the Cameroon's **Integrated Disease Surveillance and Response (IDSR)** technical guidelines.

## 🌟 Key Features

* **Weighted Clinical Analysis**: Calculation of a suspicion score based on the clinical importance of symptoms (Major signs vs. Minor signs).
* **Comprehensive IDSR Database**: Covers 23 priority pathologies including Cholera, Hemorrhagic Fevers (Ebola, Marburg), Measles, and Poliomyelitis.
* **Dynamic Dashboard**: Real-time visualization of statistical aggregates, critical alerts, and geographical distribution by health district.
* **History Management**: Persistent archiving of consultations with advanced filters (Patient code, District, Date).
* **Bulk Import**: CSV import module with a real-time progress bar for processing large patient cohorts.

## 🛠️ Project Architecture

Based on the current system tree:

```text
DETECTX/
├── app/
│   ├── data/
│   │   ├── dict_patologies_weighted.json  # Knowledge Base (Criteria & Weights)
│   │   └── analyses_history.json          # NoSQL Database of cases
│   ├── services/
│   │   └── analysis_service.py            # Business logic and stats calculations
│   ├── templates/
│   │   ├── dashboard.html                 # Epidemiological tracking interface
│   │   └── index.html                     # Individual diagnostic interface
│   ├── engine.py                          # Rule engine for scoring
│   ├── routes.py                          # REST API and workflow management
│   └── models.py                          # Data structure definitions
├── static/                                # CSS, JS, and Image resources
├── run.py                                 # Flask application entry point
├── generate_test_data.py                  # Test data generation script
└── requirements.txt                       # Dependencies (Flask, Pandas, etc.)
```

## 🚀 Quick Start

1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Data Configuration**:
    Ensure the file `dict_patologies_weighted.json` is present in the `app/data/` directory.

3.  **Launch**:
    ```bash
    python run.py
    ```
    The app will be available at `http://127.0.0.1:5000`.

## 📊 Scoring Methodology

The rule engine uses a rigorous weighting system:
* **Weight 3**: Pathognomonic or Major sign (defines the case).
* **Weight 2**: Important sign (strongly suggestive).
* **Weight 1**: Minor or General sign (common to multiple pathologies).

$$Score = \left( \frac{\sum \text{Weights of detected signs}}{\sum \text{Total weights of the disease}} \right) \times 100$$

## ⚖️ Compliance and Ethics

The application includes a mandatory **Disclaimer** at the start of each session. Detect-X is a **clinical reflection support tool** and never replaces the final diagnosis of a physician or biological confirmation in a laboratory.

---
*Project developed by Miltiade Tchifou Diefi.*
