import json
import os

LOG_FILE = "logs.json"

def save_log(result):

    logs = []

    # Load existing logs if file exists
    if os.path.exists(LOG_FILE):

        with open(LOG_FILE, "r") as f:
            logs = json.load(f)

    # Add new inspection result
    logs.append(result)

    # Save updated logs
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)