from fastapi import FastAPI
import requests

app = FastAPI()

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

# Ton Token personnel (Celui que tu viens de me donner)
AIRTABLE_TOKEN = "pat9vFzgmHe6fQuVz.8bd93fb8e3517b836bd5ace8ea31ed1ccc7038238e07f6c4309f8f935472ed6f"

# L'ID de ta base "MaintenanceNautique"
BASE_ID = "appArcT0oOcTFjVRp"

# Les entêtes pour s'authentifier auprès d'Airtable
HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_TOKEN}",
    "Content-Type": "application/json"
}

# ---------------------------------------------------------
# FONCTIONS UTILITAIRES
# ---------------------------------------------------------

def get_table_data(table_name):
    """
    Récupère toutes les lignes d'une table spécifique.
    Gère les espaces dans les noms de tables automatiquement.
    """
    url = f"https://api.airtable.com/v0/{BASE_ID}/{table_name}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("records", [])
    else:
        # En cas d'erreur, on affiche le problème dans les logs Render
        print(f"Erreur sur la table {table_name}: {response.text}")
        return []

# ---------------------------------------------------------
# ROUTES DE L'API
# ---------------------------------------------------------

@app.get("/")
def home():
    return {"status": "API Nautic en ligne ⚓️", "version": "2.0"}

@app.get("/full-data")
def get_full_data():
    """
    Cette route récupère TOUT ce dont Gemini a besoin en une seule fois.
    Elle interroge les 4 tables principales.
    """
    return {
        "bateaux": get_table_data("Boats"),
        "taches_maintenance": get_table_data("Maintenance Tasks"),
        "types_maintenance": get_table_data("Maintenance Types"),
        "techniciens": get_table_data("Technicians")
    }

# Route individuelle au cas où tu en aurais besoin pour des tests
@app.get("/bateaux")
def get_boats():
    return get_table_data("Boats")
