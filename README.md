# Emile SEGURET / Adam AHMAT / Mathys POINTARD / Melvin MIAUX / Guillaume CRISTINI - Hackaton M1 Data / Cloud / Infra

## Introduction

Ce projet a été réalisé dans le cadre du module de cours Hackaton M1 Data / Cloud / Infra. Le projet vise à développer une solution de détection d’intrusions intégrant une interface web interactive simulant les flux réseau et un agent d’analyse en temps réel entraîné sur le dataset KDD Cup 99. L’ensemble sera déployé dans un environnement conteneurisé avec API et journalisation des événements pour assurer traçabilité et audit.

## Structure du projet

Le projet est structuré en plusieurs fichiers :

- `api.py` : Le fichier principal contenant l'API développée avec FASTAPI.
- `requirements.txt` : Les dépendances nécessaires au projet.
- `function` : Le dossier contenant les fonctions principales.
- `app.py` : L'application front développée avec Streamlit pour interagir avec l'API + le dossier `pages` pour nos différentes pages.
- `model` : Le fichier contenant le modèle entraîné utilisé pour les prédictions.

## Installation

Pour installer les dépendances nécessaires, exécutez la commande suivante :

```bash
pip install -r requirements.txt
```

## Lancement à la racine du dossier

L'application streamlit :
```bash
streamlit run .\app.py
```

L'API :
```bash
uvicorn api:app --reload
```

## Vidéo démonstration