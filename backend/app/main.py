from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import your routers
from .api import users

# Create FastAPI instance
app = FastAPI()

# Add CORS middleware to allow frontend app to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify specific domains here instead of "*" for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your routers
app.include_router(users.router, prefix="/api/users")  # User signup route
