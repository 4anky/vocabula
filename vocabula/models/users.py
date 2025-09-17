from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, text
from vocabula.db.base import Base

__all__ = (
    'User',
)


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    username = Column(String(50), nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, server_default=text('true'))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))
