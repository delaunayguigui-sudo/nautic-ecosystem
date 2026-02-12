from fastapi import FastAPI, Request
import requests
from datetime import datetime

app = FastAPI()

# 🔑 Remplace par ton Token PAT (créé sur airtable.com/create/tokens)
AIRTABLE_TOKEN = "patk8yZoyU4mHYnoy"
BASE_ID = "appArcT0oOcTFjVRp"
TABLE_NAME = "Maintenance Tasks" # Nom de ta table de suivi

@app.post("/bateaux")
async def save_to_airtable(request: Request):
    data = await request.json()
    
    # Préparation des données pour Airtable
    # Assure-toi que les noms correspondent à tes colonnes (image_78ba02.png)
    payload = {
        "fields": {
            "Boat": [data.get("boat_id")], # ID du bateau lié
            "Maintenance Type": [data.get("task_id")], # ID de la tâche liée
            "Status": "Completed",
            "Completion Date": datetime.now().strftime("%Y-%m-%d"),
            "Notes": data.get("notes", "Pointage via Telegram")
        }
    }
    
    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json"
    }
    
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
