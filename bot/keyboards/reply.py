from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.misc.util import CONFIG


async def main_menu(id_user) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    if id_user in CONFIG.admin_tg_id:
        kb.button(text='Админ панель 🃏')
    kb.button(text="Оплатить Proxy 💳")
    kb.button(text="История платежей 📋")
    kb.button(text="Помощь ❕")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


async def back_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Вернуться ↩️")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


async def admin_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Платежи 💰')
    kb.button(text='Клиенты 👥')
    kb.button(text='Все Прокси ⚡️')
    kb.button(text='Вернуться ↩️')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


async def back_admin_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Назад ↩️')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


async def admin_users_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Список клиентов 📒')
    kb.button(text='Найти клиента 🔎')
    kb.button(text="Назад ↩️")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
