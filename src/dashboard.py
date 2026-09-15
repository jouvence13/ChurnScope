from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
OUTPUT_PATH = PROJECT_ROOT / "docs" / "dashboard_churn.html"


def load_data():
    data = pd.read_csv(DATA_PATH)
    data["TotalCharges"] = pd.to_numeric(
        data["TotalCharges"].replace(r"^\s*$", pd.NA, regex=True),
        errors="coerce",
    )
    data["ChurnLabel"] = data["Churn"].map({"No": "Resté", "Yes": "Parti"})
    return data


def churn_rate_by(data, column):
    return (
        data.groupby(column)["Churn"]
        .apply(lambda values: (values == "Yes").mean() * 100)
        .sort_values()
        .round(2)
    )


def build_dashboard(data):
    churn_rate = (data["Churn"] == "Yes").mean() * 100
    average_monthly = data["MonthlyCharges"].mean()
    median_tenure = data["tenure"].median()

    contract_rates = churn_rate_by(data, "Contract")
    payment_rates = churn_rate_by(data, "PaymentMethod")
    churn_counts = data["ChurnLabel"].value_counts().reindex(["Resté", "Parti"])

    figure = make_subplots(
        rows=3,
        cols=2,
        specs=[
            [{"type": "indicator"}, {"type": "indicator"}],
            [{"type": "indicator"}, {"type": "pie"}],
            [{"type": "bar"}, {"type": "bar"}],
        ],
        subplot_titles=(
            "Taux de churn",
            "Facture mensuelle moyenne",
            "Ancienneté médiane",
            "Répartition des clients",
            "Churn selon le contrat",
            "Churn selon le moyen de paiement",
        ),
        vertical_spacing=0.12,
    )

    figure.add_trace(
        go.Indicator(
            mode="number",
            value=churn_rate,
            number={"suffix": "%", "valueformat": ".1f"},
            title={"text": "Clients partis"},
        ),
        row=1,
        col=1,
    )
    figure.add_trace(
        go.Indicator(
            mode="number",
            value=average_monthly,
            number={"prefix": "€ ", "valueformat": ".2f"},
            title={"text": "Montant moyen"},
        ),
        row=1,
        col=2,
    )
    figure.add_trace(
        go.Indicator(
            mode="number",
            value=median_tenure,
            number={"suffix": " mois", "valueformat": ".0f"},
            title={"text": "Ancienneté"},
        ),
        row=2,
        col=1,
    )
    figure.add_trace(
        go.Pie(
            labels=churn_counts.index,
            values=churn_counts.values,
            marker={"colors": ["#2a9d8f", "#e76f51"]},
            hole=0.45,
        ),
        row=2,
        col=2,
    )
    figure.add_trace(
        go.Bar(
            x=contract_rates.index,
            y=contract_rates.values,
            marker_color="#264653",
            text=contract_rates.values,
            texttemplate="%{text:.1f}%",
            textposition="outside",
        ),
        row=3,
        col=1,
    )
    figure.add_trace(
        go.Bar(
            x=payment_rates.index,
            y=payment_rates.values,
            marker_color="#e9c46a",
            text=payment_rates.values,
            texttemplate="%{text:.1f}%",
            textposition="outside",
        ),
        row=3,
        col=2,
    )

    figure.update_yaxes(title_text="Taux de churn (%)", row=3, col=1)
    figure.update_yaxes(title_text="Taux de churn (%)", row=3, col=2)
    figure.update_layout(
        title="ChurnScope | Tableau de bord du churn client",
        template="plotly_white",
        height=950,
        showlegend=False,
        margin={"l": 60, "r": 40, "t": 90, "b": 80},
    )
    return figure


def main():
    data = load_data()
    dashboard = build_dashboard(data)
    dashboard.write_html(OUTPUT_PATH, include_plotlyjs=True)
    print(f"Dashboard généré : {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
