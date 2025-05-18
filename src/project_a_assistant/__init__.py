
"""Project‑A Assistant package root."""
from fastapi import FastAPI
from .api import conversation
def get_app() -> FastAPI:
    return conversation.app
