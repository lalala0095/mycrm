from fastapi import FastAPI
from .api.hello_world import router as hello_router

app = FastAPI()

# Include the hello world route
app.include_router(hello_router)
