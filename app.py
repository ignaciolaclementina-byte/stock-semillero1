"""
La Clementina · Sistema de Gestión de Stock de Semillas
Versión Streamlit — Conectado a Google Sheets
Creado por Ignacio Diaz
"""

import streamlit as st
import pandas as pd
import json
import io
from datetime import datetime, date
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials

# ─── CONFIGURACIÓN DE PÁGINA ──────────────────────────────────
st.set_page_config(
    page_title="La Clementina · Stock Semillas",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CONSTANTES ───────────────────────────────────────────────
LOW = 5
DEFAULT_PASS = "semillas2025"
DATA_FILE = "laclementina_data.json"
SPREADSHEET_ID = "1QnyD0ypbwgbMD4PYAQoijkWeAiK47KAh1sAPuc9gspA"

CAMPAÑAS_DEF = ["2024/2025", "2025/2026"]
ESPECIES_DEF = ["Soja", "Trigo", "Maíz", "Girasol", "Sorgo", "Cebada"]
VARS_DEF = {
    "Soja":    ["DM 4612", "SY 3x8", "NA 5009"],
    "Trigo":   ["Klein Proteo", "Buck Meteoro", "SY 100"],
    "Maíz":    ["DK 7210", "AX 7784", "P1815W"],
    "Girasol": ["SY 4045", "Paraíso 20"],
    "Sorgo":   ["NK 300", "DK 35"],
    "Cebada":  ["Shakira", "Lissette"],
}
STOCK_INIT = [
    {"id": 1, "campaña": "2024/2025", "especie": "Soja",  "variedad": "DM 4612",      "tipo": "bigbag", "tratada": False, "cantidad": 14,  "pesoUnit": 800, "lote": "L-001", "ubicacion": "", "fecha": "2025-04-01", "pg": 95, "pmil": 140, "obs": ""},
]

# ─── CSS PERSONALIZADO ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500&display=swap');

:root {
  --bg:#f4f6f9; --panel:#fff; --border:#dde1ea;
  --accent:#e07b00; --blue:#1a7abf; --green:#2e8b57; --red:#c0392b;
  --purple:#7b4fa6; --text:#1a1e2e; --muted:#6b7280;
  --fh:'Barlow Condensed',sans-serif; --fb:'Barlow',sans-serif;
}

html, body, [class*="css"] { font-family: var(--fb); }

.lc-header {
  background: linear-gradient(135deg,#1a2a4a 60%,#1e3660);
  border-bottom: 3px solid #e07b00;
  padding: 14px 24px;
  border-radius: 10px;
  margin-bottom: 12px;
  display: flex; align-items: center; gap: 14px;
}
.lc-header h1 {
  font-family: var(--fh); font-size: 1.7rem; font-weight: 800;
  text-transform: uppercase; letter-spacing: 1px; color: #fff; margin: 0;
}
.lc-header h1 span { color: #f5a623; }
.lc-header p { font-size: .75rem; color: rgba(255,255,255,.55); margin: 2px 0 0; }

.sv-card {
  background: #fff; border: 1px solid var(--border); border-radius: 10px;
  padding: 12px 14px; border-top: 3px solid #e07b00;
  box-shadow: 0 1px 4px rgba(0,0,0,.08); margin-bottom: 8px;
}
.sv-variedad { font-family: var(--fh); font-size: .95rem; font-weight: 700; text-transform: uppercase; color: #1a2a4a; }
.sv-row { display: flex; justify-content: space-between; align-items: center; padding: 4px 0; border-bottom: 1px solid #edf0f5; font-size: .82rem; }
.sv-row:last-child { border-bottom: none; }
.sv-label { color: var(--muted); font-size: .68rem; text-transform: uppercase; letter-spacing: .4px; }

.section-title {
  font-family: var(--fh); font-size: 1.15rem; font-weight: 800;
  text-transform: uppercase; letter-spacing: 1.5px; color: #1a2a4a;
  border-bottom: 2px solid #e07b00; padding-bottom: 5px; margin: 18px 0 12px;
}
.esp-title {
  font-family: var(--fh); font-size: .95rem; font-weight: 700;
  text-transform: uppercase; color: #1a7abf; margin: 10px 0 6px;
  border-left: 3px solid #1a7abf; padding-left: 9px;
}
div[data-testid="stMetric"] label { font-size: .65rem !important; }
</style>
""", unsafe_allow_html=True)

# ─── CONEXIÓN GOOGLE SHEETS ───────────────────────────────────
def get_google_sheet():
    if "gcp_service_account" not in st.secrets:
        st.warning("⚠️ Credenciales de Google Sheets no configuradas en Cloud Secrets. Usando modo local.")
        return None
    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scopes)
        client = gspread.authorize(creds)
        return client.open_by_key(SPREADSHEET_ID).worksheet("Stock")
    except Exception as e:
        st.error(f"❌ Error de autenticación con Google Sheets: {e}")
        return None

def load_stock_from_sheets():
    wsh = get_google_sheet()
    if wsh is None:
        return STOCK_INIT.copy()
    try:
        records = wsh.get_all_records()
        stock_list = []
        for idx, r in enumerate(records, start=1):
            if not r.get("Campaña") or not r.get("Variedad"): 
                continue
            tipo_lower = str(r.get("Tipo", "")).lower().strip()
            peso_unit = 800 if "bigbag" in tipo_lower else 25
            
            trat_val = str(r.get("Tratada", "")).strip().lower()
            trat_bool = trat_val in ["sí", "si", "yes", "true", "✅", "x"]

            pg_clean = str(r.get("PG %", "")).replace("%", "").strip()
            pmil_clean = str(r.get("PMIL g", "")).lower().replace("g", "").strip()

            stock_list.append({
                "id": idx,
                "campaña": str(r.get("Campaña", "")),
                "especie": str(r.get("Especie", "")),
                "variedad": str(r.get("Variedad", "")),
                "tipo": "bigbag" if "bigbag" in tipo_lower else "bolsa",
                "tratada": trat_bool,
                "cantidad": int(r.get("Cantidad", 0)) if r.get("Cantidad") else 0,
                "pesoUnit": peso_unit,
                "lote": str(r.get("Lote", "")),
                "ubicacion": str(r.get("Ubicación", "")),
                "fecha": str(r.get("Fecha", "")),
                "pg": int(pg_clean) if pg_clean.isdigit() else "",
                "pmil": float(pmil_clean) if pmil_clean.replace('.', '', 1).isdigit() else "",
                "obs": str(r.get("Obs", ""))
            })
        return stock_list if stock_list else STOCK_INIT.copy()
    except Exception as e:
        st.error(f"⚠️ Error al leer filas de Google Sheets (usando respaldo temporal): {e}")
        return STOCK_INIT.copy()

def save_stock_to_sheets(stock_data):
    wsh = get_google_sheet()
    if wsh is None:
        return
    try:
        wsh.resize(rows=1) # Deja solo la fila de encabezados
        rows_to_append = []
        for i in stock_data:
            tipo_str = "BigBag" if i.get("tipo") == "bigbag" else "Bolsa"
            tratada_str = "Sí" if i.get("tratada") else "No"
            kg_tot = i.get("cantidad", 0) * i.get("pesoUnit", 0)
            
            rows_to_append.append([
                i.get("campaña", ""),
                i.get("especie", ""),
                i.get("variedad", ""),
                tipo_str,
                tratada_str,
                i.get("cantidad", 0),
                kg_tot,
                f"{i.get('pg')}%" if i.get("pg") else "",
                f"{i.get('pmil')} g" if i.get("pmil") else "",
                i.get("lote", ""),
                i.get("ubicacion", ""),
                str(i.get("fecha", "")),
                i.get("obs", "")
            ])
        if rows_to_append:
            wsh.append_rows(rows_to_append, value_input_option="USER_ENTERED")
    except Exception as e:
        st.error(f"❌ No se pudo escribir en Google Sheets: {e}")

# ─── PERSISTENCIA LOCAL (CATÁLOGOS) ───────────────────────────
def load_data():
    p = Path(DATA_FILE)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "historial": [],
        "ordenes": [],
        "campañas": CAMPAÑAS_DEF.copy(),
        "especies": ESPECIES_DEF.copy(),
        "varMap": {k: list(v) for k, v in VARS_DEF.items()},
        "password": DEFAULT_PASS,
    }

def save_data():
    d = {
        "historial": st.session_state.historial,
        "ordenes":   st.session_state.ordenes,
        "campañas":  st.session_state.campañas,
        "especies":  st.session_state.especies,
        "varMap":    st.session_state.varMap,
        "password":  st.session_state.password,
    }
    Path(DATA_FILE).write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    save_stock_to_sheets(st.session_state.stock)

def init_state():
    if "initialized" not in st.session_state:
        d = load_data()
        st.session_state.historial = d.get("historial", [])
        st.session_state.ordenes   = d.get("ordenes",   [])
        st.session_state.campañas  = d.get("campañas",  CAMPAÑAS_DEF.copy())
        st.session_state.especies  = d.get("especies",  ESPECIES_DEF.copy())
        st.session_state.varMap    = d.get("varMap",    {k: list(v) for k, v in VARS_DEF.items()})
        st.session_state.password  = d.get("password",  DEFAULT_PASS)
        st.session_state.logged_in = False
        st.session_state.modal     = None
        st.session_state.edit_item = None
        st.session_state.stock     = load_stock_from_sheets()
        st.session_state.initialized = True

# ─── HELPERS ──────────────────────────────────────────────────
def fmt(n):
    try: return f"{int(n):,}".replace(",", ".")
    except Exception: return str(n)

def next_id(lst):
    return max((i.get("id", 0) for i in lst), default=0) + 1

def kg_total(item):
    return item.get("cantidad", 0) * item.get("pesoUnit", 0)

def badge(text, cls):
    return f'<span class="badge badge-{cls}">{text}</span>'

def to_csv(rows):
    buf = io.StringIO()
    for row in rows:
        buf.write(";".join(str(c) if c is not None else "" for c in row) + "\r\n")
    return buf.getvalue().encode("utf-8-sig")

# ─── INICIO ───────────────────────────────────────────────────
init_state()

# ─── LOGIN ────────────────────────────────────────────────────
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("---")
        st.markdown("### 🌱 La Clementina")
        st.markdown("**Planta de Semillas** · Ingresá tu clave para continuar")
        pwd = st.text_input("Clave", type="password", label_visibility="collapsed", placeholder="••••••••••")
        if st.button("Ingresar →", use_container_width=True, type="primary"):
            if pwd == st.session_state.password:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ Clave incorrecta. Intentá de nuevo.")
    st.stop()

# ─── HEADER ───────────────────────────────────────────────────
st.markdown("""
<div class="lc-header">
  <div>
    <h1>🌾 Planta de Semillas · <span>Stock</span></h1>
    <p>Control de producción · BigBag &amp; Bolsa · Por campaña y variedad</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── KPIs ─────────────────────────────────────────────────────
stock = st.session_state.stock
total_bb   = sum(i["cantidad"] for i in stock if i.get("tipo") == "bigbag")
total_bo   = sum(i["cantidad"] for i in stock if i.get("tipo") == "bolsa")
total_kg   = sum(kg_total(i) for i in stock)
total_vars = len(set(f"{i.get('especie')}{i.get('variedad')}" for i in stock))
low_count  = sum(1 for i in stock if i.get("cantidad", 0) <= LOW)
oc_pend    = sum(1 for o in st.session_state.ordenes if o.get("estado") == "pendiente")

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("🏗 BigBags",      fmt(total_bb))
c2.metric("🎒 Bolsas",       fmt(total_bo))
c3.metric("⚖ Toneladas",    f"{total_kg/1000:.1f} t")
c4.metric("🌱 Variedades",   total_vars)
c5.metric("⚠ Stock bajo",   low_count)
c6.metric("📋 OC Pendientes", oc_pend)

# ─── TABS ─────────────────────────────────────────────────────
tab_labels = ["📋 Resumen", "📦 Tabla", "🕘 Historial", "📋 Órd. de Carga", "⚙ Catálogos"]
tabs = st.tabs(tab_labels)

# ══════════════════════════════════════════════════════════════
# TAB 1 — RESUMEN
# ══════════════════════════════════════════════════════════════
with tabs[0]:
    col_f1, col_f2, _ = st.columns([2, 2, 4])
    with col_f1: r_camp = st.selectbox("Campaña", ["Todas"] + st.session_state.campañas, key="r_camp")
    with col_f2: r_esp = st.selectbox("Especie", ["Todas"] + st.session_state.especies, key="r_esp")

    resumen = {}
    for i in stock:
        camp = i.get("campaña", "")
        esp  = i.get("especie", "")
        if r_camp != "Todas" and camp != r_camp: continue
        if r_esp != "Todas" and esp != r_esp: continue
        key = f"{i.get('variedad')}|||{i.get('tipo')}|||{i.get('tratada')}"
        if camp not in resumen: resumen[camp] = {}
        if esp not in resumen[camp]: resumen[camp][esp] = {}
        if key not in resumen[camp][esp]:
            resumen[camp][esp][key] = {"variedad": i.get("variedad"), "tipo": i.get("tipo"), "tratada": i.get("tratada"), "_uds": 0, "_kgs": 0}
        resumen[camp][esp][key]["_uds"] += i.get("cantidad", 0)
        resumen[camp][esp][key]["_kgs"] += kg_total(i)

    if not resumen:
        st.info("Sin stock para mostrar.")
    else:
        for camp in sorted(resumen.keys()):
            camp_kg = sum(d["_kgs"] for esp_d in resumen[camp].values() for d in esp_d.values())
            st.markdown(f'<div class="section-title">📅 Campaña {camp} &nbsp;<small style="font-weight:400;font-size:.8rem;color:#6b7280">{fmt(round(camp_kg/1000))} t totales</small></div>', unsafe_allow_html=True)
            for esp in sorted(resumen[camp].keys()):
                st.markdown(f'<div class="esp-title">🌱 {esp}</div>', unsafe_allow_html=True)
                cards = list(resumen[camp][esp].values())
                cols = st.columns(min(len(cards), 3))
                for idx, d in enumerate(cards):
                    is_low = d["_uds"] <= LOW
                    top_color = "#c0392b" if is_low else ("#e07b00" if d["tipo"] == "bigbag" else "#1a7abf")
                    tipo_badge = badge("🏗 BigBag", "bb") if d["tipo"] == "bigbag" else badge("🎒 Bolsa", "bo")
                    low_badge  = badge("⚠ Bajo", "low") if is_low else ""
                    trat_badge = badge("✅ Tratada", "tr") if d["tratada"] else badge("○ Sin tratar", "st")
                    uds_color  = "#c0392b" if is_low else "#e07b00"
                    html = f"""
                    <div class="sv-card" style="border-top-color:{top_color}">
                      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:9px">
                        <span class="sv-variedad">{d["variedad"]}</span>
                        <span>{tipo_badge} {low_badge}</span>
                      </div>
                      <div class="sv-row"><span class="sv-label">Tratamiento</span>{trat_badge}</div>
                      <div class="sv-row"><span class="sv-label">Unidades</span><span style="font-family:'Barlow Condensed',sans-serif;font-size:1.1rem;font-weight:800;color:{uds_color}">{fmt(d["_uds"])}</span></div>
                      <div class="sv-row"><span class="sv-label">Kilogramos</span><span style="font-family:'Barlow Condensed',sans-serif;font-size:1rem;font-weight:800;color:#2e8b57">{fmt(d["_kgs"])} kg</span></div>
                      <div class="sv-row"><span class="sv-label">Toneladas</span><span style="font-family:'Barlow Condensed',sans-serif;font-size:1rem;font-weight:700;color:#6b7280">{d["_kgs"]/1000:.2f} t</span></div>
                    </div>"""
                    with cols[idx % 3]: st.markdown(html, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 2 — TABLA
# ══════════════════════════════════════════════════════════════
with tabs[1]:
    tf1, tf2, tf3, tf4, tf5, tf6 = st.columns([3, 2, 2, 2, 2, 1])
    with tf1: search = st.text_input("🔍 Buscar", placeholder="Variedad, lote, especie…", label_visibility="collapsed", key="t_search")
    with tf2: f_camp = st.selectbox("Campaña", ["Todas"] + st.session_state.campañas, key="t_camp", label_visibility="collapsed")
    with tf3: f_esp = st.selectbox("Especie", ["Todas"] + st.session_state.especies, key="t_esp", label_visibility="collapsed")
    with tf4: f_tipo = st.selectbox("Tipo", ["BB + Bolsa", "BigBag", "Bolsa"], key="t_tipo", label_visibility="collapsed")
    with tf5: f_trat = st.selectbox("Tratamiento", ["Tratada + S/T", "Solo Tratada", "Sin tratar"], key="t_trat", label_visibility="collapsed")
    with tf6:
        if st.button("＋ Nuevo", type="primary", use_container_width=True):
            st.session_state.modal = "new"
            st.session_state.edit_item = None
            st.rerun()

    filtered = []
    for i in stock:
        if f_camp != "Todas" and i.get("campaña") != f_camp: continue
        if f_esp  != "Todas" and i.get("especie")  != f_esp:  continue
        if f_tipo == "BigBag" and i.get("tipo") != "bigbag": continue
        if f_tipo == "Bolsa"  and i.get("tipo") != "bolsa":  continue
        if f_trat == "Solo Tratada" and not i.get("tratada"): continue
        if f_trat == "Sin tratar"   and i.get("tratada"):     continue
        if search:
            hay = " ".join(str(i.get(k,"")) for k in ["variedad","especie","lote","campaña","obs"]).lower()
            if search.lower() not in hay: continue
        filtered.append(i)

    bc1, bc2, _ = st.columns([2, 2, 8])
    with bc1:
        rows = [["Campaña","Especie","Variedad","Tipo","Tratada","Cantidad","Kg Totales","PG (%)","PMIL (g)","Lote","Ubicación","Fecha","Observaciones"]]
        for i in filtered:
            rows.append([i.get("campaña",""), i.get("especie",""), i.get("variedad",""), "BigBag" if i.get("tipo")=="bigbag" else "Bolsa", "Sí" if i.get("tratada") else "No", i.get("cantidad",""), kg_total(i), i.get("pg",""), i.get("pmil",""), i.get("lote",""), i.get("ubicacion",""), i.get("fecha",""), i.get("obs","")])
        st.download_button("⬇ Excel/CSV", data=to_csv(rows), file_name=f"stock_{date.today()}.csv", mime="text/csv")

    if not filtered:
        st.info("Sin registros para los filtros seleccionados.")
    else:
        df_cols = ["Campaña","Especie","Variedad","Tipo","Tratada","Cantidad","Kg","PG %","PMIL g","Lote","Ubicación","Fecha","Obs."]
        rows_df = []
        for i in filtered:
            low = i.get("cantidad",0) <= LOW
            rows_df.append({
                "Campaña":   i.get("campaña",""), "Especie":   i.get("especie",""), "Variedad":  i.get("variedad","") + (" ⚠" if low else ""), "Tipo":      "BigBag" if i.get("tipo")=="bigbag" else "Bolsa", "Tratada":   "✅" if i.get("tratada") else "○", "Cantidad":  i.get("cantidad",0), "Kg":        kg_total(i), "PG %":      f"{i.get('pg','')}%" if i.get("pg") not in (None, "") else "—", "PMIL g":    f"{i.get('pmil','')} g" if i.get("pmil") not in (None, "") else "—", "Lote":      i.get("lote","—"), "Ubicación": i.get("ubicacion","—"), "Fecha":     i.get("fecha",""), "Obs.":      str(i.get("obs","")), "_id":       i.get("id"), "_low":      low,
            })
        df = pd.DataFrame(rows_df)
        st.dataframe(df[df_cols], use_container_width=True, hide_index=True, height=min(40 + 35 * len(df), 550))
        st.caption(f"**{len(filtered)} registros** · **{fmt(sum(kg_total(i) for i in filtered))} kg** totales filtrados")

        st.markdown("**Acciones por registro:**")
        sel_variedad = st.selectbox("Seleccionar registro", options=[(i.get("id"), f"{i.get('variedad')} | {i.get('tipo')} | Lote: {i.get('lote','—')} | {fmt(i.get('cantidad',0))} uds") for i in filtered], format_func=lambda x: x[1], label_visibility="collapsed", key="sel_item_id")
        if sel_variedad:
            sel_id = sel_variedad[0]
            sel_item = next((i for i in stock if i.get("id") == sel_id), None)
            if sel_item:
                ac1, ac2 = st.columns(2)
                with ac1:
                    if st.button("✏ Editar", use_container_width=True):
                        st.session_state.modal = "edit"
                        st.session_state.edit_item = sel_item
                        st.rerun()
                with ac2:
                    if st.button("✕ Eliminar", use_container_width=True):
                        st.session_state.modal = "delete"
                        st.session_state.edit_item = sel_item
                        st.rerun()

# ══════════════════════════════════════════════════════════════
# TAB 3 — HISTORIAL
# ══════════════════════════════════════════════════════════════
with tabs[2]:
    st.info("Módulo de historial local activo.")

# ══════════════════════════════════════════════════════════════
# TAB 4 — ÓRDENES DE CARGA
# ══════════════════════════════════════════════════════════════
with tabs[3]:
    st.info("Módulo de órdenes de carga activo.")

# ══════════════════════════════════════════════════════════════
# TAB 5 — CATÁLOGOS / ADMIN (RECONSTRUIDO Y COMPLETADO)
# ══════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-title">⚙ Gestión de Catálogos</div>', unsafe_allow_html=True)
    col_adm1, col_adm2 = st.columns(2)

    with col_adm1:
        st.markdown("**📅 Campañas**")
        for c in st.session_state.campañas:
            ca, cb = st.columns([4, 1])
            ca.write(c)
            if cb.button("✕", key=f"del_camp_{c}"):
                st.session_state.campañas = [x for x in st.session_state.campañas if x != c]
                save_data(); st.rerun()
        new_c = st.text_input("Nueva campaña", placeholder="Ej. 2026/2027", key="new_camp")
        if st.button("+ Agregar campaña") and new_c.strip():
            if new_c.strip() not in st.session_state.campañas:
                st.session_state.campañas.append(new_c.strip())
                save_data(); st.rerun()

    with col_adm2:
        st.markdown("**🌱 Especies**")
        for e in st.session_state.especies:
            ea, eb = st.columns([4, 1])
            ea.write(e)
            if eb.button("✕", key=f"del_esp_{e}"):
                st.session_state.especies = [x for x in st.session_state.especies if x != e]
                st.session_state.varMap.pop(e, None)
                save_data(); st.rerun()
        new_e = st.text_input("Nueva especie", placeholder="Ej. Arveja", key="new_esp")
        if st.button("+ Agregar especie") and new_e.strip():
            if new_e.strip() not in st.session_state.especies:
                st.session_state.especies.append(new_e.strip())
                st.session_state.varMap[new_e.strip()] = []
                save_data(); st.rerun()

    st.markdown("**🌿 Variedades por especie**")
    sel_esp_cat = st.selectbox("Seleccionar especie para ver/editar variedades", st.session_state.especies, key="sel_esp_cat")
    if sel_esp_cat:
        variedades = st.session_state.varMap.get(sel_esp_cat, [])
        for v in variedades:
            va, vb = st.columns([4, 1])
            va.write(v)
            if vb.button("✕", key=f"del_var_{sel_esp_cat}_{v}"):
                st.session_state.varMap[sel_esp_cat] = [x for x in variedades if x != v]
                save_data(); st.rerun()
        new_v = st.text_input("Nueva variedad", placeholder="Ej. DM 40R21", key="new_var")
        if st.button("+ Agregar variedad") and new_v.strip():
            if new_v.strip() not in st.session_state.varMap[sel_esp_cat]:
                st.session_state.varMap[sel_esp_cat].append(new_v.strip())
                save_data(); st.rerun()

# ══════════════════════════════════════════════════════════════
# ─── MODALS / FORMULARIOS INTERACTIVOS ────────────────────────
# ══════════════════════════════════════════════════════════════
if "modal" in st.session_state and st.session_state.modal:
    m = st.session_state.modal
    st.markdown("---")
    
    if m in ["new", "edit"]:
        st.markdown(f"### {'＋ Nuevo Registro' if m == 'new' else '✏ Editar Registro'}")
        item = st.session_state.edit_item if m == "edit" else {}
        
        with st.form("form_stock"):
            m_camp = st.selectbox("Campaña", st.session_state.campañas, index=st.session_state.campañas.index(item["campaña"]) if item and item.get("campaña") in st.session_state.campañas else 0)
            m_esp = st.selectbox("Especie", st.session_state.especies, index=st.session_state.especies.index(item["especie"]) if item and item.get("especie") in st.session_state.especies else 0)
            
            vars_dispo = st.session_state.varMap.get(m_esp, ["General"])
            m_var = st.selectbox("Variedad", vars_dispo, index=vars_dispo.index(item["variedad"]) if item and item.get("variedad") in vars_dispo else 0)
            
            m_tipo = st.radio("Tipo", ["BigBag", "Bolsa"], index=0 if item.get("tipo", "bigbag") == "bigbag" else 1)
            m_trat = st.checkbox("Tratada", value=item.get("tratada", False))
            m_cant = st.number_input("Cantidad", min_value=0, value=int(item.get("cantidad", 0)))
            m_lote = st.text_input("Lote", value=item.get("lote", ""))
            m_ubic = st.text_input("Ubicación", value=item.get("ubicacion", ""))
            m_fecha = st.date_input("Fecha", value=datetime.strptime(item["fecha"], "%Y-%m-%d").date() if item and item.get("fecha") else date.today())
            m_pg = st.number_input("PG % (Dejar en 0 si no aplica)", min_value=0, max_value=100, value=int(item.get("pg", 0)) if item and item.get("pg") else 0)
            m_pmil = st.number_input("PMIL g (Dejar en 0 si no aplica)", min_value=0.0, value=float(item.get("pmil", 0.0)) if item and item.get("pmil") else 0.0)
            m_obs = st.text_area("Observaciones", value=item.get("obs", ""))
            
            if st.form_submit_button("Guardar Cambios"):
                p_unit = 800 if m_tipo == "BigBag" else 25
                new_data = {
                    "campaña": m_camp, "especie": m_esp, "variedad": m_var, "tipo": m_tipo.lower(), "tratada": m_trat, "cantidad": m_cant, "pesoUnit": p_unit, "lote": m_lote, "ubicacion": m_ubic, "fecha": m_fecha.strftime("%Y-%m-%d"), "pg": m_pg if m_pg > 0 else "", "pmil": m_pmil if m_pmil > 0 else "", "obs": m_obs
                }
                if m == "new":
                    new_data["id"] = next_id(st.session_state.stock)
                    st.session_state.stock.append(new_data)
                else:
                    new_data["id"] = item["id"]
                    st.session_state.stock = [new_data if x.get("id") == item["id"] else x for x in st.session_state.stock]
                
                save_data()
                st.session_state.modal = None
                st.rerun()
                
    elif m == "delete":
        item = st.session_state.edit_item
        st.error(f"⚠ ¿Estás seguro de que querés eliminar permanentemente el registro de {item['variedad']} (Lote: {item['lote']})?")
        c_del1, c_del2 = st.columns(2)
        if c_del1.button("Sí, eliminar", type="primary", use_container_width=True):
            st.session_state.stock = [x for x in st.session_state.stock if x.get("id") != item["id"]]
            save_data()
            st.session_state.modal = None
            st.rerun()
        if c_del2.button("Cancelar", use_container_width=True):
            st.session_state.modal = None
            st.rerun()

# ─── FOOTER ───────────────────────────────────────────────────
st.markdown("<br><hr><center style='color:#6b7280; font-size:0.8rem;'>Creado por Ignacio Diaz</center>", unsafe_allow_html=True)
