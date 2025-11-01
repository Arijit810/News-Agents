from langchain_groq import ChatGroq

def factual_alignment_score(text: str, reference: str):
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
    prompt = f"""
    Compare the factual accuracy of the following content relative to the reference.
    Give a score between 0 and 1 (0 = completely incorrect, 1 = perfectly accurate).

    Reference:
    {reference}

    Text:
    {text}

    Respond with only the numeric score.
    """
    response = llm.invoke(prompt)
    try:
        score = float(response.content.strip())
    except:
        score = 0.5
    return score
