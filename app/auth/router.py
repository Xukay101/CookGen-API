from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserBase, UserCreate
from app.database import get_db
from app.models import User
from app.utils import model_to_dict
from app.auth.utils import get_hashed_password, verify_password, create_access_token
from app.auth.schemas import Token
from app.auth.dependencies import get_current_user

router = APIRouter(prefix='/auth', tags=['auth'], responses={404: {"description": "Not found"}})

@router.post('/register', status_code=201, response_model=UserBase)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if username or email already exists
    query = select(User).filter((User.username == user.username) | (User.email == user.email))
    result = await db.execute(query)
    user_found = result.scalars().first()
    if user_found:
        raise HTTPException(409, 'User already exists')

    # Hashing password
    user.password = get_hashed_password(user.password)

    # New user instance
    new_user = User(**user.model_dump())

    # Add new user to database
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return model_to_dict(new_user) 

@router.post('/login', status_code=200, response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # Check username and get user
    query = select(User).filter(User.username == form_data.username)
    result = await db.execute(query)
    user = result.scalars().first()
    if not user:
        raise HTTPException(401, 'Incorrect username or password')

    # Check password
    if not verify_password(form_data.password, user.password):
        raise HTTPException(401, 'Incorrect username or password')

    # Create JWT Token
    access_token = create_access_token(user.id)

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verify", status_code=200)
async def verify_token(current_user: int = Depends(get_current_user)):
    return {"status": "Token is valid", "user_id": current_user.id}
