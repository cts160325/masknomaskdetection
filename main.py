import sys
import time
from pathlib import Path
from datetime import datetime

import cv2
from ultralytics import YOLO

from src.config import (
    MODEL_PATH, CAMERA_INDEX, CONFIDENCE, IMAGE_SIZE,
    EVIDENCE_DIR, CLASS_NAMES, VIOLATION_CLASSES
)
from src.database import EventStore

def main():
    if not MODEL_PATH.exists():
        print(f"Không tìm thấy trọng số mô hình: {MODEL_PATH}")
        print("Bạn cần chuẩn bị dataset, huấn luyện YOLO bằng train.py,")
        print("sau đó chép runs/helmet_mask/weights/best.pt vào models/best.pt.")
        sys.exit(1)

    print("[AI] Đang tải mô hình...")
    model = YOLO(str(MODEL_PATH))
    store = EventStore()

    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("Không mở được webcam. Hãy kiểm tra webcam hoặc sửa CAMERA_INDEX trong .env.")
        store.close()
        sys.exit(1)

    # Ghi nhận mỗi loại vi phạm một lần cho mỗi track trong phiên chạy.
    # ByteTrack cung cấp ID theo dõi; nếu track bị mất lâu rồi xuất hiện lại,
    # hệ thống có thể cấp ID mới và ghi nhận thành sự kiện mới.
    saved_events = set()
    print("[INFO] Nhấn Q hoặc ESC để thoát.")

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("Không đọc được khung hình từ webcam.")
                break

            results = model.track(
                frame,
                persist=True,
                tracker="bytetrack.yaml",
                conf=CONFIDENCE,
                imgsz=IMAGE_SIZE,
                verbose=False
            )

            annotated = frame.copy()
            if results and results[0].boxes is not None:
                boxes = results[0].boxes
                ids = boxes.id
                track_ids = ids.int().cpu().tolist() if ids is not None else [None] * len(boxes)

                for box, track_id in zip(boxes, track_ids):
                    cls_id = int(box.cls[0].item())
                    conf = float(box.conf[0].item())
                    label = CLASS_NAMES.get(cls_id, f"class_{cls_id}")
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

                    is_violation = label in VIOLATION_CLASSES
                    color = (0, 0, 255) if is_violation else (0, 180, 0)
                    display = f"{label} {conf:.2f}"
                    if track_id is not None:
                        display += f" ID:{track_id}"

                    cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(
                        annotated, display, (x1, max(25, y1 - 8)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2
                    )

                    if is_violation and track_id is not None:
                        event_key = (int(track_id), label)
                        if event_key not in saved_events:
                            saved_events.add(event_key)
                            stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                            image_file = EVIDENCE_DIR / f"{label.lower().replace(' ', '_')}_id{track_id}_{stamp}.jpg"
                            cv2.imwrite(str(image_file), annotated)
                            store.save_event(track_id, label, conf, image_file)

            cv2.imshow("Helmet & Mask Detection - Q/Esc to quit", annotated)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q") or key == 27:
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        store.close()

if __name__ == "__main__":
    main()
