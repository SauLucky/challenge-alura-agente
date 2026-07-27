import time
from langchain_community.vectorstores import FAISS

class VectorStoreManager:
    """
    Administra la creación, guardado y carga del índice FAISS.
    """
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model

    def create(self, documents):
        """Genera el espacio vectorial a partir de los chunks en bloques para evitar límites de API."""
        batch_size = 50
        total_docs = len(documents)
        print(f"Iniciando creación de la base vectorial. Total de fragmentos: {total_docs}")
        
        # Procesar el primer bloque para inicializar el vectorstore
        first_batch = documents[:batch_size]
        print(f"Procesando bloque 1: fragmentos del 0 al {len(first_batch)}")
        vectorstore = FAISS.from_documents(first_batch, self.embedding_model)
        
        # Procesar los bloques restantes con pausas para no agotar la cuota de Gemini
        block_count = 2
        for i in range(batch_size, total_docs, batch_size):
            print("⏳ Esperando 60 segundos para resetear la cuota por minuto de Gemini...")
            time.sleep(60)
            
            batch = documents[i:i + batch_size]
            print(f"Procesando bloque {block_count}: fragmentos del {i} al {i + len(batch)}")
            vectorstore.add_documents(batch)
            block_count += 1
            
        print("¡Base vectorial creada con éxito!")
        return vectorstore

    def save(self, vectorstore, path="vector_db"):
        """Guarda la base de datos vectorial en disco."""
        vectorstore.save_local(path)

    def load(self, path="vector_db"):
        """Carga la base de datos vectorial desde disco."""
        return FAISS.load_local(
            path, 
            self.embedding_model, 
            allow_dangerous_deserialization=True
        )
