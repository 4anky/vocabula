from datetime import datetime
from pydantic import BaseModel, EmailStr

__all__ = (
    'UserCreate',
    'UserOut',
)

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True  # важно, чтобы Pydantic мог работать с SQLAlchemy объектами


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    is_active: bool = True
