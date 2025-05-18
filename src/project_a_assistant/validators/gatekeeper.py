
from typing import List, Dict
from ..llm_client import chat
from ..prompts import load_prompt
_SYSTEM_PROMPT = load_prompt("gatekeeper")

async def is_message_allowed(msg: str) -> bool:
    messages: List[Dict[str,str]] = [
        {"role":"system","content":_SYSTEM_PROMPT},
        {"role":"user","content":msg}
    ]
    try:
        result = await chat(messages, temperature=0)
        return "true" in result.lower()
    except Exception:
        return False

def normalize(msg: str) -> str:
    return " ".join(msg.split())
