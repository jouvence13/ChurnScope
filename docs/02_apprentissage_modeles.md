# 2. Apprentissage et comparaison des modèles

## Objectif

L'objectif de cette étape est d'entraîner les modèles imposés par le brief et un second modèle linéaire de comparaison :

- régression logistique ;
- Ridge Classifier ;
- arbre de décision ;
- Random Forest.

Les expériences sont réalisées dans [02_modelisation.ipynb](../notebooks/02_modelisation.ipynb).

## Méthode de préparation

Les données ont été séparées en un jeu d'entraînement et un jeu de test avant les transformations :

- entraînement : `5634` lignes ;
- test : `1409` lignes ;
- proportion de churn dans chaque ensemble : `26,54 %`.

Un `Pipeline` scikit-learn regroupe les transformations et le modèle. Cette organisation évite que les statistiques du jeu de test soient utilisées pendant l'apprentissage.

Les variables numériques sont imputées par la médiane puis standardisées avec `StandardScaler`. Les variables catégorielles sont imputées avec la modalité la plus fréquente puis encodées avec `OneHotEncoder`. L'option `handle_unknown="ignore"` permet de gérer une modalité rencontrée uniquement dans le jeu de test.

Le paramètre `class_weight="balanced"` est utilisé pour les trois modèles afin de tenir compte du déséquilibre entre les clients restés et les clients partis.

## Modèles choisis

### Sélection des caractéristiques

La sélection repose d'abord sur le sens métier des variables et sur l'analyse exploratoire. `customerID` est supprimé car il identifie un client mais ne décrit pas son comportement. Les variables de contrat, paiement, ancienneté, facturation et services sont conservées car elles décrivent des situations susceptibles d'être associées au départ. L'encodage One-Hot permet au modèle d'utiliser les modalités catégorielles sans imposer un ordre artificiel entre elles.

### Régression logistique

La régression logistique est un modèle de référence adapté à une classification binaire. Elle est relativement simple à interpréter et permet de mesurer l'influence des variables après encodage. Elle fournit également des probabilités utiles pour calculer l'AUC et étudier différents seuils de décision.

Paramètres principaux :

- `class_weight="balanced"` ;
- `max_iter=1000` ;
- `random_state=42`.

### Ridge Classifier

Le Ridge Classifier est ajouté comme second modèle linéaire. Sa régularisation L2 limite les coefficients trop élevés après l'encodage One-Hot. Comme il ne fournit pas directement de probabilités, son score de décision est utilisé pour calculer l'AUC.

### Arbre de décision

L'arbre de décision représente la classification sous forme de règles successives. Il est facile à expliquer, mais peut surapprendre si sa profondeur n'est pas contrôlée.

Paramètres principaux :

- `class_weight="balanced"` ;
- `max_depth=5` ;
- `random_state=42`.

L'arbre obtenu a une profondeur réelle de `5` et `31` feuilles. Ses premières règles utilisent notamment le contrat mensuel, le montant mensuel, l'absence de sécurité en ligne et le service fibre optique. Une branche illustrative est : un contrat mensuel combiné à un service fibre optique et une faible ancienneté augmente le risque estimé par l'arbre. Cette lecture reste descriptive et ne constitue pas une preuve de causalité.

La complexité a été contrôlée avec `max_depth=5`. L'accuracy est de `0,764` sur l'entraînement et `0,755` sur le test, soit un écart limité de `0,009`. Cela ne suggère pas de surapprentissage marqué sur ce découpage.

### Random Forest

Le Random Forest combine plusieurs arbres. Cette méthode réduit généralement la variance d'un arbre seul et fournit un modèle plus robuste, au prix d'une interprétation moins directe.

Paramètres initiaux :

- `n_estimators=300` ;
- `max_depth=8` ;
- `class_weight="balanced"` ;
- `n_jobs=-1` ;
- `random_state=42`.

## Métriques retenues

La classe positive correspond à `Churn = 1`.

- **Accuracy** : proportion totale de prédictions correctes ;
- **précision churn** : part des alertes qui correspondent réellement à un départ ;
- **rappel churn** : part des départs effectivement détectés ;
- **F1-score** : compromis entre précision et rappel ;
- **AUC** : capacité du modèle à classer les clients selon leur risque de churn.

Le rappel churn est prioritaire, car un client sur le départ qui n'est pas détecté représente une perte potentielle non traitée.

## Résultats avant optimisation

Les modèles ont été comparés sur le même jeu de test.

| Modèle | Accuracy | Précision churn | Rappel churn | F1-score churn | AUC |
|---|---:|---:|---:|---:|---:|
| Régression logistique | 0,738 | 0,504 | 0,783 | 0,614 | 0,841 |
| Ridge Classifier | 0,737 | 0,503 | 0,789 | 0,615 | 0,836 |
| Arbre de décision | 0,755 | 0,527 | 0,759 | 0,622 | 0,832 |
| Random Forest | 0,755 | 0,526 | 0,791 | 0,632 | 0,842 |

Le Random Forest initial obtient le meilleur rappel, le meilleur F1-score et la meilleure AUC. La régression logistique reste intéressante grâce à son interprétabilité et à un rappel proche.

## Validation croisée et recherche sur grille

L'optimisation a été appliquée au Random Forest avec :

- une validation croisée stratifiée à `5` plis ;
- une optimisation du score `recall` ;
- une recherche sur `n_estimators` : `100` ou `200` ;
- une recherche sur `max_depth` : `6` ou `10` ;
- une recherche sur `min_samples_leaf` : `1` ou `3`.

Le pipeline complet a été utilisé dans `GridSearchCV`. Les transformations ont donc été recalculées à l'intérieur de chaque pli, sans fuite de données.

Les meilleurs paramètres obtenus sont :

```text
n_estimators = 200
max_depth = 6
min_samples_leaf = 1
```

Le meilleur rappel moyen obtenu en validation croisée est de `0,809`.

Sur le jeu de test, le Random Forest optimisé obtient :

- accuracy : `0,746` ;
- précision churn : `0,514` ;
- rappel churn : `0,794` ;
- F1-score churn : `0,624` ;
- AUC : `0,841`.

## Choix du modèle

Le Random Forest optimisé est retenu pour la validation finale, car le rappel est la métrique métier principale. Il détecte `79,4 %` des clients partis sur le jeu de test.

Ce choix doit toutefois être nuancé : l'optimisation du rappel produit aussi des fausses alertes. Le seuil de décision pourrait être étudié ultérieurement pour adapter le compromis entre clients manqués et campagnes de rétention inutiles.
