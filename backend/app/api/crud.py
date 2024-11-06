# backend/app/crud.py

from .models import UserModel
from pymongo.collection import Collection
from passlib.context import CryptContext
from typing import Optional
from bson import ObjectId

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(collection, email: str):
    user_data = collection.find_one({"email": email})
    if user_data:
        # Return an instance of UserModel instead of a dictionary
        return UserModel.from_mongo(user_data)
    return None

def create_user(users_collection: Collection, email: str, hashed_password: str) -> UserModel:
    user = {"email": email, "hashed_password": hashed_password}
    users_collection.insert_one(user)
    # Return UserModel with id as str
    user["id"] = str(user["_id"])  # Convert ObjectId to string
    return UserModel(**user)

