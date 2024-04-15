import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.formatting import Text, Code, Bold

from bot.database.methods.create import payment_term
from bot.keyboards.inline import extend_proxy
from bot.keyboards.reply import back_menu, main_menu
from bot.misc.Payment.TrustWalletPay import TrustWalletPay
from bot.misc.callback_data import NoPaymentProxyUser, NetworkName
from bot.misc.util import CONFIG

log = logging.getLogger(__name__)

payment_router = Router()


class PaymentId(StatesGroup):
    payment_id = State()


@payment_router.message(F.text == 'Оплатить Proxy 💳')
async def command(message: Message, state: FSMContext) -> None:
    await state.clear()
    if CONFIG.address_usdt == '':
        await message.answer('Админ не подключил адреса для оплаты')
        return
    await pay_payment(message, message.from_user.id, 0)


async def pay_payment(message, id_telegram, price):
    payment = TrustWalletPay(
        CONFIG,
        message,
        id_telegram,
        price
    )
    log.info(
        f'The user('
        f'{message.from_user.username}'
        f'-{message.from_user.id}) '
        f'started the payment process payment'
    )
    await payment.to_pay()


@payment_router.callback_query(F.data == 'extend_proxy_data')
async def message_admin(callback: CallbackQuery):
    await pay_payment(callback.message, callback.from_user.id, 0)
    await callback.answer()


@payment_router.callback_query(NoPaymentProxyUser.filter())
async def without_extension(
        callback: CallbackQuery,
        callback_data: NoPaymentProxyUser
):
    await callback.message.edit_reply_markup(
        reply_markup=await extend_proxy(day_message=1)
    )
    for admin_id in CONFIG.admin_tg_id:
        context = Text(
            'Пользователь ',
            Bold(callback_data.username),
            '(', Code(callback_data.id_user), ')'
            'не захотел продлевать прокси ',
            Code(callback_data.ip_proxy)
        )
        await callback.message.bot.send_message(
            admin_id,
            **context.as_kwargs()
        )
    await callback.answer()


@payment_router.callback_query(NetworkName.filter())
async def payment_acceptance(
        callback: CallbackQuery,
        callback_data: NetworkName,
        state: FSMContext):
    await callback.message.answer(
        'Введите ID',
        reply_markup=await back_menu()
    )
    await state.update_data(network_name=callback_data.network_name)
    await state.set_state(PaymentId.payment_id)
    await callback.answer()


@payment_router.message(PaymentId.payment_id)
async def sending_payment(message: Message, state: FSMContext):
    await state.update_data(payment_id=message.text)
    data = await state.get_data()
    await payment_term(
        data['payment_id'],
        data['network_name'],
        message.from_user.id
    )
    await state.clear()
    await message.answer(
        'ID отправлен, спасибо 👌',
        reply_markup=await main_menu(message.from_user.id)
    )
    for admin_id in CONFIG.admin_tg_id:
        context = Text(
            '❗️❗️❗️Пользователь ',
            Bold(message.from_user.username),
            '(', Code(message.from_user.id), ')', '\n',
            'отправил ID платежа ',
            Code(data['payment_id'])
        )
        await message.bot.send_message(
            admin_id,
            **context.as_kwargs()
        )
