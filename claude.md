# Contexte du projet

Je réalise un projet scolaire de Machine Learning : prédiction du churn client
dans les télécoms. Formation DPIA Année 1, L'École Multimédia. Travail individuel.

Le repo s'appelle ChurnScope. Structure déjà en place :

churnscope/
├── data/raw/          # dataset brut
├── data/processed/    # données nettoyées
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_modelisation.ipynb
│   └── 03_validation.ipynb
├── src/
├── docs/
├── requirements.txt
└── README.md

# Données

Dataset Telco Customer Churn (Kaggle, blastchar) : 7043 clients, 21 colonnes.
- Cible : Churn (départ dans le dernier mois), déséquilibrée ~73/27
- Services : téléphone, internet, sécurité en ligne, streaming, etc.
- Compte : tenure, type de contrat, mode de paiement, MonthlyCharges, TotalCharges
- Démographie : genre, senior, partenaire, personnes à charge

Anomalies connues : TotalCharges typé object avec 11 valeurs vides
(clients à tenure = 0) ; customerID sans valeur prédictive.

# Ce qui est imposé par le brief

- Python, bibliothèques libres
- Git/GitHub avec commits conventionnels (conventionalcommits.org)
- Chaque étape documentée
- Modèles imposés : régression logistique, arbre de décision, Random Forest
- Métriques : matrice de confusion, ROC, AUC, précision, rappel, F1
- Optimisation : validation croisée et recherche sur grille
- Visualisations Matplotlib/Seaborn + dashboard Plotly ou Bokeh

# Livrable : 3 documents distincts

1. Analyse et préparation : qualité des données, stats descriptives
   avec visualisations, procédure de nettoyage
2. Apprentissage : justification de l'algorithme, hyperparamètres,
   indicateurs de performance
3. Validation : procédure sur jeu de test, analyse de la généralisation,
   conclusions

# Contraintes méthodologiques importantes

- Split train/test AVANT toute transformation apprenant des données
  (pas de fuite de données) — utiliser un Pipeline scikit-learn
- L'accuracy seule est trompeuse vu le déséquilibre : le rappel sur la
  classe churn est la métrique métier prioritaire

# Comment je veux travailler

Explique-moi chaque étape avant de coder. Je suis en apprentissage,
je dois comprendre et pouvoir justifier chaque choix à l'oral.
Procède étape par étape, une à la fois, et attends ma validation
avant de passer à la suivante.

Commence par l'étape 1 : chargement du dataset et analyse de la
qualité des données.