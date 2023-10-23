from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination

from app.config import settings
from app.auth.router import router as auth_router
from app.recipes.router import router as recipes_router
from app.ingredients.router import router as ingredients_router
from app.users.router import router as users_router

app = FastAPI()

# Mount static file
app.mount('/static', StaticFiles(directory='app/static'), name='static')

# Routers
app.include_router(auth_router)
app.include_router(recipes_router)
app.include_router(ingredients_router)
app.include_router(users_router)

# Root Endpoint
@app.get('/', tags=['root'])
async def root():
    return {'message': f'Welcome to {settings.APP_NAME}'}

# Add pagination
add_pagination(app)