from src.embeddings import EmbeddingModel
from src.vectorstore import VectorStoreManager
from src.rag_chain import RAGChain

print("🤖 Inicializando el motor del agente inteligente RAG...")
embeddings = EmbeddingModel().get_model()
vector_manager = VectorStoreManager(embeddings)
vectorstore = vector_manager.load()

# Configuramos el retriever para jalar los 5 fragmentos más cercanos semánticamente
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)

# Inicializamos nuestro agente profesional
agent = RAGChain(retriever)

print("\n✨ ¡Agente listo! Escribe tu pregunta. Para salir escribe la palabra: salir")
while True:
    question = input("\nPregunta: ")
    if question.lower() == "salir":
        print("Saliendo del validador... ¡Buen trabajo!")
        break
        
    response = agent.ask(question)
    print("\nRespuesta:\n")
    print(response)
    print("-" * 60)
