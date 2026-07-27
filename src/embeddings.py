from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Cargamos la API Key desde el archivo .env
load_dotenv()

class EmbeddingModel:
    """
    Encapsula el modelo de embeddings de Google Gemini.
    """
    def __init__(self):
        # Usamos gemini-embedding-001, el estándar estable de producción de Google
        self.model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
        )

    def get_model(self):
        return self.model
