import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.formatting import Text, Code, Italic
from bot.database.methods.create import new_user
from bot.database.methods.get import found_user, every_payment
from bot.handlers.admin.user_manager import converter_date
from bot.handlers.user.user_payment import payment_router
from bot.keyboards.inline import button_message_admin, message_admin_user
from bot.keyboards.reply import main_menu, back_menu
from bot.misc.util import TEXT, CONFIG

log = logging.getLogger(__name__)


class WithdrawalFunds(StatesGroup):
    input_amount = State()
    payment_method = State()
    communication = State()
    input_message_admin = State()


user_router = Router()
user_router.include_routers(payment_router)


@user_router.message(F.text == '/start')
async def command(message: Message, state: FSMContext) -> None:
    user = await found_user(message.from_user.id)
    if user is None:
        try:
            user_name = f'@{str(message.from_user.username)}'
        except Exception as e:
            log.error(e)
            user_name = str(message.from_user.username)
        await new_user(
            message.from_user.id,
            user_name,
            message.from_user.full_name
        )
    await start_message(message, state)


async def start_message(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        TEXT.hello_message,
        reply_markup=await main_menu(message.from_user.id))


@user_router.message(F.text == 'Вернуться ↩️')
async def back(message: Message, state: FSMContext) -> None:
    await start_message(message, state)


@user_router.message(F.text == 'Помощь ❕')
async def customer_assistance(message: Message) -> None:
    await message.answer(
        TEXT.help_message,
        reply_markup=await button_message_admin()
    )


@user_router.message(F.text == 'История платежей 📋')
async def payment_history(message: Message) -> None:
    await message.answer(TEXT.history_user_massage)
    payments = await every_payment(message.from_user.id)
    if len(payments) != 0:
        list_message = ['']
        index_list = 0
        for payment in payments:
            list_message[index_list] += (
                 f'📅 Дата: {await converter_date(payment.date.date())};\n'
                 f'📫 ID платежа: {payment.payment_id};\n'
                 f'💰 Сеть: {payment.payment_system}.\n\n'
            )
            if len(list_message[index_list]) > 3500:
                list_message.append('')
                index_list += 1
        for text in list_message:
            await message.answer(text)
    else:
        await message.answer('У вас ещё нет платежей 🧐')


@user_router.callback_query(F.data == 'message_admin')
async def message_admin(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(
        'Введите сообщение которое увидит администратор',
        reply_markup=await back_menu()
    )
    await state.set_state(WithdrawalFunds.input_message_admin)
    await callback_query.answer()


@user_router.message(WithdrawalFunds.input_message_admin)
async def input_message_admin(message: Message, state: FSMContext):
    person = message.from_user
    try:
        text = Text(
            'Пользователь ', person.full_name, ' ',
            '(@', person.username, ' | ', Code(person.id), ')'
            'написал вам сообщение:',
            '\n',
            Italic(message.text.strip())
        )
        await message.bot.send_message(
            CONFIG.admin_interaction_user, **text.as_kwargs(),
            reply_markup=await message_admin_user(person.id)
        )
        await message.answer(
            'Администратор получил ваше сообщение 👌',
            reply_markup=await main_menu(person.id)
        )
    except Exception as e:
        await message.answer(
            'Администратор не смог получить ваше сообщение 😿',
            reply_markup=await main_menu(person.id)
        )
        log.error(e, 'Error admin message')
    await state.clear()
