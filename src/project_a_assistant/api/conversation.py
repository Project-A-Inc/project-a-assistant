# src/project_a_assistant/api/conversation.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..graph import build_graph

router = APIRouter(tags=["conversation"])

# Compile your graph once
compiled_graph = build_graph().compile()


class ChatRequest(BaseModel):
    """Incoming chat request payload."""
    message: str
    user_id: str | None = None


class ChatResponse(BaseModel):
    """Outgoing chat response payload."""
    role: str
    content: str


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    """
    1. Seed the graph with the user's message.
    2. Invoke the async graph API.
    3. Convert the result state to native Python.
    4. Extract the last assistant message.
    """
    try:

        state = {
            "user_message": req.message       # no outputs yet
        }
        # 2) async invoke
        result_state = await compiled_graph.ainvoke(state)

        # 3) normalize state → dict
        if hasattr(result_state, "model_dump"):
            state_data = result_state.model_dump()
        elif hasattr(result_state, "dict"):
            state_data = result_state.dict()
        else:
            # assume it’s already a dict
            state_data = result_state  

        messages = state_data.get("messages", [])
        if not messages:
            raise ValueError("Graph returned no messages")

        last = messages[-1]

        # 4) last may be a BaseModel or dict
        if not isinstance(last, dict):
            if hasattr(last, "model_dump"):
                last = last.model_dump()
            elif hasattr(last, "dict"):
                last = last.dict()
            else:
                # fallback: use vars()
                last = vars(last)

        return ChatResponse(role=last["role"], content=last["content"])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
