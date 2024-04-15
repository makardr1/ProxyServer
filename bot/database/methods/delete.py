from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.main import engine
from bot.database.models.main import Proxy


async def remove_proxy_yes(proxy_id):
    async with AsyncSession(autoflush=False, bind=engine()) as session:
        search = delete(Proxy).where(Proxy.id == proxy_id)
        await session.execute(search)
        await session.commit()
