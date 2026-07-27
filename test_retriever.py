from src.embeddings import EmbeddingModel
from src.vectorstore import VectorStoreManager

print("Cargando modelo de embeddings...")
embeddings = EmbeddingModel().get_model()
vector_manager = VectorStoreManager(embeddings)

print("Cargando índice FAISS...")
vectorstore = vector_manager.load()

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

question = "¿Cuál es la política de devoluciones?"
print(f"\nPregunta: {question}")

results = retriever.invoke(question)
print("\nResultados encontrados:\n")

for i, doc in enumerate(results, start=1):
    print("=" * 80)
    print(f"Resultado {i}")
    print(f"Archivo: {doc.metadata.get('source_file')}")
    print(f"Página/Fila: {doc.metadata.get('page', doc.metadata.get('row'))}")
    print("-" * 80)
    print(doc.page_content[:500])
    print("=" * 80)