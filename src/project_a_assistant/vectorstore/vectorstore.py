from langchain_core.vectorstores import InMemoryVectorStore
from ..llm.llm_client import get_embeddings
from ..memory.longterm_memory import load_memories_from_blob

def build_vector_store_for_chat(chat_id: str):
    """Initializes and loads InMemoryVectorStore for the session."""
    embeddings = get_embeddings()
    vector_store = InMemoryVectorStore(embeddings)
    loaded_docs = load_memories_from_blob(chat_id)
    if loaded_docs:
        vector_store.add_documents(loaded_docs)
    return vector_store
