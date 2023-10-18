import os
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Recipe, User
from app.schemas import RecipeCreate, RecipeRead, RecipeImage
from app.database import get_db
from app.config import settings
from app.auth.dependencies import get_current_user
from app.recipes.utils import get_file_extension, delete_image_from_directory
from app.recipes.dependencies import get_recipe_by_id

router = APIRouter(prefix='/recipes', tags=['recipes'], responses={404: {"description": "Not found"}})

@router.post('/', status_code=201, response_model=RecipeRead)
async def create_recipe(
    recipe: RecipeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # New recipe instance
    new_recipe = Recipe(**recipe.model_dump())

    # Add author_id
    new_recipe.author_id = current_user.id

    db.add(new_recipe)
    await db.commit()
    await db.refresh(new_recipe)

    return new_recipe 

@router.get('/{id}/image', status_code=200, response_model=RecipeImage)
async def get_recipe_image(recipe: Recipe = Depends(get_recipe_by_id)):
    image_directory = os.path.join('app', 'static', 'images')
    saved_file_extension = get_file_extension(image_directory, recipe.image_name)
    image_url = f'{settings.BASE_URL}static/images/{recipe.image_name}.{saved_file_extension}'
    return {"id": recipe.id, "image_url": image_url}

@router.post('/{id}/image', status_code=201, response_model=RecipeRead)
async def update_image(
    image_file: UploadFile,
    recipe: Recipe = Depends(get_recipe_by_id),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if current_user is owner
    if not recipe.author_id == current_user.id:
        raise HTTPException(403, 'Not authorized to modify this recipe')

    # Check if file imagen is none, if image exist delete to the database
    image_directory = os.path.join('app', 'static', 'images')
    if recipe.image_name:
        delete_image_from_directory(image_directory, recipe.image_name)

    # Read img file
    content = await image_file.read()
    file_extension = image_file.filename.split('.')[-1] 

    # Generate a unique filename using UUID
    unique_filename = uuid.uuid4()

    # Save img file
    image_path = os.path.join('app', 'static', 'images', f'{unique_filename}.{file_extension}')
    with open(image_path, 'wb') as buffer:
        buffer.write(content)

    recipe.image_name = str(unique_filename)
    await db.commit()
    await db.refresh(recipe)

    return recipe

@router.get('/{id}', status_code=200, response_model=RecipeRead)
async def get_recipe(recipe: Recipe = Depends(get_recipe_by_id), db: AsyncSession = Depends(get_db)):
    return recipe