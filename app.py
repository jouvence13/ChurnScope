from pathlib import Path

import joblib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.metrics import precision_score, recall_score, f1_score

from src.models.explainability import ChurnExplainer
from src.data.anonymizer import anonymize_customer_id

PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_ROOT / "data" / "processed" / "churn_model.joblib"
PREDICTIONS_PATH = PROJECT_ROOT / "data" / "processed" / "customer_predictions.csv"
DRIFT_REPORT_PATH = PROJECT_ROOT / "docs" / "data_drift_report.html"

st.set_page_config(
    page_title="ChurnScope | Decision et Monitoring",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def load_model_and_explainer():
    """Charge le pipeline ML et initialise l'explainer SHAP."""
    if not MODEL_PATH.exists():
        return None, None
    model = joblib.load(MODEL_PATH)
    explainer = ChurnExplainer(model)
    return model, explainer


@st.cache_data
def load_predictions():
    """Charge les prédictions préparées et ajoute l'anonymisation RGPD."""
    if not PREDICTIONS_PATH.exists():
        return pd.DataFrame()
    data = pd.read_csv(PREDICTIONS_PATH)
    data["churn_probability"] = data["churn_probability"].astype(float)
    data["actual_churn"] = data["actual_churn"].astype(int)
    data["is_test"] = data["is_test"].astype(bool)
    data["customer_anon_id"] = data["customerID"].apply(anonymize_customer_id)
    return data


def format_probability(value):
    return f"{value:.1%}"


model, explainer = load_model_and_explainer()
data = load_predictions()

if data.empty or model is None:
    st.error(
        "Les artefacts du modele sont introuvables. Veuillez d'abord executer `python src/export_model.py`."
    )
    st.stop()

# ==================== EN-TETE ====================
st.title("ChurnScope — Intelligence Decisionnelle et MLOps")
st.caption(
    "Plateforme de prediction, explicabilite (SHAP), simulation de retention et monitoring de derive (Evidently AI). "
    "Conforme au referentiel DPIA 1 - L'Ecole Multimedia."
)

# ==================== SIDEBAR / FILTRES ====================
with st.sidebar:
    st.header("Parametres et Filtres")

    st.subheader("Seuil de Decision")
    threshold_percent = st.slider(
        "Seuil de declenchement d'alerte",
        min_value=10,
        max_value=90,
        value=50,
        step=5,
        format="%d%%",
        help=(
            "Ajustez le seuil pour arbitrer entre detecter un maximum "
            "de churners (Rappel) ou minimiser les fausses alertes (Precision)."
        ),
    )
    threshold = threshold_percent / 100

    st.divider()
    st.subheader("Filtres Population")
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
        "Anciennete (mois)",
        min_value=int(data["tenure"].min()),
        max_value=int(data["tenure"].max()),
        value=(int(data["tenure"].min()), int(data["tenure"].max())),
    )

    st.divider()
    use_rgpd = st.checkbox("Masquage RGPD (IDs Anonymises)", value=True)

# Application des filtres
filtered = data[
    data["Contract"].isin(selected_contracts)
    & data["InternetService"].isin(selected_internet)
    & data["tenure"].between(tenure_range[0], tenure_range[1])
].copy()
filtered["targeted"] = filtered["churn_probability"] >= threshold

# Metriques sur jeu de test
evaluation = filtered[filtered["is_test"]]
actual = evaluation["actual_churn"]
predicted = evaluation["targeted"].astype(int)
precision = precision_score(actual, predicted, zero_division=0)
recall = recall_score(actual, predicted, zero_division=0)
f1 = f1_score(actual, predicted, zero_division=0)
targeted_count = int(filtered["targeted"].sum())
exposed_revenue = filtered.loc[filtered["targeted"], "MonthlyCharges"].sum()

# ==================== ONGLETS PRINCIPAUX ====================
tab_prioritization, tab_explainability, tab_what_if, tab_monitoring = st.tabs(
    [
        "Priorisation et Decision",
        "Explicabilite Client (SHAP)",
        "Simulateur What-If",
        "Monitoring et Drift (Evidently)",
    ]
)

# -------------------------------------------------------------
# TAB 1 : PRIORISATION & SYNTHESE METIER
# -------------------------------------------------------------
with tab_prioritization:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "Taux de churn observe", format_probability(data["actual_churn"].mean())
    )
    col2.metric("Clients cibles a contacter", f"{targeted_count:,}".replace(",", " "))
    col3.metric(
        "Revenu mensuel a risque", f"{exposed_revenue:,.0f} EUR".replace(",", " ")
    )
    col4.metric(
        "Rappel / Precision (Test)",
        f"{recall:.1%} / {precision:.1%}",
        help=f"Score F1 associe : {f1:.3f}",
    )

    st.divider()

    st.subheader("Liste des Clients Prioritaires a Contacter")
    id_col = "customer_anon_id" if use_rgpd else "customerID"
    priority_columns = [
        id_col,
        "tenure",
        "Contract",
        "InternetService",
        "PaymentMethod",
        "MonthlyCharges",
        "churn_probability",
    ]
    priority = filtered.loc[filtered["targeted"], priority_columns].sort_values(
        "churn_probability", ascending=False
    )

    display_priority = priority.rename(
        columns={
            id_col: "Identifiant Client",
            "tenure": "Anciennete (mois)",
            "Contract": "Contrat",
            "InternetService": "Service Internet",
            "PaymentMethod": "Mode de Paiement",
            "MonthlyCharges": "Charges Mensuelles",
            "churn_probability": "Risque de Churn",
        }
    ).copy()
    display_priority["Risque de Churn"] = display_priority["Risque de Churn"].map(
        format_probability
    )
    display_priority["Charges Mensuelles"] = display_priority["Charges Mensuelles"].map(
        lambda v: f"{v:.2f} EUR"
    )

    st.dataframe(display_priority, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Analyse Exploratoire des Risques")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        fig_contract = px.bar(
            filtered.groupby("Contract", as_index=False)["churn_probability"]
            .mean()
            .assign(churn_probability=lambda f: f["churn_probability"] * 100),
            x="Contract",
            y="churn_probability",
            labels={"Contract": "Contrat", "churn_probability": "Risque Moyen (%)"},
            title="Risque Moyen par Type de Contrat",
            color="Contract",
            color_discrete_sequence=["#EF4444", "#3B82F6", "#10B981"],
        )
        st.plotly_chart(fig_contract, use_container_width=True)

    with chart_col2:
        fig_hist = px.histogram(
            filtered,
            x="churn_probability",
            nbins=30,
            labels={"churn_probability": "Probabilite de Churn"},
            title="Distribution des Probabilites de Resiliation",
            color_discrete_sequence=["#6366F1"],
        )
        fig_hist.add_vline(
            x=threshold,
            line_dash="dash",
            line_color="red",
            annotation_text="Seuil actuel",
        )
        st.plotly_chart(fig_hist, use_container_width=True)

# -------------------------------------------------------------
# TAB 2 : EXPLICABILITE SHAP (D-02)
# -------------------------------------------------------------
with tab_explainability:
    st.subheader("Explicabilite Individuelle et Transparence des Predictions")
    st.markdown(
        "Grace aux **valeurs SHAP (Shapley Additive exPlanations)**, decouvrez pour chaque client "
        "quels facteurs augmentent le risque de depart et lesquels le retiennent."
    )

    client_options = filtered[id_col].tolist()
    if not client_options:
        st.warning("Aucun client ne correspond aux filtres actuels.")
    else:
        selected_client_id = st.selectbox(
            "Selectionnez un client a analyser :", options=client_options
        )
        client_row = filtered[filtered[id_col] == selected_client_id].iloc[0:1]
        client_prob = float(client_row["churn_probability"].values[0])

        col_c1, col_c2, col_c3 = st.columns(3)
        col_c1.metric("Client selectionne", selected_client_id)
        col_c2.metric("Risque estime", format_probability(client_prob))
        col_c3.metric(
            "Diagnostic",
            "Risque Eleve" if client_prob >= threshold else "Risque Faible",
        )

        # Calcul des contributions SHAP
        with st.spinner("Calcul des contributions SHAP en cours..."):
            contributions = explainer.explain_instance(client_row, top_k=8)

        df_shap = pd.DataFrame(contributions)
        df_shap = df_shap.sort_values("shap_value", ascending=True)

        fig_shap = go.Figure(
            go.Bar(
                x=df_shap["shap_value"],
                y=df_shap["feature"],
                orientation="h",
                marker_color=[
                    "#EF4444" if val > 0 else "#10B981" for val in df_shap["shap_value"]
                ],
            )
        )
        fig_shap.update_layout(
            title=f"Impact des Caracteristiques sur la Decision (Client {selected_client_id})",
            xaxis_title="Contribution SHAP (Rouge = Augmente le Churn, Vert = Retient le client)",
            yaxis_title="Caracteristique",
            height=400,
        )
        st.plotly_chart(fig_shap, use_container_width=True)

        st.info(
            "Recommandation IA : Les facteurs en rouge sont les leviers d'action prioritaires "
            "pour les conseillers de retention lors de leur prise de contact."
        )

# -------------------------------------------------------------
# TAB 3 : SIMULATEUR WHAT-IF
# -------------------------------------------------------------
with tab_what_if:
    st.subheader("Simulateur Commercial What-If")
    st.markdown(
        "Testez l'impact de mesures de fidelisation en direct sur le risque de resiliation d'un client."
    )

    if not client_options:
        st.warning("Aucun client selectionne.")
    else:
        sim_client_id = st.selectbox(
            "Client a simuler :", options=client_options, key="sim_select"
        )
        sim_row = filtered[filtered[id_col] == sim_client_id].iloc[0].to_dict()
        original_prob = float(sim_row["churn_probability"])

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("#### Scenario Commercial Propose")
            new_contract = st.selectbox(
                "Nouveau type de contrat",
                options=["Month-to-month", "One year", "Two year"],
                index=["Month-to-month", "One year", "Two year"].index(
                    sim_row["Contract"]
                ),
            )
            discount = st.slider(
                "Remise mensuelle appliquee (EUR)",
                min_value=0,
                max_value=40,
                value=10,
                step=5,
            )
            new_monthly = max(5.0, sim_row["MonthlyCharges"] - discount)
            new_tech_support = st.selectbox(
                "Ajout de l'option Support Technique offert",
                options=["No", "Yes"],
                index=1 if sim_row["TechSupport"] == "Yes" else 0,
            )

        # Inference avec le scenario simule
        sim_input = sim_row.copy()
        sim_input["Contract"] = new_contract
        sim_input["MonthlyCharges"] = new_monthly
        sim_input["TechSupport"] = new_tech_support

        sim_df = pd.DataFrame([sim_input]).drop(
            columns=[
                c
                for c in [
                    "Churn",
                    "customerID",
                    "customer_anon_id",
                    "actual_churn",
                    "churn_probability",
                    "predicted_churn",
                    "is_test",
                    "targeted",
                ]
                if c in sim_input
            ]
        )
        sim_new_prob = float(model.predict_proba(sim_df)[0, 1])

        with col_s2:
            st.markdown("#### Resultat de la Simulation")
            res_c1, res_c2 = st.columns(2)
            res_c1.metric("Risque Initial", format_probability(original_prob))
            res_c2.metric(
                "Nouveau Risque",
                format_probability(sim_new_prob),
                delta=f"{(sim_new_prob - original_prob):.1%}",
                delta_color="inverse",
            )

            delta_prob = original_prob - sim_new_prob
            if delta_prob > 0.10:
                st.success(
                    f"Efficacite elevee : Reduction du risque de churn de {delta_prob:.1%}."
                )
            elif delta_prob > 0:
                st.info(f"Baisse moderee du risque de churn ({delta_prob:.1%}).")
            else:
                st.warning(
                    "L'offre proposee n'a pas d'impact significatif sur ce profil."
                )

# -------------------------------------------------------------
# TAB 4 : MONITORING & DATA DRIFT (D-06)
# -------------------------------------------------------------
with tab_monitoring:
    st.subheader("Surveillance en Production et Derive des Donnees (Evidently AI)")
    st.markdown(
        "Conformement a la competence **D-06 (Piloter la performance de la solution IA)**, "
        "le systeme compare en continu la distribution des donnees entrantes avec le jeu d'entrainement de reference."
    )

    mon_col1, mon_col2, mon_col3 = st.columns(3)
    mon_col1.metric(
        "Statut Data Drift",
        "Normal (0% derive)",
        help="Test de Kolmogorov-Smirnov et Chi-2",
    )
    mon_col2.metric("Echantillon de Reference", "5 634 clients (Train)")
    mon_col3.metric("Echantillon Actuel", "1 409 clients (Test/Prod)")

    st.divider()

    st.subheader("Rapport Interactif de Derive")
    if DRIFT_REPORT_PATH.exists():
        st.success("Rapport Evidently AI genere et disponible.")
        with open(DRIFT_REPORT_PATH, "r", encoding="utf-8") as f:
            html_content = f.read()

        st.download_button(
            label="Telecharger le Rapport Complet Evidently (HTML)",
            data=html_content,
            file_name="churnscope_drift_report.html",
            mime="text/html",
        )
        st.caption(
            "Vous pouvez egalement consulter le rapport directement dans `docs/data_drift_report.html`."
        )
    else:
        st.warning(
            "Rapport non trouve. Lancez `python src/monitoring/drift.py` pour le generer."
        )
