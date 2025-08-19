import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import feedparser
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# ---------------- ARCHIVOS (creados desde Secrets en GitHub Actions) ----------------
SERVICE_ACCOUNT_FILE = "reporte-seguridad.json"
MUNICIPIOS_FILE = "Listado_de_Municipios.csv"
WHATSAPP_FILE = "resumen_alertas_whatsapp.txt"

# ---------------- CONFIG ----------------
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SHEET_KEY = "1HPmAsT9z6_Iefpd7Q9W5p3XgwMmLzZzaOfHaKat_jfY"
RSS_FEEDS = [
    "https://www.eltiempo.com/rss/colombia",
    "https://caracol.com.co/rss",
    # Agrega más feeds aquí
]

# ---------------- AUTENTICACIÓN ----------------
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
sh = client.open_by_key(SHEET_KEY)
sheet = sh.sheet1

# ---------------- ENCABEZADOS ----------------
if sheet.row_count == 0 or not sheet.get_all_values():
    headers = ["FECHA","FUENTES","ACCION","DESCRIPCION","UBICACIÓN",
               "DEPARTAMENTO","PAIS","MUNICIPIO","Url/Img","NIVEL_ALERTA"]
    sheet.append_row(headers)

# ---------------- LEER MUNICIPIOS ----------------
df_municipios = pd.read_csv(MUNICIPIOS_FILE, encoding='utf-8')
print("Columnas encontradas:", df_municipios.columns) 
municipios_list = df_municipios["MUNICIPIO"].tolist()

# ---------------- DATOS EXISTENTES ----------------
existing_rows = sheet.get_all_records()
existing_set = set((row["FECHA"], row["FUENTES"], row["DESCRIPCION"]) for row in existing_rows)

# ---------------- FUNCIONES ----------------
def detectar_municipio(texto):
    texto_upper = texto.upper()
    for municipio in municipios_list:
        if municipio.upper() in texto_upper:
            dep_match = df_municipios[df_municipios["MUNICIPIO"].str.upper() == municipio.upper()]
            departamento = dep_match.iloc[0]["DEPARTAMENTO"]
            return municipio, departamento
    return "Desconocido", "Desconocido"

def clasificar_alerta(texto):
    texto_lower = texto.lower()
    alto = ["atentado", "explosión", "ataque", "asesinato", "secuestro"]
    medio = ["bloqueo", "paro", "protesta", "amenaza"]
    bajo = ["advertencia", "alerta", "restricción", "aviso"]

    if any(word in texto_lower for word in alto):
        return "Alto"
    elif any(word in texto_lower for word in medio):
        return "Medio"
    else:
        return "Bajo"

def extraer_fecha(entry):
    if "published_parsed" in entry and entry.published_parsed:
        return datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
    elif "published" in entry:
        try:
            return datetime.strptime(entry.published[:10], "%Y-%m-%d").strftime("%Y-%m-%d")
        except:
            return datetime.now().strftime("%Y-%m-%d")
    else:
        return datetime.now().strftime("%Y-%m-%d")

def procesar_feed(feed_url):
    feed = feedparser.parse(feed_url)
    fuente = feed.feed.get("title", "Desconocida")
    nuevas_filas_feed = []

    for entry in feed.entries:
        fecha = extraer_fecha(entry)
        descripcion = entry.get("title", "")
        url_img = entry.get("media_content", [{"url": ""}])[0]["url"] if "media_content" in entry else ""

        if (fecha, fuente, descripcion) in existing_set:
            continue

        ubicacion, departamento = detectar_municipio(descripcion)
        pais = "Colombia"
        municipio_concat = f"{ubicacion}, {departamento}, {pais}"
        nivel_alerta = clasificar_alerta(descripcion)

        nueva_fila = [
            fecha, fuente, "Alerta", descripcion,
            ubicacion, departamento, pais,
            municipio_concat, url_img, nivel_alerta
        ]

        sheet.append_row(nueva_fila)
        existing_set.add((fecha, fuente, descripcion))
        nuevas_filas_feed.append(nueva_fila)

    return nuevas_filas_feed

# ---------------- PROCESAR TODOS LOS FEEDS ----------------
def procesar_todos_feeds():
    todas_nuevas_filas = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(procesar_feed, RSS_FEEDS)
    for filas in results:
        todas_nuevas_filas.extend(filas)
    return todas_nuevas_filas

# ---------------- GENERAR RESUMEN WHATSAPP ----------------
def generar_resumen_whatsapp(nuevas_filas):
    if not nuevas_filas:
        mensaje = f"✅ No hay noticias nuevas para hoy ({datetime.now().strftime('%Y-%m-%d')})"
    else:
        mensaje = f"📢 Resumen diario de alertas ({datetime.now().strftime('%Y-%m-%d')}):\n\n"
        for fila in nuevas_filas:
            mensaje += f"- [{fila[9]}] {fila[1]}: {fila[3]} ({fila[7]})\n"

    with open(WHATSAPP_FILE, "w", encoding="utf-8") as f:
        f.write(mensaje)
    print(f"📄 Resumen WhatsApp generado: {WHATSAPP_FILE}")

# ---------------- EJECUCIÓN ----------------
if __name__ == "__main__":
    nuevas_filas = procesar_todos_feeds()
    generar_resumen_whatsapp(nuevas_filas)








