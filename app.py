import streamlit as st
import pandas as pd
import feedparser, yaml, re
from datetime import datetime, timedelta, timezone
from dateutil import parser as dtparser
from collections import defaultdict

# ---------- CONFIG ----------
st.set_page_config(page_title="Reporte Diario de Orden Público", page_icon="🛡️", layout="wide")

@st.cache_data
def load_config():
    import io, json, yaml
    cfg_text = open("config.yaml","r",encoding="utf-8").read()
    return yaml.safe_load(cfg_text)

CFG = load_config()

# ---------- HELPERS ----------
def normalize_text(s:str)->str:
    return re.sub(r"\s+"," ", (s or "")).strip().lower()

def classify_item(title:str, summary:str):
    text = f"{title} {summary}".lower()
    cat = "otros"
    for k in CFG["keywords"]["bloqueos"]:
        if k in text: 
            return "bloqueos"
    for k in CFG["keywords"]["paros"]:
        if k in text: 
            return "paros"
    for k in CFG["keywords"]["petrolera"]:
        if k in text: 
            return "petrolera"
    for k in CFG["keywords"]["otros"]:
        if k in text: 
            cat = "otros"
    return cat

def parse_time(entry):
    for key in ["published", "updated", "created"]:
        if key in entry:
            try:
                return dtparser.parse(entry[key])
            except Exception:
                pass
    return datetime.now()

@st.cache_data(ttl=60*15)  # cache 15 min
def fetch_news():
    items = []
    for src in CFG["rss_sources"]:
        try:
            feed = feedparser.parse(src)
            for e in feed.entries:
                title = e.get("title","")
                summary = e.get("summary","")
                link = e.get("link","")
                dt = parse_time(e).astimezone(timezone.utc)
                items.append({
                    "fuente": feed.feed.get("title", src),
                    "titulo": title,
                    "resumen": re.sub("<.*?>","",summary),
                    "link": link,
                    "fecha": dt,
                    "categoria": classify_item(title, summary)
                })
        except Exception as ex:
            st.warning(f"No se pudo leer {src}: {ex}")
    df = pd.DataFrame(items)
    if not df.empty:
        df = df.sort_values("fecha", ascending=False)
    return df

def filter_colombia(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty: 
        return df
    regions = [r.lower() for r in CFG.get("region_focus",[])]
    mask = df["titulo"].str.lower().str.contains("colombia")
    for r in regions:
        mask = mask | df["titulo"].str.lower().str.contains(r)
        mask = mask | df["resumen"].str.lower().str.contains(r)
    return df[mask]

def confirm_by_sources(df: pd.DataFrame, category: str, min_sources:int=2):
    # Agrupa por título normalizado (o por palabras clave) y cuenta fuentes únicas
    if df.empty: 
        return pd.DataFrame(columns=list(df.columns)+["confirmado","agrupacion"])
    cat_df = df[df["categoria"]==category].copy()
    if cat_df.empty:
        cat_df["confirmado"] = False
        cat_df["agrupacion"] = ""
        return cat_df
    cat_df["group_key"] = cat_df["titulo"].str.replace(r"[\W_]+"," ", regex=True).str.lower().str.strip()
    grouped = []
    for g, gdf in cat_df.groupby("group_key"):
        fuentes = set(gdf["fuente"].tolist())
        confirmado = len(fuentes) >= min_sources
        for _,row in gdf.iterrows():
            r = dict(row)
            r["confirmado"] = confirmado
            r["agrupacion"] = g
            grouped.append(r)
    out = pd.DataFrame(grouped).drop(columns=["group_key"], errors="ignore")
    return out

def level_icon(level:str):
    return {"Alto":"🔴","Medio":"🟠","Bajo":"🟢"}.get(level,"🟢")

def compute_level(n_bloq:int, n_paros:int, n_pet:int):
    score = n_bloq*2 + n_pet*2 + n_paros
    if score >= 4: return "Alto"
    if score >= 2: return "Medio"
    return "Bajo"

def build_whatsapp(df_b, df_p, df_o, df_pet, level:str):
    icon = level_icon(level)
    today = datetime.now().strftime("%d/%m/%Y")
    lines = []
    lines.append(f"🔔 *Reporte Diario de Seguridad – {today}*")
    lines.append(f"👤 SMA Seguridad")
    lines.append("")
    lines.append(f"*Nivel de alerta:* {icon} *{level}*")
    lines.append("---")
    lines.append("*📊 Eventos últimos 24h:*")
    lines.append(f"- 🚧 Bloqueos: *{len(df_b)}*")
    lines.append(f"- 🚛 Amenazas de paro: *{len(df_p)}*")
    lines.append(f"- ⛽ Atentados a infraestructura: *{len(df_pet)}*")
    lines.append(f"- ⚠️ Otros: *{len(df_o)}*")
    lines.append("")
    inter = "Se observan señales de riesgo en transporte e infraestructura." if level!="Bajo" else "Sin novedades críticas confirmadas."
    lines.append("*✅ Interpretación:*")
    lines.append(inter)
    lines.append("")
    lines.append("_Este mensaje es para revisión interna. Reenvíe tras validar._")
    return "\n".join(lines)

def html_from_template(stats, logo_url="https://via.placeholder.com/120x56.png?text=SMA", primary="#003366"):
    tpl = open("template_outlook.html","r",encoding="utf-8").read()
    # simple replace
    reps = {
        "{{LOGO_URL}}": logo_url,
        "{{PRIMARY_COLOR}}": primary,
        "{{DATE}}": datetime.now().strftime("%d/%m/%Y"),
        "{{ALERT_COLOR}}": "#cc0000" if stats["level"]=="Alto" else "#ff8c00" if stats["level"]=="Medio" else "#0b8f08",
        "{{ALERT_ICON}}": level_icon(stats["level"]),
        "{{ALERT_LEVEL}}": stats["level"],
        "{{COUNT_BLOQUEOS}}": str(stats["bloqueos"]),
        "{{COUNT_PAROS}}": str(stats["paros"]),
        "{{COUNT_PETROLERA}}": str(stats["petrolera"]),
        "{{COUNT_OTROS}}": str(stats["otros"]),
        "{{DETAIL_BLOQUEOS}}": stats.get("detail_bloqueos",""),
        "{{DETAIL_PAROS}}": stats.get("detail_paros",""),
        "{{DETAIL_PETROLERA}}": stats.get("detail_petrolera",""),
        "{{DETAIL_OTROS}}": stats.get("detail_otros",""),
        "{{TREND_TEXT}}": stats.get("trend","Sin variación"),
        "{{INTERPRETACION}}": stats.get("interpretacion",""),
        "{{AGENDA_ITEMS}}": "".join([f"<li>{x}</li>" for x in stats.get("agenda",[])]),
        "{{COMPANY_NAME}}": CFG.get("company_name","SMA Seguridad")
    }
    for k,v in reps.items():
        tpl = tpl.replace(k, v)
    return tpl

def send_outlook_mail(subject:str, html_body:str, to:str):
    try:
        import win32com.client as win32
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.To = to
        mail.Subject = subject
        mail.HTMLBody = html_body
        mail.Display()  # muestra el correo listo para enviar (no envía automáticamente)
        return True, "Correo preparado en Outlook (revise, edite y envíe)."
    except Exception as ex:
        return False, f"No se pudo abrir Outlook: {ex}"

# ---------- UI ----------
st.title("🛡️ Reporte Diario de Orden Público (CO)")
st.caption("Enfoque en bloqueos/paros y ataques a infraestructura petrolera.")

col1, col2 = st.columns([3,2])
with col1:
    st.subheader("1) Noticias detectadas (últimas 24–48h)")
    df = fetch_news()
    if df.empty:
        st.info("No se encontraron noticias. Revise sus fuentes en config.yaml")
    else:
        # Filtro Colombia
        df = filter_colombia(df)
        # Clasificación y confirmación por fuentes
        df_b = confirm_by_sources(df, "bloqueos", CFG["min_confirmed_sources"])
        df_p = confirm_by_sources(df, "paros", CFG["min_confirmed_sources"])
        df_pet = confirm_by_sources(df, "petrolera", CFG["min_confirmed_sources"])
        df_o = confirm_by_sources(df, "otros", CFG["min_confirmed_sources"])

        # Mostrar tablas resumidas
        tabs = st.tabs(["🚧 Bloqueos","🚛 Paros","⛽ Petrolera","⚠️ Otros"])
        for t, subdf in zip(tabs, [df_b, df_p, df_pet, df_o]):
            with t:
                if subdf.empty:
                    st.write("Sin registros.")
                else:
                    st.dataframe(subdf[["fecha","fuente","titulo","confirmado","link"]], use_container_width=True, hide_index=True)

with col2:
    st.subheader("2) Resumen ejecutivo")
    n_b, n_p, n_pet, n_o = len(df_b), len(df_p), len(df_pet), len(df_o)
    level = compute_level(n_b, n_p, n_pet)
    st.metric("Nivel de alerta", f"{level_icon(level)} {level}")
    st.write("Eventos 24h")
    c1, c2 = st.columns(2)
    c1.metric("🚧 Bloqueos", n_b)
    c2.metric("🚛 Paros", n_p)
    c1.metric("⛽ Petrolera", n_pet)
    c2.metric("⚠️ Otros", n_o)

    interpretacion = "Riesgo bajo. Sin novedades críticas confirmadas." if level=="Bajo" else \
                     "Riesgo medio. Verificar rutas críticas y activar plan de contingencia." if level=="Medio" else \
                     "Riesgo alto. Elevar nivel de alerta y coordinar con autoridades."
    agenda = ["08:00 Comité interno de seguridad", "10:30 Seguimiento movilidad INVÍAS", "15:00 Llamada con operaciones"]
    detail = lambda sdf: " | ".join((sdf["titulo"].head(3)).tolist()) if not sdf.empty else ""
    stats = {
        "level": level,
        "bloqueos": n_b, "paros": n_p, "petrolera": n_pet, "otros": n_o,
        "detail_bloqueos": detail(df_b),
        "detail_paros": detail(df_p),
        "detail_petrolera": detail(df_pet),
        "detail_otros": detail(df_o),
        "trend": "Sin variación (demo)",
        "interpretacion": interpretacion,
        "agenda": agenda
    }

    st.divider()
    st.subheader("3) Salidas corporativas")

    # WhatsApp
    wa_msg = build_whatsapp(df_b, df_p, df_o, df_pet, level)
    st.text_area("Mensaje WhatsApp (copiar y pegar):", wa_msg, height=220)
    st.download_button("⬇️ Descargar TXT WhatsApp", data=wa_msg.encode("utf-8"), file_name=f"reporte_whatsapp_{datetime.now().strftime('%Y%m%d')}.txt")

    # HTML Outlook
    html = html_from_template(stats)
    st.download_button("⬇️ Descargar HTML Outlook", data=html.encode("utf-8"), file_name=f"reporte_outlook_{datetime.now().strftime('%Y%m%d')}.html")

    st.caption("Para envío automático desde Outlook (Windows), use el botón siguiente.")

    to = st.text_input("Enviar a (correo):", value="tu.jefe@empresa.com")
    if st.button("📧 Preparar correo en Outlook (no envía automáticamente)"):
        ok, msg = send_outlook_mail(subject=f"Reporte Diario de Seguridad – {datetime.now().strftime('%d/%m/%Y')} – {level}",
                                    html_body=html, to=to)
        (st.success if ok else st.error)(msg)

st.info("Edite 'config.yaml' para ajustar palabras clave, fuentes y parámetros de confirmación por múltiples fuentes.")
