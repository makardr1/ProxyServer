import io
import logging
from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.utils.formatting import Text, Bold, Code, Underline

from bot.database.methods.delete import remove_proxy_yes
from bot.database.methods.get import (
    all_users,
    found_user,
    every_proxy,
    one_proxy
)
from bot.database.methods.update import edit_day_proxy
from bot.database.methods.create import insert_proxy

from bot.keyboards.inline import (
    edit_client_menu,
    correction,
    change_proxy,
    btn_correction_proxy,
    btn_delete_proxy
)
from bot.keyboards.reply import admin_users_menu, back_admin_menu
from bot.misc.callback_data import (
    AddProxyClient,
    ShowProxyClient,
    AddProxy,
    ChangeProxy,
    DeleteProxy,
    EditProxy,
    DeleteProxyYes,
    DeleteProxyNo
)

log = logging.getLogger(__name__)

user_manager_router = Router()

months: dict = {
    1: "января",
    2: "февраля",
    3: "марта",
    4: "апреля",
    5: "мая",
    6: "июня",
    7: "июля",
    8: "августа",
    9: "сентября",
    10: "октября",
    11: "ноября",
    12: "декабря"
}


async def converter_date(date) -> str:
    new_date = datetime.strptime(str(date), "%Y-%m-%d")
    formatted_date = (f"<b>{new_date.day} "
                      f"{months[new_date.month]} "
                      f"{new_date.year} года</b>"
                      )
    return formatted_date


class Identifier(StatesGroup):
    id = State()


class NewProxy(StatesGroup):
    proxy = State()
    period = State()


class AddDay(StatesGroup):
    day = State()


@user_manager_router.message(F.text == 'Клиенты 👥')
async def customers(message: Message) -> None:
    await message.answer(
        'Управление клиентами 🚛',
        reply_markup=await admin_users_menu()
    )


@user_manager_router.callback_query(F.data == 'back_menu')
async def remove_new_proxy(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_reply_markup()
    await callback.message.answer(
        'Управление клиентами 🚛',
        reply_markup=await admin_users_menu()
    )


@user_manager_router.message(F.text == 'Список клиентов 📒')
async def add_client(message: Message) -> None:
    users = await all_users()
    str_user = ''
    count = 1
    for user in users:
        str_user += await string_user(user, count)
        count += 1

    file_stream = io.BytesIO(str_user.encode()).getvalue()
    input_file = BufferedInputFile(file_stream, 'All_users.txt')
    await message.answer_document(input_file)


async def string_user(client, count):
    return (
        f'{count}) {client.fullname} - '
        f'({client.username}|{client.telegram_id})\n'
    )


@user_manager_router.message(F.text == 'Найти клиента 🔎')
async def search_client(message: Message, state: FSMContext) -> None:
    await message.answer(
        'Введите 🆔 клиента',
        reply_markup=await back_admin_menu()
    )
    await state.set_state(Identifier.id)


@user_manager_router.message(Identifier.id)
async def identifier(message: Message, state: FSMContext) -> None:
    try:
        id_user = int(message.text)
    except Exception as e:
        await message.answer('Вводите только цифры')
        log.info(e)
        return
    client = await found_user(id_user)
    if not client:
        await message.answer('Пользователь не найден 🙅‍♂️\nВведите еще раз')
        return
    await message.answer(
        'Результат поиска 🔎',
        reply_markup=await admin_users_menu()
    )
    content = Text(
        '👤 Клиент: ', Bold(client.fullname), '\n',
        '🔗 Ссылка: ', client.username, '\n',
        '🆔: ', Code(client.telegram_id), '\n'
    )
    await message.answer(
        **content.as_kwargs(),
        reply_markup=await edit_client_menu(client.telegram_id)
    )
    await state.clear()


@user_manager_router.callback_query(AddProxyClient.filter())
async def new_proxy(
        callback: CallbackQuery,
        state: FSMContext,
        callback_data: AddProxyClient
):
    await state.update_data(id_user=callback_data.id_user)
    await callback.message.answer(
        '📝 Введите новый прокси для пользователя',
        reply_markup=await back_admin_menu()
    )
    await callback.answer()
    await state.set_state(NewProxy.proxy)


@user_manager_router.message(NewProxy.proxy)
async def proxy(message: Message, state: FSMContext):
    await state.update_data(proxy=message.text)
    await message.answer('📝 Укажите количество дней для работы прокси')
    await state.set_state(NewProxy.period)


@user_manager_router.message(NewProxy.period)
async def period(message: Message, state: FSMContext):
    try:
        count_day = int(message.text)
        if count_day > 2000:
            await message.answer('Максимальное количество дней 2000!')
            return
        elif count_day <= 0:
            await message.answer('Введите больше 0 дней!')
            return
    except Exception as e:
        await message.answer('Вводите только цифры')
        log.info(e)
        return
    data = await state.get_data()
    content = await check_input_proxy(
        data["proxy"],
        count_day,
        data["id_user"]
    )
    await message.answer(
        **content.as_kwargs(),
        reply_markup=await correction(
            data["id_user"],
            data["proxy"],
            count_day
        )
    )
    await state.clear()


async def check_input_proxy(proxy, count_day, id_user=None):
    id_text = '' if id_user is None else f'🆔 ID: {id_user}\n'
    return Text(
        'Вы всё правильно ввели?\n',
        f'{id_text}'
        '⚙️ Прокси: ', Underline(proxy), '\n',
        '📅 Количество дней: ', Bold(count_day)
    )


@user_manager_router.callback_query(AddProxy.filter())
async def add_proxy(callback: CallbackQuery, callback_data: AddProxy):
    await callback.message.edit_reply_markup()
    try:
        completion_time = await insert_proxy(callback_data)
        date = await converter_date(completion_time.date())
        await callback.message.answer(
            f'Прокси успешно добавлен 🎉\n'
            f'Аренда до: {date} 🕑',
            reply_markup=await admin_users_menu()
        )
    except Exception as e:
        await callback.message.answer(
            'Ошибка при попытке записи прокси к клиенту 💢',
            reply_markup=await admin_users_menu()
        )
        log.error(e)


@user_manager_router.callback_query(ShowProxyClient.filter())
async def all_proxy(callback: CallbackQuery, callback_data: ShowProxyClient):
    result = await every_proxy(callback_data.id_user)
    if len(result) == 0:
        await callback.answer(
            'У клиента нет закрепленных прокси!',
            show_alert=True
        )
        return
    for proxy in result:
        date = await converter_date(proxy.period.date())
        await callback.message.answer(
            f'️⚙️ Прокси: <u>{proxy.ip}</u>\n'
            f'📅 Аренда до: {date}',
            reply_markup=await change_proxy(proxy.id, proxy.ip)
        )
    await callback.answer()


@user_manager_router.callback_query(ChangeProxy.filter())
async def extend_proxy(
        callback: CallbackQuery,
        callback_data: ChangeProxy,
        state: FSMContext
):
    await state.update_data(ip_proxy=callback_data.ip_proxy)
    await state.update_data(id_proxy=callback_data.id_proxy)
    await callback.message.answer('📝 Укажите количество дней для продления')
    await state.set_state(AddDay.day)
    await callback.answer()


@user_manager_router.message(AddDay.day)
async def add_day_proxy(message: Message, state: FSMContext):
    try:
        day = int(message.text)
        if day > 2000 or day <= 0:
            raise ValueError
    except Exception as e:
        await message.answer(
            '1) Вводите только цифры;\n'
            '2) Не больше 2000 дней;\n'
            '3) Не меньше 1 дня.'
        )
        log.info(e)
        return
    await state.update_data(day=day)
    data = await state.get_data()
    content = await check_input_proxy(data["ip_proxy"], data["day"])
    await message.answer(
        **content.as_kwargs(),
        reply_markup=await btn_correction_proxy(data["id_proxy"], data["day"])
    )
    await state.clear()


@user_manager_router.callback_query(EditProxy.filter())
async def edit_proxy(callback: CallbackQuery, callback_data: EditProxy):
    await callback.message.edit_reply_markup()
    result = await edit_day_proxy(callback_data.id_proxy, callback_data.days)
    date = await converter_date(result[0].date())
    await callback.message.answer(
        f'⚙️ Прокси ({result[1]}) успешно продлён 🎉\n'
        f'Аренда до: {date} 🕑'
    )


@user_manager_router.callback_query(DeleteProxy.filter())
async def remove_proxy(callback: CallbackQuery,
                       callback_data: DeleteProxy
                       ):
    await callback.message.edit_reply_markup()
    await callback.message.answer(
        'Вы уверены в этом?\n'
        f'⚙️ Прокси для удаления: '
        f'<u>{callback_data.ip_proxy}</u>',
        reply_markup=await btn_delete_proxy(
          callback_data.id_proxy,
          callback_data.ip_proxy
        )
    )


@user_manager_router.callback_query(DeleteProxyYes.filter())
async def delete_proxy_yes(
        callback: CallbackQuery,
        callback_data: DeleteProxyYes
):
    await remove_proxy_yes(callback_data.id_proxy)
    await callback.message.edit_reply_markup()
    await callback.message.answer(
        f'⚙️ Прокси ({callback_data.ip_proxy}) '
        f'успешно удалён 🎉'
    )


@user_manager_router.callback_query(DeleteProxyNo.filter())
async def delete_proxy_no(
        callback: CallbackQuery,
        callback_data: DeleteProxyNo
):
    await callback.message.edit_reply_markup()
    proxy = await one_proxy(callback_data.id_proxy)
    date = await converter_date(proxy.period.date())
    await callback.message.answer(
        f'️⚙️ Прокси: <u>{proxy.ip}</u>\n'
        f'📅 Аренда до: {date}',
        reply_markup=await change_proxy(proxy.id, proxy.ip)
    )
    await callback.answer()
