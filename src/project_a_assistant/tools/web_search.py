
from duckduckgo_search import DDGS
from typing import List, Dict
def search(query: str, max_results: int = 5) -> List[Dict[str,str]]:
    with DDGS() as ddgs:
        return [{"title":r["title"],"href":r["href"],"snippet":r["body"]}
                for r in ddgs.text(query, safesearch="Moderate", max_results=max_results)]
