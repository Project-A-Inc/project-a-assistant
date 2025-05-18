
"""Load embedded prompt text files."""
from importlib import resources
def load_prompt(name: str) -> str:
    with resources.open_text(__package__, f"{name}.txt", encoding="utf-8") as fp:
        return fp.read()
