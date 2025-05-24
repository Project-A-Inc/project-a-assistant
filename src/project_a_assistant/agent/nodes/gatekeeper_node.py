from typing import List
from ...llm.llm_client import chat
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
from dataclasses import dataclass
from ...prompts import load_prompt
from ...utils import extract_json_from_message

_SYSTEM_PROMPT = load_prompt("gatekeeper")

@dataclass
class GatekeeperResult:
    allowed: bool
    reason: str
    explanation: str


async def _is_message_allowed(msg: HumanMessage) -> GatekeeperResult:
    messages: List[BaseMessage] = [
        SystemMessage(content=_SYSTEM_PROMPT),
        msg
    ]
    
    result = await chat(messages, temperature=0)
    
    result_json = extract_json_from_message(result)

    return GatekeeperResult(
        allowed=bool(result_json.get("allowed", False)),
        reason=result_json.get("reason", "unknown"),
        explanation=result_json.get("explanation", "")
    )

async def gatekeeper_node(state):
    """
    Node for message safety and etiquette validation.
    """
    message = state['user_message']
    result = await _is_message_allowed(message)

    return { 
        "safe": result.allowed,
        "refuse_explanation": result.explanation
    }
