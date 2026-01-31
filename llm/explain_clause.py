def explain_clause(text):

    text_lower = text.lower()

    if "indemnify" in text_lower:
        return "This clause means one party must cover losses or legal damages of the other party."

    if "penalty" in text_lower:
        return "This clause imposes a financial penalty if obligations are not met."

    if "terminate" in text_lower:
        return "This clause allows ending the contract under certain conditions."

    if "non-compete" in text_lower:
        return "This clause restricts working with competitors for a time period."

    if "arbitration" in text_lower:
        return "This clause sends disputes to arbitration instead of court."

    return "This clause defines responsibilities and rights between the parties."
