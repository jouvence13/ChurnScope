# 1. Analyse et préparation des données

## Objectif

L'objectif est d'identifier les facteurs associés au départ des clients d'une entreprise de télécommunications. La variable cible est `Churn`, qui indique si un client a quitté l'entreprise au cours du dernier mois.

L'analyse a été réalisée dans [01_exploration.ipynb](../notebooks/01_exploration.ipynb).

## Description du dataset

Le dataset Telco Customer Churn contient `7043` clients et `21` colonnes.

Les variables couvrent plusieurs dimensions :

- données démographiques : genre, seniorité, partenaire et personnes à charge ;
- services : téléphonie, internet, sécurité en ligne, sauvegarde, support technique et streaming ;
- contrat et paiement : type de contrat, facturation papier et moyen de paiement ;
- compte client : ancienneté, montant mensuel et montant total facturé ;
- cible : `Churn`.

La colonne `customerID` est un identifiant technique. Elle a été écartée de la modélisation car elle ne représente pas une caractéristique prédictive du client.

## Qualité des données

### Valeurs manquantes et doublons

L'inspection initiale n'a détecté aucune valeur `NaN` et aucun doublon exact.

Cependant, `TotalCharges` était importée comme variable textuelle. Onze lignes contenaient une chaîne vide au lieu d'une valeur numérique. Ces onze clients ont tous une ancienneté (`tenure`) égale à zéro. Cette situation est cohérente avec des clients nouvellement inscrits qui n'ont pas encore accumulé de montant total facturé.

### Nettoyage réalisé

Le nettoyage a suivi les étapes suivantes :

1. conserver une copie du dataset original ;
2. remplacer les chaînes vides de `TotalCharges` par des valeurs manquantes ;
3. convertir `TotalCharges` en type numérique ;
4. conserver les onze lignes concernées, car elles représentent des clients valides et non des doublons ou des erreurs manifestes ;
5. supprimer `customerID` avant la modélisation.

Après conversion, `TotalCharges` est de type `float64`, avec `11` valeurs manquantes sur `7043` lignes.

Dans les pipelines de modélisation, ces valeurs sont imputées par la médiane calculée sur le jeu d'entraînement. Cette imputation est réalisée après la séparation train/test afin d'éviter une fuite de données.

## Répartition de la cible

La variable `Churn` est déséquilibrée :

- clients restés : `5174`, soit `73,46 %` ;
- clients partis : `1869`, soit `26,54 %`.

Cette répartition rend l'accuracy insuffisante comme métrique unique. Un modèle qui prédirait toujours « pas de churn » obtiendrait une accuracy élevée tout en ne détectant aucun départ. Le rappel de la classe churn est donc la métrique métier prioritaire.

## Statistiques descriptives

Les principales statistiques numériques sont les suivantes :

| Variable | Moyenne | Médiane | Minimum | Maximum |
|---|---:|---:|---:|---:|
| `SeniorCitizen` | 0,16 | 0 | 0 | 1 |
| `tenure` | 32,37 | 29 | 0 | 72 |
| `MonthlyCharges` | 64,76 | 70,35 | 18,25 | 118,75 |
| `TotalCharges` | 2283,30 | 1397,48 | 18,80 | 8684,80 |

Les visualisations de l'exploration montrent notamment que :

- l'ancienneté médiane est de `38` mois chez les clients restés et de `10` mois chez les clients partis ;
- le montant mensuel médian est de `64,43` chez les clients restés et de `79,65` chez les clients partis ;
- le montant total médian est de `1683,60` chez les clients restés et de `703,55` chez les clients partis.

Ces écarts sont des associations descriptives. Ils ne permettent pas, à eux seuls, de conclure à une causalité.

## Analyse des variables catégorielles

Plusieurs modalités présentent des taux de churn nettement différents :

- contrat mensuel : `42,71 %` de churn ;
- contrat d'un an : `11,27 %` ;
- contrat de deux ans : `2,83 %` ;
- service internet fibre optique : `41,89 %` ;
- paiement par chèque électronique : `45,29 %` ;
- absence de partenaire : `32,96 %` ;
- absence de personnes à charge : `31,28 %`.

Les clients sans sécurité en ligne ou sans support technique présentent également des taux de churn supérieurs à `41 %`. Ces résultats orientent l'analyse et la modélisation, mais ne doivent pas être interprétés comme des effets causaux sans analyse complémentaire.

## Préparation pour la modélisation

La préparation respecte la contrainte méthodologique principale :

1. séparation des données en train et test avec stratification sur `Churn` ;
2. apprentissage des transformations uniquement sur le train ;
3. imputation et normalisation des variables numériques dans un `Pipeline` ;
4. imputation et encodage One-Hot des variables catégorielles dans le même pipeline.

La séparation utilisée est de `80 %` pour l'entraînement et `20 %` pour le test, avec `random_state=42`. La proportion de churn est conservée à `26,54 %` dans les deux sous-ensembles.

## Conclusion

Le dataset est exploitable après la conversion de `TotalCharges` et la prise en compte de ses onze valeurs manquantes. L'analyse met en évidence un risque particulièrement élevé chez les clients récents, sous contrat mensuel, avec des frais mensuels plus élevés et certains services ou moyens de paiement. Ces constats justifient la comparaison de plusieurs modèles de classification et l'utilisation du rappel churn comme indicateur principal.
