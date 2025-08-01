#!/bin/bash

# Скрипт для автоматической загрузки файлов бота в GitHub
# Автор: Assistant
# Дата: 2025-08-01

echo "🚀 Начинаем загрузку файлов бота в GitHub..."

# Проверяем, что мы в правильной директории
if [ ! -f "main.py" ]; then
    echo "❌ Ошибка: main.py не найден. Убедитесь, что вы находитесь в папке с ботом."
    exit 1
fi

# Инициализируем Git репозиторий
echo "📁 Инициализируем Git репозиторий..."
git init

# Добавляем все файлы
echo "📤 Добавляем файлы в Git..."
git add .

# Создаем первый коммит
echo "💾 Создаем коммит..."
git commit -m "Initial commit: Telegram invoice bot with all handlers and services"

# Переименовываем ветку в main
echo "🌿 Переименовываем ветку в main..."
git branch -M main

# Добавляем удаленный репозиторий
echo "🔗 Добавляем удаленный репозиторий..."
git remote add origin https://github.com/sergeyuobraztsovk-hash/telegram-invoice-bot.git

# Отправляем файлы в GitHub
echo "🚀 Отправляем файлы в GitHub..."
git push -u origin main

echo "✅ Загрузка завершена!"
echo "📋 Проверьте репозиторий: https://github.com/sergeyuobraztsovk-hash/telegram-invoice-bot" 