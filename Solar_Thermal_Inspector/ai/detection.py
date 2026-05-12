from ultralytics import YOLO

# Load trained model
model = YOLO("models/best.pt")

def detect_anomalies(image_path):

    results = model(image_path)

    detections = []

    for r in results:
        for box in r.boxes:

            cls = int(box.cls[0])
            conf = float(box.conf[0])
            xyxy = box.xyxy[0].tolist()

            detections.append({
                "type": model.names[cls],
                "confidence": round(conf, 2),
                "bbox": xyxy
            })

    return detections