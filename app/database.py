from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings 

engine = create_async_engine(settings.DATABASE_URI, echo=True, future=True, pool_pre_ping=True)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

async def init_db():
    from app.models import User
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)