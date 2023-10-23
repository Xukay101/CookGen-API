import os
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi_pagination.links import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Recipe, User, Ingredient
from app.schemas import RecipeCreate, RecipeRead, RecipeImage, RecipeUpdate
from app.database import get_db
from app.config import settings
from app.auth.dependencies import get_current_user
from app.recipes.utils import get_file_extension, delete_image_from_directory
from app.recipes.dependencies import get_recipe_by_id

router = APIRouter(prefix='/recipes', tags=['recipes'], responses={404: {'description': 'Not found'}})

@router.get('/search-by-preferences', status_code=200, response_model=Page[RecipeRead])
async def search_by_preferences(
    gluten_free: bool = False, 
    low_carb: bool = False, 
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await db.refresh(current_user, attribute_names=['preferences'])

    # Building query based in preferences
    liked_ingredients = [p.ingredient_id for p in current_user.preferences if p.preference_type == 'like']
    disliked_ingredients = [p.ingredient_id for p in current_user.preferences if p.preference_type in ['dislike', 'allergy']]

    # # Get liked ingredients
    query = select(Recipe).where(
        Recipe.ingredients.any(Ingredient.id.in_(liked_ingredients))
    )

    # # Exclude disliked ingredients
    query = query.where(
        ~Recipe.ingredients.any(Ingredient.id.in_(disliked_ingredients))
    )

    # # Check if gluten free and low carb
    if gluten_free:
        query = query.where(Recipe.gluten_free == True)
    if low_carb:
        query = query.where(Recipe.low_carb == True)

    data = await paginate(db, query)
    return data

@router.post('/', status_code=201, response_model=RecipeRead)
async def create_recipe(
    recipe: RecipeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify if ingredients exist
    result = await db.execute(select(Ingredient).filter(Ingredient.id.in_(recipe.ingredients)))
    ingredients = result.scalars().all()

    if len(ingredients) != len(recipe.ingredients):
        raise HTTPException(status_code=400, detail='Some ingredient IDs are invalid')

    # New recipe instance
    recipe_dict = recipe.model_dump()
    recipe_dict.pop('ingredients', None)
    new_recipe = Recipe(**recipe_dict)

    # Add author_id
    new_recipe.author_id = current_user.id
    new_recipe.ingredients = ingredients

    db.add(new_recipe)
    await db.commit()

    result = await db.execute(select(Recipe).options(joinedload(Recipe.ingredients)).filter_by(id=new_recipe.id))
    new_recipe = result.scalar()

    return new_recipe 

@router.get('/{id}/image', status_code=200, response_model=RecipeImage)
async def get_recipe_image(recipe: Recipe = Depends(get_recipe_by_id)):
    image_directory = os.path.join('app', 'static', 'images')
    saved_file_extension = get_file_extension(image_directory, recipe.image_name)
    image_url = f'{settings.BASE_URL}static/images/{recipe.image_name}.{saved_file_extension}'
    return {'id': recipe.id, 'image_url': image_url}

@router.patch('/{id}/image', status_code=201, response_model=RecipeRead, description='Upload/Update image')
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

    await db.refresh(recipe, attribute_names=['ingredients'])

    return recipe

@router.get('/', status_code=200, response_model=Page[RecipeRead])
async def get_recipes(db: AsyncSession = Depends(get_db)):
    data = await paginate(db, select(Recipe).options(joinedload(Recipe.ingredients)).order_by(Recipe.created_at))
    return data


@router.get('/{id}', status_code=200, response_model=RecipeRead)
async def get_recipe(recipe: Recipe = Depends(get_recipe_by_id)):
    return recipe

@router.put('/{id}', status_code=200, response_model=RecipeRead)
async def update_recipe(
    recipe_data: RecipeUpdate,
    recipe: Recipe = Depends(get_recipe_by_id),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check owner
    if not recipe.author_id == current_user.id:
        raise HTTPException(403, 'Not authorized to modify this recipe')

    for field, value in recipe_data.model_dump().items():
        if value is not None:
            setattr(recipe, field, value)

    await db.commit()

    await db.refresh(recipe, attribute_names=['ingredients'])

    return recipe


@router.delete('/{id}', status_code=204)
async def delete_recipe(
    recipe: Recipe = Depends(get_recipe_by_id),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check owner
    if not recipe.author_id == current_user.id:
        raise HTTPException(403, 'Not authorized to delete this recipe')

    await db.delete(recipe)
    await db.commit()

    return