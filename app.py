import streamlit as st
from src.embeddings import EmbeddingModel
from src.vectorstore import VectorStoreManager
from src.rag_chain import RAGChain
from src.rag_service import RAGService
from src.logger import logger

# 1. Configuración de la página web (Título e Icono)
st.set_page_config(
    page_title="Mercado Central 24h - Asistente RAG",
    page_icon="🤖",
    layout="wide"
)

# 2. Inicialización del Backend en la Caché de Streamlit (Para que cargue una sola vez y sea ultra veloz)
@st.cache_resource
def initialize_rag_system():
    logger.info("Iniciando orquestación del sistema RAG desde la interfaz Streamlit...")
    embeddings = EmbeddingModel().get_model()
    vector_manager = VectorStoreManager(embeddings)
    retriever = vector_manager.load()
    chain_manager = RAGChain()
    return RAGService(vector_manager=vector_manager, chain_manager=chain_manager)

try:
    rag_service = initialize_rag_system()
except Exception as e:
    st.error(f"❌ Error crítico al inicializar el sistema: {e}")
    st.stop()

# 3. Panel Lateral Informativo (Sidebar)
with st.sidebar:
    st.title("📚 Panel de Control")
    st.subheader("Challenge Alura Agente — ONE")
    st.write("Asistente RAG Corporativo de nivel empresarial con control estricto de alucinaciones y métricas de relevancia.")
    
    st.markdown("---")
    st.markdown("**Base de Conocimiento Indexada:**")
    st.caption("✓ Política de Atención al Cliente (PDF)")
    st.caption("✓ Manual de Proveedores (PDF)")
    st.caption("✓ Reglamento Interno (PDF)")
    st.caption("✓ FAQ — Preguntas Frecuentes (PDF)")
    st.caption("✓ Inventario de Supermercado (Excel)")
    
    st.markdown("---")
    # Botón dinámico para resetear el historial conversacional en memoria
    if st.button("🔄 Limpiar Conversación", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.memory_history = []
        st.rerun()

# 4. Inicialización de la memoria de sesión de Streamlit
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Para renderizar en pantalla estilo ChatGPT
if "memory_history" not in st.session_state:
    st.session_state.memory_history = []  # Hilo histórico conversacional para el LLM

# 5. Encabezado principal de la pantalla
st.title("🤖 Asistente Inteligente RAG — Mercado Central 24h")
st.write("Consulta cualquier duda sobre políticas, normativas, operaciones o inventarios institucionales.")

# 6. Renderizar los mensajes del historial acumulado (Estilo ChatGPT)
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Si el mensaje es de la IA y tiene fuentes, las desplegamos de forma estética
        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("📚 Ver Fuentes de Sustento y Relevancia"):
                for src in message["sources"]:
                    st.caption(src)

# 7. Caja de entrada de texto del usuario (Chat Input)
if user_question := st.chat_input("Escribe tu consulta aquí..."):
    
    # Renderizamos la pregunta del usuario en pantalla de inmediato
    with st.chat_message("user"):
        st.markdown(user_question)
    st.session_state.chat_history.append({"role": "user", "content": user_question})

    # Llamamos a nuestro Servicio unificado del backend con animación de carga
    with st.chat_message("assistant"):
        with st.spinner("Consultando base vectorial y generando respuesta fundamentada..."):
            
            # Invocamos la lógica del refactor 4.1 enviando la memoria histórica de sesión
            result = rag_service.execute_query(
                user_question, 
                memory_history=st.session_state.memory_history
            )
            
            # Desplegamos la respuesta del agente
            st.markdown(result["answer"])
            
            # Desplegamos las fuentes limpias con un expander colapsable elegante
            if result["sources"]:
                with st.expander("📚 Ver Fuentes de Sustento y Relevancia"):
                    for src in result["sources"]:
                        st.caption(src)
                        
    # Registramos la respuesta en el historial visual
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": result["answer"],
        "sources": result["sources"]
    })
    
    # Si la respuesta fue válida y fundamentada, alimentamos la memoria conversacional
    if result["sources"]:
        st.session_state.memory_history.append(f"Usuario: {user_question}")
        st.session_state.memory_history.append(f"Asistente: {result['answer']}")
