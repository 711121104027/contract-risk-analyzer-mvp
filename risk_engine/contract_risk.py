def calculate_contract_risk(results):
    score_map = {"Low":1, "Medium":2, "High":3}
    total = 0
    count = 0

    for r in results:
        for risk in r["risks"]:
            total += score_map[risk["risk"]]
            count += 1

    if count == 0:
        return "Low"

    avg = total / count

    if avg >= 2.5:
        return "High"
    elif avg >= 1.5:
        return "Medium"
    return "Low"
