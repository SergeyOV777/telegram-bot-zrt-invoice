from telegram import Update
from telegram.ext import CallbackContext
from services.sheets_service import get_all_invoices

def list_clients(update: Update, context: CallbackContext):
    data = sheets_service.get_all_records()
    clients = sorted({row.get('Клиент', '').strip() for row in data if row.get('Клиент')})
    if not clients:
        update.message.reply_text("Нет доступных клиентов.")
        return
    text = "📋 Список клиентов:\n" + "\n".join(f"• {c}" for c in clients)
    update.message.reply_text(text)
