from datetime import datetime

from fastapi import Depends, HTTPException
from pydantic import ValidationError
from jose import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models import User
from app.auth.schemas import TokenPayload
from app.auth.utils import is_token_revoked

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    # Check if token in blacklist
    token_revoked = await is_token_revoked(token)
    if token_revoked:
        raise HTTPException(status_code=401, detail='Token has been revoked')

    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=401,
                detail='Access Token expired',
                headers={'WWW-Authenticate': 'Bearer'},
            )

        # Get user
        query = select(User).where(User.id == token_data.sub)
        result = await db.execute(query)
        user = result.scalars().first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail='User not found',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        
        return user


    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

async def get_token_payload(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return TokenPayload(**payload)
    except jwt.JWTError:
        raise HTTPException(status_code=403, detail='Could not validate token')