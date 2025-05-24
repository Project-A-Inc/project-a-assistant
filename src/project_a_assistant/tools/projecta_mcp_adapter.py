# src/project_a_assistant/tools/projecta_mcp_adapter.py

from typing import Dict, Any, List
from functools import partial

from langchain_core.tools import StructuredTool, Tool

async def load_mcp_tools_with_pinning(pin_config: Dict[str, Dict[str, Any]] = None) -> List:
    """
    Loads all MCP tools and pins (locks) specified arguments based on pin_config.
    For tools listed in pin_config, those arguments will be fixed and hidden from the LLM.
    """
    from langchain_mcp_adapters.client import MultiServerMCPClient
    from ..config import get_settings

    _SETTINGS = get_settings()
    client = MultiServerMCPClient(
        {
            "primary": {
                "url": _SETTINGS.mcp_base_url,
                "transport": "streamable_http",
                "headers": {
                    _SETTINGS.mcp_api_header: _SETTINGS.mcp_api_key,
                },
            }
        }
    )
    tools = await client.get_tools()

    if not pin_config:
        return tools

    pinned_tools = []
    for t in tools:
        if t.name in pin_config:
            # Handle pinning for StructuredTool
            t = pin_structured_tool(t, pin_config[t.name])
        pinned_tools.append(t)

    return pinned_tools


def pin_structured_tool(tool, pin_args: dict):
    """
    Returns a copy of the StructuredTool with pinned arguments (for StructuredTool from MCP).
    Pinned arguments are injected at runtime and hidden from the LLM.
    """
    if isinstance(tool, StructuredTool):
        old_coroutine = tool.coroutine

        async def wrapper(**kwargs):
            # Merge pinned and provided arguments
            merged = {**pin_args, **kwargs}
            return await old_coroutine(**merged)

        # Prepare the new args_schema for LLM (remove pinned args)
        args_schema = dict(tool.args_schema)
        args_schema['properties'] = dict(args_schema.get('properties', {}))
        for key in pin_args:
            args_schema['properties'].pop(key, None)
        if "required" in args_schema:
            args_schema["required"] = [r for r in args_schema["required"] if r not in pin_args]
            if not args_schema["required"]:
                del args_schema["required"]

        # Rebuild the tool with the wrapper and modified schema
        return StructuredTool(
            name=tool.name,
            description=tool.description,
            args_schema=args_schema,
            coroutine=wrapper,
            response_format=getattr(tool, "response_format", "content_and_artifact"),
            metadata=getattr(tool, "metadata", None),
        )
    # Fallback for Tool or other types (shouldn't happen in MCP context)
    return tool

