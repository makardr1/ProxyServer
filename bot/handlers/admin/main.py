import io
import logging
from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.utils.formatting import Bold, Text

from bot.database.methods.get import all_payments
from bot.filters.main import IsAdmin
from bot.handlers.admin.proxy_manager import proxy_manager_router
from bot.handlers.admin.user_manager import user_manager_router
from bot.keyboards.reply import back_menu, admin_menu
from bot.misc.callback_data import MessageAdminUser

log = logging.getLogger(__name__)

admin_router = Router()
admin_router.message.filter(IsAdmin())

admin_router.include_routers(
    user_manager_router,
    proxy_manager_router
)


class EditUser(StatesGroup):
    input_message_user = State()


@admin_router.message(
    (F.text == 'Админ панель 🃏') |
    (F.text == 'Назад ↩️')
)
async def command(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(f"Hello Administrator, "
                         f"<b>{message.from_user.full_name}!</b>",
                         reply_markup=await admin_menu())


@admin_router.message(F.text == 'Платежи 💰')
async def admin(message: Message) -> None:
    payments = await all_payments()
    str_payments = ''
    count = 1
    for payment in payments:
        date_string = str(payment.date)
        date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f")
        formatted_date = date.strftime("%d.%m.%Y %H:%M")
        str_payments += \
            (f'{count})'
             f' Пользователь: {payment.user.username} '
             f'({payment.user.telegram_id})'
             f' - Сеть платежа: {payment.payment_system}'
             f' - ID платежа: {payment.payment_id}'
             f' | Дата: {formatted_date}\n')
        count += 1
    if str_payments == '':
        await message.answer('На ваших кошельках нет поступлений 😥')
        return

    file_stream = io.BytesIO(str_payments.encode()).getvalue()
    input_file = BufferedInputFile(file_stream, 'payments.txt')
    await message.answer_document(input_file)


@admin_router.callback_query(MessageAdminUser.filter())
async def message_admin_callback_query(
        call: CallbackQuery,
        state: FSMContext,
        callback_data: MessageAdminUser):
    await call.message.delete()
    await call.message.answer(
        'Введите сообщение 🖊',
        reply_markup=await back_menu())
    await state.update_data(tgid=callback_data.id_user)
    await state.set_state(EditUser.input_message_user)
    await call.answer()


@admin_router.message(EditUser.input_message_user)
async def edit_user_callback_query(message: Message, state: FSMContext):
    text = Text(
        Bold('Сообщение от администратора:'), '\n',
        message.text.strip()
    )
    data = await state.get_data()
    try:
        await message.bot.send_message(int(data['tgid']), **text.as_kwargs())
        await message.answer(
            'Сообщение отправлено 👍',
            reply_markup=await admin_menu()
        )
    except Exception as e:
        print(e, 'Error send message admin -- user')
        await message.answer(
            '❌ Ошибка при отправке, '
            'вероятно пользователь заблокировал бота 🤖',
            reply_markup=await admin_menu()
        )
    await state.clear()
