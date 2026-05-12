import json
import datetime

LOG_FILE = "logs.json"

def mark_as_fixed(panel_id, technician_name):
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)
    
    for log in logs:
        if log["panel_id"] == panel_id and log["status"] == "Pending":
            log["status"] = "Fixed"
            log["technician"] = technician_name
            log["fixed_at"] = str(datetime.datetime.now())

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)
    
    return{
        "message" : f"{panel_id} marked as Fixed"
    }


# What this script does:
# opens logs
# Searches panel
# updates repair status
# saves changes