import streamlit as st
import pandas as pd
import requests

# API URL
API_URL = "http://backend:8000/data/filter"

# Sidebar
st.sidebar.title("NetMonitor")
st.sidebar.markdown("""
- 📊 Tableau de bord
- 🔍 Connexions
- 🚨 Anomalies
- 📈 Statistiques
- 📝 Logs & Historique
""")

st.title("Logs & Historique")
st.write("Journal des événements réseau pour audit et analyse post-incident.")

# Filtres avancés
with st.expander("Filtres avancés"):
    col1, col2 = st.columns(2)
    service_filter = col1.selectbox("Service", ["Tous", "http", "ftp", "dns", "smtp", "ssh"])
    ip_filter = col2.text_input("Adresse IP", placeholder="Filtrer par IP")
    st.button("Appliquer les filtres")

# Requête API pour récupérer les données filtrées
params = {}
if service_filter != "Tous":
    params["service"] = service_filter
if ip_filter:
    params["src_bytes"] = ip_filter  # Remplacé pour correspondre aux colonnes du dataset

response = requests.get(API_URL, params=params)
if response.status_code == 200:
    data_logs = pd.DataFrame(response.json())
else:
    st.error("Erreur lors de la récupération des logs depuis l'API.")
    data_logs = pd.DataFrame()

# Pagination des logs
if not data_logs.empty:
    page_size = 10
    total_pages = len(data_logs) // page_size + (1 if len(data_logs) % page_size > 0 else 0)
    page = st.slider("Page", 1, total_pages, 1)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    st.dataframe(data_logs.iloc[start_idx:end_idx])
else:
    st.write("Aucun log disponible.")

# Exportation des logs
st.button("📥 Exporter les logs")