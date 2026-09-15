from src.models.train import train_and_evaluate


def test_model_performance_benchmarks(tmp_path):
    """
    Test de non-régression de performance du modèle de Machine Learning.

    Vérifie que les performances sur le jeu de test respectent les seuils minimaux
    exigés par le cahier des charges et la stratégie métier de rétention.
    """
    model_tmp = tmp_path / "temp_model.joblib"
    preds_tmp = tmp_path / "temp_preds.csv"

    _, metrics, _ = train_and_evaluate(
        model_output_path=model_tmp,
        predictions_output_path=preds_tmp,
        random_state=42,
    )

    # 1. Le rappel (Recall) doit être supérieur ou égal à 75% pour minimiser les départs manqués
    assert (
        metrics["recall"] >= 0.75
    ), f"Le rappel churn ({metrics['recall']:.3f}) est inférieur au seuil minimal de 0.75"

    # 2. Le score ROC-AUC doit être supérieur ou égal à 0.80
    assert (
        metrics["roc_auc"] >= 0.80
    ), f"Le ROC-AUC ({metrics['roc_auc']:.3f}) est inférieur au seuil minimal de 0.80"

    # 3. L'Accuracy globale doit être supérieure ou égale à 70%
    assert (
        metrics["accuracy"] >= 0.70
    ), f"L'Accuracy ({metrics['accuracy']:.3f}) est inférieure au seuil minimal de 0.70"
