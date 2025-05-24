from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate
from ...llm.llm_client import llm
from langchain_core.messages import AIMessage
from ...prompts import load_prompt


# Load system prompt at import
ASSISTANT_SYSTEM_PROMPT = load_prompt("assistant_system")

async def core_agent_node(state, tools):
    """
    Main agent node, routes requests through the LLM and tools.
    Loads system prompt from assistant_system.txt file.
    """
    user_message = state["user_message"]
    context = "\n".join(state["recall_memories"]) if state["recall_memories"] else ""
    prompt = ChatPromptTemplate.from_messages([
        ("system", ASSISTANT_SYSTEM_PROMPT),
        ("user", "{user_message}")
    ])
    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    inputs = {
        "context": context,
        "user_message": user_message.content,
        "agent_scratchpad": ""
    }
        
    result = await agent_executor.ainvoke(inputs)
    response = result["output"]
    
    answer = state["answer"]
    answer.append(AIMessage(content=response))

    history = state["history"]
    history.append({"role": "user", "content": user_message.content})
    history.append({"role": "assistant", "content": response})
    return {
        "answer": answer,
        "history": history
    }
