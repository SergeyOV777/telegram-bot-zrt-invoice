import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = "8099236215:AAEECv4myUVQDsVUEzK3mW3Pb1tDfrajLyM"
GOOGLE_CREDENTIALS = os.getenv('GOOGLE_CREDENTIALS', 'test')
SPREADSHEET_ID = "1d4_d6yhZPEPJ3JsqhxLMSZqNnJeITqO3vF7im1hX1EY"
SHEET_NAME = "Все неоплаченные счета клиентов"
CLIENTS_SHEET_NAME = "Clients"  # Попробуем английское название
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE', 'service_account.json')
