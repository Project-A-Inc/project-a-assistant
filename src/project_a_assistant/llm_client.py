# src/project_a_assistant/llm_client.py
"""Async wrapper around LangChain `ChatOpenAI` (Azure deployment)."""

from typing import List, Any

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
)

from .config import get_settings

_SETTINGS = get_settings()

# Re-usable async client
_llm = AzureChatOpenAI(
    azure_endpoint=str(_SETTINGS.azure_endpoint),
    azure_deployment=_SETTINGS.azure_deployment,
    api_key=_SETTINGS.azure_key,
    api_version="2024-02-15-preview",
    temperature=_SETTINGS.llm_temperature,
    max_tokens=_SETTINGS.llm_max_tokens,
)


# --- public async wrapper ----------------------------------------------------
async def chat(messages: List[BaseMessage], **kwargs: Any) -> AIMessage:
    """
    Send messages to Azure-hosted OpenAI and return the full AIMessage.

    Returns
    -------
    AIMessage
        LangChain message containing `.content` plus metadata.
    """
    llm = _llm.bind(
        temperature=kwargs.get("temperature", _SETTINGS.llm_temperature),
        max_tokens=kwargs.get("max_tokens", _SETTINGS.llm_max_tokens),
        top_p=kwargs.get("top_p", _SETTINGS.llm_top_p),
    )
    reply: AIMessage = await llm.ainvoke(messages)
    return reply