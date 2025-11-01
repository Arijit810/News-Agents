import requests

def web_search(query: str, num_results: int = 3) -> list[str]:
    """
    Simple DuckDuckGo web summary fetcher.
    """
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    data = requests.get(url).json()
    results = [data.get("AbstractText", "No summary found.")]
    if not results or results == [""]:
        results = [f"No results found for {query}."]
    return results[:num_results]
