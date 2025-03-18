import os
from fastapi import FastAPI, Query
from databases import Database

# DB_URL = os.getenv("DATABASE_URL")
DB_URL = "postgresql://user:password@db:5432/kdd_cup99"

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
    limit: int = Query(100, ge=1, le=5000)
):
    """
    Récupère les logs réseau en fonction des filtres donnés :
    - `protocol`: Filtrer par type de protocole (`tcp`, `udp`, etc.)
    - `service`: Filtrer par service (`http`, `ftp`, `smtp`, etc.)
    - `label`: Filtrer par type de trafic (`normal`, `anomaly`)
    - `limit`: Nombre de résultats retournés (max 5000)
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