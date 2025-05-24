# import json
# import types
# import pytest
# from langchain_core.messages import HumanMessage

# import project_a_assistant.graph as graph_mod

# CASES = [
#     ("Hello",
#      {"tools": []},
#      []),

#     ("Show me stalled deals this quarter.",
#      {"tools": ["mcp_query"]},
#      ["mcp_query"]),

#     ("Latest funding news for Acme Corp.",
#      {"tools": ["web_search"]},
#      ["web_search"]),

#     ("Compare our open opportunities with Acme’s recent press releases.",
#      {"tools": ["web_search", "mcp_query"]},
#      ["web_search", "mcp_query"]),

#     ("Explain what MEDDIC stands for.",
#      {"tools": []},
#      []),
# ]

# @pytest.mark.asyncio
# @pytest.mark.parametrize("msg, mock_json, expected", CASES)
# async def test_route_tools(monkeypatch, msg, mock_json, expected):
#     """Router should output exactly expected subset of tools."""
#     # Pretend MCP is configured
#     monkeypatch.setattr(
#         graph_mod,
#         "_SETTINGS",
#         types.SimpleNamespace(has_mcp=True, llm_temperature=0)
#     )
#     # Ensure both tool names exist in the map
#     graph_mod._TOOL_MAP.setdefault("web_search", object())
#     graph_mod._TOOL_MAP.setdefault("mcp_query", object())

#     # # Stub the LLM classifier
#     # async def fake_chat(*_, **__):
#     #     return json.dumps(mock_json)
#     # monkeypatch.setattr(graph_mod, "chat", fake_chat)

#     state = {"user_message": HumanMessage(content=msg)}
#     new_state = await graph_mod.route_tools(state)

#     assert new_state["tools_to_call"] == expected
