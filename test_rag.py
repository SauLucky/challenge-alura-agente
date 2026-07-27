from src.embeddings import EmbeddingModel
from src.vectorstore import VectorStoreManager
from src.rag_chain import RAGChain
from src.utils import logger

logger.info("Inicializando el motor del agente inteligente RAG Profesional...")

# 1. Recuperamos modelos e índices usando el nuevo esquema de configuración
embeddings = EmbeddingModel().get_model()
vector_manager = VectorStoreManager(embeddings)
retriever = vector_manager.load()

# 2. Inicializamos la cadena empresarial
agent = RAGChain(retriever)

logger.info("¡Agente empresarial listo para operar!")
print("\n✨ Sistema operativo. Escribe tu pregunta o escribe 'salir' para concluir.")

# Simulación de memoria conversacional simple por consola
historial_conversacion = []

while True:
    question = input("\nPregunta: ")
    if question.lower() == "salir":
        logger.info("Cierre de sesión interactivo solicitado por el operador.")
        break
        
    # Compilamos el hilo histórico previo
    chat_history_str = "\n".join(historial_conversacion[-4:]) # Mantiene memoria de los últimos 2 turnos
    
    # Invocamos la cadena estructurada
    result = agent.ask(question, chat_history=chat_history_str)
    
    print("\nRespuesta:\n")
    print(result["answer"])
    
    # MEJORA 1 y 3: Impresión limpia de Fuentes Consultadas verificadas
    if result["sources"]:
        print("\n📚 Fuentes consultadas:")
        for src in result["sources"]:
            print(src)
            
    print("-" * 60)
    
    # Guardamos en la memoria conversacional si la respuesta fue válida
    if result["sources"]:
        historial_conversacion.append(f"Usuario: {question}")
        historial_conversacion.append(f"Asistente: {result['answer']}")