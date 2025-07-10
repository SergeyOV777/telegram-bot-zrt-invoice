from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from services.sheets_service import get_all_vyezd_invoices
from services.vyezd_invoice_formatter import format_vyezd_invoice_block

def vyezd_invoice_callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    invoices = get_all_vyezd_invoices()
    clients = context.user_data.get('vyezd_client_list', [])
    keyboard = [[InlineKeyboardButton(client, callback_data=f"vyezd:client_idx:{i}")] for i, client in enumerate(clients)]
    keyboard.append([InlineKeyboardButton("⬅️ Назад в меню", callback_data="back_to_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    if data == "back_to_menu":
        from menu import get_main_menu_inline
        query.edit_message_text("Главное меню:", reply_markup=get_main_menu_inline())
        return

    if data.startswith("vyezd:client_idx:"):
        idx = int(data.split("vyezd:client_idx:", 1)[1])
        if idx < 0 or idx >= len(clients):
            query.answer("Ошибка выбора клиента.")
            return
        client_name = clients[idx]
        user_invoices = [inv for inv in invoices if inv.get('Name', '').strip().lower() == client_name.lower()]
        if not user_invoices:
            context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"❌ Для клиента «{client_name}» нет неоплаченных выездов."
            )
        else:
            block, total = format_vyezd_invoice_block(client_name, user_invoices)
            context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"{client_name} 👇"
            )
            context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"{block}\nИтого: {total}₽"
            )
        # После ответа снова показываем меню с клиентами
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите клиента:",
            reply_markup=reply_markup
        )
        return 