from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os
import certifi

# Xác định chính xác vị trí file .env
env_path = Path(__file__).resolve().parent / ".env"

load_dotenv(dotenv_path=env_path, override=True)

uri = os.getenv("MONGODB_URI")

# Kiểm tra đã đọc được đường dẫn chưa
if not uri:
    print("LOI: Khong tim thay MONGODB_URI trong file .env")
    print("Hay kiem tra lai ten va vi tri file .env")
    exit()

if "mongodb+srv://" not in uri:
    print("LOI: Connection String khong dung dinh dang MongoDB Atlas")
    exit()

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=10000, tlsCAFile=certifi.where())

    client.admin.command("ping")

    print("CONNECTED SUCCESSFULLY!")
    print("Da ket noi MongoDB Atlas thanh cong.")

    client.close()

except Exception as e:
    print("CONNECTION FAILED:")
    print(e)
