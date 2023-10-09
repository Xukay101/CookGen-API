from fastapi import FastAPI

from app.config import settings
from app.database import init_db

app = FastAPI()

# Root Endpoint
@app.get('/')
async def root():
    return {'message': f'Welcome to {settings.APP_NAME}'}

# Events
@app.on_event("startup")
async def on_startup():
    await init_db()