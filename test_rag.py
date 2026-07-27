from src.embeddings import EmbeddingModel
from src.vectorstore import VectorStoreManager
from src.rag_chain import RAGChain
from src.rag_service import RAGService
from src.logger import logger

logger.info("============================================================")
logger.info("🚀 SISTEMA RAG EMPRESARIAL CONFIGURADO (SPRINT 4.1)")
logger.info("============================================================")

# 1. Inicializamos infraestructura y componentes base
embeddings = EmbeddingModel().get_model()
vector_manager = VectorStoreManager(embeddings)
chain_manager = RAGChain()

# 2. Inicializamos el orquestador del Servicio
rag_service = RAGService(vector_manager=vector_manager, chain_manager=chain_manager)

print("\n✨ Entorno de producción verificado. Escribe tu pregunta (escribe 'salir' para concluir).")

# Hilo de memoria conversacional local
memory_history = []

while True:
    question = input("\nPregunta: ")
    if question.lower() == "salir":
        logger.info("Sesión finalizada por el operador.")
        break
        
    # Ejecutamos la consulta a través del Servicio Unificado
    result = rag_service.execute_query(question, memory_history=memory_history)
    
    print("\nRespuesta:\n")
    print(result["answer"])
    
    # Despliegue corporativo estilizado de fuentes sin duplicados
    if result["sources"]:
        print("\n📚 Fuentes")
        for src in result["sources"]:
            print(src)
            
    print("-" * 80)
    
    # Alimentamos la memoria si la respuesta fue legítima y fundamentada
    if result["sources"]:
        memory_history.append(f"Usuario: {question}")
        memory_history.append(f"Asistente: {result['answer']}")
