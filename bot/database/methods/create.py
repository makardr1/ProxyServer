import logging
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.main import engine

from bot.database.methods.get import _found_user
from bot.database.models.main import User, Proxy, Payment
from bot.misc.util import CONFIG

log = logging.getLogger(__name__)


async def new_user(telegram_id, username, fullname):
    async with AsyncSession(autoflush=False, bind=engine()) as session:
        user = User(
            telegram_id=telegram_id,
            username=username,
            fullname=fullname
        )
        session.add(user)
        await session.commit()
        log.info(f'add user {fullname}')


async def insert_proxy(data):
    async with AsyncSession(autoflush=False, bind=engine()) as session:
        conv_date = datetime.utcnow() + timedelta(
            days=data.count_day,
            hours=CONFIG.UTC_time
        )
        user = await _found_user(data.id_user, session)
        if user is not None:
            new_proxy = Proxy(
                ip=data.proxy,
                period=conv_date,
                user=user
            )
            session.add(new_proxy)
            await session.commit()
            log.info(f'add proxy {data.proxy} owner user ID {data.id_user}')
            return conv_date
        else:
            raise NotImplementedError(f'user {data.id_user} not found')


async def payment_term(payment_id, network_name, user_id):
    async with AsyncSession(autoflush=False, bind=engine()) as session:
        new_payment = Payment(
            date=datetime.utcnow() + timedelta(hours=CONFIG.UTC_time),
            payment_system=network_name,
            payment_id=payment_id,
            user_id=user_id
        )
        session.add(new_payment)
        await session.commit()
