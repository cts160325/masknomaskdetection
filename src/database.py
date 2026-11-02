from datetime import datetime, timezone
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import certifi

try:
    from .config import MONGODB_URI, MONGODB_DATABASE, MONGODB_COLLECTION
except ImportError:  # pragma: no cover - compatibility when run as a script
    from config import MONGODB_URI, MONGODB_DATABASE, MONGODB_COLLECTION

class EventStore:
    def __init__(self):
        self.collection = None
        self.client = None
        if not MONGODB_URI:
            print("[DB] Chưa có MONGODB_URI. Sự kiện sẽ được in ra terminal, không lưu Atlas.")
            return
        try:
            self.client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000, tlsCAFile=certifi.where())
            self.client.admin.command("ping")
            self.collection = self.client[MONGODB_DATABASE][MONGODB_COLLECTION]
            self.collection.create_index("timestamp")
            self.collection.create_index([("track_id", 1), ("event_type", 1)])
            print("[DB] Đã kết nối MongoDB Atlas.")
        except Exception as exc:
            print(f"[DB] Không kết nối được MongoDB: {exc}")
            self.collection = None

    def save_event(self, track_id, event_type, confidence, image_path):
        event = {
            "timestamp": datetime.now(timezone.utc),
            "track_id": int(track_id) if track_id is not None else None,
            "event_type": str(event_type),
            "confidence": float(confidence),
            "image_path": str(image_path),
        }
        if self.collection is None:
            print("[EVENT - LOCAL ONLY]", event)
            return False
        try:
            self.collection.insert_one(event)
            print(f"[DB] Đã lưu sự kiện: {event_type}, track={track_id}")
            return True
        except PyMongoError as exc:
            print(f"[DB] Lỗi lưu sự kiện: {exc}")
            return False

    def close(self):
        if self.client:
            self.client.close()
