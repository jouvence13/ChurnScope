from pathlib import Path
from typing import List, Optional
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RAW_DATA_PATH = (
    PROJECT_ROOT / "data" / "raw" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
)

NUMERIC_FEATURES = [
    "SeniorCitizen",
    "tenure",
    "MonthlyCharges",
    "TotalCharges",
]

CATEGORICAL_FEATURES = [
    "gender",
    "Partner",
    "Dependents",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
]


def load_raw_data(filepath: Optional[Path] = None) -> pd.DataFrame:
    """
    Charge le dataset brut Telco Churn et effectue le nettoyage initial.

    - Nettoyage des espaces vides dans TotalCharges
    - Conversion de la cible Churn en entier 0 / 1
    """
    path = filepath or DEFAULT_RAW_DATA_PATH
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable à l'emplacement : {path}")

    data = pd.read_csv(path)

    # Nettoyage de TotalCharges (espaces vides convertis en NaN)
    data["TotalCharges"] = pd.to_numeric(
        data["TotalCharges"].replace(r"^\s*$", pd.NA, regex=True),
        errors="coerce",
    )

    # Mapping binaire de la cible Churn si présente
    if "Churn" in data.columns:
        data["Churn"] = (
            data["Churn"].replace({"No": 0, "Yes": 1, "0": 0, "1": 1}).astype(int)
        )

    return data


def create_preprocessor(
    numeric_features: Optional[List[str]] = None,
    categorical_features: Optional[List[str]] = None,
) -> ColumnTransformer:
    """
    Construit un ColumnTransformer scikit-learn standardisé et sans fuite de données.
    """
    num_cols = numeric_features or NUMERIC_FEATURES
    cat_cols = categorical_features or CATEGORICAL_FEATURES

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_transformer, num_cols),
            ("categorical", categorical_transformer, cat_cols),
        ],
        remainder="drop",
    )

    return preprocessor
