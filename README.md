# 📰 Sistema de Monitoreo de Noticias de Orden Público - SMA

<img width="362" height="120" alt="logo_empresa" src="https://github.com/user-attachments/assets/0fe3b8d3-3516-4251-9357-3d3b62a3c3e6" />


**Mantente siempre informado sobre eventos críticos de seguridad a nivel nacional en Colombia.**  

---

## 🌟 Características destacadas

- 🔔 **Alertas inmediatas:** Detecta bloqueos, paros y ataques armados.  
- 🗺️ **Mapas interactivos:** Ubicación de eventos por departamento y municipio.  
- 📊 **Reportes diarios:** Nivel de alerta: **Bajo**, **Medio**, **Alto**.  
- 🖼️ **Visualización multimedia:** Incluye imágenes y URLs de fuentes confiables.  
- 🔄 **Sensado automático:** Actualización de noticias cada 6 horas.  

---

## 🛠️ Requisitos del sistema

- Python ≥ 3.11  
- Librerías Python: `pandas`, `openpyxl`, `requests`, `beautifulsoup4`, `streamlit`  
- Acceso a Google Drive para almacenamiento de reportes  
- WhatsApp en dispositivo móvil (para envío de alertas)

Instalación rápida:

```bash
pip install pandas openpyxl requests beautifulsoup4 streamlit
📂 Estructura del proyecto

.
├── app_simple.py              # Script principal
├── municipios_departamentos.csv
├── red_vial_invias_2025.xlsx
├── logo_empresa.png
├── Decalogo.png
├── requirements.txt
└── .github/workflows          # Automatización y CI/CD
Revisa el reporte generado, que incluye:

| 📅 FECHA | 📰 FUENTES | ⚡ ACCION | 📝 DESCRIPCIÓN | 📍 UBICACIÓN | 🗂️ DEPARTAMENTO | 🌎 PAÍS | 🏘️ MUNICIPIO | 🔗 URL/Img |

Copia el mensaje preparado para WhatsApp y envíalo al equipo de seguridad.

🔄 Flujo de trabajo

Sensado periódico de noticias.

Filtrado de eventos críticos según criterios de seguridad.

Generación de reporte Excel y mensaje corporativo listo para envío.

Alerta inmediata ante eventos graves: bloqueos, paros o ataques armados.

💡 Mejoras futuras

Integración con WhatsApp API para alertas automáticas.

Dashboard interactivo en Power BI con mapas y estadísticas en tiempo real.

Sistema predictivo de eventos basado en historial y presencia de grupos armados.

📞 Contacto

SMA - Salgado Melendez y Asociados Ingenieros Consultores SA
📧 edgar.diaz@smaingenieros.com.co

📞 +57 3134028054



