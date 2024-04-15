import logging
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.main import engine
from bot.database.models.main import Proxy

log = logging.getLogger(__name__)


async def edit_day_proxy(id_proxy, days):
    async with AsyncSession(autoflush=False, bind=engine()) as session:
        search = select(Proxy).where(Proxy.id == id_proxy)
        result = await session.execute(search)
        proxy = result.scalars().first()
        proxy.period += timedelta(days=days)
        proxy.first_day = False
        proxy.second_day = False
        proxy.third_day = False
        proxy.admin_message = False
        edit_day = proxy.period
        ip_proxy = proxy.ip
        await session.commit()
        return edit_day, ip_proxy


async def update_third_day(id_proxy, mes_ten, mes_fiv, mes_two, mes_adm):
    async with AsyncSession(autoflush=False, bind=engine()) as session:
        search = select(Proxy).where(Proxy.id == id_proxy)
        result = await session.execute(search)
        proxy = result.scalars().first()
        proxy.first_day = mes_two
        proxy.second_day = mes_fiv
        proxy.third_day = mes_ten
        proxy.admin_message = mes_adm
        await session.commit()
