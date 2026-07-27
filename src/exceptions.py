class RAGException(Exception):
    """Excepción base para el ecosistema RAG."""
    pass

class VectorStoreNotFoundError(RAGException):
    """Se gatilla si el índice local FAISS no se encuentra en el disco duro."""
    pass

class LLMQueryError(RAGException):
    """Se gatilla ante fallas de conectividad o respuestas vacías de la API de Google."""
    pass
