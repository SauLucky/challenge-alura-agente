from src.prompts import RAG_PROMPT
from src.logger import logger
from src.exceptions import LLMQueryError

class RAGService:
    """
    EL CORAZÓN DEL PROYECTO: Centraliza el procesamiento analítico de prompts, 
    limpieza de fuentes sin duplicados e historial conversacional.
    """
    def __init__(self, vector_manager, chain_manager):
        self.vector_manager = vector_manager
        self.chain_manager = chain_manager

    def _format_clean_sources(self, chunks: list) -> list:
        """MEJORA DE PRODUCCIÓN: Consolida páginas, calcula la relevancia y genera 
        hipervínculos reales clickeables hacia tu hosting en Hostinger."""
        url_mapping = {
            "FAQ.pdf": "https://promotazas.com",
            "Reglamento.pdf": "https://promotazas.com",
            "Manual_Proveedores.pdf": "https://promotazas.com",
            "Politica_Atencion.pdf": "https://promotazas.com",
            "inventario_supermercado.xlsx": "https://promotazas.com"
        }

        seen_sources = {}
        
        for doc in chunks:
            source_file = doc.metadata.get("source_file", "Manual_Interno.pdf")
            page = doc.metadata.get("page", doc.metadata.get("row", "N/A"))
            score = doc.metadata.get("similarity_score", 0.0)
            
            # Formateamos el número de página/fila legible (human-readable)
            page_num = int(page) + 1 if isinstance(page, int) else page
            location_str = f"Página {page_num}" if "pdf" in source_file.lower() else f"Fila {page_num}"
            
            percentage_str = f"{int(score * 100)}%"

            if source_file not in seen_sources:
                seen_sources[source_file] = {
                    "locations": {location_str},
                    "max_score": percentage_str
                }
            else:
                seen_sources[source_file]["locations"].add(location_str)

        # Construimos la lista estructurada final con formato Markdown linkeable
        formatted_sources = []
        for index, (filename, data) in enumerate(seen_sources.items(), start=1):
            locations_joined = ", ".join(sorted(list(data["locations"])))
            file_url = url_mapping.get(filename, "#")
            
            # Creamos el formato de enlace Markdown [Nombre](URL)
            formatted_sources.append(
                f"{index}. 🔗 [{filename}]({file_url}) ({locations_joined}) — Relevancia: {data['max_score']}"
            )
            
        return formatted_sources

    def execute_query(self, user_question: str, memory_history: list = None) -> dict:
        """
        MEJORA 6 y 8: Valida entradas, inyecta el contexto de memoria e invoca 
        de forma segura al modelo generativo.
        """
        # MEJORA 8: Validación estricta de preguntas vacías
        if not user_question or not user_question.strip():
            logger.warning("Se detectó un intento de consulta vacío.")
            return {
                "answer": "Por favor escribe una pregunta válida para poder asistirte.",
                "sources": []
            }

        logger.info(f"Procesando flujo unificado para la consulta: '{user_question}'")
        
        # Compilamos el hilo previo de la memoria histórica si existe
        history_context = ""
        if memory_history:
            history_context = "\n".join(memory_history[-4:]) # Lee los últimos 2 turnos

        # 1. Recuperamos fragmentos con filtrado por Score y MMR
        search_query = f"{history_context}\n{user_question}" if history_context else user_question
        chunks = self.vector_manager.search_relevant_chunks(search_query)

        # 2. Si FAISS no encuentra nada relevante, activamos de inmediato el candado de seguridad
        if not chunks:
            logger.warning("Búsqueda desierta: Ningún fragmento superó el umbral de confianza.")
            return {
                "answer": "No encontré información sobre ese tema en la base documental.",
                "sources": []
            }

        # 3. Procesamos y limpiamos las fuentes analíticas sin duplicados
        clean_sources = self._format_clean_sources(chunks)

        # 4. Compilamos el bloque de contexto textual
        context_string = "\n\n".join([
            f"[Archivo: {c.metadata.get('source_file')} | Ubicación: {c.metadata.get('page')}]\nContenido: {c.page_content}\n---"
            for c in chunks
        ])

        try:
            # 5. Uso del método oficial de LangChain para formatear el prompt de chat de forma segura
            formatted_prompt = RAG_PROMPT.format_messages(context=context_string, question=user_question)

            # 6. Ejecutamos la consulta mediante LangChain directo a Google
            llm = self.chain_manager.get_llm()
            raw_response = llm.invoke(formatted_prompt)
            answer = raw_response.content if hasattr(raw_response, 'content') else str(raw_response)
            
            # Doble candado: Si Gemini burla el prompt e intenta inventar algo, forzamos la frase corporativa
            if "no encontré" in answer.lower() or "base documental" in answer.lower():
                return {
                    "answer": "No encontré información sobre ese tema en la base documental.",
                    "sources": []
                }

            logger.info("Flujo RAG de producción finalizado con éxito.")
            return {
                "answer": answer.strip(),
                "sources": clean_sources
            }

        except Exception as e:
            logger.error(f"Falla crítica en la comunicación con el servidor generativo: {e}")
            raise LLMQueryError(f"Error al consultar al modelo de lenguaje: {e}")
