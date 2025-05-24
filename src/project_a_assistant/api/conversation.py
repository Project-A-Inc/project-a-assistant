# # src/project_a_assistant/api/conversation.py

# from typing import List
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from langchain_core.messages import HumanMessage, AIMessage
# from ..graph import build_graph

# router = APIRouter(tags=["conversation"])

# # Compile your graph once
# compiled_graph = build_graph().compile()


# class ChatRequest(BaseModel):
#     """Incoming chat request payload."""
#     message: str
#     user_id: str | None = None


# class ChatResponse(BaseModel):
#     """Outgoing chat response payload."""
#     response: List[AIMessage]


# @router.post("/chat", response_model=ChatResponse)
# async def chat_endpoint(req: ChatRequest):
#     """
#     1. Seed the graph with the user's message.
#     2. Invoke the async graph API.
#     3. Convert the result state to native Python.
#     4. Extract the last assistant message.
#     """
#     try:

#         state = {
#             "user_message": HumanMessage(content=req.message),
#             "is_allowed": True
#         }
#         # 2) async invoke
#         result_state = await compiled_graph.ainvoke(state)

#         answer = result_state['answer']
        
#         return ChatResponse(response=answer)

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
