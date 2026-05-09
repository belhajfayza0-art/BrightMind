severity_scores = {
    "SingleHotSpot": 2,
    "MultiHotSpot": 4,
    "SingleDiode": 2,
    "MultiDiode": 4,
    
    "SingleByPassed": 3,
    "MultiByPassed": 5,
    "StringOpenCircuit": 7,
    "StringReversedPolarity": 8
}

def compute_risk(detections):

    if len(detections) == 0:
        return {
            "risk_level": "LOW",
            "risk_score": 0
        }

    total_score = 0

    for d in detections:

        anomaly_type = d["type"]

        total_score += severity_scores.get(anomaly_type, 1)

    # Extra risk if many anomalies
    if len(detections) >= 3:
        total_score += 3

    # Determine risk level
    if total_score >= 10:
        level = "HIGH"

    elif total_score >= 5:
        level = "MEDIUM"

    else:
        level = "LOW"

    return {
        "risk_level": level,
        "risk_score": total_score
    }