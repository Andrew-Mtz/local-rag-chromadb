# Pre-entrega 3 — RAG local

## Objetivo

Construir un sistema RAG con documentos `.txt` o `.md`, chunking, embeddings
locales, ChromaDB persistente, búsqueda semántica y una chain LangChain LCEL.
La generación se probará con Gemini y deberá estar fundamentada en los documentos,
con una respuesta Pydantic que contenga texto y referencias.

Estado actual: ingesta, recuperación semántica y generación con Gemini mediante
LCEL y salida Pydantic. Los documentos, embeddings y vectorstore son locales;
las consultas envían la pregunta y los fragmentos recuperados a la API de Gemini.

## Estructura

```text
pre-entrega3/
├── data/
│   └── .gitkeep
├── vectorstore/
│   └── .gitkeep
├── ingest.py
├── rag.py
├── schemas.py
├── main.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md
```

`data/` contendrá los documentos fuente. `vectorstore/` contendrá los archivos
generados por ChromaDB: su contenido se ignora en Git porque podrá regenerarse
mediante la ingesta. Se conserva `vectorstore/.gitkeep` para versionar la carpeta
vacía. También se ignoran `.env`, `.venv/`, `__pycache__/` y `*.pyc`.

## Instalación

Usar Python 3.11 o superior. Desde la raíz del proyecto, en PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Completar `GOOGLE_API_KEY` en `.env` con la clave propia de Gemini. Si se clona el
proyecto y no existe `.env`, crearlo con `Copy-Item .env.example .env`.

Configuración en `.env`:

```dotenv
GOOGLE_API_KEY=...
GEMINI_MODEL=gemini-3.5-flash
```

`GEMINI_MODEL` es opcional: si no está definido, está vacío o contiene solo
espacios, se usa `gemini-3.5-flash` por defecto.

Se usan las integraciones específicas `langchain-chroma`, `langchain-huggingface`
y `langchain-google-genai`. `langchain-chroma` instala ChromaDB como dependencia.
No se incluye OpenAI. Las versiones quedan sin fijar en esta estructura inicial.

## Ejecución y preguntas de prueba

Desde la raíz del proyecto, primero poblar la colección:

```powershell
python ingest.py
```

Luego iniciar la consulta por terminal:

```powershell
python main.py
```

Cada ejecución solicita una pregunta. `main.py` nunca ejecuta la ingesta ni
reindexa archivos. `rag.py` carga `technical_docs` desde `./vectorstore`, recupera
hasta tres chunks y ejecuta `prompt | llm | parser` con temperatura 0.
El modelo de generación se configura mediante `GEMINI_MODEL` en `.env`.

Preguntas con respuesta en los documentos:

- ¿Qué base de datos usa el sistema?
- ¿Cuál es el TTL de Redis?
- ¿Qué herramienta se utiliza para visualizar métricas?

Pregunta trampa:

- ¿Qué proveedor de pagos utiliza el sistema?

Para la pregunta trampa se espera exactamente este texto en `respuesta`:

> No tengo información suficiente para responder esa pregunta con los documentos disponibles.

El prompt exige usar solo el contexto; esto reduce alucinaciones, pero no es una
garantía factual. Pydantic valida la estructura, no la veracidad del texto.
Las fuentes se obtienen de la metadata real, se deduplican conservando su orden
y representan los documentos recuperados, no citas elegidas por Gemini.
`fragmentos_recuperados` indica cuántos chunks se recuperaron, no cuántos utilizó
efectivamente el modelo. Si no existe la base, la colección no carga o no hay
resultados, se devuelve el mismo texto con fuentes vacías y cero fragmentos.
