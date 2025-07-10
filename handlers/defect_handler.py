from telegram import Update
from telegram.ext import CallbackContext

def defect_handler(update: Update, context: CallbackContext):
    update.message.reply_text("🔍 Раздел «Дефекты клиентов» пока в разработке.")
