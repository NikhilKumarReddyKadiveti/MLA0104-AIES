from collections import defaultdict
from pathlib import Path

import cv2
from ultralytics import YOLO


IMG_SIZE = 640
CONFIDENCE_THRESHOLD = 0.25
TARGET_DIR = Path("custom_dataset/images")
MODEL_FILE = "yolo11n.pt"
VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

GROUP_KEYWORDS = {
    "vehicles": {"bicycle", "boat", "bus", "car", "motorcycle", "train", "truck"},
    "animals": {
        "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe"
    },
    "characters_and_art": {"person", "backpack", "handbag", "tie", "suitcase"},
    "buildings": set(),
}


def get_group(label):
    for group, labels in GROUP_KEYWORDS.items():
        if label in labels:
            return group
    return "others"


def choose_primary_group(detections):
    group_scores = defaultdict(float)
    for detection in detections:
        group_scores[detection["group"]] += detection["confidence"]

    if not group_scores:
        return "others"
    return max(group_scores, key=group_scores.get)


def detect_and_sort_images():
    if not TARGET_DIR.exists():
        print(f"Target directory missing: {TARGET_DIR}")
        return

    image_files = sorted(
        path for path in TARGET_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in VALID_EXTENSIONS
    )
    if not image_files:
        print(f"No loose images found in {TARGET_DIR}.")
        return

    print(f"Loading real object detector: {MODEL_FILE}")
    model = YOLO(MODEL_FILE)
    print(f"Processing {len(image_files)} image(s).")

    for image_path in image_files:
        image = cv2.imread(str(image_path))
        if image is None:
            print(f"Skipped unreadable image: {image_path.name}")
            continue

        results = model.predict(
            source=image,
            imgsz=IMG_SIZE,
            conf=CONFIDENCE_THRESHOLD,
            verbose=False,
        )
        result = results[0]
        detections = []

        if result.boxes is not None:
            for class_id, confidence in zip(
                result.boxes.cls.tolist(), result.boxes.conf.tolist()
            ):
                label = result.names[int(class_id)].lower()
                detections.append({
                    "label": label,
                    "confidence": float(confidence),
                    "group": get_group(label),
                })

        primary_group = choose_primary_group(detections)
        detected_groups = sorted({detection["group"] for detection in detections})
        if not detected_groups:
            detected_groups = ["others"]

        annotated_image = result.plot()
        destination_dir = TARGET_DIR / primary_group
        destination_dir.mkdir(parents=True, exist_ok=True)
        destination_path = destination_dir / image_path.name

        if not cv2.imwrite(str(destination_path), annotated_image):
            print(f"Could not save annotated image: {image_path.name}")
            continue

        image_path.unlink()
        summary = ", ".join(
            f"{detection['label']} ({detection['confidence']:.2f})"
            for detection in detections
        ) or "no objects above threshold"
        print(
            f"{image_path.name}: {len(detections)} object(s) -> "
            f"{primary_group}; groups={', '.join(detected_groups)}; {summary}"
        )


if __name__ == "__main__":
    detect_and_sort_images()
