# 🤖 Asistente Inteligente RAG — Mercado Central 24h

Este repositorio contiene la implementación de un **Asistente Inteligente Empresarial basado en RAG (Retrieval-Augmented Generation)** desarrollado para el **Challenge Alura Agente – ONE IA for Tech** en colaboración con **Alura Latam y Oracle**.

El agente procesa lenguaje natural para responder consultas corporativas complejas, fundamentando cada respuesta exclusivamente en la documentación interna de la compañía ficticia *Mercado Central 24h*, incluyendo manuales de proveedores, reglamentos, bases de datos de inventario y políticas de servicio.

---

## 📽️ Demostración Funcional
Puedes ver el video completo con el funcionamiento de la aplicación y la interfaz interactiva aquí:
▶️ **[Ver Video Demostrativo en YouTube](https://youtu.be/PzfcRIKo8Qc)**

---

## 🏗️ Arquitectura Modular del Sistema
El proyecto se diseñó bajo una arquitectura desacoplada y orientada a servicios, garantizando escalabilidad, facilidad de pruebas y alta cohesión.

```text
Documentos Base (.pdf, .xlsx) 
      │
      ▼
src/loader.py ──► [DocumentLoader: Ingesta unificada y extracción de metadatos]
      │
      ▼
src/splitter.py ──► [DocumentSplitter: Segmentación inteligente con RecursiveCharacterTextSplitter]
      │
      ▼
src/vectorstore.py ──► [VectorStoreManager: Generación por bloques (Límites API) y persistencia en disco]
      │
      ▼
[ vector_db / ] ◄──► [Caché en Memoria RAM para aceleración del Retriever MMR]
      │
      ▼
src/rag_service.py ◄──► [RAGService: Control conversacional, validación, desduplicación de fuentes e historial]
      │
      ▼
src/rag_chain.py ──► [RAGChain: Inicialización del modelo gemini-2.5-flash vía API v1]
      │
      ▼
app.py ──► [Streamlit: Interfaz gráfica web con memoria de sesión st.session_state]
```

---

## ✨ Características y Mejoras de Nivel Empresarial

* **🛡️ Control Estricto de Alucinaciones:** Prompt Engineering avanzado con candados de seguridad en el backend. Si la consulta del usuario no se encuentra en el contexto indexado, el agente responde de forma restrictiva y estandarizada, evitando respuestas inventadas.
* **⚡ Caché del Índice Vectorial:** La base de datos vectorial FAISS se carga en la memoria RAM una sola vez al inicializar el entorno. Esto elimina llamadas repetitivas al disco duro y reduce drásticamente los tiempos de respuesta en la web.
* **📊 Búsqueda Semántica MMR (Maximal Marginal Relevance):** El retriever evalúa la diversidad semántica entre fragmentos para evitar enviarle información redundante o duplicada al modelo generativo.
* **📚 Citas de Fuentes y Métricas de Relevancia:** Las fuentes consultadas se desduplican y agrupan en tiempo real. La interfaz despliega las páginas exactas consultadas y calcula el porcentaje matemático de confianza de la búsqueda.
* **💬 Memoria Conversacional Continua:** Mantiene el hilo histórico de la sesión mediante el estado de Streamlit (`st.session_state`), permitiendo realizar preguntas de seguimiento contextuales de forma natural.
* **📝 Logging Corporativo Centralizado:** Bitácora profesional que registra marcas de tiempo, advertencias de cuota y diagnósticos en una consola limpia y en un archivo físico (`logs/production.log`).

---

## 🛠️ Tecnologías Utilizadas
* **Lenguaje:** Python 3.10+
* **Orquestación LLM:** LangChain
* **Modelo Generativo:** Google Gemini 2.5 Flash (API v1)
* **Vectores y Búsqueda:** Google Embeddings (text-embedding-004) & FAISS Vector Store
* **Interfaz Gráfica:** Streamlit
* **Manipulación de Datos y PDF:** Pandas, PyPDF, Openpyxl

---

## 🚀 Instalación y Uso Local

Sigue estos pasos para clonar el repositorio e inicializar el agente en tu entorno de desarrollo:

### 1. Clonar el repositorio y acceder a la raíz
```bash
git clone https://github.com
cd challenge-alura-agente
```

### 2. Configurar el Entorno Virtual e Instalar Dependencias
```bash
python -m venv .venv
# Activar en Windows (CMD):
.venv\Scripts\activate
# Instalar los paquetes oficiales:
pip install -r requirements.txt
```

### 3. Configurar las Variables de Entorno
Crea un archivo llamado `.env` en la raíz del proyecto e introduce tu clave de Google AI Studio:
```env
GOOGLE_API_KEY=tu_api_key_aqui
```

### 4. Inicializar y Ejecutar la Aplicación Web
```bash
streamlit run app.py
```
Abre en tu navegador la dirección local provista por la consola: `http://localhost:8501`.

---

## 🙌 Agradecimientos
Agradezco enormemente a **Alura Latam**, **Oracle Next Education (ONE)** y a todo el cuerpo de instructores del programa **ONE IA for Tech** por la mentoría, el diseño de este reto y la oportunidad de construir soluciones reales y escalables impulsadas por la Inteligencia Artificial Generativa.
