#!/bin/bash

# Скрипт для деплоя Telegram бота на сервер Timeweb

echo "🚀 Начинаем деплой Telegram бота..."

# Обновляем систему
echo "📦 Обновляем систему..."
apt update && apt upgrade -y

# Устанавливаем Python и необходимые пакеты
echo "🐍 Устанавливаем Python и зависимости..."
apt install -y python3 python3-pip python3-venv git curl wget

# Создаем директорию для бота
echo "📁 Создаем директорию для бота..."
mkdir -p /root/telegram_invoice_bot
cd /root/telegram_invoice_bot

# Клонируем репозиторий (если нужно)
# git clone https://github.com/your-repo/telegram_invoice_bot.git .

# Создаем виртуальное окружение
echo "🔧 Создаем виртуальное окружение..."
python3 -m venv venv
source venv/bin/activate

# Устанавливаем зависимости
echo "📚 Устанавливаем зависимости Python..."
pip install --upgrade pip
pip install -r requirements.txt

# Создаем .env файл (нужно будет заполнить вручную)
echo "⚙️ Создаем конфигурационный файл..."
cat > .env << EOF
# Telegram Bot Token
BOT_TOKEN=your_bot_token_here

# Google Sheets API
GOOGLE_CREDENTIALS=your_google_credentials_here
SPREADSHEET_ID=your_spreadsheet_id_here
SHEET_NAME=your_sheet_name_here
SERVICE_ACCOUNT_FILE=service_account.json
EOF

echo "⚠️  ВАЖНО: Отредактируйте файл .env и добавьте ваши токены!"

# Копируем systemd службу
echo "🔧 Настраиваем systemd службу..."
cp bot.service /etc/systemd/system/
systemctl daemon-reload

# Устанавливаем права на выполнение
chmod +x /root/telegram_invoice_bot/main.py

echo "✅ Деплой завершен!"
echo "📋 Следующие шаги:"
echo "1. Отредактируйте файл .env: nano /root/telegram_invoice_bot/.env"
echo "2. Запустите бота: systemctl start bot"
echo "3. Включите автозапуск: systemctl enable bot"
echo "4. Проверьте статус: systemctl status bot"
echo "5. Посмотрите логи: journalctl -u bot -f" 