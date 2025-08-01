from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from services.sheets_service import get_all_invoices

def remont_start_handler(update: Update, context: CallbackContext):
    invoices = get_all_invoices()
    print("DEBUG invoices:", invoices)  # Отладочный вывод
    clients = sorted({inv.get('Клиент', '').strip() for inv in invoices if inv.get('Клиент')})
    if not clients:
        text = "Нет доступных клиентов."
        if hasattr(update, 'message') and update.message:
            update.message.reply_text(text)
        elif hasattr(update, 'callback_query') and update.callback_query:
            update.callback_query.edit_message_text(text)
        return
    context.user_data['client_list'] = clients
    keyboard = [[InlineKeyboardButton(client, callback_data=f"client_idx:{i}")] for i, client in enumerate(clients)]
    keyboard.append([InlineKeyboardButton("⬅️ Назад в меню", callback_data="back_to_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    if hasattr(update, 'message') and update.message:
        update.message.reply_text("Выберите клиента:", reply_markup=reply_markup)
    elif hasattr(update, 'callback_query') and update.callback_query:
        update.callback_query.edit_message_text("Выберите клиента:", reply_markup=reply_markup) 