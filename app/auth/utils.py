from typing import Union, Any
from datetime import timedelta, datetime

from passlib.context import CryptContext
from jose import jwt

from app.config import settings
from app.database import get_redis

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Password hash
def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Token generation
def create_access_token(subject: Union[str, Any]) -> str:
    expires_delta = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
    return encoded_jwt

# Cache Tokens
async def revoke_token(token: str, expires_in: int):
    r = await get_redis()
    await r.set(token, "revoked", ex=expires_in)
    await r.aclose()

async def is_token_revoked(token: str) -> bool:
    r = await get_redis()
    token_status = await r.get(token)
    await r.aclose()
    if token_status:
        return token_status.decode('utf-8')  == "revoked"
    return False

