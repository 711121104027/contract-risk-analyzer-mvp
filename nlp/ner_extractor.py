import re

def extract_entities(text):

    entities = []

    # -------- MONEY --------
    money = re.findall(r'Rs\.?\s?\d[\d,]*', text)
    for m in money:
        entities.append((m, "MONEY"))

    # -------- DATE --------
    dates = re.findall(r'\d+\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}', text)
    for d in dates:
        entities.append((d, "DATE"))

    # -------- ORG (simple heuristic) --------
    orgs = re.findall(r'[A-Z][A-Za-z]+\s+(Pvt Ltd|Ltd|LLP|Technologies|Services)', text)
    for o in orgs:
        entities.append((o, "ORG"))

    return entities
