# ChurnScope
Prédiction du churn client en télécommunications — analyse exploratoire, modèles de classification (régression logistique, arbre de décision, Random Forest) et évaluation comparative.

churn-prediction/
├── data/
│   ├── raw/          # le CSV Kaggle, jamais modifié
│   └── processed/    # les sorties de ton nettoyage
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_modelisation.ipynb
│   └── 03_validation.ipynb
├── src/              # fonctions réutilisables
├── docs/             # les 3 documents du livrable
├── .gitignore
├── requirements.txt
└── README.md

## Installation

```bash
git clone https://github.com/<utilisateur>/churnscope.git
cd churnscope
python -m venv .venv
source .venv/bin/activate    # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

## Approche

1. **Qualité des données** — typage, valeurs manquantes, cohérence des modalités
2. **Analyse exploratoire** — profils comparés des clients partis et restés
3. **Préparation** — encodage des variables catégorielles, normalisation des numériques
4. **Modélisation** — régression logistique, arbre de décision, Random Forest
5. **Évaluation** — matrice de confusion, courbe ROC, AUC, précision, rappel, F1
6. **Optimisation** — validation croisée et recherche sur grille d'hyperparamètres

Le jeu de données étant déséquilibré (environ 26 % de churn), l'*accuracy* seule
serait trompeuse. Le **rappel sur la classe churn** est retenu comme métrique
principale : ne pas détecter un client sur le départ coûte plus cher qu'une
fausse alerte.

## Résultats

_À compléter._

## Statut

Projet en cours.

## Auteur

Jouvence — DPIA 1, L'École Multimédia