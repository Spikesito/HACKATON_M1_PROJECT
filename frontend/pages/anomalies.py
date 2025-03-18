import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# API URL
API_URL = "http://backend:8000/data/filter"


try:
    response = requests.get(API_URL)
    print(f"Status Code: {response.status_code}")
    print(response.text)  # Afficher la réponse brute pour voir l'erreur exacte
except requests.exceptions.RequestException as e:
    print("Erreur de connexion :", e)
    
# Sidebar
st.sidebar.title("NetMonitor")
st.sidebar.markdown("""
- 📊 Tableau de bord
- 🔍 Connexions
- 🚨 Anomalies
- 📈 Statistiques
- 📝 Logs & Historique
""")

st.title("Détection d'Anomalies")
st.write("Visualisez les anomalies détectées par l'agent de Machine Learning.")

# Filtres par label (normal ou anomalie)
label_filter = st.radio("Filtrer par type d'anomalie", ["Toutes", "anomaly", "normal"], horizontal=True)

# Requête API pour récupérer les données filtrées
params = {}
if label_filter != "Toutes":
    params["label"] = label_filter

response = requests.get(API_URL, params=params)
if response.status_code == 200:
    data = pd.DataFrame(response.json())
else:
    st.error("Erreur lors de la récupération des données depuis l'API.")
    data = pd.DataFrame()

# Pagination des données
if not data.empty:
    page_size = 10
    total_pages = len(data) // page_size + (1 if len(data) % page_size > 0 else 0)
    page = st.slider("Page", 1, total_pages, 1)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    st.dataframe(data.iloc[start_idx:end_idx])
else:
    st.write("Aucune donnée disponible.")

# Graphique des tendances des anomalies (Histogramme groupé)
st.subheader("Tendance des Anomalies")
if not data.empty:
    data_histogram = data.groupby(["label"]).size().reset_index(name="Nombre")
    
    fig = px.bar(data_histogram, x="label", y="Nombre", color="label", barmode="group",
                 labels={"label": "Type d'Anomalie", "Nombre": "Nombre d'anomalies"})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Aucune donnée à afficher pour le graphique.")

# Bouton d'exportation
st.button("📥 Exporter le rapport")