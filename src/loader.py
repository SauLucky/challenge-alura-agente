from pathlib import Path
import pandas as pd
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader

class DocumentLoader:
    def __init__(self, data_path="data"):
        self.data_path = Path(data_path)

    def load_pdfs(self):
        documents = []
        pdf_path = self.data_path / "pdf"
        
        # Buscamos todos los archivos .pdf en la carpeta
        for pdf_file in pdf_path.glob("*.pdf"):
            print(f"📄 Cargando PDF: {pdf_file.name}")
            loader = PyPDFLoader(str(pdf_file))
            docs = loader.load()
            
            # Agregamos el metadato del nombre del archivo a cada página
            for doc in docs:
                doc.metadata["source_file"] = pdf_file.name
            
            # CORRECCIÓN: Guardamos las páginas fuera del bucle 'for doc'
            documents.extend(docs)
            
        return documents

    def load_excel(self):
        documents = []
        excel_path = self.data_path / "excel"
        
        # Buscamos todos los archivos de Excel en la carpeta
        for excel_file in excel_path.glob("*.xlsx"):
            print(f"📊 Cargando Excel: {excel_file.name}")
            df = pd.read_excel(excel_file)
            
            for index, row in df.iterrows():
                text = "\n".join(
                    f"{column}: {value}" for column, value in row.items() if pd.notna(value)
                )
                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source_file": excel_file.name,
                            "row": index + 1,
                            "type": "inventory"
                        }
                    )
                )
        return documents

    def load_all_documents(self):
        documents = []
        documents.extend(self.load_pdfs())
        documents.extend(self.load_excel())
        print(f"✨ Ingesta completada con éxito. Total de documentos cargados: {len(documents)}")
        return documents

if __name__ == "__main__":
    # Prueba del código estructurado en clase
    print("Probando el nuevo DocumentLoader estructurado...")
    loader = DocumentLoader()
    loader.load_all_documents()
