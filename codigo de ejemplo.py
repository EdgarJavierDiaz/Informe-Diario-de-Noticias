from datetime import datetime

# -------- DATOS DE EJEMPLO --------
noticia = {
    "nivel_alerta": "ALTA",
    "categoria": "Bloqueo",
    "titular": "Bloqueo en la vía Bogotá–Villavicencio",
    "departamento": "Meta",
    "municipio": "Villavicencio",
    "fuente": "El Tiempo",
    "url": "https://www.eltiempo.com/colombia/bloqueo-villavicencio-2025"
}

# -------- GENERAR MENSAJE --------
def generar_mensaje(noticia):
    fecha = datetime.now().strftime("%d/%m/%Y - %I:%M %p")
    icono_alerta = {
        "BAJA": "🟢 ALERTA BAJA",
        "MEDIA": "🟡 ALERTA MEDIA",
        "ALTA": "🚨 ALERTA ALTA 🚨"
    }

    mensaje = f"""
{icono_alerta.get(noticia['nivel_alerta'], 'ℹ️ ALERTA')}
{noticia['categoria']} - {noticia['titular']}
📍 {noticia['departamento']} - {noticia['municipio']}
📰 Fuente: {noticia['fuente']}
🕒 {fecha}

👉 {noticia['url']}
"""
    return mensaje.strip()

# -------- PRUEBA --------
print(generar_mensaje(noticia))
