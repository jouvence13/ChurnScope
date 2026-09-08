# Présentation dirigeante — ChurnScope

## 1. Question métier

**Qui devons-nous contacter cette semaine, et pourquoi ?**

ChurnScope transforme une probabilité de départ en une liste priorisée de clients à contacter. Le modèle aide à organiser les actions de rétention ; il ne remplace pas la décision des équipes métier.

## 2. Chiffres clés

- `7043` clients analysés ;
- `26,54 %` de churn dans le dataset ;
- rappel churn final : `79,4 %` ;
- AUC : `0,841` ;
- `297` churns détectés sur `374` ;
- `77` churns non détectés ;
- `281` fausses alertes.

## 3. Profil des clients à risque

L'exploration met en évidence plusieurs segments associés à un churn plus élevé :

- contrat mensuel : `42,71 %` de churn ;
- paiement par chèque électronique : `45,29 %` ;
- service fibre optique : `41,89 %` ;
- ancienneté médiane des clients partis : `10` mois ;
- charges mensuelles médianes des clients partis : `79,65`.

Ces résultats décrivent des associations et ne prouvent pas que ces facteurs causent directement le départ.

## 4. Comment utiliser le dashboard

1. ouvrir le dashboard Streamlit ;
2. choisir les segments à examiner ;
3. régler le seuil de probabilité selon la capacité de l'équipe ;
4. consulter la table triée par probabilité décroissante ;
5. vérifier le contrat, l'ancienneté, le service internet et les charges ;
6. préparer une action de rétention adaptée au profil.

## 5. Arbitrage métier

Un seuil bas cible davantage de clients et augmente les chances de détecter les départs, mais génère davantage de fausses alertes. Un seuil haut réduit le volume de contacts, mais laisse passer davantage de clients qui vont partir.

Le seuil doit être choisi selon :

- le coût d'une campagne de rétention ;
- la valeur mensuelle du client ;
- le coût d'un churn manqué ;
- la capacité hebdomadaire des équipes.

## 6. Recommandation

Commencer par les clients ayant la probabilité la plus élevée, puis tester des offres ou actions différentes sur des groupes comparables. Un groupe témoin est nécessaire pour mesurer si les actions réduisent réellement le churn.

## 7. Limites à rappeler à l'oral

- le modèle indique un risque, pas une certitude ;
- une fausse alerte peut entraîner un coût inutile ;
- les résultats doivent être suivis sur de nouvelles périodes ;
- le dashboard doit servir à prioriser, jamais à automatiser une décision commerciale sans contrôle humain.
