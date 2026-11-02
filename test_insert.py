from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timezone
import os

load_dotenv()

uri = os.getenv("MONGODB_URI")
database_name = os.getenv("MONGODB_DATABASE")
collection_name = os.getenv("MONGODB_COLLECTION")

try:
    client = MongoClient(uri)
    db = client[database_name]
    collection = db[collection_name]

    event = {
        "event_type": "test_connection",
        "message": "MongoDB Atlas test successful",
        "timestamp": datetime.now(timezone.utc)
    }

    result = collection.insert_one(event)

    print("Luu du lieu thanh cong!")
    print("ID:", result.inserted_id)

    client.close()

except Exception as e:
    print("Loi:", e)