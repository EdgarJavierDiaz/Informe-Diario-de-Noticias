from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# --- Cargar plantilla ---
plantilla = Image.open("plantilla_reporte.png").convert("RGBA")
draw = ImageDraw.Draw(plantilla)

# --- Fuentes ---
# Cambia "arial.ttf" por otra si no la tienes (ej: "C:/Windows/Fonts/Arial.ttf")
font_titulo = ImageFont.truetype("arialbd.ttf", 40)   # Arial negrita
font_texto  = ImageFont.truetype("arial.ttf", 28)

# --- Posiciones (ajustadas para no chocar con el encabezado) ---
x_inicio, y_inicio = 120, 420   # punto de inicio más abajo
line_height = 65                # espacio entre líneas

# --- Datos de ejemplo (mañana vendrán del script real) ---
fecha = datetime.now().strftime("%d/%m/%Y")
nivel_alerta = "Medio 🟠"
bloqueos, paros, petrolera, otros = 2, 1, 0, 3
interpretacion = "Riesgo medio. Verificar rutas críticas y coordinar transporte."

# --- Escribir contenido ---
draw.text((x_inicio, y_inicio), f"📅 Fecha: {fecha}", font=font_texto, fill="black")
draw.text((x_inicio, y_inicio + line_height), f"🔔 Nivel de alerta: {nivel_alerta}", font=font_titulo, fill="orange")

draw.text((x_inicio, y_inicio + 2*line_height), f"🚧 Bloqueos: {bloqueos}", font=font_texto, fill="black")
draw.text((x_inicio, y_inicio + 3*line_height), f"🚛 Paros: {paros}", font=font_texto, fill="black")
draw.text((x_inicio, y_inicio + 4*line_height), f"⛽ Petrolera: {petrolera}", font=font_texto, fill="black")
draw.text((x_inicio, y_inicio + 5*line_height), f"⚠️ Otros: {otros}", font=font_texto, fill="black")

draw.text((x_inicio, y_inicio + 7*line_height), "✅ Interpretación:", font=font_texto, fill="black")
draw.text((x_inicio, y_inicio + 8*line_height), interpretacion, font=font_texto, fill="black")

# --- Guardar resultado ---
plantilla.save("reporte_generado.png")
print("✅ Reporte generado como imagen: reporte_generado.png")
