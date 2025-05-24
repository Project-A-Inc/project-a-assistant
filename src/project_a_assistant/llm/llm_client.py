from typing import List
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
)
from ..config import get_settings

_SETTINGS = get_settings()

llm = AzureChatOpenAI(
    azure_endpoint=str(_SETTINGS.azure_endpoint),
    azure_deployment=_SETTINGS.azure_deployment,
    api_key=_SETTINGS.azure_key,
    api_version="2024-02-15-preview",
    temperature=_SETTINGS.llm_temperature,
    max_tokens=_SETTINGS.llm_max_tokens,
)

def get_embeddings():
    return AzureOpenAIEmbeddings(
        deployment="text-embedding-3-small",
        api_key=_SETTINGS.azure_key,
        azure_endpoint=str(_SETTINGS.azure_endpoint),
        openai_api_version="2023-05-15"
    )

# --- public async wrapper ----------------------------------------------------
async def chat(messages: List[BaseMessage], **kwargs: any) -> AIMessage:
    """
    Send messages to Azure-hosted OpenAI and return the full AIMessage.

    Returns
    -------
    AIMessage
        LangChain message containing `.content` plus metadata.
    """
    _llm = llm.bind(
        temperature=kwargs.get("temperature", _SETTINGS.llm_temperature),
        max_tokens=kwargs.get("max_tokens", _SETTINGS.llm_max_tokens),
        top_p=kwargs.get("top_p", _SETTINGS.llm_top_p),
    )
    reply: AIMessage = await _llm.ainvoke(messages)
    return reply