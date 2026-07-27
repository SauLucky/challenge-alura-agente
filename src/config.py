import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Rutas del sistema
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"
    VECTOR_DB_DIR = BASE_DIR / "vector_db"
    LOGS_DIR = BASE_DIR / "logs"

    # Parámetros del Splitter
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200

    # Modelos de Inteligencia Artificial (Google Gemini)
    EMBEDDING_MODEL = "models/gemini-embedding-001"
    CHAT_MODEL = "gemini-2.5-flash"
    API_VERSION = "v1"
    TEMPERATURE = 0.0

    # Seguridad y Cuotas
    BATCH_SIZE = 50
    COOLDOWN_TIME = 60  # Segundos de espera entre bloques
