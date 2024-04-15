from aiogram.filters import Filter
from aiogram.types import Message

from bot.misc.util import CONFIG


class IsAdmin(Filter):
    def __init__(self):
        self.id_admins = CONFIG.admin_tg_id

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.id_admins
