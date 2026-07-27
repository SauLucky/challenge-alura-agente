import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Rutas del Sistema
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

    # Configuración del Retriever Inteligente (MMR)
    SEARCH_TYPE = "mmr"
    TOP_K = 5          # Número de fragmentos finales para el contexto
    FETCH_K = 20       # Total de candidatos evaluados inicialmente para garantizar diversidad
    LAMBDA_MULT = 0.7  # Balance: 1.0 relevancia pura / 0.0 diversidad extrema

    # Umbral Mínimo de Confianza (Filtro de Relevancia)
    MIN_SIMILARITY_SCORE = 0.35

    # Seguridad y Cuotas
    BATCH_SIZE = 50
    COOLDOWN_TIME = 60
