from __future__ import annotations
import asyncio
import json
from typing import Any, Dict, List, TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.tools import Tool
from langchain_core.messages import AIMessage, BaseMessage, SystemMessage, HumanMessage
from .config import get_settings
from .prompts import load_prompt
from .utils import safe_json_list, truncate
from .validators import gatekeeper
from .tools import web_search, mcp_client
from .llm_client import chat


class AgentState(TypedDict):
    user_message: str
    output_messages: List[BaseMessage]
    tools_to_call: List[str]
    tool_outputs: Dict[Any, str | None]



_SETTINGS = get_settings()

# Define tools
WEB_SEARCH_TOOL = Tool(
    name="web_search",
    description="Search public web via DuckDuckGo",
    func=lambda q: web_search.search(q)
)

TOOLS = [WEB_SEARCH_TOOL]
_TOOL_MAP = {"web_search": WEB_SEARCH_TOOL}

if _SETTINGS.has_mcp:
    MCP_TOOL = Tool(
        name="mcp_query",
        description="Query internal sources via FastMCP",
        func=lambda payload: mcp_client.mcp_call(payload.get("tool"), payload)
    )
    TOOLS.append(MCP_TOOL)
    _TOOL_MAP["mcp_query"] = MCP_TOOL

# Load prompts
SYSTEM_PROMPT = load_prompt("assistant_system")
ROUTER_PROMPT = load_prompt("tool_router")


# Node: Validate message
async def validate(state: AgentState) -> AgentState:
    # Pull out the last message in the conversation
    last_msg = state["user_message"]

    # If it’s not allowed, append an assistant reply and return
    if not await gatekeeper.is_message_allowed(last_msg):
        state.output_messages.append(
            AIMessage(content="Sorry—outside my scope.")
        )
        return state

    # Otherwise normalize in place
    last_msg.content = gatekeeper.normalize(last_msg)
    return state


# Node: Route tools
async def route_tools(state: AgentState) -> AgentState:
    last_msg = state.user_message
    messages = [
        SystemMessage(content= ROUTER_PROMPT),
        HumanMessage(content= last_msg)
    ]
    raw = await chat(messages, temperature=0)
    state.tools_to_call = [t for t in safe_json_list(raw) if t in _TOOL_MAP]
    return state


# Node: Call tools and collect outputs
async def collect_tools(state: AgentState) -> AgentState:
    async def _call(name: str):
        last_msg = state.user_message
        tool = _TOOL_MAP[name]
        if name == "web_search":
            return tool.func(last_msg.content)
        if name == "mcp_query":
            return tool.func({"tool": "crm.search", "query": last_msg.content})

    outs = await asyncio.gather(*[_call(t) for t in state.tools_to_call]) if state.tools_to_call else []
    state.tool_outputs = dict(zip(state.tools_to_call, outs))
    return state


# Node: Generate LLM answer
async def llm_answer(state: AgentState) -> AgentState:
    context_json = json.dumps(state.tool_outputs, ensure_ascii=False, indent=2) if state.tool_outputs else ""
    context = f"Tool results:\n{truncate(context_json)}" if context_json else ""
    last_msg = state.user_message
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        SystemMessage(content=context),
        HumanMessage(content=last_msg)
    ]
    answer = await chat(messages)
    state.output_messages.append(
        AIMessage(content=answer)
    )
    
    return state


# Node: Append next steps
def next_steps(state: AgentState) -> AgentState:
    addon = "\n\n**Next steps:** _Visualize metrics_, _Export CSV_, _Schedule follow-up_."
    state.output_messages.append(
        AIMessage(content=addon)
    )
    return state


# Build LangGraph
def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    graph.add_node("validate", validate)
    graph.add_node("route_tools", route_tools)
    graph.add_node("collect_tools", collect_tools)
    graph.add_node("llm_answer", llm_answer)
    graph.add_node("next_steps", next_steps)

    graph.set_entry_point("validate")
    graph.add_conditional_edges(
        "validate",
        lambda s: not s["output_messages"],
        {
        True:  "route_tools",  # if output_messages is empty → go on
        False: END            # if not empty → end immediately
        }
    )
    graph.add_edge("route_tools", "collect_tools")
    graph.add_edge("collect_tools", "llm_answer")
    graph.add_edge("llm_answer", "next_steps")

    return graph
