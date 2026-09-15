from typing import List, Dict, Any
import numpy as np
import pandas as pd
import shap
from sklearn.pipeline import Pipeline


def get_feature_names(pipeline: Pipeline) -> List[str]:
    """Extrait les noms des colonnes après transformation par le préprocesseur."""
    preprocessor = pipeline.named_steps["preprocessor"]
    raw_names = preprocessor.get_feature_names_out()
    # Nettoyage des préfixes générés par ColumnTransformer (ex: 'categorical__', 'numeric__')
    clean_names = [
        name.replace("categorical__", "").replace("numeric__", "") for name in raw_names
    ]
    return clean_names


class ChurnExplainer:
    """Gestionnaire d'explicabilité SHAP pour le modèle ChurnScope."""

    def __init__(self, pipeline: Pipeline):
        self.pipeline = pipeline
        self.preprocessor = pipeline.named_steps["preprocessor"]
        self.classifier = pipeline.named_steps["classifier"]
        self.feature_names = get_feature_names(pipeline)
        self.explainer = shap.TreeExplainer(self.classifier)

    def explain_instance(
        self, customer_df: pd.DataFrame, top_k: int = 6
    ) -> List[Dict[str, Any]]:
        """
        Calcule les contributions SHAP pour un client spécifique.

        Retourne les `top_k` variables les plus influentes (positives et négatives).
        """
        # Préparation des features (on retire les colonnes non features)
        cols_to_drop = [
            col
            for col in [
                "Churn",
                "customerID",
                "actual_churn",
                "churn_probability",
                "predicted_churn",
                "is_test",
                "targeted",
            ]
            if col in customer_df.columns
        ]
        features_only = customer_df.drop(columns=cols_to_drop)

        # Transformation via le préprocesseur
        transformed_data = self.preprocessor.transform(features_only)

        # Calcul des valeurs SHAP
        shap_values = self.explainer.shap_values(transformed_data)

        # Pour RandomForest binary classification:
        # shap_values est soit une liste de 2 arrays [classe 0, classe 1], soit un array 3D
        if isinstance(shap_values, list):
            class_1_shap = shap_values[1][0]
        elif len(shap_values.shape) == 3:
            class_1_shap = shap_values[0, :, 1]
        else:
            class_1_shap = shap_values[0]

        contributions = []
        for name, value in zip(self.feature_names, class_1_shap):
            contributions.append(
                {
                    "feature": name,
                    "shap_value": float(value),
                    "impact": "Augmente le risque" if value > 0 else "Réduit le risque",
                    "abs_impact": abs(float(value)),
                }
            )

        # Tri par impact absolu décroissant
        contributions.sort(key=lambda x: x["abs_impact"], reverse=True)
        return contributions[:top_k]

    def get_global_importance(
        self, background_df: pd.DataFrame, top_k: int = 10
    ) -> pd.DataFrame:
        """Calcule l'importance globale moyenne des features selon SHAP."""
        cols_to_drop = [
            col
            for col in [
                "Churn",
                "customerID",
                "actual_churn",
                "churn_probability",
                "predicted_churn",
                "is_test",
                "targeted",
            ]
            if col in background_df.columns
        ]
        features_only = background_df.drop(columns=cols_to_drop)

        transformed_data = self.preprocessor.transform(features_only)
        shap_values = self.explainer.shap_values(transformed_data)

        if isinstance(shap_values, list):
            class_1_shap = shap_values[1]
        elif len(shap_values.shape) == 3:
            class_1_shap = shap_values[:, :, 1]
        else:
            class_1_shap = shap_values

        mean_abs_shap = np.mean(np.abs(class_1_shap), axis=0)

        df_importance = (
            pd.DataFrame(
                {
                    "feature": self.feature_names,
                    "mean_shap_value": mean_abs_shap,
                }
            )
            .sort_values("mean_shap_value", ascending=False)
            .head(top_k)
        )

        return df_importance
