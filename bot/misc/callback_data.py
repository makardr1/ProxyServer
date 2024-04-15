from aiogram.filters.callback_data import CallbackData


class MessageAdminUser(CallbackData, prefix='message_admin_user'):
    id_user: int


class AddProxyClient(CallbackData, prefix='add_proxy_client'):
    id_user: int


class ShowProxyClient(CallbackData, prefix='show_proxy_client'):
    id_user: int


class AddProxy(CallbackData, prefix='add_proxy'):
    id_user: int
    proxy: str
    count_day: int


class ChangeProxy(CallbackData, prefix='change_proxy'):
    id_proxy: int
    ip_proxy: str


class DeleteProxy(CallbackData, prefix='delete_proxy'):
    id_proxy: int
    ip_proxy: str


class DeleteProxyYes(CallbackData, prefix='delete_proxy_yes'):
    id_proxy: int
    ip_proxy: str


class DeleteProxyNo(CallbackData, prefix='delete_proxy_no'):
    id_proxy: int
    ip_proxy: str


class EditProxy(CallbackData, prefix='edit_proxy'):
    id_proxy: int
    days: int


class NoPaymentProxyUser(CallbackData, prefix='edit_proxy'):
    ip_proxy: str
    id_user: int
    username: str


class NetworkName(CallbackData, prefix='network_name'):
    network_name: str
