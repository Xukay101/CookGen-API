from fastapi import FastAPI

from app.config import settings
from app.auth.router import router as auth_router

app = FastAPI()

# Routers
app.include_router(auth_router)

# Root Endpoint
@app.get('/', tags=["root"])
async def root():
    return {'message': f'Welcome to {settings.APP_NAME}'}