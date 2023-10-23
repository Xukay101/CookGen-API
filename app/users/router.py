from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserRead
from app.models import User
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.users.schemas import UserPreferenceRead

router = APIRouter(prefix='/users', tags=['users'], responses={404: {"description": "Not found"}})

@router.get('/me', status_code=200, response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get('/me/preferences', status_code=200, response_model=List[UserPreferenceRead])
async def get_preferences(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await db.refresh(current_user, attribute_names=["preferences"])
    
    return current_user.preferences

