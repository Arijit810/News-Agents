import os
from pprint import pprint
from dotenv import load_dotenv
from graph_builder import build_graph

def main():
    print("🧠 News Insight Agent (LangGraph + LangSmith + Groq)")
    topic = input("Enter a topic or event: ")

    print("Current working directory:", os.getcwd())

    # Try loading .env explicitly
    dotenv_path = os.path.join(os.getcwd(), ".env")
    print("Looking for .env at:", dotenv_path)

    load_dotenv()
    print("GROQ_API_KEY loaded:", os.getenv("GROQ_API_KEY") is not None)
    graph = build_graph()
    # Add a thread_id or checkpoint_id (unique identifier)
    result = graph.invoke(
        {"topic": topic},
        config={"configurable": {"thread_id": "news_insight_session"}}
    )

    print("\n🔹 Final Output:")
    pprint(result)

if __name__ == "__main__":
    main()
