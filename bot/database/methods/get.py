from datetime import datetime, timedelta
from typing import Sequence

from sqlalchemy import select, not_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from bot.database.main import engine
from bot.database.models.main import User, Proxy, Payment
from bot.misc.util import CONFIG


async def all_users():
    async with AsyncSession(autoflush=False, bind=engine()) as session:
        result = await session.execute(select(User))
        return result.scalars().all()


async def all_payments():
    async with AsyncSession(autoflush=False, bind=engine()) as session:
        search = select(Payment).options(joinedload(Payment.user))
        result = await session.execute(search)
        return result.scalars().all()


async def found_user(telegram_id) -> User:
    async with AsyncSession(autoflush=False, bind=engine()) as session:
        return await _found_user(telegram_id, session)


async def _found_user(telegram_id, session) -> User:
    result = await session.execute(
        select(User).filter(User.telegram_id == telegram_id))
    return result.scalars().first()


async def every_proxy(id_user) -> Sequence[Proxy]:
    async with AsyncSession(autoflush=False, bind=engine()) as session:
        search = select(Proxy).where(Proxy.user_id == id_user)
        result = await session.execute(search)
        proxies = result.scalars().all()
        return proxies


async def all_active_proxy() -> Sequence[Proxy]:
    async with AsyncSession(autoflush=False, bind=engine()) as session:
        search = select(Proxy).where(
            not_(Proxy.first_day) |
            not_(Proxy.second_day) |
            not_(Proxy.third_day)
        ).options(joinedload(Proxy.user))
        result = await session.execute(search)
        proxies = result.scalars().all()
        return proxies


async def all_proxy() -> Sequence[Proxy]:
    async with AsyncSession(autoflush=False, bind=engine()) as session:
        search = select(Proxy).options(
            joinedload(Proxy.user)
        ).order_by(Proxy.period)
        result = await session.execute(search)
        proxies = result.scalars().all()
        return proxies


async def one_proxy(id_proxy):
    async with AsyncSession(autoflush=False, bind=engine()) as session:
        search = select(Proxy).where(Proxy.id == id_proxy)
        result = await session.execute(search)
        proxies = result.scalars().first()
        return proxies


async def every_payment(id_user) -> Sequence[Payment]:
    async with AsyncSession(autoflush=False, bind=engine()) as session:
        search = select(Payment).where(Payment.user_id == id_user)
        result = await session.execute(search)
        payments = result.scalars().all()
        return payments


async def payment_verification(id_user):
    async with AsyncSession(autoflush=False, bind=engine()) as session:
        search = select(Payment).where(Payment.user_id == id_user)
        result = await session.execute(search)
        payments = result.scalars().all()
        for payment in payments:
            current_date = datetime.utcnow() + timedelta(hours=CONFIG.UTC_time)
            later_date = datetime.utcnow() + timedelta(hours=CONFIG.UTC_time-1)
            if (payment.date.day,
                payment.date.hour) == (current_date.day,
                                       current_date.hour):
                return True
            elif (payment.date.day,
                  payment.date.hour) == (later_date.day,
                                         later_date.hour):
                return True
        return False
