from langchain_core.messages import AIMessage

async def refuse_node(state):
    """
    Node for polite refusal in case of unsafe or offensive user input.
    """
   
    answer = state["answer"]
    refuse_explanation = state["refuse_explanation"]
    history = state["history"]

    answer.append(AIMessage(content=refuse_explanation))
    history.append({"role": "assistant", "content": state["answer"]})
    return {
        "answer": answer,
        "history": history 
    }