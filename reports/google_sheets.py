import gspread
from google.oauth2.service_account import Credentials

def actualizar_google_sheets(datos, spreadsheet_id, sheet_name):
    """Actualiza una hoja de Google Sheets con los datos proporcionados"""
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
    client = gspread.authorize(creds)

    try:
        spreadsheet = client.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.worksheet(sheet_name)
        worksheet.clear()
        worksheet.update([datos.columns.values.tolist()] + datos.values.tolist())
        print(f"Hoja {sheet_name} actualizada correctamente.")
    except Exception as e:
        print(f"Error al actualizar Google Sheets: {e}")