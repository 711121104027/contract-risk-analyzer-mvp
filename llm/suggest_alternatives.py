def suggest_alternative(text):

    text_lower = text.lower()

    if "sole discretion" in text_lower:
        return "Suggest adding mutual termination rights for both parties."

    if "indemnify" in text_lower:
        return "Limit indemnity only to proven negligence."

    if "penalty" in text_lower:
        return "Add a penalty cap or cure period before penalty applies."

    if "non-compete" in text_lower:
        return "Reduce non-compete duration and scope."

    return "Consider clarifying terms and adding mutual protections."
