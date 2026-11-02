"""Ingesta local de documentos en ChromaDB, sin retrieval ni RAG."""

from functools import lru_cache
from pathlib import Path

import chromadb
from chromadb.errors import NotFoundError
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from transformers import AutoTokenizer

DATA_DIR = Path("./data")
PERSIST_DIR = "./vectorstore"
COLLECTION_NAME = "technical_docs"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embeddings() -> HuggingFaceEmbeddings:
    """Crear una única instancia reutilizable cuando se necesite."""
    return HuggingFaceEmbeddings(model_name=MODEL_NAME)


def ingest() -> Chroma:
    """Crear el índice o cargar la colección existente sin reindexar."""
    files = sorted(
        path for path in DATA_DIR.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".txt"}
    )
    print(f"Archivos encontrados: {len(files)}")

    # Una carpeta con .gitkeep no constituye un índice existente.
    client = chromadb.PersistentClient(path=PERSIST_DIR)
    try:
        collection = client.get_collection(COLLECTION_NAME)
    except NotFoundError:
        collection = None

    if collection is not None and collection.count() > 0:
        print(f"Cargando índice existente: {COLLECTION_NAME}")
        print("Chunks generados: 0 (se reutiliza el índice persistido)")
        store = Chroma(
            client=client,
            collection_name=COLLECTION_NAME,
            persist_directory=PERSIST_DIR,
            create_collection_if_not_exists=False,
        )
        print(f"Chunks almacenados en la colección: {collection.count()}")
        return store

    if not files:
        raise ValueError(f"No hay documentos .md o .txt en {DATA_DIR.resolve()}")

    documents = [
        Document(
            page_content=path.read_text(encoding="utf-8"),
            metadata={"source": path.as_posix()},
        )
        for path in files
    ]
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        tokenizer, chunk_size=500, chunk_overlap=50,
    )
    chunks = splitter.split_documents(documents)
    print(f"Chunks generados: {len(chunks)}")
    if not chunks:
        raise ValueError("Los documentos no contienen texto para indexar.")

    # Se miden tokens, no caracteres. El overlap puede ser menor según los
    # separadores naturales. MiniLM trunca por defecto a 256 tokens para los
    # embeddings; Chroma conserva el texto completo del chunk de ~500 tokens.
    print(f"Creando índice nuevo: {COLLECTION_NAME}")
    store = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        client=client,
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIR,
    )
    # La persistencia es automática: no hace falta llamar a persist().
    count = client.get_collection(COLLECTION_NAME).count()
    print(f"Chunks almacenados en la colección: {count}")
    return store


if __name__ == "__main__":
    ingest()
