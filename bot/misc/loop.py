import logging
from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.utils.formatting import Text, Code, Underline, Bold

from bot.database.methods.get import all_active_proxy
from bot.database.methods.update import update_third_day
from bot.keyboards.inline import extend_proxy
from bot.misc.Payment.payment_systems import check_payments
from bot.misc.util import CONFIG

log = logging.getLogger(__name__)

COUNT_SECOND_DAY = 86400

ONE_DAY = 1


async def loop(bot: Bot):
    try:
        active_proxy = await all_active_proxy()
        for proxy in active_proxy:
            await check_date(proxy, bot)
    except Exception as e:
        log.error(e)


async def check_date(proxy, bot: Bot):
    date_proxy = proxy.period
    now_date = datetime.utcnow() + timedelta(hours=CONFIG.UTC_time)
    count_day = (date_proxy - now_date).days
    fun_message = ACTION_MESSAGE.get(count_day + ONE_DAY)
    if fun_message is not None:
        await fun_message(proxy, bot)


async def admin_message(proxy, bot: Bot):
    for admin_id in CONFIG.admin_tg_id:
        context = Text(
            'У пользователя ID', Code(proxy.user_id),
            ' истекла аренда прокси\n',
            '🔗 ', Underline(proxy.ip), '\n'
                                       '🗓 ', Bold(proxy.period)
        )
        await bot.send_message(
            admin_id,
            **context.as_kwargs()
        )
        await update_third_day(proxy.id, True, True, True, True)


async def tree_message_user(proxy, bot: Bot):
    if not proxy.first_day:
        await update_third_day(proxy.id, True, True, True, False)
        text = Text(
            'Добрый день 👋',
            'У вас заканчивается срок аренды прокси ',
            Code(proxy.ip),
            ' уже через 2 дня, если вы не продлите аренду мы будем вынуждены '
            'отозвать прокси 🗓\n',
        )
        await bot.send_message(
            proxy.user_id,
            **text.as_kwargs(),
            reply_markup=await extend_proxy(day_message=2)
        )


async def two_message_user(proxy, bot: Bot):
    if not proxy.second_day:
        await update_third_day(proxy.id, True, True, False, False)
        text = Text(
            'Добрый день 👋',
            'У вас заканчивается срок аренды прокси ',
            Code(proxy.ip), ' через 5 дней!\n'
            'Вы будете продливать?'
        )
        await bot.send_message(
            proxy.user_id,
            **text.as_kwargs(),
            reply_markup=await extend_proxy(day_message=5, proxy=proxy)
        )
        await check_payments(proxy.user_id, bot)


async def one_message_user(proxy, bot: Bot):
    if not proxy.third_day:
        await update_third_day(proxy.id, True, False, False, False)
        text = Text(
            'Добрый день 👋 \n',
            'У вас заканчивается срок аренды прокси ', Code(proxy.ip), '\n'
            'через 10 дней! 🗓'
        )
        await bot.send_message(
            proxy.user_id,
            **text.as_kwargs()
        )


ACTION_MESSAGE = {
    0: admin_message,
    2: tree_message_user,
    5: two_message_user,
    10: one_message_user,
}
