
import json
import re
from typing import List, Any
from langchain_core.messages import BaseMessage


try:
    import tiktoken
    _ENC = tiktoken.get_encoding("cl100k_base")
except ModuleNotFoundError:
    _ENC = None

_JSON_RE = re.compile(r"\{[^\{}]*\}\s*$", re.DOTALL)
_MAX_CHARS = 2000
_MAX_TOKENS = 800

def _clip_tokens(tokens: List[int]) -> List[int]:
    if len(tokens) <= _MAX_TOKENS or _ENC is None:
        return tokens
    clipped = tokens[:_MAX_TOKENS]
    text = _ENC.decode(clipped)
    while clipped and not text.rstrip().endswith('}'):
        clipped.pop()
        text = _ENC.decode(clipped)
    return clipped

def truncate(text: str) -> str:
    if _ENC:
        tokens = _ENC.encode(text)
        if len(tokens) <= _MAX_TOKENS:
            return text
        return _ENC.decode(_clip_tokens(tokens)) + ' …'
    if len(text) <= _MAX_CHARS:
        return text
    seg = text[:_MAX_CHARS]
    brace = seg.rfind('}')
    if brace != -1:
        seg = seg[:brace+1]
    return seg + ' …'

# Matches JSON inside optional markdown block like ```json ... ```
_JSON_RE = re.compile(r'\{(?:[^{}"]|"(?:\\.|[^"\\])*"|\{(?:[^{}"]|"(?:\\.|[^"\\])*")*\})*\}')

def extract_json_from_message(message: Any) -> dict:
    """
    Extract JSON from AIMessage or raw string.
    Handles markdown code blocks and fallback to regex.
    """
    if isinstance(message, BaseMessage):
        text = message.content
    elif isinstance(message, str):
        text = message
    else:
        return {}

    # Remove markdown fences like ```json\n...\n```
    text = text.strip().strip("`").strip()
    if text.startswith("json"):
        text = text[4:].strip()

    try:
        return json.loads(text)
    except Exception:
        match = _JSON_RE.search(text)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                return {}
        return {}

def safe_json_list(message: Any) -> List[str]:
    """
    Extract a list from message JSON field "tools".
    """
    data = extract_json_from_message(message)
    return data.get("tools", [])
