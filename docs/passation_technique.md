# Guide de Passation Technique et Architecture - ChurnScope

Ce document regroupe le récapitulatif exhaustif des développements réalisés, l'architecture technique, les choix méthodologiques, les procédures d'exécution et le speech de présentation destiné aux développeurs prenant en main le projet.

---

## 1. Vue d'Ensemble du Projet

* **Projet** : ChurnScope (Projet 3 - Titre Directeur de projet en intelligence artificielle, Année 1 - L'École Multimédia)
* **Objectif métier** : Prédire le risque de résiliation (churn) des clients télécoms, comprendre les motifs individuels de départ et prioriser les actions de rétention.
* **Jeu de données** : *Telco Customer Churn* (7 043 lignes, 21 colonnes, cible binaire `Churn`).
* **Compétences RNCP couvertes** :
  * **D-02** : Création d'un algorithme d'IA performant, robuste, équitable et transparent (Explicabilité SHAP locale et globale).
  * **D-04** : Conception d'un pipeline d'intégration et de déploiement continu (CI/CD GitHub Actions, suite de tests Pytest, contrôle de non-régression).
  * **D-06** : Surveillance de la performance de la solution en production (Monitoring du *Data Drift* avec Evidently AI).

---

## 2. Récapitulatif des Fichiers Créés et Modifiés

### Fichiers et Dossiers Créés
* `src/data/schema.py` : Validation stricte des données d'entrée via des schémas Pydantic (vérification des types, plages de valeurs pour `tenure` et `MonthlyCharges`, énumérations).
* `src/data/anonymizer.py` : Conformité RGPD avec hachage cryptographique HMAC-SHA256 salé des identifiants clients (PII).
* `src/data/loader.py` : Chargement du dataset brut et construction du `ColumnTransformer` scikit-learn sans fuite de données (*data leakage*).
* `src/models/train.py` : Pipeline d'entraînement scikit-learn, optimisation Random Forest, calcul des métriques et export des artefacts.
* `src/models/explainability.py` : Module SHAP (`TreeExplainer`) pour calculer l'impact de chaque variable au niveau global et par client (Compétence D-02).
* `src/monitoring/drift.py` : Module de surveillance de la dérive des distributions avec Evidently AI (Compétence D-06).
* `docs/data_drift_report.html` : Rapport interactif HTML généré par Evidently AI.
* `tests/test_data_validation.py` : Tests unitaires Pydantic (rejet des données invalides).
* `tests/test_pipeline.py` : Tests unitaires de transformation et d'inférence.
* `tests/test_model_performance.py` : Tests de non-régression validant les seuils minimaux ($Recall \ge 75\%$, $ROC\text{-}AUC \ge 0.80$).
* `tests/test_security.py` : Tests d'anonymisation RGPD et d'isolation des clés.
* `.github/workflows/ci.yml` : Workflow CI/CD GitHub Actions (Linting Flake8, Formatage Black, Tests Pytest, Build).
* `scripts/package_submission.py` : Script d'automatisation de l'archive ZIP officielle du brief.
* `.env.example` : Template de configuration pour les variables d'environnement.
* `pytest.ini` & `.flake8` : Fichiers de configuration pour Pytest et Flake8.

### Fichiers Modifiés
* `app.py` : Dashboard Streamlit structuré en 4 onglets (*Priorisation Métier*, *Explicabilité SHAP*, *Simulateur What-If*, *Monitoring de Dérive*).
* `requirements.txt` : Dépendances mises à jour avec `pydantic`, `shap`, `evidently`, `pytest`, `flake8`, `black`, `python-dotenv`.
* `src/export_model.py` : Point d'entrée d'entraînement refactorisé sur l'architecture modulaire.
* `README.md` : Documentation exhaustive du projet et des compétences certifiantes.
* `.gitignore` : Exclusion sécurisée des fichiers `.env`, `*.zip` et artefacts de build.

---

## 3. Architecture Technique

```text
ChurnScope/
├── .github/
│   └── workflows/
│       └── ci.yml                     # Pipeline CI/CD GitHub Actions (D-04)
├── data/
│   ├── raw/                           # Dataset Telco original non altéré
│   └── processed/                     # Modèle sérialisé (.joblib) et prédictions exportées
├── docs/
│   ├── 01_analyse_preparation.md       # Livrable 1 : Qualité & Préparation
│   ├── 02_apprentissage_modeles.md     # Livrable 2 : Apprentissage & Optimisation
│   ├── 03_validation_conclusion.md     # Livrable 3 : Validation & Conclusions
│   ├── presentation_dirigeants.md      # Support de restitution pour la direction
│   ├── data_drift_report.html         # Rapport Evidently AI interactif (D-06)
│   ├── passation_technique.md         # Guide de passation technique (ce document)
│   └── guide_explication_oral.md      # Guide de préparation à la soutenance
├── notebooks/
│   ├── 01_exploration.ipynb           # EDA et visualisations
│   ├── 02_modelisation.ipynb          # Comparaison des 4 algorithmes
│   └── 03_validation.ipynb            # Évaluation fine et matrice de confusion
├── src/
│   ├── data/
│   │   ├── schema.py                  # Schémas de validation Pydantic
│   │   ├── anonymizer.py              # Anonymisation RGPD (HMAC-SHA256)
│   │   └── loader.py                  # Chargement et prétraitement scikit-learn
│   ├── models/
│   │   ├── train.py                   # Entraînement et calcul des métriques
│   │   └── explainability.py          # Module d'explicabilité SHAP (D-02)
│   ├── monitoring/
│   │   └── drift.py                   # Monitoring Data Drift Evidently (D-06)
│   ├── export_model.py                # Script principal d'entraînement/export
│   └── dashboard.py                   # Dashboard HTML Plotly
├── tests/
│   ├── test_data_validation.py        # Validation Pydantic
│   ├── test_pipeline.py               # Inférence et preprocessing
│   ├── test_model_performance.py      # Non-régression ML (Recall >= 0.75, AUC >= 0.80)
│   └── test_security.py               # Sécurité et anonymisation
├── scripts/
│   └── package_submission.py          # Script de génération du ZIP de rendu
├── app.py                             # Application Streamlit multi-onglets
├── requirements.txt                   # Dépendances du projet
├── pytest.ini                         # Configuration Pytest
├── .flake8                            # Configuration Flake8
└── README.md
```

---

## 4. Choix Méthodologiques et Modélisation

1. **Prétraitement** :
   * Variables numériques (`SeniorCitizen`, `tenure`, `MonthlyCharges`, `TotalCharges`) : Imputation médiane (`SimpleImputer`) + Standardisation (`StandardScaler`).
   * Variables catégorielles (15 colonnes) : Imputation par le mode (`SimpleImputer`) + Encodage One-Hot (`OneHotEncoder(handle_unknown='ignore')`).
   * Séparation train/test (80/20) effectuée avant toute transformation pour éviter tout *data leakage*.
2. **Modèle retenu** :
   * `RandomForestClassifier(n_estimators=200, max_depth=6, class_weight='balanced', random_state=42)`.
   * **Justification métier** : Le coût d'un faux négatif (client churner non détecté qui quitte le service) est nettement supérieur au coût d'un faux positif (action de fidélisation préventive sur un client qui serait resté). Le paramètre `class_weight='balanced'` et l'optimisation par grille ciblent un **Rappel élevé (79,4 %)** tout en conservant une **AUC de 0,841**.

---

## 5. Guide des Commandes pour le Développeur

### Installation et environnement virtuel
```bash
# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Entraînement et régénération des artefacts
```bash
python3 src/export_model.py
```

### Génération du rapport de dérive (Data Drift - D-06)
```bash
python3 src/monitoring/drift.py
```

### Lancement des tests unitaires et de qualité
```bash
pytest tests/ -v
flake8 src/ app.py tests/ scripts/
black --check src/ app.py tests/ scripts/
```

### Lancement du Dashboard Streamlit
```bash
streamlit run app.py
```

### Création de l'archive ZIP officielle
```bash
python3 scripts/package_submission.py --name "nom_prenom" --classe "AIA01"
```

---

## 6. Speech de Présentation et Passation (À transmettre au développeur)

Bonjour,

Voici la synthèse complète de l'architecture et du fonctionnement de ChurnScope pour faciliter ta prise en main du projet :

### Contexte et Enjeu
Nous travaillons sur le Projet 3 du cursus Directeur de projet en IA (L'École Multimédia). L'enjeu est de fournir une solution complète d'aide à la décision pour réduire l'attrition client (churn) dans les télécoms. Le projet valide trois compétences professionnelles majeures :
- D-02 : Algorithme d'IA performant, robuste et transparent grâce à l'explicabilité SHAP.
- D-04 : Pipeline d'intégration et de validation continue via GitHub Actions et Pytest.
- D-06 : Surveillance de la performance et détection de dérive (Data Drift) avec Evidently AI.

### Choix du Modèle et Performances
Le modèle final sélectionné est un Random Forest optimisé avec pondération équilibrée des classes.
- Sur le jeu de test (20% des données), il atteint une AUC de 0.841 et un Rappel de 79.4% sur la classe Churn (soit 297 churners réels détectés sur 374).
- La précision est de 51.4% pour un F1-score de 0.624.
- Le seuil de décision est ajustable en direct dans l'interface pour permettre aux équipes métier d'arbitrer entre exhaustivité et coût de ciblage.

### Structure du Code source
Le code est modularisé dans le dossier src :
- src/data/ : Contient la validation Pydantic (schema.py), le module d'anonymisation RGPD (anonymizer.py) et le loader scikit-learn sans fuite de données (loader.py).
- src/models/ : Contient le pipeline d'entraînement reproductible (train.py) et le module d'explicabilité SHAP locale et globale (explainability.py).
- src/monitoring/ : Contient le script Evidently AI (drift.py) qui compare la distribution des données entrantes avec le jeu de référence et produit un rapport HTML interactif.

### Application Streamlit (app.py)
L'interface utilisateur est organisée en 4 onglets :
1. Priorisation & Décision : Métriques financières (revenu mensuel exposé), réglage dynamique du seuil avec recalcul en direct du rappel et de la précision, et liste priorisée des clients à contacter.
2. Explicabilité Client (SHAP) : Diagnostic transparent au niveau individuel détaillant quelles caractéristiques augmentent ou diminuent le risque pour un client donné.
3. Simulateur What-If : Outil commercial permettant de simuler immédiatement l'effet d'un changement de contrat, d'une remise ou d'un service offert sur la probabilité de résiliation.
4. Monitoring & Drift : Indicateurs de santé du modèle et accès direct au rapport interactif Evidently AI.

### Qualité, Sécurité et Livraison
- La suite de tests Pytest (8 tests dans tests/) valide l'intégrité des schémas, le pipeline de prédiction, l'anonymisation des identifiants et les seuils de non-régression de performance.
- Le pipeline CI/CD GitHub Actions (.github/workflows/ci.yml) automatise l'ensemble des vérifications à chaque push.
- Le script scripts/package_submission.py permet de créer en une seule commande l'archive ZIP propre respectant les critères de nommage du brief (nom_prenom_projet3_AIA01.zip).

L'ensemble des tests est vert, le code respecte strictement les normes PEP 8 et l'environnement est prêt pour l'exécution.
