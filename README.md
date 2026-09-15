# ChurnScope

**Prediction, Explicabilite (SHAP), Aide a la Decision et Surveillance (MLOps) du Churn Client.**

[![CI/CD Pipeline](https://github.com/jouvence13/ChurnScope/actions/workflows/ci.yml/badge.svg)](https://github.com/jouvence13/ChurnScope/actions)
[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linting: flake8](https://img.shields.io/badge/linting-flake8-green.svg)](https://flake8.pycqa.org/)
[![Security: RGPD](https://img.shields.io/badge/security-RGPD%20%2F%20PII%20Hash-success.svg)](https://www.cnil.fr/)

---

## Presentation du Projet

ChurnScope est un projet industriel de Machine Learning developpe dans le cadre de la formation **Directeur de projet en intelligence artificielle (DPIA 1)** a **L'Ecole Multimedia**.

L'objectif est d'aider les equipes de retention d'une entreprise de telecommunications a :
1. **Identifier avec precision les clients a haut risque de depart (Churn)**.
2. **Comprendre individuellement les causes du risque grace a l'explicabilite SHAP**.
3. **Simuler l'impact d'offres commerciales de fidelisation (Simulateur What-If)**.
4. **Surveiller la derive des donnees et du modele en production (Evidently AI)**.

---

## Competences RNCP Couvertes

| Referentiel | Intitule de la Competence | Realisation dans ChurnScope |
| :--- | :--- | :--- |
| **D-02** | *Creer un algorithme d'Intelligence Artificielle adapte et accessible.* | Pipeline scikit-learn equilibre, modele Random Forest optimise, explicabilite SHAP locale et globale, interface accessible et intuitive. |
| **D-04** | *Concevoir des pipelines d'integration et deploiement continu (CI/CD).* | Workflow GitHub Actions (`.github/workflows/ci.yml`), validation automatique du code (`flake8`, `black`), suite de tests unitaires et de non-regression (`pytest`). |
| **D-06** | *Piloter la performance de la solution d'IA via des outils de monitoring.* | Monitoring de derive de distribution (*Data Drift* et *Target Drift*) avec **Evidently AI** et generation de rapports interactifs. |

---

## Performance du Modele Retenu

Le modele final est un **Random Forest optimise** avec validation croisee stratifiee et ponderation equilibree des classes.

| Metrique | Performance sur Jeu de Test (20%) | Interpretation Metier |
| :--- | :---: | :--- |
| **ROC-AUC** | **0,841** | Excellente capacite de discrimination globale des profils a risque. |
| **Rappel Churn (Recall)** | **79,4 %** | **297 clients churners detectes sur 374** (manque seulement 77 departs). |
| **Precision Churn** | **51,4 %** | 1 client cible sur 2 est un churner reel (arbitrage parametrable via seuil). |
| **F1-Score Churn** | **0,624** | Equilibre optimise entre detection exhaustive et cout de ciblage. |
| **Accuracy** | **74,6 %** | Precision globale sur l'ensemble de la population testee. |

---

## Application et Dashboard Interactif Streamlit

Le dashboard Streamlit (`app.py`) offre 4 espaces de travail :

1. **Priorisation & Synthese Decisionnelle** :
   - Indicateurs en temps reel (taux de churn, clients a contacter, revenu mensuel a risque).
   - Curseur de seuil interactif avec calcul en direct de la precision et du rappel.
   - Liste des clients prioritaires triee par probabilite de resiliation.
2. **Explicabilite Client (SHAP)** *(Competence D-02)* :
   - Selection d'un client et affichage des facteurs qui augmentent ou reduisent son risque de depart.
3. **Simulateur What-If Retention** :
   - Simulation immediate de l'efficacite d'un changement de contrat, d'une remise tarifaire ou d'un service offert.
4. **Monitoring & Data Drift (Evidently AI)** *(Competence D-06)* :
   - Surveillance de la stabilite des donnees de production et telechargement du rapport interactif complet.

### Lancer l'application :
```bash
streamlit run app.py
```
Puis accedez a `http://localhost:8501`.

---

## Securite, Qualite et Conformite RGPD

* **Protection des PII / RGPD** : Anonymisation des `customerID` via un hachage cryptographique **HMAC-SHA256 sale** (`src/data/anonymizer.py`).
* **Validation stricte des donnees** : Schemas **Pydantic** (`src/data/schema.py`) garantissant l'integrite et la validite des entrees.
* **Isolation des secrets** : Template `.env.example` et fichier `.env` non versionne.
* **Qualite de code** : 100% conforme PEP 8 (`flake8`) et formatte avec `black`.

---

## Organisation du Code

```text
ChurnScope/
├── .github/
│   └── workflows/
│       └── ci.yml                     # Pipeline CI/CD GitHub Actions (D-04)
├── data/
│   ├── raw/                           # Dataset brut Telco Customer Churn
│   └── processed/                     # Modele serialise (.joblib) et predictions
├── docs/
│   ├── 01_analyse_preparation.md       # Livrable 1 : Qualite & Preparation
│   ├── 02_apprentissage_modeles.md     # Livrable 2 : Apprentissage & Optimisation
│   ├── 03_validation_conclusion.md     # Livrable 3 : Validation & Conclusions
│   ├── presentation_dirigeants.md      # Support de restitution pour la direction
│   ├── data_drift_report.html         # Rapport Evidently AI interactif (D-06)
│   └── guide_explication_oral.md      # Guide de preparation a la soutenance
├── notebooks/
│   ├── 01_exploration.ipynb           # EDA et visualisations
│   ├── 02_modelisation.ipynb          # Comparaison des 4 algorithmes
│   └── 03_validation.ipynb            # Evaluation fine et matrice de confusion
├── src/
│   ├── data/
│   │   ├── schema.py                  # Schemas de validation Pydantic
│   │   ├── anonymizer.py              # Anonymisation RGPD (HMAC-SHA256)
│   │   └── loader.py                  # Chargement et pretraitement scikit-learn
│   ├── models/
│   │   ├── train.py                   # Entrainement et calcul des metriques
│   │   └── explainability.py          # Module d'explicabilite SHAP (D-02)
│   ├── monitoring/
│   │   └── drift.py                   # Monitoring Data Drift Evidently (D-06)
│   ├── export_model.py                # Script principal d'entrainement/export
│   └── dashboard.py                   # Dashboard HTML Plotly
├── tests/
│   ├── test_data_validation.py        # Validation Pydantic
│   ├── test_pipeline.py               # Inference et preprocessing
│   ├── test_model_performance.py      # Non-regression ML (Recall >= 0.75, AUC >= 0.80)
│   └── test_security.py               # Securite et anonymisation
├── scripts/
│   └── package_submission.py          # Script de generation du ZIP de rendu
├── app.py                             # Application Streamlit multi-onglets
├── requirements.txt                   # Dependances du projet
├── pytest.ini                         # Configuration Pytest
├── .flake8                            # Configuration Flake8
└── README.md
```

---

## Installation et Guide d'Execution

### 1. Cloner et configurer l'environnement
```bash
git clone https://github.com/jouvence13/ChurnScope.git
cd ChurnScope

# Creation et activation de l'environnement virtuel
python3 -m venv .venv
source .venv/bin/activate  # Windows : .\.venv\Scripts\Activate.ps1

# Installation des dependances
pip install -r requirements.txt
```

### 2. Entrainer le modele et exporter les artefacts
```bash
python3 src/export_model.py
```

### 3. Executer l'analyse de Data Drift (Evidently AI)
```bash
python3 src/monitoring/drift.py
```

### 4. Lancer la suite de tests automatises (Pytest)
```bash
pytest tests/ -v
```

### 5. Generer l'archive ZIP de rendu final
Pour creer le fichier de rendu officiel (ex: `arthur_mensch_projet3_AIA01.zip`) :
```bash
python3 scripts/package_submission.py --name "nom_prenom" --classe "AIA01"
```

---

## Auteur et Certification

* **Auteur** : Jouvence
* **Formation** : Directeur de Projet en Intelligence Artificielle (DPIA 1)
* **Etablissement** : L'Ecole Multimedia — Annee 2026
