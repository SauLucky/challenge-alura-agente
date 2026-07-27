from src.loader import DocumentLoader

# Inicializamos el cargador estructurado
loader = DocumentLoader()
documents = loader.load_all_documents()

print("\n" + "="*60)
print("🔍 VALIDACIÓN DE METADATOS EN PROCESO")
print("="*60)

# Buscaremos un ejemplo de cada tipo en la lista completa para verificar su estructura
ejemplo_pdf = None
ejemplo_excel = None

for doc in documents:
    # Detectamos formato PDF por los metadatos que inyecta PyPDFLoader
    if "page" in doc.metadata and not ejemplo_pdf:
        ejemplo_pdf = doc
    # Detectamos formato Excel por la bandera "type" que definimos en la clase
    if doc.metadata.get("type") == "inventory" and not ejemplo_excel:
        ejemplo_excel = doc
    
    # Si ya encontramos ambos ejemplos, rompemos el bucle
    if ejemplo_pdf and ejemplo_excel:
        break

# Imprimimos los resultados del análisis en pantalla
if ejemplo_pdf:
    print("\n[✓] METADATOS DETECTADOS PARA PDFs:")
    print({
        "page": ejemplo_pdf.metadata.get("page"),
        "source_file": ejemplo_pdf.metadata.get("source_file")
    })
else:
    print("\n[×] No se encontraron metadatos válidos de archivos PDF.")

if ejemplo_excel:
    print("\n[✓] METADATOS DETECTADOS PARA EXCEL:")
    print({
        "source_file": ejemplo_excel.metadata.get("source_file"),
        "row": ejemplo_excel.metadata.get("row"),
        "type": ejemplo_excel.metadata.get("type")
    })
else:
    print("\n[×] No se encontraron metadatos válidos de archivos Excel.")

print("\n" + "="*60)
