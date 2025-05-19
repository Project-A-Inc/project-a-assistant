from langchain_community.tools.tavily_search import TavilySearchResults
from asyncio import to_thread

# Instantiate once
tavily_tool = TavilySearchResults()

# Async wrapper
async def search(query: str) -> str:
    return await to_thread(tavily_tool.run, query)