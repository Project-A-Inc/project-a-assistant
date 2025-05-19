import json
import re
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
from typing import List
from dataclasses import dataclass
from ..llm_client import chat
from ..prompts import load_prompt

_SYSTEM_PROMPT = load_prompt("gatekeeper")

@dataclass
class GatekeeperResult:
    allowed: bool
    reason: str
    explanation: str

# Regular expression to extract a JSON object from the LLM response
_JSON_REGEX = re.compile(r'\{(?:[^{}"]|"(?:\\.|[^"\\])*"|\{(?:[^{}"]|"(?:\\.|[^"\\])*")*\})*\}')

async def is_message_allowed(msg: HumanMessage) -> GatekeeperResult:
    messages: List[BaseMessage] = [
        SystemMessage(content=_SYSTEM_PROMPT),
        HumanMessage(content=msg)
    ]
    try:
        result = await chat(messages, temperature=0)

        # Extract the first valid JSON object from the response using regex
        match = _JSON_REGEX.search(result.content)
        if not match:
            raise ValueError("No valid JSON object found in response.")

        json_str = match.group(0)
        result_json = json.loads(json_str)

        return GatekeeperResult(
            allowed=bool(result_json.get("allowed", False)),
            reason=result_json.get("reason", "unknown"),
            explanation=result_json.get("explanation", "")
        )

    except Exception as e:
        # Return a default response with error details
        return GatekeeperResult(
            allowed=False,
            reason="error",
            explanation=f"Failed to process message: {str(e)}"
        )
