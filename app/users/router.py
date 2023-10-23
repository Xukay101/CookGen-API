from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserRead
from app.models import User, UserPreference
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.users.schemas import UserPreferenceRead, UserPreferenceCreate

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
    return {"message": "Preferences updated successfully"}