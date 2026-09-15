import numpy as np
from src.data.loader import create_preprocessor, load_raw_data
from src.models.train import build_random_forest_pipeline


def test_preprocessor_transformation():
    """Vérifie que le ColumnTransformer s'exécute correctement sans lever d'exception."""
    data = load_raw_data()
    features = data.drop(columns=["Churn", "customerID"])
    preprocessor = create_preprocessor()

    transformed = preprocessor.fit_transform(features)
    assert isinstance(transformed, np.ndarray)
    assert transformed.shape[0] == len(features)
    assert transformed.shape[1] > len(
        features.columns
    )  # Encodage One-Hot étend les colonnes


def test_pipeline_prediction_shape():
    """Vérifie que le pipeline complet génère des probabilités valides dans [0, 1]."""
    data = load_raw_data()
    features = data.drop(columns=["Churn", "customerID"]).head(50)
    target = data["Churn"].head(50)

    pipeline = build_random_forest_pipeline()
    pipeline.fit(features, target)

    probs = pipeline.predict_proba(features)[:, 1]
    assert len(probs) == 50
    assert np.all(probs >= 0.0)
    assert np.all(probs <= 1.0)
