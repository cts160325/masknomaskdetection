from pathlib import Path
import os
from dotenv import load_dotenv

PROJECT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_DIR / ".env")

# Sau khi huấn luyện, chép runs/helmet_mask/weights/best.pt vào models/best.pt
MODEL_PATH = Path(os.getenv("MODEL_PATH", PROJECT_DIR / "models" / "best.pt"))

CAMERA_INDEX = int(os.getenv("CAMERA_INDEX", "0"))
CONFIDENCE = float(os.getenv("CONFIDENCE", "0.35"))
IMAGE_SIZE = int(os.getenv("IMAGE_SIZE", "640"))

EVIDENCE_DIR = PROJECT_DIR / "evidence"
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

MONGODB_URI = os.getenv("MONGODB_URI", "").strip()
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "helmet_mask_db")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "events")

# Chỉ ghi một lần cho mỗi track ID + loại vi phạm trong một phiên chạy.
# Nếu muốn cho phép ghi lại sau một khoảng thời gian, thay đổi logic trong main.py.
CLASS_NAMES = {
    0: "Helmet",
    1: "No Helmet",
    2: "Mask",
    3: "No Mask",
}
VIOLATION_CLASSES = {"No Helmet", "No Mask"}
