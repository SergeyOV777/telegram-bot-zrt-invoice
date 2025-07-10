from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from services.sheets_service import get_all_invoices, get_all_vyezd_invoices
from services.invoice_formatter import format_invoice_block
from services.vyezd_invoice_formatter import format_vyezd_invoice_block

def remont_vyezd_invoice_callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    invoices_remont = get_all_invoices()
    invoices_vyezd = get_all_vyezd_invoices()
    clients = context.user_data.get('remont_vyezd_client_list', [])
    keyboard = [[InlineKeyboardButton(client, callback_data=f"remontvyezd:client_idx:{i}")] for i, client in enumerate(clients)]
    keyboard.append([InlineKeyboardButton("⬅️ Назад в меню", callback_data="back_to_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    if data == "back_to_menu":
        from menu import get_main_menu_inline
        query.edit_message_text("Главное меню:", reply_markup=get_main_menu_inline())
        return

    if data.startswith("remontvyezd:client_idx:"):
        idx = int(data.split("remontvyezd:client_idx:", 1)[1])
        if idx < 0 or idx >= len(clients):
            query.answer("Ошибка выбора клиента.")
            return
        client_name = clients[idx]
        user_remont = [inv for inv in invoices_remont if inv.get('Клиент', '').strip().lower() == client_name.lower()]
        user_vyezd = [inv for inv in invoices_vyezd if inv.get('Name', '').strip().lower() == client_name.lower()]
        total_remont = 0
        total_vyezd = 0
        block_remont = block_vyezd = ""
        if user_remont:
            block_remont, total_remont = format_invoice_block(client_name, user_remont)
        if user_vyezd:
            block_vyezd, total_vyezd = format_vyezd_invoice_block(client_name, user_vyezd)
        if not user_remont and not user_vyezd:
            context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"❌ Для клиента «{client_name}» нет неоплаченных ремонтов и выездов."
            )
        else:
            total_sum = total_remont + total_vyezd
            payment_details = context.user_data.get('payment_details', 'Сбербанк, Тинькофф, Альфа — по номеру телефона 89264071093.')
            text = f"{client_name} 👇"
            context.bot.send_message(
                chat_id=query.message.chat_id,
                text=text
            )
            text2 = f""
            if block_remont:
                text2 += f"{block_remont}\nИтого обслуживание: {total_remont}₽\n\n"
            if block_vyezd:
                text2 += f"{block_vyezd}\nИтого тренировки: {total_vyezd}₽\n\n"
            text2 += f"Всего к оплате: {total_sum}₽\n\n{payment_details}"
            context.bot.send_message(
                chat_id=query.message.chat_id,
                text=text2
            )
        # После ответа снова показываем меню с клиентами
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите клиента:",
            reply_markup=reply_markup
        )
        return 