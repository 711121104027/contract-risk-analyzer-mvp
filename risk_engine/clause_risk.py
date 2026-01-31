import json

with open("risk_engine/risk_rules.json") as f:
    RULES = json.load(f)

def assess_clause_risk(text):
    text = text.lower()
    risks = []

    for name, rule in RULES.items():
        for kw in rule["keywords"]:
            if kw in text:
                risks.append({
                    "type": name,
                    "risk": rule["risk"]
                })
    return risks
