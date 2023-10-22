import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import engine, Base
from app.models import User, Ingredient
from app.auth.utils import get_hashed_password

async def init_admin_user(session):
    admin = User(username='admin', email='admin@admin.com', password=get_hashed_password('admin'), full_name='Administrator')
    session.add(admin)
    await session.commit()

async def load_ingredients_from_csv(session, csv_path):
    df = pd.read_csv(csv_path, encoding='utf8')

    df['name'] = df['name'].astype(str).apply(lambda x: x.encode('utf-8'))
    df['description'] = df['description'].astype(str).apply(lambda x: x.encode('utf-8'))

    for _, row in df.iterrows():
        ingredient = Ingredient(
            name=row['name'],
            description=row['description'],
            author_id=1
        )
        session.add(ingredient)
    await session.commit()

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:
        await init_admin_user(session)

        await load_ingredients_from_csv(session, 'app/static/ingredients.csv')

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())