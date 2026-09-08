# 3. Validation finale et conclusion

## Objectif

Cette étape mesure la capacité du modèle retenu à généraliser sur des clients qui n'ont pas servi à son entraînement. La validation est réalisée dans [03_validation.ipynb](../notebooks/03_validation.ipynb).

Le modèle évalué est le Random Forest optimisé par validation croisée et recherche sur grille :

- `n_estimators=200` ;
- `max_depth=6` ;
- `min_samples_leaf=1` ;
- `class_weight="balanced"`.

## Protocole de validation

Le dataset a été séparé une seule fois en deux sous-ensembles stratifiés :

- `80 %` pour l'entraînement ;
- `20 %` pour le test ;
- `random_state=42` ;
- proportion de churn conservée à `26,54 %` dans les deux ensembles.

Le jeu de test n'a pas été utilisé pour apprendre les transformations ni pour sélectionner les hyperparamètres. Le modèle final est entraîné sur le jeu d'entraînement, puis évalué sur les `1409` observations du test.

## Résultats finaux

| Métrique | Résultat |
|---|---:|
| Accuracy | 0,75 |
| Précision churn | 0,51 |
| Rappel churn | 0,79 |
| F1-score churn | 0,62 |
| AUC | 0,841 |

Le rappel de `0,79` signifie que le modèle détecte `297` des `374` clients ayant réellement quitté l'entreprise. Il manque donc `77` churns.

## Matrice de confusion

La matrice de confusion obtenue est :

```text
[[754 281]
 [ 77 297]]
```

Son interprétation est la suivante :

| | Prédit : No churn | Prédit : Churn |
|---|---:|---:|
| Réel : No churn | 754 | 281 |
| Réel : Churn | 77 | 297 |

- `754` clients restés sont correctement identifiés ;
- `297` clients partis sont correctement détectés ;
- `281` clients restés sont classés à tort comme des clients à risque ;
- `77` clients partis ne sont pas détectés.

Le modèle privilégie la détection des départs, ce qui explique le nombre élevé de fausses alertes. Ce choix est cohérent avec la priorité donnée au rappel churn.

## Courbe ROC et AUC

L'AUC de `0,841` indique une bonne capacité à classer les clients selon leur probabilité de départ. La courbe ROC est nettement au-dessus de la diagonale correspondant à un classement aléatoire.

L'AUC évalue la qualité générale du classement, tandis que la matrice de confusion dépend d'un seuil de décision précis. Ces deux analyses sont donc complémentaires.

## Analyse de la généralisation

Le Random Forest initial obtenait sur le test une AUC de `0,842` et un rappel de `0,791`. Après optimisation du rappel par validation croisée, le modèle final obtient une AUC de `0,841` et un rappel de `0,794`.

Les performances restent très proches. Cela suggère que la recherche sur grille n'a pas créé d'amélioration artificielle importante et que le modèle conserve un comportement relativement stable entre la validation croisée et le test final.

L'écart entre le rappel moyen de validation croisée (`0,809`) et le rappel final (`0,794`) reste limité. Il existe néanmoins une incertitude liée à un seul découpage du jeu de test. Une validation externe ou une nouvelle campagne de données serait nécessaire pour confirmer la performance en production.

## Limites

Plusieurs limites doivent être prises en compte :

- les associations observées ne prouvent pas une causalité ;
- le dataset décrit une période et une population particulières ;
- les fausses alertes peuvent générer des campagnes de rétention coûteuses ;
- les clients partis mais non détectés représentent encore un risque commercial ;
- le seuil de décision de `0,5` n'a pas encore été optimisé selon un coût métier explicite ;
- l'identifiant client a été supprimé, ce qui est correct pour éviter une variable sans sens prédictif, mais empêche toute personnalisation directe sans rattacher les prédictions aux identifiants en dehors du modèle.

## Recommandations métier

Le modèle peut servir à prioriser les clients à contacter, et non à prendre automatiquement une décision définitive. Il serait pertinent de :

1. définir le coût d'un churn manqué et celui d'une fausse alerte ;
2. ajuster le seuil de décision en fonction de ces coûts ;
3. tester les actions de rétention sur un groupe témoin ;
4. surveiller régulièrement le rappel, la précision et la dérive des données ;
5. réentraîner le modèle avec de nouvelles périodes lorsque les comportements clients évoluent.

## Conclusion

Le projet répond aux objectifs méthodologiques : nettoyage documenté, séparation train/test avant transformation, pipelines scikit-learn, comparaison des trois modèles imposés, validation croisée, recherche sur grille et évaluation finale par matrice de confusion et courbe ROC.

Le Random Forest optimisé est le modèle retenu pour sa capacité à détecter environ `79 %` des clients partis, avec une AUC de `0,841`. Il constitue un outil d'aide à la priorisation des actions de fidélisation, mais son utilisation doit rester accompagnée d'un suivi des coûts, des fausses alertes et de la performance dans le temps.
