import requests
from langchain.tools import tool
from ..config import get_settings

_SETTINGS = get_settings()

def make_context_search_tool(index_name: str, community_level: int):
    endpoint = f"{_SETTINGS.mcp_base_url}"

    headers = {
        _SETTINGS.mcp_api_header: _SETTINGS.mcp_api_key,
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }

    @tool
    def context_search(query: str) -> str:
        """
        Knowledge-graph context search via Data Catalog /context.
        This tool searches the internal MCP knowledge base (emails, chat history, documents) for information relevant to the query.
        """
        payload = {
            "index_name": index_name,
            "query": query,
            "community_level": community_level,
        }
        try:
            response = requests.post(endpoint, headers=headers, json=payload, timeout=20)
            response.raise_for_status()
            try:
                return response.json()
            except Exception:
                return response.text
        except Exception as e:
            return f"Error querying MCP: {e}"
    return context_search
