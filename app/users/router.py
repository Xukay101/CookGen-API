from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import paginate
from fastapi_pagination.links import Page
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserRead, RecipeRead
from app.models import User, UserPreference, Recipe
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.users.schemas import UserPreferenceRead, UserPreferenceCreate, SavedRecipe
from app.users.dependencies import get_recipe_by_id

router = APIRouter(prefix='/users', tags=['users'], responses={404: {'description': 'Not found'}})

@router.get('/me', status_code=200, response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get('/me/preferences', status_code=200, response_model=List[UserPreferenceRead])
async def get_preferences(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await db.refresh(current_user, attribute_names=['preferences'])
    
    return current_user.preferences

@router.post('/me/preferences', status_code=201)
async def set_user_preference(
    preference: UserPreferenceCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Check if preferences exist
    query = select(UserPreference).where(UserPreference.user_id == current_user.id)
    result = await db.execute(query)
    existing_preferences = result.scalars().all()

    for existing_preference in existing_preferences:
        if existing_preference.ingredient_id == preference.ingredient_id:
            # If preference exist, update
            existing_preference.preference_type = preference.preference_type
            break
    else:
        # Create new preference
        new_preference = UserPreference(
            user_id = current_user.id,
            **preference.model_dump()
        )
        db.add(new_preference)

    await db.commit()
    return {'message': 'Preferences updated successfully'}

@router.get('/me/saved-recipes', status_code=200, response_model=Page[RecipeRead])
async def get_saved_recipes(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await db.refresh(current_user, attribute_names=['saved_recipes'])

    for saved_recipe in current_user.saved_recipes:
        await db.refresh(saved_recipe, attribute_names=['ingredients'])

    return paginate(current_user.saved_recipes)

@router.post('/me/saved-recipes', status_code=201)
async def add_saved_recipe(
    saved_recipe: SavedRecipe,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Recipe).options(joinedload(Recipe.ingredients)).filter_by(id=saved_recipe.recipe_id)
    result = await db.execute(query)
    recipe = result.scalar()
    if not recipe:
        raise HTTPException(status_code=404, detail='Recipe not found')

    await db.refresh(current_user, attribute_names=['saved_recipes'])
    if recipe not in current_user.saved_recipes:
        current_user.saved_recipes.append(recipe)
    else:
        raise HTTPException(status_code=400, detail='Recipe already saved')

    await db.commit()

    return {'message': 'Recipe saved successfully'}

@router.delete('/me/saved-recipes/{id}', status_code=204)
async def delete_saved_recipe(
    recipe: Recipe = Depends(get_recipe_by_id),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await db.refresh(current_user, attribute_names=['saved_recipes'])
    if recipe in current_user.saved_recipes:
        current_user.saved_recipes.remove(recipe)
    else:
        raise HTTPException(status_code=400, detail='Recipe not found in saved recipes')

    await db.commit()

    return
