import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.header("🗂️ Documentation API", divider="orange")

# Sidebar
st.sidebar.title("NetMonitor")
st.sidebar.markdown("""
Dans ce projet de Hackathon, nous avons développé une application de surveillance de réseau appelée NetMonitor.
- 📊 Tableau de bord
- 🚨 Anomalies
- 📈 Prédictions
- 📝 Documentation API

Participants :
 - Adam AHMAT
 - Mathys POINTARD
 - Melvin MIAUX
 - Guillaume CRISTINI
 - Emile SEGURET
""")

components.iframe("http://localhost:8000/docs", height=600, scrolling=True)