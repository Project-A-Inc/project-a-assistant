from langgraph.graph import StateGraph, END
from .state import AgentState
from ..vectorstore.vectorstore import build_vector_store_for_chat
from ..memory.longterm_memory import (
    save_memories_to_blob, save_chat_history, load_chat_history
)
from ..tools.memory_tool import build_personal_memory_tools
from ..tools.projecta_mcp_adapter import load_mcp_tools_with_pinning

# Import node functions
from .nodes.gatekeeper_node import gatekeeper_node
from .nodes.load_memories_node import load_memories_node
from .nodes.core_agent_node import core_agent_node
from .nodes.next_steps_node import next_steps_node
from .nodes.refuse_node import refuse_node

from langchain_core.messages import (
    HumanMessage,
)


async def build_tools(vector_store, index_id: str):
    """Builds the complete set of tools for the agent, including MCP tools."""
    duck_search, search_recall_memories, save_recall_memory = build_personal_memory_tools(vector_store)

    pin_cfg = {
        "context_search": {
            "index_name": index_id,
            "community_level": 2
        }
    }
    mcp_tools = await load_mcp_tools_with_pinning(pin_cfg)
    mcp_tools_dict = {tool.name: tool for tool in mcp_tools}
    
    return {
        "search": duck_search,
        "search_recall_memories": search_recall_memories,
        "save_recall_memory": save_recall_memory,
        **mcp_tools_dict,
    }

async def build_agent_for_chat(chat_id: str, index_id: str):
    """Builds the agent's state graph and vector store for a given session."""
    vector_store = build_vector_store_for_chat(chat_id)
    tools = await build_tools(vector_store, index_id)

    async def load_memories_node_async(state):
        return await load_memories_node(state, tools)

    async def core_agent_node_async(state):
        return await core_agent_node(state, list(tools.values()))
    

    graph = StateGraph(AgentState)
    graph.add_node("gatekeeper", gatekeeper_node)
    graph.add_node("load_memories", load_memories_node_async)
    graph.add_node("core_agent", core_agent_node_async)
    graph.add_node("next_steps", next_steps_node)
    graph.add_node("refuse", refuse_node)

    graph.set_entry_point("gatekeeper")

    def gatekeeper_edge(state: AgentState):
        return "load_memories" if state["safe"] else "refuse"
    graph.add_conditional_edges(
        "gatekeeper", gatekeeper_edge, ["load_memories", "refuse"]
    )
    graph.add_edge("load_memories", "core_agent")
    graph.add_edge("core_agent", "next_steps")
    graph.add_edge("next_steps", END)
    graph.add_edge("refuse", END)

    agent = graph.compile()
    return agent, vector_store

async def run_agent(user_message: HumanMessage, chat_id: str, agent, vector_store):
    """Runs the agent for a given user message and chat session."""
    state = {
        "user_message": user_message,
        "answer": [],
        "safe": False,
        "refuse_explanation": "",
        "history": load_chat_history(chat_id),
        "recall_memories": [],
        "chat_id": chat_id,
    }
    result = await agent.ainvoke(state)
    save_memories_to_blob(vector_store, chat_id)
    save_chat_history(chat_id, result["history"])
    return result
