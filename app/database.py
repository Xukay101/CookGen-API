import redis.asyncio as redis

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings 

DATABASE_URI = f'mysql+asyncmy://{settings.DATABASE_USER}:{settings.DATABASE_PASS}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

engine = create_async_engine(DATABASE_URI, echo=True, future=True, pool_pre_ping=True)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db() -> AsyncSession:
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

async def get_redis():
    redis_url = f"redis://:{settings.REDIS_PASS}@{settings.REDIS_HOST}:{settings.REDIS_PORT}"
    return redis.from_url(redis_url)