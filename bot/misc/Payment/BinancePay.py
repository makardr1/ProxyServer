import logging
import asyncio
import random

from bot.keyboards.inline import binance_pay
from bot.misc.Payment.payment_systems import PaymentSystem
from binance.pay.merchant import Merchant as Client
from binance.pay.lib.utils import config_logging


config_logging(logging, logging.DEBUG)


class BinancePay(PaymentSystem):
    PREPAY_ID: str
    ORDER_ID: str

    def __init__(self, config, message, user_id, price):
        super().__init__(message, user_id, price)
        self.client = Client(config.binance_api_key, config.binance_secret_key)
        self.ORDER_ID = ''.join([str(random.randint(0, 9)) for _ in range(20)])

    async def check_pay_wallet(self, time):
        tic = 0
        while tic < time:
            response = self.client.get_order(merchantTradeNo=self.ORDER_ID)
            if response['data']['status'] == 'PAID':
                await self.successful_payment(
                    self.price,
                    'BinancePay'
                )
                return
            tic += 2
            await asyncio.sleep(2)
        return

    async def new_order(self):
        parameters = {
            "env": {"terminalType": "MINI_PROGRAM"},
            "merchantTradeNo": self.ORDER_ID,
            "orderAmount": self.price,
            "currency": "USDT",
            "goods": {
                "goodsType": "01",
                "goodsCategory": "0000",
                "referenceGoodsId": "abc001",
                "goodsName": "Proxy",
                "goodsUnitAmount": {"currency": "USDT", "amount": self.price},
            },
            "shipping": {
                "shippingName": {"firstName": "Joe", "lastName": "Don"},
                "shippingAddress": {"region": "NZ"},
            },
            "buyer": {"buyerName": {"firstName": "cz", "lastName": "zhao"}},
        }
        response = self.client.new_order(parameters)
        self.PREPAY_ID = response['data']['prepayId']
        return response

    async def to_pay(self):
        order = await self.new_order()
        await self.message.answer_photo(
            photo=order['data']['qrcodeLink'],
            caption=f'Оплата Proxy на <b>{self.price} $</b>',
            reply_markup=await binance_pay(order['data']['checkoutUrl'])
        )
        try:
            await self.check_pay_wallet(self.TIME_CHECK)
        except Exception as e:
            print(e, 'The payment count_day has expired')

    def __str__(self):
        return 'Платежная система WalletPay'
