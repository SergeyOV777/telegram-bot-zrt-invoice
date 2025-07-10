from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext

def show_main_menu(update: Update, context: CallbackContext):
    keyboard = [
        [KeyboardButton("🧾 Получить счёт по клиенту")],
        [KeyboardButton("📤 Список клиентов")],
        [KeyboardButton("🔍 Дефекты клиентов")]
    ]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("Выберите действие:", reply_markup=markup)

def start(update: Update, context: CallbackContext):
    show_main_menu(update, context)
