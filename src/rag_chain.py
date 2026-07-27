from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.prompts import RAG_PROMPT
from src.config import Config
from src.utils import logger

class RAGChain:
    def __init__(self, retriever):
        self.retriever = retriever
        # Conexión pura LangChain forzada a producción estable v1
        self.llm = ChatGoogleGenerativeAI(
            model=Config.CHAT_MODEL,
            temperature=Config.TEMPERATURE,
            api_version=Config.API_VERSION
        )

    def _format_context_and_extract_sources(self, input_data):
        """Busca fragmentos semánticos en FAISS, los formatea y aísla las fuentes únicas."""
        question = input_data["question"]
        chat_history = input_data.get("chat_history", "")

        # Construimos un término de búsqueda combinado con la memoria histórica si existe
        search_query = f"{chat_history}\n{question}" if chat_history else question
        
        # Recuperamos los chunks usando la configuración inteligente de MMR
        docs = self.retriever.invoke(search_query)
        
        formatted_chunks = []
        sources = set()

        for doc in docs:
            source_file = doc.metadata.get("source_file", "Documento_Interno.pdf")
            # Extrae la clave 'page' para archivos PDF o 'row' para bases de datos Excel
            page = doc.metadata.get("page", doc.metadata.get("row", "N/A"))
            
            # Estructuramos la cita limpia requerida
            citation = f"• {source_file} (Página/Fila: {int(page) + 1 if isinstance(page, int) else page})"
            sources.add(citation)

            formatted_chunks.append(f"[Fuente: {source_file} | Ubicación: {page}]\nContenido: {doc.page_content}\n---")

        context_string = "\n\n".join(formatted_chunks)
        
        # Guardamos temporalmente las fuentes en el flujo de ejecución de la cadena
        input_data["formatted_context"] = context_string
        input_data["extracted_sources"] = list(sources)
        return input_data

    def ask(self, question: str, chat_history: str = "") -> dict:
        """
        Procesa la consulta y devuelve un diccionario estructurado empresarial
        con la respuesta final del agente y su respectiva lista de fuentes reales.
        """
        logger.info(f"Procesando consulta del usuario: '{question}'")
        
        # Inicializamos los datos estructurados en el pipeline de ejecución
        payload = {
            "question": question,
            "chat_history": chat_history,
            "formatted_context": "",
            "extracted_sources": []
        }

        # 1. Recuperación MMR y Extracción de Fuentes Analíticas
        payload = self._format_context_and_extract_sources(payload)

        # 2. Si el contexto quedó vacío, aplicamos el candado de seguridad preventivo
        if not payload["formatted_context"].strip():
            logger.warning("El recuperador FAISS no retornó fragmentos de información útiles.")
            return {
                "answer": "No encontré información sobre ese tema en la base documental.",
                "sources": []
            }

        # 3. Compilamos el prompt final enviando las variables requeridas
        full_prompt = RAG_PROMPT.format(
            context=payload["formatted_context"],
            question=payload["question"]
        )

        try:
            # 4. Generación fundamentada mediante el servidor de Google
            raw_response = self.llm.invoke(full_prompt)
            answer = raw_response.content if hasattr(raw_response, 'content') else str(raw_response)
            
            # Candado secundario: Si el modelo alucina o burla el prompt, forzamos la frase oficial
            if "no encontré" in answer.lower() or "base documental" in answer.lower():
                return {
                    "answer": "No encontré información sobre ese tema en la base documental.",
                    "sources": []
                }

            logger.info("Respuesta generada con éxito y validada contra alucinaciones.")
            return {
                "answer": answer,
                "sources": payload["extracted_sources"]
            }

        except Exception as e:
            logger.error(f"Error crítico en la llamada de generación del LLM: {e}")
            return {
                "answer": "Ocurrió un inconveniente técnico al procesar tu solicitud. Por favor intenta de nuevo.",
                "sources": []
            }