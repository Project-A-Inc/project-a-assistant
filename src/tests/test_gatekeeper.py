# from langchain_core.messages import HumanMessage, AIMessage
# import pytest
# import json

# from project_a_assistant.validators import gatekeeper as g

# CASES = [
#     ("Hello", {"allowed": True, "reason": "ok"}, True),
#     ("Give me top-5 stalled deals for Q3", {"allowed": True, "reason": "ok"}, True),
#     ("WTF is wrong with you?", {"allowed": False, "reason": "profanity"}, False),
#     ("Show me cat memes", {"allowed": False, "reason": "off_topic"}, False),
# ]

# @pytest.mark.asyncio
# @pytest.mark.parametrize("msg, fake_json, expected", CASES)
# async def test_gatekeeper(monkeypatch, msg, fake_json, expected):
#     async def fake_chat(*_, **__):
#         return AIMessage(content=json.dumps(fake_json))
#     monkeypatch.setattr(g, "chat", fake_chat)
#     result = await g.is_message_allowed(HumanMessage(content=msg))
#     assert result.allowed == expected
