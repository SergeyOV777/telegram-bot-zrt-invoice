# Деплой Telegram бота на сервер Timeweb

Этот документ содержит инструкции по настройке автономной работы Telegram бота для создания инвойсов на сервере Timeweb.

## 📋 Предварительные требования

1. **Сервер Timeweb** с доступом по SSH
2. **Telegram Bot Token** (получить у @BotFather)
3. **Google Sheets API** настроенный
4. **Service Account JSON** файл для Google API

## 🚀 Быстрый деплой

### 1. Подключение к серверу
```bash
ssh root@your-server-ip
```

### 2. Загрузка файлов
```bash
# Создаем директорию
mkdir -p /root/telegram_invoice_bot
cd /root/telegram_invoice_bot

# Загружаем файлы проекта (через scp или git)
# scp -r ./telegram_invoice_bot/* root@your-server-ip:/root/telegram_invoice_bot/
```

### 3. Запуск автоматического деплоя
```bash
chmod +x deploy.sh
./deploy.sh
```

### 4. Настройка конфигурации
```bash
nano /root/telegram_invoice_bot/.env
```

Заполните файл `.env`:
```env
BOT_TOKEN=your_telegram_bot_token_here
GOOGLE_CREDENTIALS=your_google_credentials_here
SPREADSHEET_ID=your_spreadsheet_id_here
SHEET_NAME=your_sheet_name_here
SERVICE_ACCOUNT_FILE=service_account.json
```

### 5. Запуск бота
```bash
# Делаем скрипт управления исполняемым
chmod +x manage.sh

# Запускаем бота
./manage.sh start

# Включаем автозапуск
./manage.sh enable

# Проверяем статус
./manage.sh status
```

## 🔧 Ручная настройка

### Установка зависимостей
```bash
apt update && apt upgrade -y
apt install -y python3 python3-pip python3-venv git curl wget
```

### Создание виртуального окружения
```bash
cd /root/telegram_invoice_bot
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Настройка systemd служб
```bash
# Копируем службы
cp bot.service /etc/systemd/system/
cp monitor.service /etc/systemd/system/

# Перезагружаем systemd
systemctl daemon-reload

# Включаем автозапуск
systemctl enable bot
systemctl enable monitor
```

## 📊 Управление ботом

### Основные команды
```bash
# Запуск/остановка
./manage.sh start
./manage.sh stop
./manage.sh restart

# Статус и логи
./manage.sh status
./manage.sh logs

# Обновление
./manage.sh update
```

### Просмотр логов
```bash
# Логи бота в реальном времени
journalctl -u bot -f

# Логи мониторинга
journalctl -u monitor -f

# Все логи
journalctl -u bot
journalctl -u monitor
```

## 🔍 Мониторинг

### Автоматический мониторинг
Мониторинг запускается автоматически и проверяет:
- Статус службы бота
- Ответы API Telegram
- Автоматический перезапуск при сбоях

### Ручная проверка
```bash
# Проверка статуса службы
systemctl status bot

# Проверка API бота
curl "https://api.telegram.org/botYOUR_TOKEN/getMe"
```

## 🛠️ Устранение неполадок

### Бот не запускается
```bash
# Проверяем логи
journalctl -u bot -n 50

# Проверяем конфигурацию
cat /root/telegram_invoice_bot/.env

# Проверяем зависимости
source /root/telegram_invoice_bot/venv/bin/activate
python -c "import telegram; print('OK')"
```

### Проблемы с Google API
```bash
# Проверяем service account файл
ls -la /root/telegram_invoice_bot/service_account.json

# Тестируем подключение к Google Sheets
python -c "
from services.sheets_service import get_clients
print('Testing Google Sheets connection...')
try:
    clients = get_clients()
    print(f'Found {len(clients)} clients')
except Exception as e:
    print(f'Error: {e}')
"
```

### Проблемы с сетью
```bash
# Проверяем подключение к интернету
ping -c 3 api.telegram.org
ping -c 3 googleapis.com

# Проверяем DNS
nslookup api.telegram.org
```

## 📈 Производительность

### Мониторинг ресурсов
```bash
# Использование памяти
free -h

# Использование CPU
top

# Дисковое пространство
df -h
```

### Оптимизация
- Бот использует ~50-100MB RAM
- Логи автоматически ротируются
- Перезапуск при превышении памяти

## 🔒 Безопасность

### Рекомендации
1. Используйте сильные пароли для SSH
2. Настройте firewall
3. Регулярно обновляйте систему
4. Не храните токены в открытом виде

### Firewall настройка
```bash
# Устанавливаем ufw
apt install ufw

# Настраиваем правила
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи: `./manage.sh logs`
2. Проверьте статус: `./manage.sh status`
3. Перезапустите бота: `./manage.sh restart`
4. Проверьте конфигурацию в файле `.env`

## 🔄 Обновления

### Автоматическое обновление
```bash
./manage.sh update
```

### Ручное обновление
```bash
cd /root/telegram_invoice_bot
git pull
source venv/bin/activate
pip install -r requirements.txt
systemctl restart bot
```

---

**Важно**: После деплоя обязательно проверьте работу бота, отправив ему команду `/start` в Telegram! 