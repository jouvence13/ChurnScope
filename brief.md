# Projet #3 — Prédiction du Churn Client avec des Modèles de Machine Learning

**Introduction au Machine Learning**
Directeur de projet en intelligence artificielle — Année 1 — L'École Multimédia

---

## Sommaire

- [Contexte](#contexte)
- [Contraintes](#contraintes)
- [Libertés](#libertés)
- [Objectifs](#objectifs)
- [Étapes du projet](#étapes-du-projet)
- [Données](#données)
- [Rendu final](#rendu-final)
- [Évaluations](#évaluations)
- [Compétences visées](#compétences-visées)
- [Conseils](#conseils)

---

## Contexte

### Présentation

Vous êtes embauché en tant que data scientiste au sein d'une entreprise de télécommunications. Votre mission consiste à développer un modèle de Machine Learning capable de prédire le churn des clients, c'est-à-dire le risque qu'ils résilient leur abonnement.

Vous devrez explorer les données des clients, sélectionner et entraîner différents modèles de régression et de classification, et optimiser ces modèles pour obtenir les meilleures prédictions possibles.

Vous présenterez également vos résultats sous forme de visualisations claires et d'une documentation détaillée.

## Contraintes

- **Travail en autonomie** : vous travaillerez seul sur ce projet, ce qui implique une gestion efficace du temps et des ressources.
- **Documentation complète** : chaque étape du projet doit être clairement documentée.
- **Utilisation de Git et GitHub** : tout le projet doit être versionné sur GitHub, avec des commits réguliers et bien nommés (tel que <https://www.conventionalcommits.org>), un README détaillé, et une bonne structuration du code.
- **Respect des délais** : le projet doit être livré sous la forme d'une archive ZIP et dans les délais imposés sous peine de pénalisation.

## Libertés

- **Bibliothèques** : dans la mesure où la base de votre code est écrite en Python, vous pouvez utiliser les bibliothèques (apprentissage, calcul numérique, visualisation) qui vous sembleront les plus appropriées.
- **Algorithmes** : vous pouvez utiliser les algorithmes que vous souhaitez (à condition de le justifier).
- **Déploiement** : bien que cela ne soit pas le cœur du projet, vous pouvez proposer des pistes pour le déploiement en ligne de votre modèle, via un tableau de bord de consultation des données, soit via une API (avec Flask ou FastAPI, par exemple).
- **Améliorations** : en fonction de votre familiarité avec le sujet, vous pouvez proposer des options qui permettraient d'améliorer le pipeline de base de l'apprentissage.

## Objectifs

Vous devrez avoir réalisé les éléments suivants :

1. Collecter et préparer les données nécessaires pour prédire le churn des clients.
2. Développer et comparer différents modèles de Machine Learning (régression logistique, arbres de décision, Random Forest) pour identifier les clients à risque.
3. Évaluer et optimiser les performances des modèles en utilisant des techniques de validation et d'optimisation des hyperparamètres.
4. Visualiser les résultats pour aider à interpréter les prédictions et faciliter la prise de décision.
5. Documenter le processus complet et présenter les conclusions à l'équipe dirigeante.

## Étapes du projet

### 1. Collecte et préparation des données

- **Collecte des données** : utilisez un dataset public (par exemple, le dataset « Telco Customer Churn » de Kaggle) ou des données internes fournies par l'entreprise.
- **Préparation des données** : nettoyez les données, traitez les valeurs manquantes, encodez les variables catégorielles, et normalisez les variables numériques pour améliorer les performances des modèles.

### 2. Exploration des données

- **Analyse exploratoire des données (EDA)** : analysez les caractéristiques des clients qui sont restés et ceux qui ont churné, en utilisant des visualisations avec Seaborn et Matplotlib.
- **Sélection des caractéristiques** : identifiez les variables les plus pertinentes pour prédire le churn, telles que l'âge, le type de contrat, le nombre de services souscrits, etc.

### 3. Développement des modèles de régression

- **Régression logistique** :
  - Implémentez un modèle de régression logistique pour prédire le churn.
  - Évaluez les performances du modèle à l'aide de matrices de confusion, courbes ROC, et scores AUC.
- **Comparaison avec d'autres modèles de régression** : testez d'autres modèles de régression pour déterminer si la régression logistique est la plus adaptée.

### 4. Développement des modèles de classification avancés

- **Arbres de décision** :
  - Construisez un arbre de décision pour modéliser la probabilité de churn en fonction des caractéristiques des clients.
  - Interprétez les règles de décision et analysez la complexité du modèle.
- **Random Forest** :
  - Implémentez un modèle de Random Forest pour améliorer la précision des prédictions.
  - Analysez l'importance des caractéristiques et optimisez les hyperparamètres du modèle.

### 5. Évaluation et optimisation des modèles

- **Comparaison des modèles** : comparez les performances des différents modèles en utilisant des métriques telles que la précision, le rappel, le score F1, et le score AUC.
- **Optimisation des hyperparamètres** : utilisez des techniques comme la validation croisée et la recherche en grille pour ajuster les hyperparamètres et maximiser les performances.

### 6. Visualisation et présentation des résultats

- **Visualisation des performances** : créez des graphiques avec Matplotlib et Seaborn pour illustrer les performances des modèles (courbes ROC, importance des caractéristiques, etc.).
- **Création de dashboards** : utilisez Plotly ou Bokeh pour créer des visualisations interactives permettant d'explorer les prédictions de churn.
- **Préparation d'une présentation** : rédigez un rapport et préparez une présentation pour expliquer les résultats et les recommandations basées sur ces résultats.

### 7. Documentation et gestion du projet

- **Documentation** : documenter chaque étape du processus, incluant la préparation des données, l'implémentation des modèles, et l'analyse des résultats.
- **Utilisation de GitHub** : gérez votre projet avec Git et GitHub, en versionnant le code source, en suivant les modifications, et en collaborant avec vos coéquipiers.

## Données

Pour réaliser les objectifs du projet, vous utiliserez le jeu de données que vous pourrez télécharger via la ligne de commande suivante :

```bash
#!/bin/bash
curl -L -o ~/Downloads/telco-customer-churn.zip \
  https://www.kaggle.com/api/v1/datasets/download/blastchar/telco-customer-churn
```

### Contenu

Chaque ligne représente un client, chaque colonne contient les attributs du client décrits dans la colonne Métadonnées.

L'ensemble de données comprend des informations sur :

- Les clients qui ont quitté dans le dernier mois — la colonne est appelée `Churn`.
- Les services auxquels chaque client s'est abonné — téléphone, Internet, sécurité en ligne, sauvegarde en ligne, protection de l'appareil, support technique, et streaming TV et films.
- Les informations sur le compte client — combien de temps ils ont été client, contrat, mode de paiement, facturation sans papier, frais mensuels et frais totaux.
- Les informations démographiques sur les clients — sexe, tranche d'âge, et s'ils ont des partenaires et des personnes à charge.

## Rendu final

Votre rendu final prendra la forme d'une archive ZIP et devra comporter les éléments suivants :

1. Un document (comme un carnet Jupyter, par exemple) dans lequel vous analyserez le jeu de données fourni et où vous préparerez ce jeu de données de manière à ce qu'il soit acceptable comme entrée de votre processus d'apprentissage. Dont :
   - une analyse de la qualité des données ;
   - une analyse statistique descriptive des données (avec visualisation) ;
   - une procédure pour nettoyer le jeu de données.
2. Un document développant la mise en œuvre du processus d'apprentissage, en détaillant et justifiant :
   - le choix d'un algorithme particulier ;
   - les hyperparamètres du modèle ;
   - les indicateurs de performance de votre modèle.
3. Une procédure de validation du modèle, sur un jeu de données de test, avec une analyse de la capacité de votre modèle à généraliser son apprentissage et les conclusions que vous en tirez.

Cette archive aura comme titre votre nom et prénom avec votre classe.

Exemple : `arthur_mensch_projet3_AIA01.zip`

> **Attention** : un rendu non livré ou en retard vous pénalise pour la certification.

## Évaluations

- **Qualité de la préparation des données** : pertinence du nettoyage, de la normalisation, et de la sélection des caractéristiques.
- **Performance des modèles développés** : précision des prédictions et efficacité des techniques de modélisation utilisées.
- **Capacité à évaluer et optimiser les modèles** : utilisation appropriée des métriques et des techniques d'optimisation pour améliorer les performances des modèles.
- **Clarté et interactivité des visualisations** : efficacité des visualisations pour transmettre les résultats et soutenir la prise de décision.
- **Documentation et gestion du projet** : exhaustivité et clarté de la documentation, ainsi que l'utilisation appropriée de GitHub pour la gestion du projet.
- **Présentation professionnelle des résultats** : qualité de la présentation finale, incluant l'explication des choix méthodologiques, l'interprétation des résultats, et les recommandations.

## Compétences visées

| Code | Compétence |
|------|------------|
| **D-02** | Créer un algorithme d'Intelligence Artificielle adapté aux données d'entraînement et conforme aux spécifications du cahier des charges, en veillant à répondre aux besoins spécifiques, notamment en termes d'accessibilité. |
| **D-04** | Concevoir des pipelines d'intégration et déploiement continu pour automatiser le processus de déploiement d'une solution d'IA. |
| **D-06** | Piloter la performance de la solution d'IA dans l'infrastructure à travers la mise en place d'outils de monitoring (comme Aporia ou Evidently) pour s'assurer qu'elle respecte les spécifications du cahier des charges dans un environnement de production. |

## Conseils

- Bien prendre le temps d'analyser le brief et comprendre le client.
- Organisez-vous et planifiez votre travail : donnez-vous des objectifs intermédiaires.
- Planifiez des sessions de travail régulières.
- Utilisez Git pour versionner votre code dès le départ.
- Ne jamais être trop ambitieux.
- Faites directement les documents du livrable.
- Mettez en œuvre les bonnes pratiques vues en cours.
- Refactorisez pour éviter le code redondant.
- Soignez la qualité de votre code (commentaires, indentation).
- Pensez à la qualité du résultat !