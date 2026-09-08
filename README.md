# ChurnScope

Prédiction et priorisation du churn client dans les télécommunications.

ChurnScope est un projet de Machine Learning réalisé dans le cadre de la formation DPIA 1 à L'École Multimédia. L'objectif est d'identifier les clients susceptibles de quitter l'entreprise et d'aider les équipes de rétention à décider qui contacter en priorité.

## Résumé

Le projet couvre l'ensemble du parcours :

- analyse de la qualité des données ;
- exploration des profils de clients partis et restés ;
- préparation sans fuite de données ;
- comparaison de quatre modèles de classification ;
- optimisation par validation croisée et recherche sur grille ;
- validation finale sur un jeu de test indépendant ;
- dashboard Streamlit destiné aux équipes métier.

## Résultat principal

Le modèle retenu est un **Random Forest optimisé**. Il a été sélectionné en donnant la priorité au rappel de la classe churn, car manquer un client sur le départ peut coûter davantage qu'une fausse alerte.

| Métrique | Résultat sur le jeu de test |
|---|---:|
| Accuracy | 0,746 |
| Précision churn | 0,514 |
| Rappel churn | 0,794 |
| F1-score churn | 0,624 |
| AUC | 0,841 |

Sur les `374` clients ayant réellement quitté l'entreprise, le modèle en détecte `297` et en manque `77`. Il génère également `281` fausses alertes. Le seuil de décision doit donc être adapté au coût réel des campagnes de rétention.

## Dashboard interactif

Le dashboard Streamlit répond à la question : **« Qui dois-je contacter cette semaine, et pourquoi ? »**

Il propose :

- des indicateurs de synthèse ;
- des filtres par contrat, service internet et ancienneté ;
- une table des clients triée par probabilité de churn ;
- le revenu mensuel exposé ;
- trois graphiques d'exploration ;
- un curseur de seuil affichant en direct le nombre de clients ciblés, le rappel et la précision.

### Lancer le dashboard

Depuis la racine du projet :

```bash
streamlit run app.py
```

Puis ouvrir l'adresse affichée par Streamlit, généralement :

```text
http://localhost:8501
```

Le dashboard charge le modèle sérialisé et les prédictions préparées. Il ne réentraîne pas le modèle au démarrage.

## Installation

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### macOS ou Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Reproduire les artefacts du modèle

Le dataset brut doit être placé dans :

```text
data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv
```

Pour régénérer le modèle et les prédictions utilisées par Streamlit :

```bash
python src/export_model.py
```

Cette commande crée :

- `data/processed/churn_model.joblib` : pipeline scikit-learn sérialisé ;
- `data/processed/customer_predictions.csv` : données clients, probabilités et prédictions.

Le modèle est entraîné une seule fois par cette commande. L'application charge ensuite le fichier `.joblib` avec `joblib` et met les données en cache avec `st.cache_data`.

## Organisation du projet

```text
ChurnScope/
├── app.py                              # dashboard Streamlit interactif
├── data/
│   ├── raw/                            # dataset original, non modifié
│   └── processed/                      # modèle et prédictions exportés
├── docs/
│   ├── 01_analyse_preparation.md       # qualité et exploration
│   ├── 02_apprentissage_modeles.md     # modèles et optimisation
│   ├── 03_validation_conclusion.md     # validation et limites
│   ├── presentation_dirigeants.md      # support de restitution métier
│   └── dashboard_churn.html             # dashboard Plotly autonome
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_modelisation.ipynb
│   └── 03_validation.ipynb
├── src/
│   ├── dashboard.py                    # génération du dashboard Plotly HTML
│   └── export_model.py                 # entraînement et export du pipeline
├── requirements.txt
└── README.md
```

## Méthodologie

### Données

Le projet utilise le dataset **Telco Customer Churn**, attribué à blastchar et disponible sur Kaggle. Il contient `7043` clients et `21` colonnes.

La cible `Churn` est déséquilibrée :

- `5174` clients restés, soit `73,46 %` ;
- `1869` clients partis, soit `26,54 %`.

`TotalCharges` contient `11` chaînes vides pour des clients dont `tenure = 0`. Elles sont converties en valeurs manquantes puis imputées dans le pipeline. `customerID` est conservé pour identifier les clients dans le dashboard, mais exclu des variables d'apprentissage.

### Modèles comparés

- régression logistique ;
- Ridge Classifier ;
- arbre de décision ;
- Random Forest.

Le prétraitement est intégré à un `Pipeline` scikit-learn :

- imputation médiane et standardisation des variables numériques ;
- imputation de la modalité la plus fréquente et encodage One-Hot des variables catégorielles.

La séparation train/test est effectuée avant toute transformation apprenante, avec stratification sur la cible.

### Optimisation

Le Random Forest est optimisé avec une validation croisée stratifiée à `5` plis et une recherche sur grille. Le score optimisé est le rappel de la classe churn.

Paramètres retenus :

```text
n_estimators=200
max_depth=6
min_samples_leaf=1
class_weight="balanced"
```

## Documents et notebooks

Les trois livrables sont disponibles dans [docs/](docs/) :

1. [Analyse et préparation](docs/01_analyse_preparation.md)
2. [Apprentissage et modèles](docs/02_apprentissage_modeles.md)
3. [Validation et conclusion](docs/03_validation_conclusion.md)

Le support de restitution métier est disponible dans [presentation_dirigeants.md](docs/presentation_dirigeants.md).

Les notebooks contiennent le détail reproductible des étapes :

- [01_exploration.ipynb](notebooks/01_exploration.ipynb)
- [02_modelisation.ipynb](notebooks/02_modelisation.ipynb)
- [03_validation.ipynb](notebooks/03_validation.ipynb)

## Limites et suite possible

Le modèle est un outil d'aide à la priorisation, pas une décision automatique. Les principales limites sont :

- les résultats sont descriptifs et ne prouvent pas de causalité ;
- le dataset représente une période et une population données ;
- le seuil `0,5` n'est pas nécessairement optimal économiquement ;
- les fausses alertes peuvent entraîner des coûts de rétention ;
- les performances doivent être surveillées sur de nouvelles données.

Une suite naturelle consiste à calibrer le seuil selon le coût d'un churn manqué et celui d'une fausse alerte, puis à mesurer l'effet réel des actions de rétention avec un groupe témoin.

## Auteur

Jouvence — DPIA 1, L'École Multimédia
