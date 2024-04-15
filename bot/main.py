import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.database.models.main import create_all_table
from bot.misc import TgKeys
from bot.handlers.user import user_router
from bot.handlers.admin import admin_router
from bot.misc.commands import set_commands
from bot.misc.loop import loop


async def start_bot():
    dp = Dispatcher(
        storage=MemoryStorage(),
        fsm_strategy=FSMStrategy.USER_IN_CHAT
    )
    dp.include_routers(
        user_router,
        admin_router
    )
    await create_all_table()
    scheduler = AsyncIOScheduler()
    bot = Bot(token=TgKeys.TOKEN, parse_mode=ParseMode.HTML)
    await set_commands(bot)
    scheduler.add_job(loop, "interval", seconds=15, args=(bot,))
    logging.getLogger('apscheduler.executors.default').setLevel(
        logging.WARNING)
    scheduler.start()
    await dp.start_polling(bot)
