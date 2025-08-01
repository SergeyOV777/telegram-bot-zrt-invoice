#!/bin/bash

# Скрипт для управления Telegram ботом

BOT_NAME="bot"

case "$1" in
    start)
        echo "🚀 Запускаем бота..."
        systemctl start $BOT_NAME
        systemctl status $BOT_NAME
        ;;
    stop)
        echo "⏹️ Останавливаем бота..."
        systemctl stop $BOT_NAME
        ;;
    restart)
        echo "🔄 Перезапускаем бота..."
        systemctl restart $BOT_NAME
        systemctl status $BOT_NAME
        ;;
    status)
        echo "📊 Статус бота:"
        systemctl status $BOT_NAME
        ;;
    logs)
        echo "📝 Логи бота (Ctrl+C для выхода):"
        journalctl -u $BOT_NAME -f
        ;;
    logs-all)
        echo "📝 Все логи бота:"
        journalctl -u $BOT_NAME
        ;;
    enable)
        echo "✅ Включаем автозапуск бота..."
        systemctl enable $BOT_NAME
        ;;
    disable)
        echo "❌ Отключаем автозапуск бота..."
        systemctl disable $BOT_NAME
        ;;
    update)
        echo "🔄 Обновляем бота..."
        cd /root/telegram_invoice_bot
        git pull
        source venv/bin/activate
        pip install -r requirements.txt
        systemctl restart $BOT_NAME
        echo "✅ Обновление завершено!"
        ;;
    *)
        echo "📋 Использование: $0 {start|stop|restart|status|logs|logs-all|enable|disable|update}"
        echo ""
        echo "Команды:"
        echo "  start     - Запустить бота"
        echo "  stop      - Остановить бота"
        echo "  restart   - Перезапустить бота"
        echo "  status    - Показать статус"
        echo "  logs      - Показать логи в реальном времени"
        echo "  logs-all  - Показать все логи"
        echo "  enable    - Включить автозапуск"
        echo "  disable   - Отключить автозапуск"
        echo "  update    - Обновить код и перезапустить"
        exit 1
        ;;
esac 