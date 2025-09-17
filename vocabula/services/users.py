from sqlalchemy.future import select
from ..models import User
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas import UserCreate

__all__ = (
    'create_user',
    'get_all_users',
)


async def create_user(db: AsyncSession, user_in: UserCreate):
    user = User(email=str(user_in.email), username=user_in.username)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()
