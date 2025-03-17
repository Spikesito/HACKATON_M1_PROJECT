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

st.title("Statistiques Réseau")
st.write("Vue d'ensemble des statistiques et indicateurs clés du réseau.")

# Filtres de période
periode_filter = st.radio("Période", ["Aujourd'hui", "Cette semaine", "Ce mois"], horizontal=True)

# Dataset simulé avec comparaison des périodes
data_stats = {
    "Aujourd'hui": {"Connexions Totales": 1245, "Connexions Suspectes": 3.2, "Connexions Actives": 42, "Anomalies Détectées": 8,
                    "Evolution": {"Connexions Totales": 8, "Connexions Suspectes": 0.3, "Connexions Actives": -1, "Anomalies Détectées": -1}},
    "Cette semaine": {"Connexions Totales": 8923, "Connexions Suspectes": 4.1, "Connexions Actives": 389, "Anomalies Détectées": 52,
                      "Evolution": {"Connexions Totales": 12, "Connexions Suspectes": -0.1, "Connexions Actives": 5, "Anomalies Détectées": -3}},
    "Ce mois": {"Connexions Totales": 35214, "Connexions Suspectes": 3.8, "Connexions Actives": 1512, "Anomalies Détectées": 197,
                 "Evolution": {"Connexions Totales": -5, "Connexions Suspectes": 0.2, "Connexions Actives": -15, "Anomalies Détectées": 2}}
}

data_selected = data_stats[periode_filter]
evolution = data_selected["Evolution"]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Connexions Totales", f"{data_selected['Connexions Totales']}", f"{evolution['Connexions Totales']}%", delta_color="inverse" if evolution['Connexions Totales'] < 0 else "normal")
col2.metric("Connexions Suspectes", f"{data_selected['Connexions Suspectes']}%", f"{evolution['Connexions Suspectes']}%", delta_color="inverse" if evolution['Connexions Suspectes'] < 0 else "normal")
col3.metric("Connexions Actives", f"{data_selected['Connexions Actives']}", f"{evolution['Connexions Actives']}", delta_color="inverse" if evolution['Connexions Actives'] < 0 else "normal")
col4.metric("Anomalies Détectées", f"{data_selected['Anomalies Détectées']}", f"{evolution['Anomalies Détectées']}", delta_color="inverse" if evolution['Anomalies Détectées'] < 0 else "normal")

# Graphiques
data_activity = {
    "Heure": ["00:00", "06:00", "12:00", "18:00"],
    "HTTPS": [120, 140, 160, 130],
    "HTTP": [80, 85, 100, 95],
    "DNS": [30, 35, 40, 38],
    "SSH": [10, 15, 12, 14]
}
df_activity = pd.DataFrame(data_activity)
fig = px.line(df_activity, x="Heure", y=["HTTPS", "HTTP", "DNS", "SSH"], title="Activité Réseau")
st.plotly_chart(fig, use_container_width=True)

# Répartition des protocoles
protocols = {"Protocoles": ["HTTPS", "HTTP", "DNS", "SSH", "Autres"], "%": [45, 25, 15, 10, 5]}
df_protocols = pd.DataFrame(protocols)
fig_pie = px.pie(df_protocols, names="Protocoles", values="%", title="Répartition des Protocoles")
st.plotly_chart(fig_pie, use_container_width=True)