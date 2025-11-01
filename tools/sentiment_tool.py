from langchain_groq import ChatGroq

def sentiment_analysis(text: str):
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
    prompt = f"""
    Analyze the sentiment of this text and classify it as Positive, Negative, or Neutral:
    ---
    {text}
    ---
    Respond with only one word (Positive, Negative, or Neutral).
    """
    response = llm.invoke(prompt)
    return {"label": response.content.strip()}
