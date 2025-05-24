from ...llm.llm_client import chat
from langchain.prompts import ChatPromptTemplate
from ...prompts import load_prompt

# Load the system prompt once (module-level)
NEXT_STEPS_PROMPT = load_prompt("next_steps")

async def next_steps_node(state):
    """
    Node for suggesting next steps after assistant's reply.
    """
    answer = state["answer"]
    all_answers = "\n\n".join(msg.content for msg in answer) if answer else ""
    
    prompt = ChatPromptTemplate.from_messages([
        ("user", NEXT_STEPS_PROMPT)
    ])

    message = prompt.format_messages(answer=all_answers)
    next_steps = await chat(message, temperature=0)
    history = state["history"]

    answer.append(next_steps)
    history.append({"role": "assistant", "content": next_steps.content})
    return {
        "answer": answer,
        "history": history,
    }
