import os

ruta = r"C:\Users\Usuario\Desktop\AUTOMATIZACION DE NOTICIAS\reporte-seguridad-3543314de55c.json"

if os.path.exists(ruta):
    print("✅ El archivo existe en la ruta:", ruta)
else:
    print("❌ No se encontró el archivo en:", ruta)
