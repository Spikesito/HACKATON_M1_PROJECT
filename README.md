# 📌 **Hackathon M1 Data / Cloud / Infra**
**👥 Équipe :** *Emile SEGURET / Adam AHMAT / Mathys POINTARD / Melvin MIAUX / Guillaume CRISTINI*

## 🏆 **Introduction**
Ce projet a été réalisé dans le cadre du module *Hackathon M1 Data / Cloud / Infra*.  
L'objectif est de développer une **solution de détection d’intrusions** intégrant :
- 🔍 **Une interface web interactive** simulant les flux réseau.
- 🚨 **Un agent d’analyse en temps réel** entraîné sur le dataset *KDD Cup 99*.
- 🔗 **Une API FastAPI** permettant la récupération et l’analyse des logs réseau.
- 🛠 **Un environnement conteneurisation (Docker)** pour assurer la scalabilité et la portabilité.
- 📝 **Une journalisation des événements** pour assurer la traçabilité et l'audit des connexions.

---

## 📚 **Structure du projet**
Le projet est organisé en **trois composants principaux** : **Backend (API)**, **Frontend (UI Web)** et **Base de données (PostgreSQL)**.

### 📁 **Backend (`backend/`)**
Fournit une **API REST avec FastAPI** pour :
- Stocker et récupérer les logs réseau.
- Appliquer un modèle de **Machine Learning** pour détecter les anomalies.
- Retourner les prédictions à l'interface utilisateur.

> 📌 **Contenu du dossier :**
- `main.py` ➔ API développée avec **FastAPI**.
- `models/` ➔ Dossier contenant le modèle de **Machine Learning** (XGBoost).
- `requirements.txt` ➔ Fichier des dépendances **Python** pour l'API.
- `Dockerfile` ➔ Conteneurisation du **Backend** via Docker.

---

### 📁 **Base de données (`db/`)**
La base de données **PostgreSQL** est utilisée pour stocker les logs réseau.

> 📌 **Contenu du dossier :**
- `init.sql` ➔ Script SQL pour **initialiser la base de données**.

---

### 📁 **Frontend (`frontend/`)**
Fournit une **interface utilisateur avec Streamlit** pour visualiser :
- 📊 **Les statistiques réseau**.
- 🚨 **Les anomalies détectées**.
- 🤖 **Les prédictions du modèle ML**.
- 📝 **La documentation API**.

> 📌 **Contenu du dossier :**
- `app.py` ➔ Application **Streamlit** principale.
- `pages/` ➔ Contient les différentes pages de l’application :
  - `dashboard.py` ➔ **Tableau de bord des connexions**.
  - `anomalies.py` ➔ **Détection et analyse des anomalies**.
  - `prediction.py` ➔ **Résultats des prédictions du modèle**.
  - `documentation_api.py` ➔ **Documentation de l’API**.
- `requirements.txt` ➔ Fichier des dépendances pour Streamlit.
- `Dockerfile` ➔ Conteneurisation du **Frontend** via Docker.

---

### 📁 **Données (`data/`)**
Contient le dataset utilisé pour l'entraînement du modèle.

> 📌 **Contenu du dossier :**
- `KDDCup99.csv` ➔ Dataset original pour la détection des intrusions.

---

### 📁 **Fichiers de configuration**
- `.gitignore` ➔ Exclusions de fichiers sensibles et temporaires.
- `docker-compose.yml` ➔ Orchestration des **conteneurs Docker** pour le backend, frontend et la base de données.
- `README.md` ➔ **Documentation** du projet.

---

## 🚀 **Installation & Lancement**

### **1⃣ Cloner le projet**
```bash
git clone https://github.com/votre-repo/hackathon_m1_project.git
cd hackathon_m1_project
```

### **2⃣ ▶️ Lancer le projet avec Docker**
```bash
docker-compose up --build
```
- L’API FastAPI sera accessible sur **`http://localhost:8000/docs`**
- L'interface Streamlit sera disponible sur **`http://localhost:8501`**

---

### **🔍 Installer les dépendances manuellement**
📞 **Backend (FastAPI)**
```bash
cd backend
pip install -r requirements.txt
```
🖥 **Frontend (Streamlit)**
```bash
cd frontend
pip install -r requirements.txt
```

---

### **🔍 Tester les services manuellement**
📀 **Démarrer l'API :**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
📺 **Lancer l’interface utilisateur :**
```bash
cd frontend
streamlit run app.py
```

---

## 📢 **Contributeurs**
- **Emile SEGURET**
- **Adam AHMAT**
- **Mathys POINTARD**
- **Melvin MIAUX**
- **Guillaume CRISTINI**

🔥 **Projet réalisé lors du Hackathon M1 Data / Cloud / Infra 2025 !** 🚀