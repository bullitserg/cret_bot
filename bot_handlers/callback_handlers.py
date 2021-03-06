import decorators
from config import *
from logger import logger, chat_info_logger
import bot_workers.checks_workers as checks_workers
import bot_workers.reports_workers as reports_workers
from bot_functions.bot_functions import standard_message, get_username


# обработка колбэков
@decorators.only_registered
@decorators.only_authorised(USER_DATA)
@decorators.is_activity(USER_DATA)
def callback_query_handler(bot, update):
    query = update.callback_query
    chat_id = query.message.chat_id

    menu = data = query.data
    last_menu = USER_DATA[chat_id]['last_menu']
    message_text = USER_DATA[chat_id]['menu'][last_menu]['message'][menu]

    update.callback_query.message.delete()

    # если существует клавиатура, то отправляем и ее, если нет, то только текст
    # если клавиатуры нет, то
    if menu in USER_DATA[chat_id]['menu'].keys():
        reply_markup = USER_DATA[chat_id]['menu'][menu]['buttons']
        worker = False
    else:
        reply_markup = None
        worker = query.data

    bot.send_message(text=message_text,
                     chat_id=chat_id,
                     reply_markup=reply_markup)

    # пишем указатель на последнее меню
    USER_DATA[chat_id]['last_menu'] = menu

    # указываем, что ожидать
    USER_DATA[chat_id]['wait'] = data

    # если определен воркер - вызываем его
    if worker:
        worker_type = 'callback'
        sh_worker = '_'.join([worker_type, worker])
        # пишем указатель о последней выполненной команде и сообщении в ней
        USER_DATA[chat_id]['last_command'] = (worker, worker_type, message_text)

        if hasattr(checks_workers, sh_worker):
            worker_call = getattr(checks_workers, sh_worker)
            return worker_call(bot, update, USER_DATA)

        elif hasattr(reports_workers, sh_worker):
            worker_call = getattr(reports_workers, sh_worker)
            return worker_call(bot, update, USER_DATA)

        else:
            logger.info('%s: Worker %s not exists' % (__name__, sh_worker))


# обработка колбэков диалога
@decorators.only_registered
@decorators.only_authorised(USER_DATA)
@decorators.is_activity(USER_DATA)
def callback_dialog_handler(bot, update):
    username = get_username(update)
    query = update.callback_query
    chat_id = query.message.chat_id

    update.callback_query.message.delete()

    if query['data'] == 'dialog_yes':
        message = USER_DATA[chat_id]['dialog_function']()
    else:
        message = USER_DATA[chat_id]['dialog_answer_on_no']

    bot.send_message(text=message,
                     chat_id=chat_id
                     )

    chat_info_logger(username, chat_id, message)



