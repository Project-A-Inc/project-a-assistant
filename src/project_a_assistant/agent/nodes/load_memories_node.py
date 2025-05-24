async def load_memories_node(state, tools):
    """
    Async node for loading relevant long-term memories for the session.
    Expects tools as a dict, uses 'search_recall_memories' tool by name.
    """
    tool = tools["search_recall_memories"]
    user_message = state["user_message"]

    if hasattr(tool, "ainvoke"):
        recall_memories = await tool.ainvoke(user_message.content)
    else:
        recall_memories = tool.invoke(user_message.content)

    return {
        "recall_memories": recall_memories
    }