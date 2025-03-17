import streamlit as st
import pandas as pd

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
st.expander("Filtres avancés")
col1, col2, col3 = st.columns(3)
col1.selectbox("Type d'événement", ["Tous", "Connexion établie", "Requête DNS", "Connexion suspecte"])
col2.text_input("Adresse IP", placeholder="Filtrer par IP")
col3.date_input("Date")
st.button("Appliquer les filtres")

# Journal des événements
data_logs = pd.DataFrame({
    "Horodatage": ["2023-03-15 14:32:45", "2023-03-15 14:35:01", "2023-03-15 14:40:12"],
    "IP": ["192.168.1.105", "45.33.12.186", "203.0.113.42"],
    "Événement": ["Connexion établie", "Tentative de connexion SSH", "Scan de ports"],
    "Détails": ["HTTPS vers 216.58.215.110", "SSH depuis IP suspecte", "Scan séquentiel de ports"],
    "Type": ["Normal", "Suspect", "Suspect"]
})
st.dataframe(data_logs)

# Exportation des logs
st.button("📥 Exporter les logs")
