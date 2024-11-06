from fastapi import APIRouter, HTTPException, Depends
from .crud import get_user_by_email, create_user
from .schemas import UserCreate, UserResponse
from pymongo import MongoClient
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import jwt
import os
from .models import UserModel  # Assuming this is where the UserModel is defined

# MongoDB client connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client["mycrm"]
users_collection = db["users"]

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT secret key and algorithm
SECRET_KEY = "mysecretkey"  # Change to a stronger secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time

router = APIRouter()

# Function to hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Function to create JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Signup endpoint
@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate):
    # Check if email already exists
    existing_user = get_user_by_email(users_collection, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password before saving
    hashed_password = hash_password(user.password)

    # Create new user in the database (returns a UserModel instance)
    new_user_data = create_user(users_collection, user.email, hashed_password)
    
    # If create_user returns a Pydantic UserModel, no need for from_mongo
    if isinstance(new_user_data, UserModel):
        return new_user_data  # Directly return the UserModel instance
    
    # Otherwise, use from_mongo to convert the data
    new_user = UserModel.from_mongo(new_user_data)
    return new_user

# Login endpoint
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Find user by email
    user = get_user_by_email(users_collection, form_data.username)
    
    # Check if the user exists and the password is correct
    if not user or not verify_password(form_data.password, user.hashed_password):  # Use hashed_password
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer", "message": "Login successful"}
