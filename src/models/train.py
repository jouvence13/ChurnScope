from pathlib import Path
from typing import Dict, Any, Tuple
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.data.loader import (
    load_raw_data,
    create_preprocessor,
    DEFAULT_RAW_DATA_PATH,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DEFAULT_MODEL_PATH = PROCESSED_DIR / "churn_model.joblib"
DEFAULT_PREDICTIONS_PATH = PROCESSED_DIR / "customer_predictions.csv"


def build_random_forest_pipeline() -> Pipeline:
    """Construit le pipeline complet Prétraitement + Modèle Random Forest optimisé."""
    preprocessor = create_preprocessor()
    classifier = RandomForestClassifier(
        n_estimators=200,
        max_depth=6,
        min_samples_leaf=1,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier),
        ]
    )


def train_and_evaluate(
    raw_data_path: Path = DEFAULT_RAW_DATA_PATH,
    model_output_path: Path = DEFAULT_MODEL_PATH,
    predictions_output_path: Path = DEFAULT_PREDICTIONS_PATH,
    test_size: float = 0.2,
    random_state: int = 42,
) -> Tuple[Pipeline, Dict[str, Any], pd.DataFrame]:
    """
    Entraîne le modèle, évalue ses performances sur le jeu de test et sauvegarde les artefacts.
    """
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    data = load_raw_data(raw_data_path)
    features = data.drop(columns=["Churn", "customerID"])
    target = data["Churn"]

    train_features, test_features, train_target, test_target = train_test_split(
        features,
        target,
        test_size=test_size,
        stratify=target,
        random_state=random_state,
    )

    pipeline = build_random_forest_pipeline()
    pipeline.fit(train_features, train_target)

    # Inférence sur le jeu de test
    test_pred_proba = pipeline.predict_proba(test_features)[:, 1]
    test_pred_binary = (test_pred_proba >= 0.5).astype(int)

    # Calcul des métriques de validation
    metrics = {
        "accuracy": float(accuracy_score(test_target, test_pred_binary)),
        "precision": float(
            precision_score(test_target, test_pred_binary, zero_division=0)
        ),
        "recall": float(recall_score(test_target, test_pred_binary, zero_division=0)),
        "f1": float(f1_score(test_target, test_pred_binary, zero_division=0)),
        "roc_auc": float(roc_auc_score(test_target, test_pred_proba)),
        "confusion_matrix": confusion_matrix(test_target, test_pred_binary).tolist(),
    }

    # Préparation du dataframe global de prédictions pour l'application
    predictions = data.drop(columns=["Churn"]).copy()
    predictions["actual_churn"] = data["Churn"].values
    predictions["is_test"] = predictions.index.isin(test_features.index)
    predictions["churn_probability"] = pipeline.predict_proba(
        data.drop(columns=["Churn", "customerID"])
    )[:, 1]
    predictions["predicted_churn"] = (predictions["churn_probability"] >= 0.5).astype(
        int
    )

    # Sauvegarde des artefacts
    joblib.dump(pipeline, model_output_path)
    predictions.to_csv(predictions_output_path, index=False)

    return pipeline, metrics, predictions


if __name__ == "__main__":
    pipeline, metrics, preds = train_and_evaluate()
    print("=== Métriques de Test ===")
    for k, v in metrics.items():
        if k != "confusion_matrix":
            print(f"{k.capitalize():12}: {v:.4f}")
    print(f"Confusion Matrix: {metrics['confusion_matrix']}")
