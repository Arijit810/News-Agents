from tools.sentiment_tool import sentiment_analysis

def sentiment_node(state):
    summary = state["summary"]
    sentiment = sentiment_analysis(summary)
    state["sentiment"] = sentiment
    return state
