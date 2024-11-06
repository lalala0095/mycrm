from pydantic import BaseModel, EmailStr
from bson import ObjectId

# from initial without knowledge
class Item(BaseModel):
    name: str
    description: str

# from starting to integrate users
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Custom Pydantic model to handle MongoDB ObjectId
class UserResponse(BaseModel):
    email: str
    _id: str  # Convert ObjectId to string

    # This is for serialization of ObjectId to string in the response
    class Config:
        orm_mode = True
        # You can use a custom function to convert ObjectId to str if needed
        json_encoders = {
            ObjectId: str
        }
