from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import DateTime, Boolean

from bot.database.main import engine


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)
    fullname = Column(String)
    proxies = relationship("Proxy", back_populates="user")
    payments = relationship("Payment", back_populates="user")


class Proxy(Base):
    __tablename__ = 'proxy'
    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String)
    period = Column(DateTime)
    admin_message = Column(Boolean, default=False)
    first_day = Column(Boolean, default=False)
    second_day = Column(Boolean, default=False)
    third_day = Column(Boolean, default=False)
    user = relationship("User", back_populates="proxies")
    user_id = Column(Integer, ForeignKey('users.telegram_id'))


class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    payment_system = Column(String)
    payment_id = Column(String)
    user_id = Column(Integer, ForeignKey('users.telegram_id'))
    user = relationship("User", back_populates="payments")


async def create_all_table():
    async_engine = engine()
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
