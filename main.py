import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram.ext import PicklePersistence
from menu import get_main_menu_inline
from handlers.invoice_handler import invoice_handler, invoice_callback_handler
from handlers.client_list_handler import list_clients
from handlers.defect_handler import defect_handler
from handlers.remont_start_handler import remont_start_handler
from handlers.vyezd_start_handler import vyezd_start_handler
from handlers.vyezd_invoice_handler import vyezd_invoice_callback_handler
from handlers.remont_vyezd_start_handler import remont_vyezd_start_handler
from handlers.remont_vyezd_invoice_handler import remont_vyezd_invoice_callback_handler
import config
from telegram import ReplyKeyboardRemove

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


def log_message(update, context):
    user = update.effective_user
    logging.info(f"Получено сообщение от {user.id} ({user.first_name} {user.last_name}): {update.message.text}")

# Обёртка для логирования ответов
class LoggingContext:
    def __init__(self, context, update):
        self._context = context
        self.update = update

    def reply_text(self, text, *args, **kwargs):
        logging.info(f"Бот отправил ответ пользователю {self.update.effective_user.id}: {text}")
        return self.update.message.reply_text(text, *args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._context, name)

# Обёртка для всех хендлеров

def with_logging(handler_func):
    def wrapper(update, context):
        log_message(update, context)
        logging_context = LoggingContext(context, update)
        return handler_func(update, logging_context)
    return wrapper


def start(update, context):
    """Хэндлер команды /start — показывает главное меню."""
    update.message.reply_text(
        "Главное меню:",
        reply_markup=ReplyKeyboardRemove()
    )
    update.message.reply_text(
        "Главное меню:",
        reply_markup=get_main_menu_inline()
    )


def unknown(update, context):
    """Хэндлер неизвестных сообщений."""
    update.message.reply_text(
        "Извините, я не понимаю. Пожалуйста, выберите команду из меню.",
        reply_markup=get_main_menu_inline()
    )


def stub_handler(update, context):
    update.message.reply_text("Раздел в разработке.")

# Оборачиваем все хендлеры (перемещено сюда)
start = with_logging(start)
unknown = with_logging(unknown)
stub_handler = with_logging(stub_handler)
remont_start_handler = with_logging(remont_start_handler)
defect_handler = with_logging(defect_handler)
invoice_handler = with_logging(invoice_handler)


def main_menu_callback_handler(update, context):
    print("main_menu_callback_handler called")
    query = update.callback_query
    data = query.data

    if data == 'main:remont':
        from handlers.remont_start_handler import remont_start_handler
        remont_start_handler(update, context)
    elif data == 'main:vyezd':
        vyezd_start_handler(update, context)
    elif data == 'main:remont_vyezd':
        remont_vyezd_start_handler(update, context)
    elif data == 'main:payedit':
        context.user_data['wait_payment_details'] = True
        query.edit_message_text("Введите новые реквизиты оплаты ⬇️")
        return
    elif data == 'main:defects':
        query.answer()
        query.edit_message_text("Раздел в разработке.", reply_markup=get_main_menu_inline())
    else:
        query.answer()
        query.edit_message_text("Неизвестная команда.", reply_markup=get_main_menu_inline())


def text_handler(update, context):
    # Обработка ввода новых реквизитов оплаты
    if context.user_data.get('wait_payment_details'):
        context.user_data['payment_details'] = update.message.text.strip()
        context.user_data['wait_payment_details'] = False
        update.message.reply_text("Реквизиты приняты")
        update.message.reply_text("Главное меню:", reply_markup=get_main_menu_inline())
        return
    # иначе — стандартная логика invoice_handler
    invoice_handler(update, context)


def error_handler(update, context):
    import traceback
    print("Exception:", traceback.format_exc())
    if update and hasattr(update, 'callback_query') and update.callback_query:
        update.callback_query.answer("Произошла ошибка.", show_alert=True)
    elif update and hasattr(update, 'message') and update.message:
        update.message.reply_text("Произошла ошибка.")


def main():
    """Инициализация и запуск бота."""
    persistence = PicklePersistence(filename='bot_data.pkl')
    updater = Updater(config.BOT_TOKEN, use_context=True, persistence=persistence)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text('💼 Получить счёт по клиенту (ремонт + выезды)'), stub_handler))
    dp.add_handler(MessageHandler(Filters.text('🔧 Получить счёт по клиенту (ремонт)'), remont_start_handler))
    dp.add_handler(MessageHandler(Filters.text('🚚 Получить счёт по клиенту (выезды)'), stub_handler))
    dp.add_handler(MessageHandler(Filters.text('🐞 Дефекты клиентов'), stub_handler))
    dp.add_handler(MessageHandler(Filters.text('💰 Изменить реквизиты оплаты'), stub_handler))
    dp.add_handler(MessageHandler(Filters.text, text_handler))
    dp.add_handler(CallbackQueryHandler(main_menu_callback_handler, pattern='^main:'))
    dp.add_handler(CallbackQueryHandler(remont_vyezd_invoice_callback_handler, pattern='^remontvyezd:'))
    dp.add_handler(CallbackQueryHandler(vyezd_invoice_callback_handler, pattern='^vyezd:'))
    dp.add_handler(CallbackQueryHandler(invoice_callback_handler))
    dp.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()