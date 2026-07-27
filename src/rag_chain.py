from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import Config
from src.logger import logger

class RAGChain:
    """Únicamente administra el enlace y la inicialización limpia del modelo generativo."""
    def __init__(self):
        logger.info(f"Conectando con el servidor de Google AI Studio [{Config.CHAT_MODEL}]...")
        self.llm = ChatGoogleGenerativeAI(
            model=Config.CHAT_MODEL,
            temperature=Config.TEMPERATURE,
            api_version=Config.API_VERSION
        )

    def get_llm(self):
        return self.llm
