from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_PATH = PROCESSED_DIR / "churn_model.joblib"
PREDICTIONS_PATH = PROCESSED_DIR / "customer_predictions.csv"


def load_data():
    data = pd.read_csv(DATA_PATH)
    data["TotalCharges"] = pd.to_numeric(
        data["TotalCharges"].replace(r"^\s*$", pd.NA, regex=True),
        errors="coerce",
    )
    data["Churn"] = data["Churn"].map({"No": 0, "Yes": 1})
    return data


def build_pipeline(data):
    features = data.drop(columns=["Churn", "customerID"])
    numeric_features = [
        "SeniorCitizen",
        "tenure",
        "MonthlyCharges",
        "TotalCharges",
    ]
    categorical_features = features.select_dtypes(include="object").columns.tolist()

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_transformer, numeric_features),
            ("categorical", categorical_transformer, categorical_features),
        ]
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=200,
                    max_depth=6,
                    min_samples_leaf=1,
                    class_weight="balanced",
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )


def main():
    data = load_data()
    features = data.drop(columns=["Churn", "customerID"])
    target = data["Churn"]
    train_features, test_features, train_target, _ = train_test_split(
        features,
        target,
        test_size=0.2,
        stratify=target,
        random_state=42,
    )

    model = build_pipeline(data)
    model.fit(train_features, train_target)

    predictions = data.drop(columns=["Churn"]).copy()
    predictions["actual_churn"] = data["Churn"].values
    predictions["is_test"] = predictions.index.isin(test_features.index)
    predictions["churn_probability"] = model.predict_proba(
        data.drop(columns=["Churn", "customerID"])
    )[:, 1]
    predictions["predicted_churn"] = (
        predictions["churn_probability"] >= 0.5
    ).astype(int)
    predictions.to_csv(PREDICTIONS_PATH, index=False)
    joblib.dump(model, MODEL_PATH)

    print(f"Modèle exporté : {MODEL_PATH}")
    print(f"Prédictions exportées : {PREDICTIONS_PATH}")
    print(f"Nombre de clients : {len(predictions)}")


if __name__ == "__main__":
    main()
