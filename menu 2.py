from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu_inline():
    keyboard = [
        [InlineKeyboardButton('💼 Получить счёт по клиенту (ремонт + выезды)', callback_data='main:remont_vyezd')],
        [InlineKeyboardButton('🔧 Получить счёт по клиенту (ремонт)', callback_data='main:remont')],
        [InlineKeyboardButton('🚚 Получить счёт по клиенту (выезды)', callback_data='main:vyezd')],
        [InlineKeyboardButton('🐞 Дефекты клиентов', callback_data='main:defects')],
        [InlineKeyboardButton('💰 Изменить реквизиты оплаты', callback_data='main:payedit')],
    ]
    return InlineKeyboardMarkup(keyboard)