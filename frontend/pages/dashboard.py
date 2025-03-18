import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

st.title("Surveillance Réseau")
st.write("Visualisez et analysez les connexions réseau en temps réel ou en mode replay.")

# Recherche et filtres
search_query = st.text_input("Recherche", placeholder="Rechercher par service, protocole...")
col1, col2 = st.columns(2)
protocole_filter = col1.selectbox("Protocole", ["Tous", "tcp", "udp", "icmp"])
service_filter = col2.selectbox("Service", ["Tous", "http", "ftp", "dns", "smtp", "ssh"])
st.button("Filtrer")

# Requête API pour récupérer les données filtrées
params = {}
if protocole_filter != "Tous":
    params["protocol_type"] = protocole_filter
if service_filter != "Tous":
    params["service"] = service_filter

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

# Graphique Activité Réseau avec anomalies
st.subheader("Activité Réseau")
if not data.empty:
    data_graph = data.groupby("protocol_type").agg({"label": "count", "flag": lambda x: (x == "SF").sum()}).reset_index()
    data_graph.columns = ["Protocole", "Connexions", "Anomalies"]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=data_graph["Protocole"], y=data_graph["Connexions"], name='Connexions', marker_color='blue'))
    fig.add_trace(go.Bar(x=data_graph["Protocole"], y=data_graph["Anomalies"], name='Anomalies', marker_color='red'))

    fig.update_layout(title="Flux de connexions et anomalies",
                      xaxis_title="Protocole",
                      yaxis_title="Nombre d'événements",
                      barmode='group')

    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Aucune donnée à afficher pour le graphique.")