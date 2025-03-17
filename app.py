import streamlit as st

# Initialize session state variables
# TODO

st.set_page_config(
    page_title="Hackaton App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

dashboard = st.Page("pages/dashboard.py", title="Tableau de bord", icon=":material/security:")

anomalies = st.Page("pages/anomalies.py", title="Anomalies", icon=":material/bug_report:")

statistiques_reseau = st.Page("pages/statistiques_reseau.py", title="Statistiques", icon=":material/insights:")

logs_historique = st.Page("pages/logs_historique.py", title="Logs & Historique", icon=":material/history:")

# Pages Documentation
doc_api = st.Page("./pages/documentation_api.py", title="Documentation API", icon=":material/description:")

pg = st.navigation(
    {
        "📊 Monitoring et Surveillance": [dashboard, statistiques_reseau],
        "🚨 Détection et Analyse des Anomalies": [anomalies, logs_historique],
        "📁 Documentation": [doc_api]
    }
)
pg.run()