from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentSplitter:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        # Configuramos el divisor inteligente con tus parámetros y separadores
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def split_documents(self, documents):
        """Recibe la lista de documentos y los corta en fragmentos."""
        chunks = self.splitter.split_documents(documents)
        print(f"✂️ Segmentación completada: {len(documents)} páginas originales se transformaron en {len(chunks)} fragmentos.")
        return chunks

if __name__ == "__main__":
    # Bloque de prueba interno para el Sprint 2
    from src.loader import DocumentLoader
    print("Iniciando prueba del módulo DocumentSplitter...")
    
    loader = DocumentLoader()
    docs = loader.load_all_documents()
    
    splitter = DocumentSplitter()
    splitter.split_documents(docs)