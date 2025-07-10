# handlers/invoice_handler.py

from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from services.sheets_service import get_all_invoices
from services.invoice_formatter import format_invoice_block


def invoice_handler(update: Update, context: CallbackContext):
    """Отправляет счёт(а) по имени клиента из Google Sheets."""
    client_name = update.message.text.strip()

    # Обработка кнопки '⬅️ Назад в меню'
    if client_name == "⬅️ Назад в меню":
        from menu import get_main_menu_keyboard
        update.message.reply_text("Главное меню:", reply_markup=get_main_menu_keyboard())
        return

    invoices = get_all_invoices()

    # Фильтруем счета по имени клиента
    user_invoices = [
        inv for inv in invoices if inv.get('Клиент', '').strip().lower() == client_name.lower()
    ]

    # Получаем список клиентов для клавиатуры
    clients = sorted({inv.get('Клиент', '').strip() for inv in invoices if inv.get('Клиент')})
    keyboard = [[client] for client in clients]
    keyboard.append(["⬅️ Назад в меню"])
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    if not user_invoices:
        update.message.reply_text(
            f"❌ Для клиента «{client_name}» нет неоплаченных счетов.",
            reply_markup=reply_markup
        )
        return

    # Формируем и отправляем счёт по шаблону
    block, total = format_invoice_block(client_name, user_invoices)
    payment_details = context.user_data.get('payment_details', 'Сбербанк, Тинькофф, Альфа — по номеру телефона 89264071093.')
    update.message.reply_text(f"{client_name} 👇", parse_mode='HTML', reply_markup=reply_markup)
    update.message.reply_text(f"{block}\nИтого: {total}₽\n\n{payment_details}")

# Новый обработчик для inline-кнопок

def invoice_callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data

    invoices = get_all_invoices()
    clients = context.user_data.get('client_list', [])
    keyboard = [[InlineKeyboardButton(client, callback_data=f"client_idx:{i}")] for i, client in enumerate(clients)]
    keyboard.append([InlineKeyboardButton("⬅️ Назад в меню", callback_data="back_to_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    if data == "back_to_menu":
        from menu import get_main_menu_inline
        query.edit_message_text("Главное меню:", reply_markup=get_main_menu_inline())
        return

    if data.startswith("client_idx:"):
        idx = int(data.split("client_idx:", 1)[1])
        if idx < 0 or idx >= len(clients):
            query.answer("Ошибка выбора клиента.")
            return
        client_name = clients[idx]
        user_invoices = [
            inv for inv in invoices if inv.get('Клиент', '').strip().lower() == client_name.lower()
        ]
        if not user_invoices:
            context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"❌ Для клиента «{client_name}» нет неоплаченных счетов."
            )
        else:
            block, total = format_invoice_block(client_name, user_invoices)
            payment_details = context.user_data.get('payment_details', 'Сбербанк, Тинькофф, Альфа — по номеру телефона 89264071093.')
            context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"{client_name} 👇"
            )
            context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"{block}\nИтого: {total}₽\n\n{payment_details}"
            )
        # После ответа снова показываем меню с клиентами
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите клиента:",
            reply_markup=reply_markup
        )
        return
