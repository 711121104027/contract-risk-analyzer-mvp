import re

def split_into_clauses(text):
    clauses = re.split(r'\n\s*\d+[\.\)]\s+', text)
    return [
        {"id": f"C{i+1}", "text": c.strip()}
        for i, c in enumerate(clauses)
        if len(c.strip()) > 40
    ]
