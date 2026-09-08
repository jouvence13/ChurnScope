from pathlib import Path

import joblib
import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.metrics import precision_score, recall_score


PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_ROOT / "data" / "processed" / "churn_model.joblib"
PREDICTIONS_PATH = PROJECT_ROOT / "data" / "processed" / "customer_predictions.csv"

st.set_page_config(
    page_title="ChurnScope | Priorisation des clients",
    page_icon="📊",
    layout="wide",
)


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


@st.cache_data
def load_predictions():
    data = pd.read_csv(PREDICTIONS_PATH)
    data["churn_probability"] = data["churn_probability"].astype(float)
    data["actual_churn"] = data["actual_churn"].astype(int)
    data["is_test"] = data["is_test"].astype(bool)
    return data


def format_probability(value):
    return f"{value:.1%}"


model = load_model()
data = load_predictions()

st.title("ChurnScope")
st.subheader("Prioriser les clients à contacter cette semaine")
st.caption(
    "Les probabilités proviennent du Random Forest optimisé. Ajustez le seuil "
    "pour choisir l'équilibre entre clients détectés et fausses alertes."
)

with st.sidebar:
    st.header("Filtres")
    selected_contracts = st.multiselect(
        "Type de contrat",
        options=sorted(data["Contract"].dropna().unique()),
        default=sorted(data["Contract"].dropna().unique()),
    )
    selected_internet = st.multiselect(
        "Service internet",
        options=sorted(data["InternetService"].dropna().unique()),
        default=sorted(data["InternetService"].dropna().unique()),
    )
    tenure_range = st.slider(
        "Ancienneté (mois)",
        min_value=int(data["tenure"].min()),
        max_value=int(data["tenure"].max()),
        value=(int(data["tenure"].min()), int(data["tenure"].max())),
    )
    threshold = st.slider(
        "Seuil de probabilité",
        min_value=0.10,
        max_value=0.90,
        value=0.50,
        step=0.05,
        format="%.0f%%",
    )

filtered = data[
    data["Contract"].isin(selected_contracts)
    & data["InternetService"].isin(selected_internet)
    & data["tenure"].between(tenure_range[0], tenure_range[1])
].copy()
filtered["targeted"] = filtered["churn_probability"] >= threshold

evaluation = filtered[filtered["is_test"]]
actual = evaluation["actual_churn"]
predicted = evaluation["targeted"].astype(int)
precision = precision_score(actual, predicted, zero_division=0)
recall = recall_score(actual, predicted, zero_division=0)
targeted_count = int(filtered["targeted"].sum())
exposed_revenue = filtered.loc[filtered["targeted"], "MonthlyCharges"].sum()

metric_columns = st.columns(4)
metric_columns[0].metric(
    "Taux de churn global",
    format_probability(data["actual_churn"].mean()),
)
metric_columns[1].metric(
    "Clients à contacter",
    f"{targeted_count:,}".replace(",", " "),
)
metric_columns[2].metric(
    "Revenu mensuel exposé",
    f"{exposed_revenue:,.0f} €".replace(",", " "),
)
metric_columns[3].metric(
    "Rappel / précision (test)",
    f"{recall:.1%} / {precision:.1%}",
)

st.divider()

st.header("Liste prioritaire")
priority_columns = [
    "customerID",
    "tenure",
    "Contract",
    "InternetService",
    "MonthlyCharges",
    "churn_probability",
]
priority = filtered.loc[filtered["targeted"], priority_columns].sort_values(
    "churn_probability", ascending=False
)
priority = priority.rename(
    columns={
        "customerID": "Client",
        "tenure": "Ancienneté (mois)",
        "Contract": "Contrat",
        "InternetService": "Internet",
        "MonthlyCharges": "Charges mensuelles",
        "churn_probability": "Probabilité de churn",
    }
)
priority["Probabilité de churn"] = priority["Probabilité de churn"].map(format_probability)
priority["Charges mensuelles"] = priority["Charges mensuelles"].map(lambda value: f"{value:.2f} €")
st.dataframe(priority, use_container_width=True, hide_index=True)

st.divider()

st.header("Explorer les signaux")
chart_columns = st.columns(3)

segment = (
    filtered.groupby("Contract", as_index=False)["actual_churn"]
    .mean()
    .assign(actual_churn=lambda frame: frame["actual_churn"] * 100)
)
segment_chart = px.bar(
    segment,
    x="Contract",
    y="actual_churn",
    labels={"Contract": "Contrat", "actual_churn": "Taux de churn (%)"},
    title="Taux de churn par contrat",
    color="actual_churn",
    color_continuous_scale="Tealgrn",
)
chart_columns[0].plotly_chart(segment_chart, use_container_width=True)

probability_chart = px.histogram(
    filtered,
    x="churn_probability",
    color="targeted",
    nbins=20,
    labels={
        "churn_probability": "Probabilité de churn",
        "targeted": "À contacter",
    },
    title="Distribution des probabilités",
    color_discrete_map={True: "#e76f51", False: "#2a9d8f"},
)
probability_chart.update_xaxes(tickformat=".0%")
chart_columns[1].plotly_chart(probability_chart, use_container_width=True)

preprocessor = model.named_steps["preprocessor"]
classifier = model.named_steps["classifier"]
feature_names = preprocessor.get_feature_names_out()
importance = pd.DataFrame(
    {"Variable": feature_names, "Importance": classifier.feature_importances_}
).sort_values("Importance", ascending=False).head(12)
importance["Variable"] = (
    importance["Variable"]
    .str.replace("numeric__", "", regex=False)
    .str.replace("categorical__", "", regex=False)
)
importance_chart = px.bar(
    importance.sort_values("Importance"),
    x="Importance",
    y="Variable",
    orientation="h",
    title="Variables les plus importantes",
    labels={"Importance": "Importance", "Variable": "Variable"},
    color="Importance",
    color_continuous_scale="Sunset",
)
chart_columns[2].plotly_chart(importance_chart, use_container_width=True)

st.caption(
    "Le seuil ne constitue pas une décision automatique : il sert à prioriser "
    "les actions de rétention et doit être associé à une analyse des coûts."
)
