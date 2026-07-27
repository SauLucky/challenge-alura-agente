import time
from langchain_community.vectorstores import FAISS
from src.config import Config
from src.utils import logger

class VectorStoreManager:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model

    def create(self, documents):
        """Genera el espacio vectorial a partir de los chunks en bloques respetando cuotas."""
        total_docs = len(documents)
        logger.info(f"Iniciando creación de la base vectorial FAISS para {total_docs} fragmentos.")
        
        first_batch = documents[:Config.BATCH_SIZE]
        vectorstore = FAISS.from_documents(first_batch, self.embedding_model)
        
        block_count = 2
        for i in range(Config.BATCH_SIZE, total_docs, Config.BATCH_SIZE):
            logger.info(f"Esperando {Config.COOLDOWN_TIME} segundos para proteger la cuota de la API...")
            time.sleep(Config.COOLDOWN_TIME)
            
            batch = documents[i:i + Config.BATCH_SIZE]
            logger.info(f"Procesando bloque {block_count} (fragmentos del {i} al {i + len(batch)})")
            vectorstore.add_documents(batch)
            block_count += 1
            
        logger.info("¡Base de datos vectorial FAISS consolidada con éxito!")
        return vectorstore

    def save(self, vectorstore):
        """Guarda la base de datos vectorial en disco."""
        vectorstore.save_local(str(Config.VECTOR_DB_DIR))
        logger.info(f"Base de datos vectorial guardada en: '{Config.VECTOR_DB_DIR}'")

    def load(self):
        """Carga la base de datos vectorial activando el Retriever MMR Inteligente."""
        logger.info(f"Cargando índice vectorial desde '{Config.VECTOR_DB_DIR}'...")
        vectorstore = FAISS.load_local(
            str(Config.VECTOR_DB_DIR), 
            self.embedding_model, 
            allow_dangerous_deserialization=True
        )
        
        # MEJORA 5: Configuración del Retriever MMR (Maximal Marginal Relevance)
        retriever = vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 4,             # Número de fragmentos finales para el contexto
                "fetch_k": 15,       # Total de candidatos evaluados inicialmente
                "lambda_mult": 0.7   # Balance: 1.0 relevancia pura / 0.0 diversidad extrema
            }
        )
        return retriever