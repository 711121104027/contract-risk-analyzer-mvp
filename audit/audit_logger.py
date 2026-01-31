import json
from datetime import datetime

def log_action(action):
    entry = {
        "time": str(datetime.now()),
        "action": action
    }

    try:
        data = json.load(open("audit/logs.json"))
    except:
        data = []

    data.append(entry)
    json.dump(data, open("audit/logs.json","w"), indent=2)
