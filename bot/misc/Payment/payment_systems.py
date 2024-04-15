import asyncio
import logging

from aiogram.utils.formatting import Text, Bold, Code

from bot.database.methods.get import payment_verification
from bot.keyboards.reply import main_menu
from bot.misc.util import CONFIG

log = logging.getLogger(__name__)


class PaymentSystem:
    TOKEN: str
    TIME_CHECK = 60 * 60
    STEP = 5

    def __init__(self, message, user_id, price=None):
        self.message = message
        self.user_id = user_id
        self.price = price

    async def to_pay(self):
        raise NotImplementedError()

    async def successful_payment(self, total_amount, name_payment):
        log.info(f'The user('
                 f'{self.message.from_user.username}'
                 f'-{self.message.from_user.id})'
                 f' paid proxy,'
                 f' amount: {total_amount} USDT,'
                 f' payment: {name_payment}'
                 f' --OK')
        await self.message.answer(
            f'<b>Оплата прошла успешно!</b>\n'
            f'Вы купили Proxy общей стоимостью: '
            f'<u><b>'
            f'{total_amount} $'
            f'</b></u>',
            reply_markup=await main_menu(self.message.from_user.id)
        )
        for admin_id in CONFIG.admin_tg_id:
            context = Text(
                'Пользователь ',
                Bold(self.message.from_user.username),
                '(', Code(self.message.from_user.id), ')', '\n',
                'Оплатил на сумму ', Bold(total_amount), ' $'
            )
            await self.message.bot.send_message(
                admin_id,
                **context.as_kwargs()
            )


async def check_payments(id_user, bot):
    for _ in range(144):
        if await payment_verification(id_user):
            return
        await asyncio.sleep(600)
    for admin_id in CONFIG.admin_tg_id:
        await bot.send_message(
            admin_id,
            f'Пользователь <code>{id_user}</code> не оплатил прокси 🤷‍♂️'
        )
    return
