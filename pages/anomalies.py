import streamlit as st
import pandas as pd
import plotly.express as px

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

# Filtres par niveau de risque
risque_filter = st.radio("Filtrer par niveau de risque", ["Toutes", "Risque Élevé", "Risque Moyen", "Risque Faible"], horizontal=True)

# Table des anomalies détectées
data = pd.DataFrame({
    "Horodatage": ["2023-03-15 14:35:01", "2023-03-15 14:40:12", "2023-03-15 15:00:45"],
    "IP Source": ["45.33.12.186", "203.0.113.42", "198.51.100.123"],
    "IP Destination": ["192.168.1.1", "192.168.1.1", "192.168.1.105"],
    "Type": ["Tentative de connexion SSH", "Scan de ports", "Trafic HTTP suspect"],
    "Risque": ["Élevé", "Moyen", "Faible"]
})

if risque_filter != "Toutes":
    data = data[data["Risque"] == risque_filter.replace("Risque ", "")]

st.dataframe(data)

# Graphique des tendances des anomalies (Histogramme groupé)
st.subheader("Tendance des Anomalies")
data_histogram = pd.DataFrame({
    "Heure": ["00:00", "08:00", "12:00", "16:00", "00:00", "08:00", "12:00", "16:00", "00:00", "08:00", "12:00", "16:00"],
    "Nombre": [1, 3, 4, 2, 2, 5, 3, 1, 0, 1, 2, 3],
    "Risque": ["Élevé", "Élevé", "Élevé", "Élevé", "Moyen", "Moyen", "Moyen", "Moyen", "Faible", "Faible", "Faible", "Faible"]
})

if risque_filter != "Toutes":
    data_histogram = data_histogram[data_histogram["Risque"] == risque_filter.replace("Risque ", "")]

fig = px.bar(data_histogram, x="Heure", y="Nombre", color="Risque", barmode="group",
             labels={"Heure": "Heure", "Nombre": "Nombre d'anomalies", "Risque": "Niveau de Risque"})
st.plotly_chart(fig, use_container_width=True)

# Bouton d'exportation
st.button("📥 Exporter le rapport")
