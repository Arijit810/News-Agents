import re

def quality_score(text: str) -> dict:
    sentences = re.split(r"[.!?]", text)
    word_count = len(text.split())
    avg_sentence_len = sum(len(s.split()) for s in sentences if s.strip()) / max(1, len(sentences))
    
    coherence = 1 if avg_sentence_len < 30 else 0.7
    length_score = 1 if 60 <= word_count <= 180 else 0.5
    grammar_penalty = 0.9 if re.search(r"[\d]{4}", text) else 1
    
    overall = round((coherence + length_score + grammar_penalty) / 3, 2)
    
    remarks = []
    if length_score < 0.8: remarks.append("Length imbalance.")
    if coherence < 1: remarks.append("Complex sentences.")
    if grammar_penalty < 1: remarks.append("Too numeric.")
    
    return {"quality_score": overall, "remarks": " ".join(remarks) or "Well structured."}
