import sys
from pathlib import Path
from typing import Dict, Any, Optional

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset

from src.data.loader import load_raw_data

DOCS_DIR = PROJECT_ROOT / "docs"
DEFAULT_DRIFT_HTML_PATH = DOCS_DIR / "data_drift_report.html"


def generate_drift_report(
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    output_html_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Génère un rapport Evidently AI comparant la distribution des données de référence
    et des données actuelles/production (Compétence D-06).
    """
    output_path = output_html_path or DEFAULT_DRIFT_HTML_PATH
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cols_to_exclude = ["customerID"]
    ref = reference_data.drop(
        columns=[c for c in cols_to_exclude if c in reference_data.columns]
    )
    curr = current_data.drop(
        columns=[c for c in cols_to_exclude if c in current_data.columns]
    )

    # Initialisation et exécution du rapport de drift Evidently
    report = Report(
        metrics=[
            DataDriftPreset(),
        ]
    )

    snapshot = report.run(reference_data=ref, current_data=curr)

    # Export HTML interactif pour la documentation et consultation métier
    snapshot.save_html(str(output_path))

    # Récupération des résultats
    report_dict = snapshot.dict()

    # Extraction des métriques clés synthétiques
    metrics_data = report_dict.get("metric_results", {})
    drift_share = 0.0
    number_of_drifted_columns = 0
    dataset_drift = False

    if isinstance(metrics_data, dict):
        for metric_id, res in metrics_data.items():
            if isinstance(res, dict):
                if "dataset_drift" in res:
                    dataset_drift = bool(res.get("dataset_drift", False))
                if "drift_share" in res:
                    drift_share = float(res.get("drift_share", 0.0))
                if "number_of_drifted_columns" in res:
                    number_of_drifted_columns = int(
                        res.get("number_of_drifted_columns", 0)
                    )

    summary = {
        "dataset_drift_detected": dataset_drift,
        "drift_share": drift_share,
        "number_of_drifted_columns": number_of_drifted_columns,
        "report_path": str(output_path),
    }

    return summary


def run_drift_analysis() -> Dict[str, Any]:
    """Exécute l'analyse de drift en utilisant la séparation Train/Test comme base de référence."""
    data = load_raw_data()
    # Séparation 80/20 pour simuler Données d'entraînement (Ref) vs Données de production (Current)
    ref_df = data.iloc[: int(len(data) * 0.8)]
    curr_df = data.iloc[int(len(data) * 0.8) :]

    summary = generate_drift_report(ref_df, curr_df)
    return summary


if __name__ == "__main__":
    summary = run_drift_analysis()
    print("=== Rapport de Data Drift (Evidently AI - D-06) ===")
    print(f"Dérive globale détectée : {summary['dataset_drift_detected']}")
    print(f"Part de colonnes en dérive : {summary['drift_share']:.1%}")
    print(f"Nombre de colonnes en dérive : {summary['number_of_drifted_columns']}")
    print(f"Rapport HTML sauvegardé dans : {summary['report_path']}")
