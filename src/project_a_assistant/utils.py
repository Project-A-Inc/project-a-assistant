
import json, re
from typing import List

try:
    import tiktoken
    _ENC = tiktoken.get_encoding("cl100k_base")
except ModuleNotFoundError:
    _ENC = None

_JSON_RE = re.compile(r"\{[^\{}]*\}\s*$", re.DOTALL)
_MAX_CHARS = 2000
_MAX_TOKENS = 800

def safe_json_list(text: str) -> List[str]:
    try:
        return json.loads(text).get("tools", [])
    except Exception:
        m = _JSON_RE.search(text)
        if m:
            try:
                return json.loads(m.group()).get("tools", [])
            except Exception:
                pass
    return []

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
