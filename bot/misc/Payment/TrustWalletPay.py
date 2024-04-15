import io
import logging

from aiogram.types import BufferedInputFile

from bot.keyboards.inline import sending_id
from bot.misc.Payment.payment_systems import PaymentSystem
from binance.pay.lib.utils import config_logging
import qrcode

config_logging(logging, logging.DEBUG)


class TrustWalletPay(PaymentSystem):
    ADDRESS_USDT: str
    ADDRESS_BITCOIN: str

    def __init__(self, config, message, user_id, price):
        super().__init__(message, user_id, price)
        self.ADDRESS_USDT = config.address_usdt
        self.ADDRESS_BITCOIN = config.address_bitcoin

    async def to_pay(self):
        await self.message.answer('<b>💰Оплата прокси💰</b>')

        async def qr_code(address) -> BufferedInputFile:
            qr = qrcode.make(address)
            stream = io.BytesIO()
            qr.save(stream, 'PNG')
            stream.seek(0)
            input_file = BufferedInputFile(stream.getvalue(), 'qr-code.png')
            return input_file

        await self.message.answer_photo(
            caption='<b>🎫 Сеть:</b> USDT TRC20\n'
                    '<b>📪 Адрес:</b> '
                    f'<code>{self.ADDRESS_USDT}</code>',
            photo=await qr_code(self.ADDRESS_USDT),
            reply_markup=await sending_id('USDT TRC20')
        )
        await self.message.answer_photo(
            caption='<b>🎫 Сеть:</b> Bitcoin\n'
                    '<b>📪 Адрес:</b> '
                    f'<code>{self.ADDRESS_BITCOIN}</code>',
            photo=await qr_code(self.ADDRESS_BITCOIN),
            reply_markup=await sending_id('Bitcoin')
        )
