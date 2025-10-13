from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_db
from ..models import User
from ..schemas import UserCreate, UserOut
from ..services import create_user, get_all_users

__all__ = ('users_router',)

users_router = APIRouter(prefix='/users', tags=['Users'])


@users_router.post('', response_model=UserOut)
async def create_one_user(
    user_in: UserCreate, db: AsyncSession = Depends(get_db)
) -> User:
    return await create_user(db, user_in)


@users_router.get('', response_model=list[UserOut])
async def get_users(db: AsyncSession = Depends(get_db)) -> Sequence[User]:
    return await get_all_users(db)
