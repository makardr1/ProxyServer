from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.misc.callback_data import MessageAdminUser, AddProxyClient, \
    ShowProxyClient, AddProxy, ChangeProxy, DeleteProxy, EditProxy, \
    NoPaymentProxyUser, DeleteProxyYes, DeleteProxyNo, NetworkName

from bot.misc.util import TEXT


async def button_message_admin() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Написать администратору 💬',
        callback_data='message_admin'
    )
    return kb.as_markup()


async def wallet_pay(order) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='👛 Pay via Wallet', url=order.pay_link)
    kb.button(text='Инструкция по оплате 🧾', url=TEXT.instruction_walletpay)
    kb.adjust(1)
    return kb.as_markup()


async def binance_pay(link) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔶 Заплатить 🔶', url=link)
    kb.adjust(1)
    return kb.as_markup()


async def message_admin_user(tgid_user) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Ответить 💬',
        callback_data=MessageAdminUser(id_user=tgid_user)
    )
    kb.adjust(1)
    return kb.as_markup()


async def edit_client_menu(telegram_id) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Выдать прокси 📥',
        callback_data=AddProxyClient(id_user=telegram_id)
    )
    kb.button(
        text='Выданные прокси 📄',
        callback_data=ShowProxyClient(id_user=telegram_id)
    )
    kb.adjust(1)
    return kb.as_markup()


async def correction(id_user, proxy, count_day) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Да ✔️',
        callback_data=AddProxy(
            id_user=id_user,
            proxy=proxy,
            count_day=count_day
        )
    )
    kb.button(
        text='Нет ✖',
        callback_data='back_menu'
    )
    kb.adjust(1)
    return kb.as_markup()


async def change_proxy(id_proxy, ip_proxy) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Продлить ⏱',
        callback_data=ChangeProxy(
            id_proxy=id_proxy,
            ip_proxy=ip_proxy
        )
    )
    kb.button(
        text='Удалить 🗑',
        callback_data=DeleteProxy(
            id_proxy=id_proxy,
            ip_proxy=ip_proxy
        )
    )
    kb.adjust(1)
    return kb.as_markup()


async def btn_correction_proxy(id_proxy, days) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Да ✔️',
        callback_data=EditProxy(
            id_proxy=id_proxy,
            days=days
        )
    )
    kb.button(
        text='Нет ✖',
        callback_data='back_menu'
    )
    kb.adjust(1)
    return kb.as_markup()


async def extend_proxy(day_message, proxy=None) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Хочу продлить 👈',
        callback_data='extend_proxy_data'
    )
    if day_message == 5:
        kb.button(
            text='Пока что нет 😚',
            callback_data=NoPaymentProxyUser(
                ip_proxy=proxy.ip,
                id_user=proxy.user_id,
                username=proxy.user.username
            )
        )
    kb.adjust(1)
    return kb.as_markup()


async def btn_delete_proxy(id_proxy, ip_proxy) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Да ✔️',
        callback_data=DeleteProxyYes(
            id_proxy=id_proxy,
            ip_proxy=ip_proxy
        )
    )
    kb.button(
        text='Нет ✖',
        callback_data=DeleteProxyNo(
            id_proxy=id_proxy,
            ip_proxy=ip_proxy
        )
    )
    kb.adjust(1)
    return kb.as_markup()


async def sending_id(network_name) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Отправить ID платежа',
        callback_data=NetworkName(
            network_name=network_name
        )
    )
    kb.adjust(1)
    return kb.as_markup()
