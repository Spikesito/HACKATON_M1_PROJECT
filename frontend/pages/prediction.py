import streamlit as st
import requests

# API URL (modifiez selon votre configuration d'API)
API_URL = "http://backend:8000/predict/"

# Sidebar
st.sidebar.title("NetMonitor")
st.sidebar.markdown("""
- 📊 Tableau de bord
- 🔍 Connexions
- 🚨 Anomalies
- 📈 Statistiques
- 📝 Logs & Historique
""")

# Titre de la page
st.title("Détection d'Anomalies")
st.write("Visualisez les anomalies détectées par l'agent de Machine Learning.")

# Formulaire pour saisir les informations
st.subheader("Saisir les données pour prédiction")

# Saisie des informations
srv_count = st.number_input("srv_count", min_value=0, max_value=10000, step=1)
dst_host_same_src_port_rate = st.number_input("dst_host_same_src_port_rate", min_value=0.0, max_value=1.0, step=0.01)
count = st.number_input("count", min_value=0, max_value=10000, step=1)
protocol_type = st.selectbox("protocol_type", ["tcp", "udp", "icmp"])  # Exemple de catégories possibles
service = st.selectbox("service", ["http", "ftp", "ssh", "telnet", "smtp", "pop3", "imap", "dns", "other"])  # Liste des services possibles
dst_host_srv_count = st.number_input("dst_host_srv_count", min_value=0, max_value=10000, step=1)
dst_host_same_srv_rate = st.number_input("dst_host_same_srv_rate", min_value=0.0, max_value=1.0, step=0.01)
same_srv_rate = st.number_input("same_srv_rate", min_value=0.0, max_value=1.0, step=0.01)
flag = st.selectbox("flag", ["SF", "S0", "REJ", "RSTO", "RSTR", "S1", "S2", "S3", "OTH", "SH", "RSTOS0"])  # Liste des flags possibles
dst_host_serror_rate = st.number_input("dst_host_serror_rate", min_value=0.0, max_value=1.0, step=0.01)

# Exemple d'entrée depuis Streamlit
data_input = {
    "srv_count": srv_count,
    "dst_host_same_src_port_rate": dst_host_same_src_port_rate,
    "count": count,
    "protocol_type": protocol_type,
    "service": service,
    "dst_host_srv_count": dst_host_srv_count,
    "dst_host_same_srv_rate": dst_host_same_srv_rate,
    "same_srv_rate": same_srv_rate,
    "flag": flag,
    "dst_host_serror_rate": dst_host_serror_rate
}

# Bouton pour lancer la prédiction
if st.button("Faire la prédiction"):
    try:
        # Envoi des données à l'API pour obtenir la prédiction
        response = requests.post(API_URL, json=data_input)
        
        # Vérifier la réponse
        if response.status_code == 200:
            prediction = response.json()
            st.write(prediction)
            st.write(f"📊 **Prédiction** : {prediction['prediction']}")
            st.write(f"🔒 **Confiance** : {prediction['confidence']}")
        else:
            st.error("Erreur dans la prédiction.")
            st.write(response.text)
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de connexion à l'API : {e}")

 