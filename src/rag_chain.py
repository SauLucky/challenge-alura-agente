from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.prompts import RAG_PROMPT

class RAGChain:
    def __init__(self, retriever):
        self.retriever = retriever
        # Forzamos api_version="v1" para que gemini-2.5-flash funcione de inmediato
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            api_version="v1"
        )
        # Construcción de la cadena unificada LCEL solicitada por la guía de Alura
        self.chain = (
            {
                "context": self.retriever,
                "question": RunnablePassthrough()
            }
            | RAG_PROMPT
            | self.llm
            | StrOutputParser()
        )

    def ask(self, question):
        """Envía la pregunta al pipeline RAG y devuelve la respuesta del modelo."""
        return self.chain.invoke(question)
