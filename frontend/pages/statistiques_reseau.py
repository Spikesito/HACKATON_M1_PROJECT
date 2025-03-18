import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# API URL
API_URL = "http://localhost:8000/data/filter"

# Sidebar
st.sidebar.title("NetMonitor")
st.sidebar.markdown("""
- 📊 Tableau de bord
- 🔍 Connexions
- 🚨 Anomalies
- 📈 Statistiques
- 📝 Logs & Historique
""")

st.title("Statistiques Réseau")
st.write("Vue d'ensemble des statistiques et indicateurs clés du réseau.")

# Requête API pour récupérer les statistiques
response = requests.get(API_URL)
if response.status_code == 200:
    data_selected = response.json()
else:
    st.error("Erreur lors de la récupération des statistiques depuis l'API.")
    data_selected = {}

evolution = data_selected.get("Evolution", {})

col1, col2, col3 = st.columns(3)
col1.metric("Connexions Totales", f"{data_selected.get('Connexions Totales', 0)}", delta_color="inverse" if evolution.get('Connexions Totales', 0) < 0 else "normal")
col2.metric("Connexions Suspectes", f"{data_selected.get('Connexions Suspectes', 0)}", delta_color="inverse" if evolution.get('Connexions Suspectes', 0) < 0 else "normal")
col3.metric("Anomalies Détectées", f"{data_selected.get('Anomalies Détectées', 0)}", delta_color="inverse" if evolution.get('Anomalies Détectées', 0) < 0 else "normal")

# Graphiques
response = requests.get(f"{API_URL}/activity")
if response.status_code == 200:
    df_activity = pd.DataFrame(response.json())
    fig = px.bar(df_activity, x="protocol_type", y="Connexions", title="Activité Réseau")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Erreur lors de la récupération des données d'activité réseau.")

# Répartition des protocoles
response = requests.get(f"{API_URL}/protocols")
if response.status_code == 200:
    df_protocols = pd.DataFrame(response.json())
    fig_pie = px.pie(df_protocols, names="Protocoles", values="%", title="Répartition des Protocoles")
    st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.error("Erreur lors de la récupération des données de protocoles.")