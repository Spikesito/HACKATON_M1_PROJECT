import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# API URLs
API_URL_LABELS = "http://backend:8000/stats/labels"

# Sidebar
st.sidebar.title("NetMonitor")
st.sidebar.markdown("""
Dans ce projet de Hackathon, nous avons développé une application de surveillance de réseau appelée NetMonitor.
- 📊 **Tableau de bord**
- 🚨 **Détection d'anomalies**
- 🤖 **Prédictions du modèle**
- 📈 **Statistiques réseau**
""")

st.title("🚨 Analyse des Anomalies")
st.write("Visualisez les différentes anomalies détectées sur le réseau.")

# 📡 **Requête API pour récupérer les anomalies groupées**
st.subheader("📡 Récupération des données...")
response = requests.get(API_URL_LABELS)

if response.status_code == 200:
    data = pd.DataFrame(response.json())
else:
    st.error("❌ Erreur lors de la récupération des données depuis l'API.")
    data = pd.DataFrame()

# 📋 **Affichage du tableau des anomalies**
if not data.empty:
    st.subheader("📋 Détails des Anomalies")

    # Sélecteur de type d'anomalie
    unique_anomalies = data["label"].unique().tolist()
    unique_anomalies.insert(0, "Toutes")
    selected_anomaly = st.selectbox("Filtrer par type d'anomalie", unique_anomalies)

    # Filtrage des données
    if selected_anomaly != "Toutes":
        data = data[data["label"] == selected_anomaly]

    # 📊 Grouper les données
    grouped_data = data.groupby(["protocol_type", "service", "label"]).sum().reset_index()

    # 📋 Pagination
    page_size = 50
    total_pages = (len(grouped_data) // page_size) + (1 if len(grouped_data) % page_size > 0 else 0)

    if "page" not in st.session_state:
        st.session_state.page = 1

    col1, col2, col3 = st.columns([1, 4, 1])

    with col1:
        if st.session_state.page > 1:
            if st.button("⬅️ Précédent"):
                st.session_state.page -= 1

    with col3:
        if st.session_state.page < total_pages:
            if st.button("Suivant ➡️"):
                st.session_state.page += 1

    start_idx = (st.session_state.page - 1) * page_size
    end_idx = start_idx + page_size

    st.dataframe(grouped_data.iloc[start_idx:end_idx])
else:
    st.write("⚠️ Aucune anomalie détectée.")

# 📊 **Histogramme des anomalies par protocole**
st.subheader("📊 Répartition des Anomalies par Protocole")

if not data.empty:
    fig_protocol = px.bar(
        data,
        x="protocol_type",
        y="count",
        color="label",
        title="Nombre d'Anomalies par Protocole",
        labels={"protocol_type": "Protocole", "count": "Nombre d'anomalies"},
        barmode="group"
    )
    st.plotly_chart(fig_protocol, use_container_width=True)

# 📊 **Pie Chart des anomalies par service**
st.subheader("📊 Répartition des Anomalies par Service")

if not data.empty:
    fig_service = px.pie(
        data,
        names="service",
        values="count",
        title="Répartition des Anomalies par Service",
        color="service"
    )
    st.plotly_chart(fig_service, use_container_width=True)
