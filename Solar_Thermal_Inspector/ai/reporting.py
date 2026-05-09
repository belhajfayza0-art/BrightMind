# Still needs more details to be added to the final report
from collections import Counter

def generate_report(logs):

    risks = [log["risk"]["risk_level"] for log in logs]

    anomalies = [
        a["type"]
        for log in logs
        for a in log["anomalies"]
    ]

    report = {
        "total_panels_checked": len(logs),
        "risk_distribution": dict(Counter(risks)),
        "anomaly_distribution": dict(Counter(anomalies))
    }

    return report