import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
search_query = st.text_input("Recherche", placeholder="Rechercher par IP, port...")
col1, col2, col3 = st.columns(3)
protocole_filter = col1.selectbox("Protocole", ["Tous", "HTTP", "HTTPS", "DNS", "SSH"])
statut_filter = col2.selectbox("Statut", ["Tous", "Normal", "Suspect"])
periode_filter = col3.selectbox("Période", ["Dernière heure", "Aujourd'hui", "Cette semaine"])  
st.button("Filtrer")

# Table des connexions réseau
data = pd.DataFrame({
    "Horodatage": ["2023-03-15 14:32:45", "2023-03-15 14:35:01", "2023-03-15 14:36:22"],
    "Source": ["192.168.1.105:54321", "45.33.12.186:22", "192.168.1.105:54324"],
    "Destination": ["216.58.215.110:443", "192.168.1.1:22345", "104.244.42.65:443"],
    "Protocole": ["HTTPS", "SSH", "HTTPS"],
    "Durée": ["00:02:15", "00:05:22", "00:01:30"],
    "Statut": ["Normal", "Suspect", "Normal"]
})

if protocole_filter != "Tous":
    data = data[data["Protocole"] == protocole_filter]
if statut_filter != "Tous":
    data = data[data["Statut"] == statut_filter]
if search_query:
    data = data[data.apply(lambda row: search_query.lower() in row.to_string().lower(), axis=1)]

st.dataframe(data)

# Graphique Activité Réseau avec anomalies
st.subheader("Activité Réseau")
data_graph = pd.DataFrame({
    "Heure": ["14:30", "14:35", "14:40", "14:45", "14:50"],
    "Connexions": [9, 18, 27, 36, 30],
    "Anomalies": [0, 2, 4, 5, 3]
})

fig = go.Figure()

# Ajout des connexions
fig.add_trace(go.Scatter(x=data_graph["Heure"], y=data_graph["Connexions"], mode='lines', fill='tozeroy',
                         name='Connexions', line=dict(color='blue')))

# Ajout des anomalies
fig.add_trace(go.Scatter(x=data_graph["Heure"], y=data_graph["Anomalies"], mode='lines', fill='tozeroy',
                         name='Anomalies', line=dict(color='red')))

# Mise en forme des axes
fig.update_layout(title="Flux de connexions et anomalies",
                  xaxis_title="Heure",
                  yaxis_title="Nombre d'événements",
                  hovermode="x unified")

st.plotly_chart(fig, use_container_width=True)