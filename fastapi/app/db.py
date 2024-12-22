from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

mongo_db_url = os.getenv("MONGODB_URL")
client = MongoClient(mongo_db_url)
db = client["items_db"]

collections = {
    "items": db["items"],
}
