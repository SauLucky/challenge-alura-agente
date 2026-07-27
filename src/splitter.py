from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import Config
from src.utils import logger

class DocumentSplitter:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def split_documents(self, documents):
        """Recibe la lista de documentos y los corta en fragmentos."""
        if not documents:
            logger.warning("No se proporcionaron documentos para segmentar.")
            return []
            
        chunks = self.splitter.split_documents(documents)
        logger.info(f"Segmentación completada: {len(documents)} páginas originales transformadas en {len(chunks)} fragmentos.")
        return chunks