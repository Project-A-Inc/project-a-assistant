
import httpx
from typing import Any, Dict, List
from ..config import get_settings
_SETTINGS = get_settings()
async def mcp_call(tool_name: str, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    url = f"{_SETTINGS.mcp_base_url}/tools/{tool_name}"
    headers = {"Authorization": f"Bearer {_SETTINGS.mcp_api_key}", "User-ID": _SETTINGS.default_user_id}
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()
