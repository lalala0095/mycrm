# from intro
from pymongo import MongoClient
from .config import MONGO_URI
from pydantic import BaseModel, EmailStr
from bson import ObjectId
from typing import Optional

client = MongoClient(MONGO_URI)
db = client.get_database("mycrm")
collection = db.get_collection("users")

class UserModel(BaseModel):
    id: Optional[str]  # Ensure this is a string, not ObjectId
    email: EmailStr
    hashed_password: str

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


    @classmethod
    def from_mongo(cls, data):
        # Check if data is a dictionary (i.e., not already a UserModel)
        if isinstance(data, dict):
            data["id"] = str(data["_id"])  # Convert ObjectId to string if it's a dict
            del data["_id"]  # Optional: Remove _id key to avoid confusion
        return cls(**data)  # Return an instance of UserModel


