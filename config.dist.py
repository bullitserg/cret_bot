from collections import defaultdict

CONFIG = 'config.conf'
MESSAGE_PREFIX = {'OK': '✅'}

TOKEN = '***:******'
administrator_email = 'bullit88@mail.ru'
bot_version = '0.5'
bot_nickname = 'ebender_bot'
authorisation_regexp = "^pass [0-9]{4}$"
registered_chat_id = [********]
log_format = '[%(asctime)s]# %(levelname)-8s   %(message)s'
clear_waits_time = 1
unlogin_timeout = 60
message_max_len = 500

# создаем словари, заполняемые на любую глубину по вызову ключа
tree = lambda: defaultdict(tree)
USER_DATA = defaultdict(tree)
