import io
import logging
from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
from bot.database.methods.get import all_proxy

log = logging.getLogger(__name__)

proxy_manager_router = Router()


@proxy_manager_router.message(F.text == 'Все Прокси ⚡️')
async def remove_proxy(message: Message) -> None:
    all_proxi = await all_proxy()
    str_proxi = ''
    count = 1
    for proxy in all_proxi:
        date_string = str(proxy.period)
        date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f")
        formatted_date = date.strftime("%d.%m.%Y %H:%M")
        str_proxi += (
            f'{count})'
            f'{proxy.ip} | до: {formatted_date}--  '
            f' Пользователь: {proxy.user.username} '
            f'({proxy.user.telegram_id})'
            f' \n'
        )
        count += 1
    if str_proxi == '':
        await message.answer('Ни у одного клиента нету прокси')
        return

    file_stream = io.BytesIO(str_proxi.encode()).getvalue()
    input_file = BufferedInputFile(file_stream, 'all_proxy.txt')
    await message.answer_document(input_file)
