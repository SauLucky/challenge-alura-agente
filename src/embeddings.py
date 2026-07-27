from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Cargamos las variables de entorno
load_dotenv()

class EmbeddingModel:
    """
    Encapsula el modelo de embeddings estable de Google Gemini para LangChain.
    """
    def __init__(self):
        # Usamos gemini-embedding-001, homologado y libre de errores 404 en la API de Google
        self.model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
        )

    def get_model(self):
        return self.model
