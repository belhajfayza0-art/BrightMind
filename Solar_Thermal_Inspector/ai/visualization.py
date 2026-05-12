import cv2

def draw_detections(image_path, detections, output_path="output.jpg"):
    image = cv2.imread(image_path)

    for det in detections:
        x1, y1, x2, y2 = map(int, det["bbox"])
        label = f"{det['type']} ({det['confidence']:.2f})"

        color = (0, 0, 255)
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

        cv2.putText(
            image,
            label,
            (x1,y1-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            2
        )
    cv2.imwrite(output_path, image)

    return output_path
