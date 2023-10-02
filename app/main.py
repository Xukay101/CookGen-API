from fastapi import FastAPI

from app.config import settings

app = FastAPI()

# Root Endpoint
@app.get('/')
async def root():
    return {'message': f'Welcome to {settings.APP_NAME}'}
