from ai.detection import detect_anomalies
from ai.risk_analysis import compute_risk
from ai.localization import assign_panel_id

import datetime

def analyze_panel(image_path, panel_index):

    detections = detect_anomalies(image_path)

    risk = compute_risk(detections)

    result = {
        "panel_id": assign_panel_id(panel_index),
        "timestamp": str(datetime.datetime.now()),
        "risk": risk,
        "anomalies": detections,
        "count": len(detections)
    }

    return result