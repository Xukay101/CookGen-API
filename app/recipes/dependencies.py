from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Recipe

async def get_recipe_by_id(id: int, db: AsyncSession = Depends(get_db)) -> Recipe:
    result = await db.execute(select(Recipe).options(joinedload(Recipe.ingredients)).filter_by(id=id))
    recipe = result.scalars().first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe