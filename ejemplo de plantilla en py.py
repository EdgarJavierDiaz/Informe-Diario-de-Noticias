from fpdf import FPDF
from datetime import datetime

# Ruta del archivo de la plantilla (debe estar en la misma carpeta que el script)
template_image = "plantilla_reporte.png"  # Usa el nombre real del archivo que subiste

# Crear clase personalizada para el PDF
class ReporteSeguridad(FPDF):
    def header(self):
        # Insertar la imagen como fondo de página (A4: 210x297 mm)
        self.image(template_image, x=0, y=0, w=210, h=297)

    def footer(self):
        pass  # El pie de página ya está en la plantilla

# Crear el PDF
pdf = ReporteSeguridad()
pdf.add_page()

# Posición para escribir debajo del encabezado
pdf.set_xy(20, 80)
pdf.set_font("Arial", size=12)

# Titulares simulados
titulares = [
    "1. Manifestación pacífica en el centro de la ciudad sin afectaciones.",
    "2. Bloqueo intermitente en la vía principal hacia el norte.",
    "3. Presencia policial reforzada en zonas de alto riesgo.",
    "4. Reporte de disturbios menores en el sector industrial.",
    "5. Actividad normal en estaciones de transporte público."
]

# Escribir los titulares en el PDF
for titular in titulares:
    pdf.multi_cell(0, 10, titular)

# Guardar el archivo
pdf.output("reporte_seguridad_final.pdf")
