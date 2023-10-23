from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination.links import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Ingredient, User
from app.schemas import IngredientRead, IngredientCreate, IngredientUpdate
from app.ingredients.dependencies import get_ingredient_by_id
from app.auth.dependencies import get_current_user

router = APIRouter(prefix='/ingredients', tags=['ingredients'], responses={404: {"description": "Not found"}})

@router.get('/', status_code=200, response_model=Page[IngredientRead])
async def get_ingredients(db: AsyncSession = Depends(get_db)):
    query = select(Ingredient).options(joinedload(Ingredient.recipes)).order_by(Ingredient.name)
    data = await paginate(db, query)
    return data

@router.get('/{id}', status_code=200, response_model=IngredientRead)
async def get_ingredient(ingredient: Ingredient = Depends(get_ingredient_by_id)):
    return ingredient

@router.post('/', status_code=201, response_model=IngredientRead)
async def create_ingredient(
    ingredient: IngredientCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Create new ingredient
    new_ingredient = Ingredient(**ingredient.model_dump())
    new_ingredient.author_id = current_user.id

    # Add new ingredient
    db.add(new_ingredient)
    await db.commit()
    await db.refresh(new_ingredient)

    return new_ingredient

@router.put('/{id}', status_code=200, response_model=IngredientRead)
async def update_ingredient(
    ingredient_data: IngredientUpdate,
    ingredient: Ingredient = Depends(get_ingredient_by_id),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if is owner
    if not ingredient.author_id == current_user.id:
        raise HTTPException(403, 'Not authorized to modify this ingredient')

    # Update ingredients values
    for field, value in ingredient_data.model_dump().items():
        if value is not None:
            setattr(ingredient, field, value)

    await db.commit()
    await db.refresh(ingredient)

    return ingredient

@router.put('/{id}', status_code=204)
async def delete_ingredient(
    ingredient: Ingredient = Depends(get_ingredient_by_id),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if is owner
    if not ingredient.author_id == current_user.id:
        raise HTTPException(403, 'Not authorized to delete this ingredient')

    await db.delete(ingredient)
    await db.commit()

    return

