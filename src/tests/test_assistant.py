import uuid
import pytest
from project_a_assistant.agent.assistant import build_agent_for_chat, run_agent
from langchain_core.messages import (
    HumanMessage,
)

@pytest.mark.asyncio
async def test_full_assistant_pipeline():
    chat_id = str(uuid.uuid4())
    index_id = 'vlad12'
    agent, vector_store = await build_agent_for_chat(chat_id, index_id)
    user_message = HumanMessage(content="Who is Vlad")
    result = await run_agent(user_message, chat_id=chat_id, agent=agent, vector_store=vector_store)
    assert "answer" in result
    # You can also add more checks for next steps etc
