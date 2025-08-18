import gspread
from google.oauth2.service_account import Credentials

# Ruta al JSON (si está en la misma carpeta que el script, usa solo el nombre)
SERVICE_ACCOUNT_FILE = "reporte-seguridad-3543314de55c.json"

# 👉 Aquí definimos SCOPES
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Autenticación con el service account
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# ID de tu hoja de cálculo (la parte intermedia de la URL)
SHEET_ID = "1HPmAsT9z6_Iefpd7Q9W5p3XgwMmLzZzaOfHaKat_jfY"

# Abrir la hoja
sh = client.open_by_key(SHEET_ID)

print("✅ Conexión correcta. Hojas disponibles:")
print(sh.worksheets())

