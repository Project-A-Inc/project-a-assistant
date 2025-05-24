import uuid
from langchain.tools import DuckDuckGoSearchRun, tool
from langchain_core.documents import Document
from ..config import get_settings

_SETTINGS = get_settings()
ORG = _SETTINGS.default_org_id
USER = _SETTINGS.default_user_id

def build_personal_memory_tools(vector_store):
    """Builds personal memory tools: save and search recall memory."""
    @tool
    def save_recall_memory(memory: str) -> str:
        """
        Save a new memory to the user's personal long-term memory vector store for cross-session recall.
        """
        doc = Document(page_content=memory, id=str(uuid.uuid4()),
                       metadata={"org": ORG, "user": USER})
        vector_store.add_documents([doc])
        return "Memory saved!"

    @tool
    def search_recall_memories(query: str):
        """
        Search the user's personal long-term memory for relevant information using a semantic query.
        """
        docs = vector_store.similarity_search(
            query, k=5,
            filter=lambda d: d.metadata.get("org") == ORG and d.metadata.get("user") == USER
        )
        return [d.page_content for d in docs]

    duck_search = DuckDuckGoSearchRun()

    return duck_search, search_recall_memories, save_recall_memory
