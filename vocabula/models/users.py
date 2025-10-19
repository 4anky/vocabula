from sqlalchemy import BigInteger, Column, DateTime, String, text

from vocabula.db.base import Base

__all__ = ('User',)


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))
