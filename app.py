from src.loader import DocumentLoader
from src.splitter import DocumentSplitter
from src.embeddings import EmbeddingModel
from src.vectorstore import VectorStoreManager

def main():
    # 1. Cargamos documentos (Sprint 1)
    print("Cargando documentos...")
    loader = DocumentLoader()
    documents = loader.load_all_documents()
    print(f"Documentos: {len(documents)}")

    # 2. Segmentación de texto (Sprint 2)
    splitter = DocumentSplitter()
    chunks = splitter.split_documents(documents)
    print(f"Chunks: {len(chunks)}")

    # 3. Inicialización de Embeddings y Administrador (Sprint 3)
    embeddings = EmbeddingModel().get_model()
    vector_manager = VectorStoreManager(embeddings)

    # 4. Creación Segura por Bloques (Evita el Error 429)
    print("Generando embeddings y creando base vectorial...")
    vectorstore = vector_manager.create(chunks)
    
    # 5. Persistencia en disco
    vector_manager.save(vectorstore)
    print("Base vectorial creada correctamente.")

if __name__ == "__main__":
    main()
