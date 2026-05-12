from ai.detection import detect_anomalies
from ai.risk_analysis import compute_risk
from ai.localization import assign_panel_id
from ai.visualization import draw_detections
from ai.logging_system import save_log
import datetime

def analyze_panel(image_path, panel_index):

    detections = detect_anomalies(image_path)

    risk = compute_risk(detections)

    annotated_image = draw_detections(image_path, detections)

    result = {
        "panel_id": assign_panel_id(panel_index),
        "timestamp": str(datetime.datetime.now()),
        "risk": risk,
        "anomalies": detections,
        "count": len(detections),
        "annotated_image": annotated_image,
        "status" : "Pending",
        "technician" : None,
        "fixed_at" : None
    }
    save_log(result)
    

    return result