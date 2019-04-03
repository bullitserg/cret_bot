from cret.cret_mysql_lib import get_query_top, MysqlConnection as Mc
from bot_functions.bot_functions import *
from bot_queries import bot_queries


class BotDbFunctions:
    def __init__(self):
        self.BOT_DB_CONNECTION = Mc(connection=Mc.MS_BOT_CONNECT).connect()

    # Функция получения пароля
    def get_password(self, chat_id):
        user_password = self.BOT_DB_CONNECTION.execute_query(bot_queries.get_user_password_query % chat_id)[0][0]
        return user_password

    # Функция получения help страницы
    def get_help(self, chat_id):
        help_page = '''<b>ОСНОВНОЕ МЕНЮ</b>
        /menu    меню
        /repeat   повтор последней команды
        /help    список доступных команд
        /exit    выход'''
        help_page += '''\n\n<b>ПОЛЬЗОВАТЕЛЬСКОЕ МЕНЮ</b>\n'''
        try:
            help_page += self.BOT_DB_CONNECTION.execute_query(bot_queries.get_help_query % chat_id)[0][0]
        except TypeError:
            help_page += '  Извините, пользовательские команды отсутствуют'
        return help_page

    # Проверка регистрации пользователя
    def is_registered(self, chat_id):
        try:
            self.BOT_DB_CONNECTION.execute_query(bot_queries.check_registration_query % chat_id)[0][0]
        except IndexError:
            is_registered_b = False
        else:
            is_registered_b = True
        return is_registered_b

    # Получение сведений о меню для пользователя и их создание
    def get_menu(self, chat_id):
        user_menu_data = self.BOT_DB_CONNECTION.execute_query(bot_queries.get_menu_query % {'chat_id': chat_id})
        if user_menu_data[0][1]:
            # собираем данные меню из данных mysql
            user_menu = {}
            for menu in user_menu_data:
                # если есть доступные команды

                user_menu[menu[0]] = {
                    'buttons': [menu[1].split(';'),
                                menu[2].split(';')],
                    'message':
                        dict(zip(menu[2].split(';'), menu[3].split(';')))
                }

            # если не заполнен message, то вместо него в запросе UNDEFINED, их надо заменить на None
            # и сразу же создаем меню в формате InlineKeyboard
            for menu in user_menu.keys():
                for message in user_menu[menu]['message'].keys():
                    if user_menu[menu]['message'][message] == 'UNDEFINED':
                        user_menu[menu]['message'][message] = None
                user_menu[menu]['buttons'] = build_menu(user_menu[menu]['buttons'])
        else:
            # если данных по меню нет, значит меню для пользователя не назначено
            user_menu = False
        return user_menu



