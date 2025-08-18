# Sistema de Reporte Diario de Orden Público (Colombia)
Genera automáticamente un **resumen corporativo** con énfasis en: paros/bloqueos, ataques a infraestructura petrolera y otros incidentes. Produce:
- Mensaje **WhatsApp** (texto con íconos) listo para copiar/reenviar.
- Correo **Outlook** en HTML corporativo (con logo y colores).
- CSV base con eventos para histórico/Power BI.
- (Opcional) Envío por Outlook con `win32com.client` en Windows.

## Requisitos
- Python 3.10+
- `pip install -r requirements.txt`

## Cómo ejecutar (local)
1. Active su venv (opcional) e instale dependencias.
2. Edite `config.yaml` (palabras clave, fuentes RSS).
3. Ejecute:
   ```bash
   streamlit run app.py
   ```
4. El panel mostrará:
   - Eventos detectados
   - Nivel de alerta
   - Botones para **generar WhatsApp** y **generar HTML Outlook**
   - Botón (opcional) para **enviar por Outlook** si está en Windows

## Fuentes
Por defecto se muestran fuentes de ejemplo. Cambie/añada RSS de medios colombianos confiables en `config.yaml`.

## Notas
- El clasificador es **ligero** (reglas + conteo de fuentes). Para producción, considere un modelo de ML o verificación adicional.
- El envío por WhatsApp está pensado **para que usted reciba primero** el mensaje y reenvíe manualmente.
