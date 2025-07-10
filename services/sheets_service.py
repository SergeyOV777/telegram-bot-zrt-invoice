from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import config

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def get_all_invoices():
    """Читает все строки из Google Sheets и возвращает список словарей-счетов."""
    # Загружаем учетные данные сервисного аккаунта
    creds = Credentials.from_service_account_file(
        config.SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )

    # Создаем клиент API
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # Читаем данные из указанного листа
    result = sheet.values().get(
        spreadsheetId=config.SPREADSHEET_ID,
        range=config.SHEET_NAME
    ).execute()
    rows = result.get('values', [])

    if not rows:
        return []

    # Первая строка — заголовки столбцов
    headers = rows[0]
    # Каждая последующая строка — данные счета
    invoices = [dict(zip(headers, row)) for row in rows[1:]]
    return invoices


def get_all_vyezd_invoices():
    """Читает все строки из вкладки 'Счета за выездные' и возвращает только неоплаченные выезды (Fact pay == 'FALSE')."""
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    import config
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    creds = Credentials.from_service_account_file(
        config.SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=config.SPREADSHEET_ID,
        range='Счета за выездные'
    ).execute()
    rows = result.get('values', [])
    if not rows:
        return []
    headers = rows[0]
    invoices = [dict(zip(headers, row)) for row in rows[1:]]
    # Фильтруем только неоплаченные
    return [inv for inv in invoices if inv.get('Fact pay', '').strip().upper() == 'FALSE']