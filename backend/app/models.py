from pymongo import MongoClient
from .config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.get_database("mycrm")
collection = db.get_collection("users")
