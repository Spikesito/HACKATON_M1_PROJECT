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

prediction = st.Page("pages/prediction.py", title="Prédiction", icon=":material/insights:")

# Pages Documentation
doc_api = st.Page("./pages/documentation_api.py", title="Documentation API", icon=":material/description:")

pg = st.navigation(
    {
        "📊 Monitoring et Surveillance": [dashboard],
        "🚨 Détection et Analyse des Anomalies": [anomalies, prediction],
        "📁 Documentation": [doc_api]
    }
)
pg.run()