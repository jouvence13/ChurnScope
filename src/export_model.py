"""
Script d'entrainement et d'export du pipeline ML ChurnScope.
Point d'entree principal pour regenerer le modele et les predictions.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.train import train_and_evaluate


def main():
    print("Debut de l'entrainement et de l'evaluation du modele...")
    pipeline, metrics, predictions = train_and_evaluate()
    print("\nModele entraine et artefacts exportes avec succes !")
    print("--------------------------------------------------")
    print(f"Accuracy         : {metrics['accuracy']:.4f}")
    print(f"Precision Churn  : {metrics['precision']:.4f}")
    print(f"Rappel Churn     : {metrics['recall']:.4f}")
    print(f"F1-Score Churn   : {metrics['f1']:.4f}")
    print(f"ROC-AUC Score    : {metrics['roc_auc']:.4f}")
    print("--------------------------------------------------")
    print(f"Matrice de confusion : {metrics['confusion_matrix']}")
    print(f"Total predictions enregistrees : {len(predictions)}")


if __name__ == "__main__":
    main()
