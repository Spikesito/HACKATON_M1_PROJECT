import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# API URLs
API_URL_FILTER = "http://backend:8000/data/filter"
API_URL_LABELS = "http://backend:8000/stats/labels"

# Sidebar
st.sidebar.title("NetMonitor")
st.sidebar.markdown("""
Dans ce projet de Hackathon, nous avons développé une application de surveillance de réseau appelée NetMonitor.
- 📊 Tableau de bord
- 🚨 Anomalies
- 📈 Prédictions
- 📝 Documentation API

Participants :
 - Adam AHMAT
 - Mathys POINTARD
 - Melvin MIAUX
 - Guillaume CRISTINI
 - Emile SEGURET
""")

st.title("Détection d'Anomalies")
st.write("Visualisez les anomalies détectées par l'agent de Machine Learning.")

# Requête API pour récupérer les données filtrées
response = requests.get(API_URL_FILTER)
if response.status_code == 200:
    data = pd.DataFrame(response.json())
else:
    st.error("Erreur lors de la récupération des données depuis l'API.")
    data = pd.DataFrame()

# Vérification de la présence des données
if not data.empty:
    # Grouper par protocole, service et label
    grouped_data = data.groupby(["protocol_type", "service", "label"]).size().reset_index(name="Nombre d'occurrences")

    # Sélecteur de type d'anomalie
    unique_anomalies = data["label"].unique().tolist()
    unique_anomalies.insert(0, "Toutes")
    selected_anomaly = st.selectbox("Filtrer par type d'anomalie", unique_anomalies)

    # Filtrage des données
    if selected_anomaly != "Toutes":
        grouped_data = grouped_data[grouped_data["label"] == selected_anomaly]

    # Affichage du tableau groupé avec pagination
    page_size = 10
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
    st.write("Aucune donnée disponible.")

# 📊 **Histogramme et Pie Chart de la répartition des anomalies**
st.subheader("Répartition des connexions anormales par type")

if not data.empty:
    anomaly_data = data[data["label"] != "normal"]

    if not anomaly_data.empty:
        anomaly_counts = anomaly_data["label"].value_counts().reset_index()
        anomaly_counts.columns = ["Type d'anomalie", "Nombre"]

        # Pie Chart
        fig_pie = px.pie(
            anomaly_counts, 
            names="Type d'anomalie", 
            values="Nombre", 
            title="Proportion des types d'anomalies",
            color="Type d'anomalie"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    else:
        st.write("Aucune anomalie détectée dans les données filtrées.")
else:
    st.write("Aucune donnée à afficher pour les graphiques.")
