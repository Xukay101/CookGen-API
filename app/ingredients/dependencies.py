from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Ingredient

async def get_ingredient_by_id(id: int, db: AsyncSession = Depends(get_db)) -> Ingredient:
    result = await db.execute(select(Ingredient).options(joinedload(Ingredient.recipes)).filter_by(id=id))
    ingredient = result.scalars().first()
    if not ingredient:
        raise HTTPException(status_code=404, detail='Ingredient not found')
    return ingredient