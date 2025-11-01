from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from nodes.search_node import search_node
from nodes.summarize_node import summarize_node
from nodes.sentiment_node import sentiment_node
from nodes.evaluator_node import evaluator_node

from typing import TypedDict, Optional


class NewsState(TypedDict):
    topic: str
    search_results: Optional[str]
    summary: Optional[str]
    sentiment: Optional[dict]
    score: Optional[float]


def build_graph():
    graph = StateGraph(state_schema=NewsState)

    # node names: "ingest" -> search, "summary" -> summarize, etc.
    graph.add_node("ingest", search_node)
    graph.add_node("summary", summarize_node)
    graph.add_node("sentiment", sentiment_node)
    graph.add_node("evaluate", evaluator_node)

    graph.set_entry_point("ingest")

    # Flow: ingest -> summary -> sentiment -> (conditionally) evaluate -> END
    graph.add_edge("ingest", "summary")
    graph.add_edge("summary", "sentiment")

    # Example conditional: if sentiment label not Neutral then evaluate else END
    def decide_next(state):
        s = state.get("sentiment")
        if not s:
            return "end"
        # if sentiment stored as {"label": "Neutral"} adapt as needed
        label = s.get("label") if isinstance(s, dict) else None
        return "evaluate" if label and label != "Neutral" else "end"

    graph.add_conditional_edges(
        "sentiment",
        decide_next,
        {"evaluate": "evaluate", "end": END}
    )

    graph.add_edge("evaluate", END)

    memory = MemorySaver()
    return graph.compile(checkpointer=memory)

