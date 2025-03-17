from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import logging

app = FastAPI(
    title="KDDCup99 API",
    description="API pour requêter et filtrer les données du dataset KDDCup99",
    version="1.0.0"
)

# Chargement du dataset
try:
    df = pd.read_csv("./data/KDDCup99.csv")
    df.columns = df.columns.str.strip()  # Nettoyage des noms de colonnes
except Exception as e:
    logging.error(f"Erreur lors du chargement du dataset : {e}")
    df = pd.DataFrame()

@app.get("/data", tags=["Données"])
def get_data():
    """Renvoie l'intégralité du dataset KDDCup99"""
    if df.empty:
        raise HTTPException(status_code=500, detail="Le dataset n'a pas pu être chargé.")
    return df.to_dict(orient="records")

@app.get("/data/filter", tags=["Données"])
def filter_data(statut: str = None, protocole: str = None, periode: str = None):
    """Filtre les données selon le statut, le protocole et la période"""
    if df.empty:
        raise HTTPException(status_code=500, detail="Le dataset n'a pas pu être chargé.")
    df_filtered = df.copy()
    
    if statut:
        df_filtered = df_filtered[df_filtered["Statut"] == statut]
    if protocole:
        df_filtered = df_filtered[df_filtered["Protocole"] == protocole]
    if periode:
        df_filtered["Horodatage"] = pd.to_datetime(df_filtered["Horodatage"], errors='coerce')
        if periode == "Aujourd'hui":
            df_filtered = df_filtered[df_filtered["Horodatage"].dt.date == pd.to_datetime("today").date()]
        elif periode == "Cette semaine":
            df_filtered = df_filtered[df_filtered["Horodatage"].dt.isocalendar().week == pd.to_datetime("today").isocalendar().week]
        elif periode == "Ce mois":
            df_filtered = df_filtered[df_filtered["Horodatage"].dt.month == pd.to_datetime("today").month]
    
    return df_filtered.to_dict(orient="records")

@app.get("/stats", tags=["Statistiques"])
def get_stats(periode: str = "Aujourd'hui"):
    """Renvoie les statistiques générales en fonction de la période sélectionnée"""
    if df.empty:
        raise HTTPException(status_code=500, detail="Le dataset n'a pas pu être chargé.")
    
    df_filtered = df.copy()
    df_filtered["Horodatage"] = pd.to_datetime(df_filtered["Horodatage"], errors='coerce')
    
    if periode == "Aujourd'hui":
        df_filtered = df_filtered[df_filtered["Horodatage"].dt.date == pd.to_datetime("today").date()]
    elif periode == "Cette semaine":
        df_filtered = df_filtered[df_filtered["Horodatage"].dt.isocalendar().week == pd.to_datetime("today").isocalendar().week]
    elif periode == "Ce mois":
        df_filtered = df_filtered[df_filtered["Horodatage"].dt.month == pd.to_datetime("today").month]
    
    stats = {
        "Connexions Totales": len(df_filtered),
        "Connexions Suspectes": df_filtered[df_filtered["Statut"] == "Suspect"].shape[0],
        "Connexions Actives": df_filtered[df_filtered["Actif"] == True].shape[0],
        "Anomalies Détectées": df_filtered[df_filtered["Risque"] == "Élevé"].shape[0]
    }
    return stats