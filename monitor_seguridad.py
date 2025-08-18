import gspread
from google.oauth2.service_account import Credentials

# ---------------- CONFIG ----------------
SERVICE_ACCOUNT_FILE = "reporte-seguridad-0bfdcfee9c9d.json"  # archivo JSON en la misma carpeta
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SHEET_KEY = "1HPmAsT9z6_Iefpd7Q9W5p3XgwMmLzZzaOfHaKat_jfY"  # solo el ID de la hoja

# ---------------- AUTENTICACIÓN ----------------
try:
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    print("✅ Autenticación correcta con la cuenta de servicio.")
except Exception as e:
    print("❌ Error en la autenticación:", e)
    exit()

# ---------------- ABRIR HOJA ----------------
try:
    sh = client.open_by_key(SHEET_KEY)
    sheet = sh.sheet1
    print("✅ Conexión correcta. Nombre de la hoja:", sh.title)

    # Leer todas las filas
    records = sheet.get_all_records()
    print("📄 Datos actuales de la hoja:")
    for row in records:
        print(row)

except Exception as e:
    print("❌ Error al conectar con la hoja:", e)






