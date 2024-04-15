import asyncio
import uuid

from WalletPay import AsyncWalletPayAPI

from bot.keyboards.inline import wallet_pay
from bot.misc.Payment.payment_systems import PaymentSystem


class WalletPay(PaymentSystem):
    WALLET: type(AsyncWalletPayAPI)

    def __init__(self, config, message, user_id, price):
        super().__init__(message, user_id, price)
        self.WALLET = AsyncWalletPayAPI(api_key=config.tg_wallet_token)

    async def new_order(self):
        order = await self.WALLET.create_order(
            amount=self.price,
            currency_code="RUB",
            description='Оплата Proxy',
            external_id=str(uuid.uuid4()),
            timeout_seconds=60,
            customer_telegram_user_id=self.user_id
        )
        return order

    async def check_pay_wallet(self, order, time):
        tic = 0
        while tic < time:
            order_preview = await self.WALLET.get_order_preview(
                order_id=order.id)
            if order_preview.status == "PAID":
                await self.successful_payment(
                    self.price,
                    'WalletPay'
                )
                return
            tic += 2
            await asyncio.sleep(2)
        return

    async def to_pay(self):
        order = await self.new_order()
        await self.message.answer(
            f'Оплата Proxy на <b>{self.price} $</b>',
            reply_markup=await wallet_pay(order)
        )
        try:
            await self.check_pay_wallet(order, self.TIME_CHECK)
        except Exception as e:
            print(e, 'The payment count_day has expired')

    def __str__(self):
        return 'Платежная система WalletPay'
