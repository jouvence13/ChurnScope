# Guide explicatif du projet ChurnScope

Ce document sert à comprendre le projet et à l'expliquer à l'oral. Il ne remplace pas les trois livrables techniques.

## 1. Problème métier

L'entreprise veut repérer les clients qui risquent de partir afin de leur proposer une action de fidélisation avant leur départ.

La question métier est :

> Qui devons-nous contacter cette semaine, et pourquoi ?

Le modèle ne prédit pas une certitude. Il attribue à chaque client une probabilité de churn. Le dashboard transforme ensuite ces probabilités en une liste de clients à contacter en priorité.

## 2. Les données

Le dataset Telco Customer Churn contient `7043` clients et `21` colonnes.

Les variables décrivent :

- le profil du client ;
- les services utilisés ;
- le type de contrat ;
- le moyen de paiement ;
- l'ancienneté ;
- les montants facturés.

La cible est `Churn` :

- `No` signifie que le client est resté ;
- `Yes` signifie que le client est parti.

La cible est déséquilibrée : `73,46 %` des clients sont restés et `26,54 %` sont partis.

## 3. Nettoyage des données

`TotalCharges` était importée comme texte alors qu'elle représente un montant numérique. Onze lignes contenaient une chaîne vide. Ces lignes correspondent toutes à des clients avec `tenure = 0`.

La procédure est :

1. remplacer les chaînes vides par des valeurs manquantes ;
2. convertir `TotalCharges` en numérique ;
3. conserver les lignes concernées car ce sont des clients valides ;
4. imputer les valeurs manquantes dans le pipeline avec la médiane du train ;
5. supprimer `customerID` des variables utilisées par le modèle.

`customerID` est conservé dans les prédictions pour retrouver le client dans le dashboard, mais il n'est pas utilisé pour apprendre.

## 4. Pourquoi séparer train et test ?

Le jeu d'entraînement sert à apprendre. Le jeu de test sert à vérifier si le modèle fonctionne sur des données qu'il n'a jamais vues.

La séparation est faite avant l'imputation, la normalisation et l'encodage :

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
```

`stratify=y` conserve la même proportion de churn dans les deux parties.

Cette règle évite la fuite de données : le modèle ne doit jamais apprendre des informations statistiques provenant du test.

## 5. Pourquoi utiliser un Pipeline ?

Le `Pipeline` regroupe les transformations et le modèle. Ainsi, pendant l'entraînement ou la validation croisée :

- la médiane est calculée sur les données d'entraînement du pli ;
- le scaler est ajusté sur ces mêmes données ;
- l'encodage est appris sur ces mêmes données ;
- le modèle est entraîné après ces transformations.

C'est plus fiable qu'une transformation réalisée une fois sur tout le dataset avant le split.

## 6. Préparation des variables

Pour les variables numériques :

- imputation par la médiane ;
- normalisation avec `StandardScaler`.

Pour les variables catégorielles :

- imputation par la modalité la plus fréquente ;
- encodage One-Hot avec `OneHotEncoder`.

Le One-Hot est nécessaire car un modèle ne peut pas utiliser directement des textes comme `Month-to-month` ou `Electronic check`.

## 7. Analyse exploratoire

Les comparaisons montrent notamment :

- ancienneté médiane : `38` mois pour les clients restés contre `10` mois pour les clients partis ;
- charges mensuelles médianes : `64,43` contre `79,65` ;
- churn des contrats mensuels : `42,71 %` ;
- churn des contrats de deux ans : `2,83 %` ;
- churn avec paiement par chèque électronique : `45,29 %`.

Ces chiffres montrent des associations. Ils ne prouvent pas qu'un facteur cause directement le départ.

## 8. Les modèles

### Régression logistique

Elle sert de modèle de référence pour une classification binaire. Elle est rapide, relativement interprétable et produit des probabilités.

Résultats :

- rappel : `0,783` ;
- F1-score : `0,614` ;
- AUC : `0,841`.

### Ridge Classifier

Il s'agit d'un second modèle linéaire régularisé. La régularisation L2 limite des coefficients trop importants après l'encodage One-Hot.

Résultats :

- rappel : `0,789` ;
- F1-score : `0,615` ;
- AUC : `0,836`.

### Arbre de décision

Il applique des règles successives. Par exemple, ses premiers niveaux utilisent le type de contrat, les charges mensuelles, la sécurité en ligne et le service internet.

La profondeur est limitée à `5` pour éviter un arbre trop complexe. L'arbre obtenu possède `31` feuilles. Son accuracy est de `0,764` sur le train et `0,755` sur le test, ce qui indique un écart limité.

### Random Forest

Il combine plusieurs arbres. Cela réduit généralement la variance d'un arbre isolé et améliore la stabilité.

Le modèle initial obtient :

- rappel : `0,791` ;
- F1-score : `0,632` ;
- AUC : `0,842`.

## 9. Pourquoi le Random Forest est retenu ?

Le Random Forest obtient le meilleur compromis parmi les modèles comparés :

- meilleur F1-score ;
- meilleur rappel ou rappel très proche du meilleur ;
- meilleure AUC avant optimisation.

Il est ensuite optimisé avec une validation croisée à `5` plis et une recherche sur grille.

Les paramètres retenus sont :

```text
n_estimators=200
max_depth=6
min_samples_leaf=1
class_weight="balanced"
```

Le score optimisé est le rappel, car l'objectif est de manquer le moins possible de clients susceptibles de partir.

## 10. Comprendre les métriques

### Accuracy

Proportion totale de prédictions correctes. Elle peut être trompeuse avec une cible déséquilibrée.

### Précision

Parmi les clients signalés comme à risque, combien vont réellement partir ?

Une faible précision signifie que le modèle génère beaucoup de fausses alertes.

### Rappel

Parmi les clients qui vont réellement partir, combien sont détectés ?

C'est la métrique métier prioritaire dans ce projet.

### F1-score

Compromis entre précision et rappel.

### AUC

Mesure la capacité du modèle à classer les clients du moins risqué au plus risqué, indépendamment d'un seuil précis.

## 11. Résultats finaux

Sur le jeu de test :

- accuracy : `0,746` ;
- précision churn : `0,514` ;
- rappel churn : `0,794` ;
- F1-score churn : `0,624` ;
- AUC : `0,841`.

Matrice de confusion :

```text
[[754 281]
 [ 77 297]]
```

Cela signifie :

- `297` churns détectés ;
- `77` churns manqués ;
- `281` fausses alertes ;
- `754` clients restés correctement identifiés.

## 12. Le rôle du seuil

Le seuil par défaut est `0,5`.

Si on baisse le seuil :

- davantage de clients sont ciblés ;
- le rappel augmente généralement ;
- la précision peut diminuer ;
- les équipes doivent traiter plus de fausses alertes.

Si on augmente le seuil :

- moins de clients sont ciblés ;
- la précision peut augmenter ;
- certains clients à risque ne sont pas détectés.

Le bon seuil dépend du coût d'une campagne de rétention, de la valeur du client et de la capacité des équipes.

## 13. Le dashboard

Le dashboard Streamlit charge :

- le modèle sérialisé dans `data/processed/churn_model.joblib` ;
- les prédictions dans `data/processed/customer_predictions.csv`.

Il ne réentraîne pas le modèle au démarrage.

Il permet de :

1. filtrer les clients par contrat, service internet et ancienneté ;
2. choisir un seuil de probabilité ;
3. voir le nombre de clients ciblés ;
4. voir le revenu mensuel exposé ;
5. consulter les clients par probabilité décroissante ;
6. observer le rappel et la précision sur le jeu de test.

## 14. Réponses courtes pour l'oral

### Pourquoi ne pas utiliser seulement l'accuracy ?

Parce que la classe churn est minoritaire. Un modèle pourrait obtenir une bonne accuracy en prédisant presque toujours que les clients restent, tout en ratant les départs.

### Pourquoi supprimer customerID ?

C'est un identifiant technique. Il ne décrit pas le comportement du client et pourrait conduire le modèle à apprendre du bruit.

### Pourquoi utiliser class_weight balanced ?

Pour donner davantage de poids à la classe minoritaire et éviter que le modèle favorise trop les clients restés.

### Pourquoi un pipeline ?

Pour apprendre l'imputation, la normalisation et l'encodage uniquement sur les données d'entraînement et éviter la fuite de données.

### Pourquoi le rappel est prioritaire ?

Parce qu'un churn manqué représente un client perdu qui n'a pas pu être ciblé par une action de rétention.

### Le modèle est-il parfait ?

Non. Il détecte `79,4 %` des churns, mais produit aussi des fausses alertes. C'est un outil de priorisation, pas une décision automatique.

### Quelles améliorations prévoir ?

Calibrer le seuil selon les coûts métier, suivre la performance sur de nouvelles données et mesurer l'efficacité réelle des actions avec un groupe témoin.

## 15. Phrase de conclusion

> ChurnScope permet de prioriser les actions de fidélisation en classant les clients selon leur risque de départ. Le Random Forest optimisé détecte environ quatre churns sur cinq, mais le seuil doit être ajusté avec les équipes métier pour équilibrer les clients manqués et les fausses alertes.
