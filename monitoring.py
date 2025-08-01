#!/usr/bin/env python3
"""
Скрипт для мониторинга Telegram бота
Проверяет состояние бота и перезапускает при необходимости
"""

import subprocess
import time
import logging
import requests
import json
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/bot_monitor.log'),
        logging.StreamHandler()
    ]
)

class BotMonitor:
    def __init__(self, bot_token, check_interval=300):  # 5 минут
        self.bot_token = bot_token
        self.check_interval = check_interval
        self.last_restart = None
        
    def check_bot_status(self):
        """Проверяет статус бота через systemctl"""
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', 'bot'],
                capture_output=True,
                text=True
            )
            return result.stdout.strip() == 'active'
        except Exception as e:
            logging.error(f"Ошибка при проверке статуса бота: {e}")
            return False
    
    def check_bot_response(self):
        """Проверяет, отвечает ли бот на API запросы"""
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/getMe"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('ok', False)
            return False
        except Exception as e:
            logging.error(f"Ошибка при проверке API бота: {e}")
            return False
    
    def restart_bot(self):
        """Перезапускает бота"""
        try:
            logging.warning("Перезапускаем бота...")
            subprocess.run(['systemctl', 'restart', 'bot'], check=True)
            self.last_restart = datetime.now()
            logging.info("Бот успешно перезапущен")
            return True
        except Exception as e:
            logging.error(f"Ошибка при перезапуске бота: {e}")
            return False
    
    def get_bot_logs(self, lines=10):
        """Получает последние логи бота"""
        try:
            result = subprocess.run(
                ['journalctl', '-u', 'bot', '-n', str(lines), '--no-pager'],
                capture_output=True,
                text=True
            )
            return result.stdout
        except Exception as e:
            logging.error(f"Ошибка при получении логов: {e}")
            return ""
    
    def run_monitoring(self):
        """Основной цикл мониторинга"""
        logging.info("Запуск мониторинга бота...")
        
        while True:
            try:
                # Проверяем статус службы
                service_active = self.check_bot_status()
                
                # Проверяем API бота
                api_responding = self.check_bot_response()
                
                if not service_active:
                    logging.error("Служба бота неактивна!")
                    self.restart_bot()
                elif not api_responding:
                    logging.error("Бот не отвечает на API запросы!")
                    self.restart_bot()
                else:
                    logging.info("Бот работает нормально")
                
                # Ждем следующей проверки
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                logging.info("Мониторинг остановлен пользователем")
                break
            except Exception as e:
                logging.error(f"Ошибка в цикле мониторинга: {e}")
                time.sleep(60)  # Ждем минуту перед повторной попыткой

def main():
    """Главная функция"""
    import os
    
    # Получаем токен бота из переменной окружения
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        logging.error("BOT_TOKEN не установлен!")
        return
    
    # Создаем монитор и запускаем
    monitor = BotMonitor(bot_token)
    monitor.run_monitoring()

if __name__ == "__main__":
    main() 