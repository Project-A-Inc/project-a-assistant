# import pytest
# from project_a_assistant.graph import build_graph
# from langchain_core.messages import HumanMessage, AIMessage
# import project_a_assistant.validators.gatekeeper as gatekeeper_module

# @pytest.mark.asyncio
# async def test_graph_with_mocked_chat(monkeypatch):
#     # Mock chat function used inside gatekeeper.is_message_allowed()
#     async def mock_chat(messages, temperature=0.0):
#         return AIMessage(content='{"allowed": false, "reason": "off_topic", "explanation": "This is off-topic."}')

#     # Patch chat only where it is used
#     monkeypatch.setattr(gatekeeper_module, "chat", mock_chat)

#     compiled_graph = build_graph().compile()

#     state = {
#         "user_message": HumanMessage(content="how far is the moon from the sun?")
#     }

#     result = await compiled_graph.ainvoke(state)

#     assert "answer" in result
#     assert result["is_allowed"] is False

# @pytest.mark.asyncio
# async def test_graph_with_icebreaker(monkeypatch):
#     # Mock chat function used inside gatekeeper.is_message_allowed()
#     async def mock_chat(messages, temperature=0.0):
#         return AIMessage(content='{"allowed": false, "reason": "off_topic", "explanation": "This is off-topic."}')

#     # Patch chat only where it is used
#     # monkeypatch.setattr(gatekeeper_module, "chat", mock_chat)

#     compiled_graph = build_graph().compile()

#     state = {
#         "user_message": HumanMessage(content="hello")
#     }

#     result = await compiled_graph.ainvoke(state)

#     assert "answer" in result
#     assert result["is_allowed"] is True


# @pytest.mark.asyncio
# async def test_graph_with_web_search(monkeypatch):

#     # Patch chat only where it is used
#     # monkeypatch.setattr(gatekeeper_module, "chat", mock_chat)

#     compiled_graph = build_graph().compile()

#     state = {
#         "user_message": HumanMessage(content="Latest funding news for Acme Corp.")
#     }

#     result = await compiled_graph.ainvoke(state)

#     assert "answer" in result
#     assert result["is_allowed"] is True
