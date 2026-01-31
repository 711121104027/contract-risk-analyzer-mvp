def classify_clause(text):
    text = text.lower()
    if "shall not" in text or "prohibited" in text:
        return "Prohibition"
    elif "shall" in text or "must" in text:
        return "Obligation"
    elif "may" in text:
        return "Right"
    return "Neutral"
