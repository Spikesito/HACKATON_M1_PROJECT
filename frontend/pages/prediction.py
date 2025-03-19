import streamlit as st
import requests
import pandas as pd

# API URL (modifiez selon votre configuration)
API_URL = "http://backend:8000/predict_csv"


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

st.subheader("Importer un fichier CSV pour analyse")
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])

# Bouton pour lancer la prédiction
if uploaded_file is not None:
    if st.button("Analyser les données"):
        try:
            # Lire le fichier et l'envoyer à l'API
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
            response = requests.post(API_URL, files=files)

            # Vérifier la réponse de l'API
            if response.status_code == 200:
                results = response.json()["predictions"]
                
                # Convertir les résultats en DataFrame
                df_results = pd.DataFrame(results)
                
                # Affichage des résultats
                st.subheader("📊 Résultats des Prédictions")
                st.dataframe(df_results)

                # Statistiques sur les anomalies
                anomaly_count = df_results[df_results["prediction"] != "normal"].shape[0]
                total_count = df_results.shape[0]
                st.write(f"🚨 **Nombre d'anomalies détectées :** {anomaly_count} / {total_count}")
            else:
                st.error("Erreur lors de la prédiction.")
                st.write(response.text)

        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion à l'API : {e}")