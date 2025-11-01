# nodes/summarize_node.py
from langchain_groq import ChatGroq

def summarize_node(state):
    topic = state["topic"]
    search_results = state.get("search_results")
    if not search_results:
        raise ValueError("summarize_node expected 'search_results' in state but found none.")

    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3)

    prompt = f"""
        You are an AI journalist. Summarize the following information about '{topic}'
        in a clear, factual, and concise way (100–150 words). Avoid opinions.

        Context:
        {search_results}
        """

    print("🧠 Generating summary using Groq...")
    response = llm.invoke(prompt)
    # response.content expected; adapt if your ChatGroq object returns differently
    summary = getattr(response, "content", str(response)).strip()

    print("✅ Summary generated. Returning summary to graph state.")
    return {"summary": summary}
