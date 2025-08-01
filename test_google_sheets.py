#!/usr/bin/env python3
"""
Тестовый скрипт для проверки интеграции с Google Sheets
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.sheets_service import get_all_invoices, get_clients
import config

def test_google_sheets_integration():
    """Тестирует интеграцию с Google Sheets"""
    print("🔍 Тестирование интеграции с Google Sheets...")
    
    # Проверяем конфигурацию
    print(f"📋 Конфигурация:")
    print(f"   SPREADSHEET_ID: {config.SPREADSHEET_ID}")
    print(f"   SHEET_NAME: {config.SHEET_NAME}")
    print(f"   SERVICE_ACCOUNT_FILE: {config.SERVICE_ACCOUNT_FILE}")
    
    # Проверяем наличие файла service_account.json
    if not os.path.exists(config.SERVICE_ACCOUNT_FILE):
        print("❌ Файл service_account.json не найден!")
        return False
    
    print("✅ Файл service_account.json найден")
    
    # Проверяем ID таблицы
    if not config.SPREADSHEET_ID:
        print("❌ SPREADSHEET_ID не указан!")
        print("💡 Укажите ID вашей Google таблицы в config.py")
        return False
    
    print("✅ SPREADSHEET_ID указан")
    
    # Тестируем подключение к Google Sheets
    try:
        print("\n🔄 Тестирование подключения к Google Sheets...")
        
        # Пробуем получить инвойсы
        invoices = get_all_invoices()
        print(f"✅ Получено инвойсов: {len(invoices)}")
        if invoices:
            print(f"   Пример: {invoices[0]}")
        
        # Пробуем получить клиентов
        clients = get_clients()
        print(f"✅ Получено клиентов: {len(clients)}")
        if clients:
            print(f"   Пример: {clients[0]}")
        
        print("🎉 Интеграция с Google Sheets работает!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при подключении к Google Sheets: {e}")
        return False

if __name__ == "__main__":
    test_google_sheets_integration() 