from datetime import datetime

from pydantic import BaseModel

__all__ = (
    'UserCreate',
    'UserOut',
)


class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        orm_mode = True  # важно, чтобы Pydantic мог работать с SQLAlchemy объектами


class UserCreate(BaseModel):
    username: str
