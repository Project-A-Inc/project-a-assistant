
from fastapi import FastAPI
from .conversation import router as conversation_router
app = FastAPI(title="Project-A Assistant API")
app.include_router(conversation_router, prefix="/api")
