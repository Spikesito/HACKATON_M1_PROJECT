import os
from fastapi import FastAPI, Query, File, UploadFile, HTTPException
from databases import Database
import joblib
import pandas as pd
import xgboost as xgb
import numpy as np
from pydantic import BaseModel, validator
from typing import Optional
import io

DB_URL = os.getenv("DATABASE_URL")

app = FastAPI(
    title="KDDCup99 API", 
    description="API de logs réseau avec PostgreSQL", 
    version="1.0.0"
)

database = Database(DB_URL)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def read_root():
    return {"message": "Bienvenue sur l'API KDDCup99 !"}

@app.get("/data/filter", tags=["Données"])
async def filter_data(
    protocol: str = Query(None, alias="protocol_type"),
    service: str = Query(None),
    label: str = Query(None),
    limit: int = 5000
):
    """
    Récupère les logs réseau en fonction des filtres donnés :
    - `protocol`: Filtrer par type de protocole (`tcp`, `udp`, etc.)
    - `service`: Filtrer par service (`http`, `ftp`, `smtp`, etc.)
    - `label`: Filtrer par type de trafic (`normal`, `anomaly`)
    - `limit`: Nombre de résultats retournés (default 5000)
    """
    query = "SELECT * FROM network_logs WHERE 1=1"
    params = {}

    if protocol:
        query += " AND protocol_type = :protocol"
        params["protocol"] = protocol
    if service:
        query += " AND service = :service"
        params["service"] = service
    if label:
        query += " AND label = :label"
        params["label"] = label

    query += " LIMIT :limit"
    params["limit"] = limit

    rows = await database.fetch_all(query, values=params)
    return rows

@app.get("/stats/labels", tags=["Statistiques"])
async def get_label_counts():
    """
    Récupère le nombre d'occurrences de chaque type de label (normal et anomalies),
    groupées par protocole et service.
    """
    query = """
        SELECT protocol_type, service, label, COUNT(*) AS count
        FROM network_logs
        GROUP BY protocol_type, service, label
        ORDER BY count DESC
    """
    rows = await database.fetch_all(query)
    
    return [
        {"protocol_type": row["protocol_type"], "service": row["service"], "label": row["label"], "count": row["count"]}
        for row in rows
    ]

# Chargement du modèle XGBoost
model_data = joblib.load('/app/backend/models/xgboost_kddcup_combined.pkl')
model = model_data['model']
label_encoders = model_data['label_encoders']
label_encoder_y = model_data['label_encoder_y']
selected_features = model_data['selected_features']

class NetworkLog(BaseModel):
    srv_count: int
    dst_host_same_src_port_rate: float
    count: int
    protocol_type: str
    service: str
    dst_host_srv_count: int
    dst_host_same_srv_rate: float
    same_srv_rate: float
    flag: str
    dst_host_serror_rate: float

    # Validation des types de données (au cas où ils ne seraient pas valides)
    @validator('srv_count', pre=True)
    def validate_srv_count(cls, v):
        if not isinstance(v, int):
            raise ValueError('srv_count must be an integer')
        return v

    @validator('dst_host_same_src_port_rate', pre=True)
    def validate_dst_host_same_src_port_rate(cls, v):
        if not isinstance(v, (int, float)):
            raise ValueError('dst_host_same_src_port_rate must be a number')
        return v

    @validator('count', pre=True)
    def validate_count(cls, v):
        if not isinstance(v, int):
            raise ValueError('count must be an integer')
        return v

    @validator('protocol_type', 'service', 'flag', pre=True)
    def validate_string_fields(cls, v):
        if not isinstance(v, str):
            raise ValueError('Field must be a string')
        return v

    @validator('dst_host_srv_count', pre=True)
    def validate_dst_host_srv_count(cls, v):
        if not isinstance(v, int):
            raise ValueError('dst_host_srv_count must be an integer')
        return v

    @validator('dst_host_same_srv_rate', 'same_srv_rate', 'dst_host_serror_rate', pre=True)
    def validate_float_fields(cls, v):
        if not isinstance(v, (int, float)):
            raise ValueError('Field must be a float')
        return v

@app.post("/predict/")
async def predict(log: NetworkLog):
    try:
        # Conversion en DataFrame
        df_input = pd.DataFrame([log.dict()])

        # Appliquer l'encodage des variables catégoriques
        for col in ['protocol_type', 'service', 'flag']:
            le = label_encoders[col]  # Récupérer le bon label encoder pour chaque colonne
            df_input[col] = le.transform(df_input[col])

        # Prédiction avec le modèle
        pred = model.predict(df_input)  # La classe prédite
        proba = model.predict_proba(df_input)  # Probabilités pour chaque classe
        
        # Récupérer la classe prédite et la probabilité associée
        predicted_class = pred[0]
        predicted_class_prob = proba[0][predicted_class]  # Probabilité pour la classe prédite

        # Récupérer le nom de la classe prédite à partir de label_encoder_y
        predicted_class_name = label_encoder_y.inverse_transform([predicted_class])[0]

        # Retourner la classe prédite et sa probabilité
        return {
            "prediction": predicted_class_name,  # Nom de la classe prédite
            "confidence": round(float(predicted_class_prob), 4)  # Probabilité associée à la prédiction (convertie en float)
        }
    except Exception as e:
        return {"error": f"Erreur lors de la prédiction : {str(e)}"}
    
@app.post("/predict_csv")
async def predict_csv(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")), sep=';')

        required_columns = ['srv_count', 'dst_host_same_src_port_rate', 'count', 'protocol_type', 
                            'service', 'dst_host_srv_count', 'dst_host_same_srv_rate', 'same_srv_rate', 
                            'flag', 'dst_host_serror_rate']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(status_code=400, detail=f"Colonnes manquantes: {', '.join(missing_columns)}")


        for col in ['protocol_type', 'service', 'flag']:
            if col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = label_encoders[col].transform(df[col])
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = pd.to_numeric(df[col], errors='coerce')  
        df.fillna(0, inplace=True)  
        df = df[required_columns]


        predictions = model.predict(df)
        probabilities = model.predict_proba(df)
        
        results = []
        
        for i in range(len(predictions)):
            results.append({
                "id": i,
                "prediction": label_encoder_y.inverse_transform([predictions[i]])[0],
                "confidence": float(max(probabilities[i]))  
            })
        return {"predictions": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction : {str(e)}")