import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- 1. CONFIGURATION DE LA BASE DE DONNÉES ---
# Récupère l'adresse de la base de données du Cloud, sinon utilise une locale (test)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Correction pour Render (l'URL doit commencer par postgresql://)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- 2. MODÈLE DE DONNÉES (TABLE BATEAU) ---
class BateauDB(Base):
    __tablename__ = "bateaux"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    moteur = Column(String)
    heures_moteur = Column(Integer)
    en_service = Column(Boolean, default=True)

# Création des tables dans la base de données
Base.metadata.create_all(bind=engine)

# --- 3. DÉFINITION DE L'API ---
app = FastAPI(title="Nautic API - Système Cloud")

# Modèle pour recevoir les données (ce que tu envoies)
class BateauCreate(BaseModel):
    nom: str
    moteur: str
    heures_moteur: int
    en_service: bool = True

# --- 4. LES FONCTIONS (ENDPOINTS) ---

@app.get("/")
def home():
    return {"message": "API Nautique connectée au Cloud et prête !"}

@app.post("/bateaux/")
def ajouter_bateau(bateau: BateauCreate):
    db = SessionLocal()
    nouveau_bateau = BateauDB(**bateau.dict())
    db.add(nouveau_bateau)
    db.commit()
    db.refresh(nouveau_bateau)
    db.close()
    return nouveau_bateau

@app.get("/bateaux/")
def lire_bateaux():
    db = SessionLocal()
    bateaux = db.query(BateauDB).all()
    db.close()
    return bateaux