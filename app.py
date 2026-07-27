from src.loader import DocumentLoader
from src.splitter import DocumentSplitter

# 1. Ingesta de datos (Sprint 1)
loader = DocumentLoader()
documents = loader.load_all_documents()

# 2. Chunking Inteligente (Sprint 2)
splitter = DocumentSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(documents)

print("\n" + "=" * 60)
print(f"📊 Documentos originales: {len(documents)}")
print(f"📊 Chunks generados: {len(chunks)}")
print("=" * 60)

# 3. Pruebas rápidas (Inspección manual de los primeros 3 chunks)
print("\n🔍 INSPECCIÓN DE FRAGMENTOS INDIVIDUALES:")
for i in range(min(3, len(chunks))):
    print("\n" + "=" * 60)
    print(f"🧩 Chunk {i+1}")
    print("=" * 60)
    print(f"📋 Metadatos: {chunks[i].metadata}")
    print(f"\n📝 Contenido (Primeros 400 caracteres):\n{chunks[i].page_content[:400]}")
    print("-" * 60)
