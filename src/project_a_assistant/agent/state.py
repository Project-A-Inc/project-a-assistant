from typing import TypedDict, List
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
)

class AgentState(TypedDict):
    user_message: HumanMessage
    answer: List[AIMessage]
    safe: bool
    refuse_explanation: str
    history: List[dict]
    recall_memories: List[str]
    chat_id: str
