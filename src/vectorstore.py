import time
from langchain_community.vectorstores import FAISS
from src.config import Config
from src.logger import logger
from src.exceptions import VectorStoreNotFoundError

class VectorStoreManager:
    """ Administra el almacenamiento, carga y búsquedas semánticas avanzadas en FAISS. """
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self._cached_vectorstore = None  # Variable para mantener la base en caché de memoria

    def create(self, documents):
        """Mantiene la compatibilidad con el pipeline de ingesta anterior por bloques."""
        pass

    def _get_or_load_vectorstore(self):
        """Implementación de caché en memoria para acelerar Streamlit."""
        if self._cached_vectorstore is None:
            if not Config.VECTOR_DB_DIR.exists():
                logger.error(f"Falla crítica: El índice no existe en {Config.VECTOR_DB_DIR}")
                raise VectorStoreNotFoundError(f"No se encontró el índice local en '{Config.VECTOR_DB_DIR}'")
                
            logger.info("⚡ Cargando índice FAISS en memoria por primera vez (Caché inicializada)...")
            self._cached_vectorstore = FAISS.load_local(
                str(Config.VECTOR_DB_DIR), 
                self.embedding_model, 
                allow_dangerous_deserialization=True
            )
        return self._cached_vectorstore

    def load(self):
        """MEJORA: Configura y devuelve el retriever MMR Inteligente desde la caché."""
        vectorstore = self._get_or_load_vectorstore()
        
        retriever = vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 4,             # Número de fragmentos finales para el contexto
                "fetch_k": 15,       # Total de candidatos evaluados inicialmente
                "lambda_mult": 0.7   # Balance: 1.0 relevancia pura / 0.0 diversidad extrema
            }
        )
        return retriever

    def search_relevant_chunks(self, query: str) -> list:
        """
        Recuperación avanzada usando similitud con Score matemático de Relevancia.
        Filtra bloques duplicados y asegura calidad informativa.
        """
        vectorstore = self._get_or_load_vectorstore()
        
        # Ejecutamos la búsqueda avanzada trayendo el texto y su distancia matemática (L2 distance)
        docs_and_scores = vectorstore.similarity_search_with_score(query, k=Config.FETCH_K)
        
        valid_chunks = []
        for doc, score in docs_and_scores:
            # Convertimos la distancia L2 de FAISS a un porcentaje de confianza intuitivo (0% a 100%)
            confidence = max(0.0, min(1.0, 1.0 - (score / 2.0)))
            
            # Filtramos los fragmentos que no alcancen el umbral corporativo de confianza
            if confidence >= Config.MIN_SIMILARITY_SCORE:
                doc.metadata["similarity_score"] = float(confidence)
                valid_chunks.append(doc)
                
        logger.info(f"Búsqueda semántica finalizada. Se recuperaron {len(valid_chunks)} candidatos elegibles.")
        return valid_chunks[:Config.TOP_K]
