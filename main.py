from fastapi import FastAPI, Request
import requests
from datetime import datetime

app = FastAPI()

# Configuration Airtable
AIRTABLE_TOKEN = "pat9vFzgmHe6fQuVz.8bd93fb8e3517b836bd5ace8ea31ed1ccc7038238e07f6c4309f8f935472ed6f"
BASE_ID = "appArcT0oOcTFjVRp"
TABLE_NAME = "tblrlCheKVSCX1ntE"

@app.get("/")
async def root():
    return {"message": "API Nautic Operationnelle - En attente de donnees"}

@app.post("/bateaux")
async def save_to_airtable(request: Request):
    data = await request.json()
    
    # Préparation des champs pour Airtable
    # On adapte selon tes colonnes (Nom du Bateau, Heures Moteur, Notes, etc.)
    payload = {
        "fields": {
            "Nom_Bateau": data.get("nom", "Inconnu"),
            "Heures_Moteur": data.get("heures", 0),
            "Description": data.get("notes", "Pointage via Telegram"),
            "Date_Intervention": datetime.now().strftime("%Y-%m-%d"),
            "Statut": "Pointé"
        }
    }
    
    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json"
    }
    
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    response = requests.post(url, json=payload, headers=headers)
    
    return response.json()

@app.get("/bateaux")
async def get_records():
    headers = {"Authorization": f"Bearer {AIRTABLE_TOKEN}"}
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    response = requests.get(url, headers=headers)
    return response.json()

