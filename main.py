from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
# Ton Token personnel
AIRTABLE_TOKEN = "pat9vFzgmHe6fQuVz.8bd93fb8e3517b836bd5ace8ea31ed1ccc7038238e07f6c4309f8f935472ed6f"
BASE_ID = "appArcT0oOcTFjVRp"

# Headers pour l'authentification
HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_TOKEN}",
    "Content-Type": "application/json"
}

# ---------------------------------------------------------
# MODÈLE DE DONNÉES (Pour valider ce que Make envoie)
# ---------------------------------------------------------
class MaintenanceTask(BaseModel):
    boat_name: str
    description: str
    status: str = "Pending"  # Par défaut, le statut est "En attente"

# ---------------------------------------------------------
# ROUTES DE L'API
# ---------------------------------------------------------

@app.get("/")
def home():
    return {"status": "API Nautic Operationnelle ⚓️", "mode": "Lecture & Ecriture"}

# 1. ROUTE POUR LIRE (GET) - Celle qu'on a faite avant
@app.get("/full-data")
def get_full_data():
    """Récupère Bateaux, Tâches et Techniciens en un seul appel"""
    tables = ["Boats", "Maintenance Tasks", "Maintenance Types", "Technicians"]
    data = {}
    
    for table in tables:
        url = f"https://api.airtable.com/v0/{BASE_ID}/{table}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            data[table] = response.json().get("records", [])
        else:
            data[table] = []
            
    return data

# 2. ROUTE POUR ÉCRIRE (POST) - La nouveauté !
@app.post("/create-task")
async def create_maintenance_task(task: MaintenanceTask):
    """
    Reçoit une demande de maintenance depuis Make/Telegram
    et la crée dans Airtable.
    """
    
    # Étape 1 : Trouver l'ID du bateau à partir de son nom
    # On doit chercher dans la table "Boats" quel ID correspond au nom reçu
    url_search = f"https://api.airtable.com/v0/{BASE_ID}/Boats?filterByFormula={{Boat Name}}='{task.boat_name}'"
    search_response = requests.get(url_search, headers=HEADERS)
    
    boat_id = None
    if search_response.status_code == 200:
        records = search_response.json().get("records", [])
        if records:
            boat_id = records[0]["id"]
    
    if not boat_id:
        # Si on ne trouve pas le bateau, on arrête tout
        raise HTTPException(status_code=404, detail=f"Bateau '{task.boat_name}' introuvable.")

    # Étape 2 : Créer la tâche dans "Maintenance Tasks"
    url_post = f"https://api.airtable.com/v0/{BASE_ID}/Maintenance%20Tasks"
    
    # On prépare les données pour Airtable
    payload = {
        "fields": {
            "Description": task.description,
            "Status": task.status,
            "Related Boat": [boat_id]  # On lie la tâche au bon bateau via son ID
        }
    }
    
    response = requests.post(url_post, json=payload, headers=HEADERS)
    
    if response.status_code == 200:
        return {"message": "Tâche créée avec succès !", "data": response.json()}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
