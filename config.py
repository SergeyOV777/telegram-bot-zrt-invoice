import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
GOOGLE_CREDENTIALS = os.getenv('GOOGLE_CREDENTIALS')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
SHEET_NAME = os.getenv('SHEET_NAME')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
