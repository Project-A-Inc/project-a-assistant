import json
from typing import List
from azure.storage.blob import BlobServiceClient
from langchain_core.documents import Document
from ..config import get_settings

_SETTINGS = get_settings()
ORG = _SETTINGS.default_org_id
USER = _SETTINGS.default_user_id
AZURE_CONNECTION_STRING = _SETTINGS.azure_storage_connection_string
BLOB_CONTAINER = _SETTINGS.blob_container

def get_memory_blob_path(chat_id: str) -> str:
    """Returns the path for long-term memory blob."""
    return f"{ORG}/{USER}/{chat_id}/longterm_memory.json"

def get_history_blob_path(chat_id: str) -> str:
    """Returns the path for chat history blob."""
    return f"{ORG}/{USER}/{chat_id}/chat_history.json"

def load_memories_from_blob(chat_id: str) -> List[Document]:
    """Loads long-term memory documents from Azure Blob Storage."""
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=BLOB_CONTAINER, blob=get_memory_blob_path(chat_id))
    try:
        data = blob_client.download_blob().readall()
        memories = json.loads(data)
        docs = [Document(**doc) for doc in memories]
        return docs
    except Exception:
        return []

def save_memories_to_blob(vectorstore, chat_id: str):
    """Saves all documents from the vector store to Azure Blob Storage."""
    docs = vectorstore.as_retriever().get_relevant_documents("")
    docs_as_dicts = [doc.dict() for doc in docs]
    data = json.dumps(docs_as_dicts, ensure_ascii=False, indent=2)
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=BLOB_CONTAINER, blob=get_memory_blob_path(chat_id))
    blob_client.upload_blob(data, overwrite=True)

def load_chat_history(chat_id: str) -> list:
    """Loads chat history from Azure Blob Storage."""
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=BLOB_CONTAINER, blob=get_history_blob_path(chat_id))
    try:
        data = blob_client.download_blob().readall()
        return json.loads(data)
    except Exception:
        return []

def save_chat_history(chat_id: str, history: list):
    """Saves chat history to Azure Blob Storage."""
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=BLOB_CONTAINER, blob=get_history_blob_path(chat_id))
    data = json.dumps(history, ensure_ascii=False, indent=2)
    blob_client.upload_blob(data, overwrite=True)
