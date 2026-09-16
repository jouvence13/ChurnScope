# ChurnScope

**Prédiction du Churn Client avec des modèles de Machine Learning.**

[![CI/CD Pipeline](https://github.com/jouvence13/ChurnScope/actions/workflows/ci.yml/badge.svg)](https://github.com/jouvence13/ChurnScope/actions)
[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linting: flake8](https://img.shields.io/badge/linting-flake8-green.svg)](https://flake8.pycqa.org/)
[![Security: RGPD](https://img.shields.io/badge/security-RGPD%20%2F%20PII%20Hash-success.svg)](https://www.cnil.fr/)

Projet #3 — *Introduction au Machine Learning* — Directeur de projet en intelligence artificielle, Année 1 — L'École Multimédia.

---

## Objectif

L'objectif est de prédire si un client d'une entreprise de télécommunications risque de résilier son abonnement (`Churn = Yes`), afin d'aider les équipes de rétention à prioriser leurs actions.

La question métier posée par le projet est :

> **Qui devons-nous contacter cette semaine, et pourquoi ?**

Trois familles de modèles imposées par le brief sont comparées, plus un second modèle linéaire ajouté à titre de comparaison :

- Régression logistique
- Ridge Classifier *(comparaison supplémentaire)*
- Arbre de décision
- Random Forest — **modèle retenu**

Au-delà du pipeline de base, le projet propose une explicabilité par client (SHAP), un dashboard interactif (Streamlit), un monitoring de dérive des données (Evidently AI) et une chaîne qualité automatisée (tests + CI/CD), conformément aux libertés d'amélioration proposées par le brief.

---

## Compétences RNCP couvertes

| Référentiel | Intitulé de la compétence | Réalisation dans ChurnScope |
| :--- | :--- | :--- |
| **D-02** | Créer un algorithme d'Intelligence Artificielle adapté et accessible. | Pipeline scikit-learn équilibré, Random Forest optimisé, explicabilité SHAP locale et globale, interface accessible et intuitive. |
| **D-04** | Concevoir des pipelines d'intégration et déploiement continu (CI/CD). | Workflow GitHub Actions (`.github/workflows/ci.yml`), validation automatique du code (`flake8`, `black`), suite de tests unitaires et de non-régression (`pytest`). |
| **D-06** | Piloter la performance de la solution d'IA via des outils de monitoring. | Monitoring de dérive de distribution (*Data Drift*) avec **Evidently AI** et génération de rapports interactifs. |

---

## Données

Dataset : [**Telco Customer Churn**](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) (Kaggle).

Le fichier contient **7 043 clients** et **21 colonnes**. Le taux de churn est d'environ **26,54 %**.

Les variables couvrent quatre dimensions :

- **démographiques** : genre, senior, partenaire, personnes à charge ;
- **services** : téléphonie, internet, sécurité en ligne, sauvegarde, support technique, streaming ;
- **compte client** : ancienneté (`tenure`), type de contrat, facturation, moyen de paiement, `MonthlyCharges`, `TotalCharges` ;
- **cible** : `Churn` (`Yes` / `No`).

Le CSV brut est versionné dans le dépôt pour la reproductibilité du rendu :

```text
data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv
```

---

## Structure du dépôt

```text
ChurnScope/
├── .github/
│   └── workflows/
│       └── ci.yml                       # Pipeline CI/CD GitHub Actions (D-04)
├── data/
│   ├── raw/                             # Dataset brut Telco Customer Churn
│   └── processed/                       # Modèle sérialisé (.joblib) et prédictions
├── docs/
│   ├── 01_analyse_preparation.md        # Livrable 1 : qualité et préparation des données
│   ├── 02_apprentissage_modeles.md      # Livrable 2 : apprentissage et optimisation
│   ├── 03_validation_conclusion.md      # Livrable 3 : validation et conclusions
│   ├── presentation_dirigeants.md       # Support de restitution pour la direction
│   ├── passation_technique.md           # Guide de passation technique (architecture, choix)
│   └── data_drift_report.html           # Rapport Evidently AI interactif (D-06)
├── notebooks/
│   ├── 01_exploration.ipynb             # EDA, qualité des données et visualisations
│   ├── 02_modelisation.ipynb            # Comparaison des 4 modèles + GridSearchCV
│   └── 03_validation.ipynb              # Validation finale et matrice de confusion
├── presentation/                        # Support de soutenance (non versionné, voir .gitignore)
│   ├── generate_presentation.py         # Génère soutenance_churnscope.pptx (11 diapositives)
│   ├── generate_presentation.ps1        # Point d'entrée Windows pour le script ci-dessus
│   ├── soutenance_churnscope.pptx       # Diaporama généré (régénérable, non commité)
│   └── guide_explication_oral.md        # Questions/réponses pour préparer l'oral (non commité)
├── src/
│   ├── data/
│   │   ├── schema.py                    # Schémas de validation Pydantic
│   │   ├── anonymizer.py                # Anonymisation RGPD (HMAC-SHA256)
│   │   └── loader.py                    # Chargement et prétraitement scikit-learn
│   ├── models/
│   │   ├── train.py                     # Entraînement et calcul des métriques
│   │   └── explainability.py            # Module d'explicabilité SHAP (D-02)
│   ├── monitoring/
│   │   └── drift.py                     # Monitoring Data Drift Evidently (D-06)
│   ├── export_model.py                  # Script principal d'entraînement/export
│   └── dashboard.py                     # Dashboard HTML Plotly (export statique)
├── scripts/
│   └── package_submission.py            # Génère l'archive ZIP de rendu final
├── tests/
│   ├── test_data_validation.py          # Validation Pydantic
│   ├── test_pipeline.py                 # Inférence et prétraitement
│   ├── test_model_performance.py        # Non-régression ML (Recall ≥ 0.75, AUC ≥ 0.80)
│   └── test_security.py                 # Sécurité et anonymisation
├── app.py                               # Application Streamlit multi-onglets
├── requirements.txt                     # Dépendances du projet
├── pytest.ini                           # Configuration Pytest
├── .flake8                              # Configuration Flake8
└── README.md
```

---

## Installation

```bash
git clone https://github.com/jouvence13/ChurnScope.git
cd ChurnScope

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Sous Windows PowerShell :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Exécution

**Entraîner le modèle et exporter les artefacts :**

```bash
python src/export_model.py
```

**Lancer le dashboard interactif Streamlit :**

```bash
streamlit run app.py
```

Puis accéder à `http://localhost:8501`.

**Exécuter l'analyse de Data Drift (Evidently AI) :**

```bash
python src/monitoring/drift.py
```

> ⚠️ Nécessite Python ≥ 3.11.4 (un bug connu du module `typing` sur Python 3.11.0 empêche l'import d'Evidently).

**Lancer la suite de tests automatisés :**

```bash
pytest tests/ -v
```

**Régénérer le support de soutenance (optionnel, local) :**

```bash
python presentation/generate_presentation.py
```

**Générer l'archive ZIP de rendu final :**

```bash
python scripts/package_submission.py --name "nom_prenom" --classe "AIA01"
```

---

## Préparation des données

Les étapes principales, détaillées dans [docs/01_analyse_preparation.md](docs/01_analyse_preparation.md) et exécutées dans [notebooks/01_exploration.ipynb](notebooks/01_exploration.ipynb), sont :

1. suppression de `customerID`, un simple identifiant technique sans valeur prédictive ;
2. conversion de `TotalCharges` en numérique (11 chaînes vides détectées, correspondant à des clients avec `tenure = 0`) ;
3. imputation des valeurs numériques manquantes par la médiane, calculée **après** la séparation train/test pour éviter toute fuite de données ;
4. encodage One-Hot des variables catégorielles ;
5. standardisation des variables numériques (`StandardScaler`) ;
6. séparation des données en **80 % entraînement / 20 % test**, avec un **split stratifié** (`stratify=y`) pour conserver la même proportion de churn (26,54 %) dans les deux jeux.

Toutes ces transformations sont regroupées dans un `Pipeline` scikit-learn afin qu'elles soient systématiquement réapprises à l'intérieur de chaque pli de validation croisée.

## Pourquoi plusieurs métriques ?

Le dataset est déséquilibré : environ trois clients sur quatre ne churnent pas (73,46 % / 26,54 %).

L'**accuracy** seule n'est donc pas suffisante — un modèle qui prédirait systématiquement « pas de churn » obtiendrait une accuracy élevée sans détecter aucun départ. On regarde aussi :

- **Précision (Precision)** : parmi les clients prédits comme churners, combien le sont vraiment ?
- **Rappel (Recall)** : parmi les vrais churners, combien sont détectés ? *(métrique métier prioritaire ici)*
- **F1-score** : compromis entre précision et rappel.
- **ROC-AUC** : capacité globale du modèle à classer les clients du moins au plus risqué, indépendamment d'un seuil.

## Résultats de la comparaison

Les quatre modèles sont comparés sur le même jeu de test (1 409 clients), avant optimisation :

| Modèle | Accuracy | Précision | Rappel | F1-score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Régression logistique | 0,738 | 0,504 | 0,783 | 0,614 | 0,841 |
| Ridge Classifier | 0,737 | 0,503 | 0,789 | 0,615 | 0,836 |
| Arbre de décision | 0,755 | 0,527 | 0,759 | 0,622 | 0,832 |
| **Random Forest** | 0,755 | 0,526 | 0,791 | 0,632 | **0,842** |

Le Random Forest obtient le meilleur rappel, le meilleur F1-score et la meilleure AUC : c'est le modèle retenu pour l'optimisation. La régression logistique reste une alternative crédible pour sa simplicité d'interprétation, avec des performances très proches.

## Hyperparamètres testés

Une recherche en grille (`GridSearchCV`) avec validation croisée stratifiée à 5 plis a été appliquée au Random Forest, en optimisant le **rappel** :

- `n_estimators` : 100 ou 200
- `max_depth` : 6 ou 10
- `min_samples_leaf` : 1 ou 3

Meilleurs réglages obtenus (rappel moyen en validation croisée : **0,809**) :

```text
n_estimators = 200
max_depth = 6
min_samples_leaf = 1
class_weight = "balanced"
```

**Performances finales du modèle optimisé sur le jeu de test :**

| Métrique | Résultat |
|---|---:|
| Accuracy | 0,746 |
| Précision churn | 0,514 |
| Rappel churn | 0,794 |
| F1-score churn | 0,624 |
| ROC-AUC | 0,841 |

Matrice de confusion :

```text
[[754 281]
 [ 77 297]]
```

Le modèle détecte **297 des 374 clients** ayant réellement quitté l'entreprise (77 churns manqués), au prix de 281 fausses alertes — un compromis cohérent avec la priorité donnée au rappel.

## Variables importantes

Les variables qui ressortent le plus, à la fois dans les règles de l'arbre de décision et dans l'importance des caractéristiques du Random Forest, sont notamment :

- le type de contrat, en particulier **Month-to-month** (contrat mensuel, très associé au churn) et **Two year** (à l'inverse protecteur) ;
- l'**ancienneté** du client (`tenure`) ;
- **MonthlyCharges** et **TotalCharges** ;
- le service **fibre optique** (`InternetService`) ;
- l'absence de **sécurité en ligne** (`OnlineSecurity`) ou de **support technique** (`TechSupport`).

Ces résultats montrent des **associations** apprises par le modèle, pas des relations de cause à effet.

## Limites et recommandations

- les associations observées ne prouvent pas une causalité ;
- le dataset décrit une population et une période particulières, sans validation temporelle ;
- le seuil de décision (`0,5` par défaut) n'a pas été calibré sur un coût métier réel — l'abaisser augmente le rappel mais aussi les fausses alertes ;
- une validation externe (nouvelles données) serait nécessaire pour confirmer la performance en production.

Détail complet dans [docs/03_validation_conclusion.md](docs/03_validation_conclusion.md).

## Conclusion simple

Le projet montre qu'il est possible d'identifier une part importante des clients susceptibles de résilier leur abonnement : le Random Forest optimisé détecte environ **4 churns sur 5** (79,4 % de rappel), avec une AUC de 0,841.

Dans un contexte réel, l'entreprise pourrait utiliser ce score de risque pour prioriser les clients à contacter en premier, le seuil de décision restant à ajuster avec les équipes métier selon le coût d'une campagne de rétention et la valeur du client.

---

## Application et dashboard interactif Streamlit

Le dashboard Streamlit (`app.py`) offre 4 espaces de travail :

1. **Priorisation & synthèse décisionnelle** : indicateurs en temps réel (taux de churn, clients à contacter, revenu mensuel à risque), curseur de seuil interactif avec calcul en direct de la précision et du rappel, liste des clients prioritaires.
2. **Explicabilité client (SHAP)** *(Compétence D-02)* : sélection d'un client et affichage des facteurs qui augmentent ou réduisent son risque de départ.
3. **Simulateur What-If Rétention** : simulation immédiate de l'effet d'un changement de contrat, d'une remise tarifaire ou d'un service offert.
4. **Monitoring & Data Drift (Evidently AI)** *(Compétence D-06)* : surveillance de la stabilité des données de production et téléchargement du rapport interactif complet.

## Sécurité, qualité et conformité RGPD

- **Protection des PII / RGPD** : anonymisation des `customerID` via un hachage cryptographique **HMAC-SHA256 salé** (`src/data/anonymizer.py`).
- **Validation stricte des données** : schémas **Pydantic** (`src/data/schema.py`) garantissant l'intégrité et la validité des entrées.
- **Isolation des secrets** : template `.env.example`, `.env` non versionné.
- **Qualité de code** : conforme PEP 8 (`flake8`) et formaté avec `black`.

---

## Documents du rendu

1. [notebooks/01_exploration.ipynb](notebooks/01_exploration.ipynb) — qualité des données, statistiques descriptives, visualisations et procédure de nettoyage.
2. [notebooks/02_modelisation.ipynb](notebooks/02_modelisation.ipynb) — comparaison des 4 modèles, optimisation par GridSearchCV et validation croisée.
3. [notebooks/03_validation.ipynb](notebooks/03_validation.ipynb) — validation finale, matrice de confusion, courbe ROC et analyse de généralisation.
4. [docs/01_analyse_preparation.md](docs/01_analyse_preparation.md) — livrable 1 : qualité et préparation des données.
5. [docs/02_apprentissage_modeles.md](docs/02_apprentissage_modeles.md) — livrable 2 : apprentissage, comparaison et optimisation des modèles.
6. [docs/03_validation_conclusion.md](docs/03_validation_conclusion.md) — livrable 3 : validation et conclusions.
7. [docs/presentation_dirigeants.md](docs/presentation_dirigeants.md) — synthèse orientée décision pour l'équipe dirigeante.
8. [docs/passation_technique.md](docs/passation_technique.md) — guide de passation technique et d'architecture.

## Conventions Git

Les commits suivent [Conventional Commits](https://www.conventionalcommits.org) : `feat:`, `fix:`, `docs:`, `chore:`, `test:`.

---

## Auteur et certification

- **Auteur** : Jouvence
- **Formation** : Directeur de Projet en Intelligence Artificielle (DPIA 1)
- **Établissement** : L'École Multimédia — Année 2026
