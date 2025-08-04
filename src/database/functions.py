from sqlalchemy.future import select

from src.database import models
from sqlalchemy.ext.asyncio import AsyncSession


async def add_new_user(user_id: int, db: AsyncSession):
    query = select(models.Users).where(models.Users.id == user_id)

    instance = await db.scalar(query)

    if instance:
        return

    user_model = models.Users(id=user_id)
    db.add(user_model)
    await db.commit()


async def add_new_executor(user_id: int, data: dict, db: AsyncSession):
    new_executor = models.Executors(id=user_id,
                                    region=data.get('location'),
                                    name=data.get('name'),
                                    categories=list(data.get('selected_categories')))

    db.add(new_executor)
    await db.commit()
