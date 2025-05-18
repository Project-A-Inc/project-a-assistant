
"""Async wrapper for Azure OpenAI Chat Completion."""
import httpx, json
from typing import List, Dict, Any
from .config import get_settings

_SETTINGS = get_settings()

async def chat(messages: List[Dict[str,str]], **kwargs) -> str:
    url = f"{_SETTINGS.azure_endpoint}openai/deployments/{_SETTINGS.azure_deployment}/chat/completions?api-version=2024-02-15-preview"
    headers = {"api-key": _SETTINGS.azure_key, "Content-Type": "application/json"}
    payload: Dict[str, Any] = {
        "messages": messages,
        "max_tokens": kwargs.get("max_tokens", _SETTINGS.llm_max_tokens),
        "temperature": kwargs.get("temperature", _SETTINGS.llm_temperature),
        "top_p": kwargs.get("top_p", _SETTINGS.llm_top_p),
    }
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
