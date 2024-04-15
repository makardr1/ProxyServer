import json
import os


class Text:
    name: str
    hello_message: str
    help_message: str
    payment_massage: str
    instruction_walletpay: str
    history_user_massage: str

    def __init__(self):
        try:
            with open('texts.json', encoding="utf-8") as file_handler:
                text_mess = json.load(file_handler)
            for k, v in text_mess.items():
                setattr(self, k, v)
        except FileNotFoundError as e:
            text_error = (f'Файла text.json не существует\n'
                          f'Скопируйте из архива и вставьте в корень проекта\n'
                          f'{e}')
            raise FileNotFoundError(text_error)
        except ValueError as e:
            text_error = (f'Вы допустили ошибку в файле text.json\n'
                          f'Проверьте там должна быть такая структура:\n'
                          f'{{\n'
                          f'"value1":"текст",\n'
                          f'"value2":"текст" \n '
                          f'}}\n'
                          f'{e}')
            raise ValueError(text_error)


class Config:
    admin_tg_id: list
    UTC_time: int
    admin_interaction_user: int
    tg_token: str
    COUNT_SECOND_DAY: int = 86400
    address_usdt: str
    address_bitcoin: str

    def __init__(self):
        try:
            with open('config.json', encoding="utf-8") as file_handler:
                text_mess = json.load(file_handler)
            for k, v in text_mess.items():
                setattr(self, k, v)

        except FileNotFoundError as e:
            text_error = (f'Файла config.json не существует\n'
                          f'Скопируйте из архива и вставьте в корень проекта\n'
                          f'{e}')
            raise FileNotFoundError(text_error)
        except ValueError as e:
            text_error = (f'Вы допустили ошибку в файле config.json\n'
                          f'Проверьте там должна быть такая структура:\n'
                          f'{{\n'
                          f'"value1":"текст",\n'
                          f'"value2": 150 \n '
                          f'}}\n'
                          f'{e}')
            raise ValueError(text_error)
        self.write_env()

    def write_env(self):
        env_admin = int(os.getenv("ADMIN_ID", 0))
        list_admin = [env_admin]
        self.admin_tg_id = (
            list_admin
            if self.admin_tg_id == []
            else self.admin_tg_id
        )
        self.admin_interaction_user = (
            os.getenv("ADMIN_ID", 0)
            if self.admin_interaction_user == 0
            else self.admin_interaction_user
        )


CONFIG = Config()
TEXT = Text()
