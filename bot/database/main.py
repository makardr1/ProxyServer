from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "sqlite+aiosqlite:///bot/database/Database.db"


def engine():
    return create_async_engine(DATABASE_URL)
