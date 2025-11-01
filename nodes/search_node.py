# nodes/search_node.py
from langchain_community.tools import DuckDuckGoSearchResults

search_tool = DuckDuckGoSearchResults()

def search_node(state):
    topic = state["topic"]
    print(f"🔍 Searching web for '{topic}' ...")
    try:
        results = search_tool.run(topic)  # expected to be a single string
    except Exception as e:
        results = f"Search failed: {e}"

    print("✅ Search completed. Returning search_results to graph state.")
    return {"search_results": results}
