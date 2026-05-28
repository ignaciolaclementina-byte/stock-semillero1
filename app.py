La Clementina · Sistema de Gestión de Stock de Semillas
Versión Streamlit — Equivalente al HTML original
"""

import streamlit as st
import pandas as pd
import json
import io
from datetime import datetime, date
from pathlib import Path

# ─── CONFIGURACIÓN ────────────────────────────────────────────
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
    {"id": 2, "campaña": "2024/2025", "especie": "Soja",  "variedad": "DM 4612",      "tipo": "bolsa",  "tratada": True,  "cantidad": 320, "pesoUnit": 25,  "lote": "L-001", "ubicacion": "", "fecha": "2025-04-01", "pg": 95, "pmil": 140, "obs": "Curasemillas MaximXL"},
    {"id": 3, "campaña": "2024/2025", "especie": "Maíz",  "variedad": "DK 7210",      "tipo": "bigbag", "tratada": True,  "cantidad": 8,   "pesoUnit": 800, "lote": "L-002", "ubicacion": "", "fecha": "2025-04-02", "pg": 92, "pmil": 280, "obs": "Tratado"},
    {"id": 4, "campaña": "2024/2025", "especie": "Trigo", "variedad": "Klein Proteo", "tipo": "bolsa",  "tratada": False, "cantidad": 480, "pesoUnit": 25,  "lote": "L-003", "ubicacion": "", "fecha": "2025-04-03", "pg": 88, "pmil": 32,  "obs": ""},
    {"id": 5, "campaña": "2025/2026", "especie": "Soja",  "variedad": "SY 3x8",       "tipo": "bigbag", "tratada": False, "cantidad": 20,  "pesoUnit": 800, "lote": "L-010", "ubicacion": "", "fecha": "2025-04-04", "pg": 97, "pmil": 155, "obs": ""},
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

/* Header */
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

/* KPI strip */
.kpi-wrap { display: flex; gap: 2px; margin-bottom: 14px; }
.kpi-box {
  flex: 1; background: #fff; padding: 12px 16px;
  border: 1px solid var(--border); border-radius: 8px; text-align: center;
}
.kpi-val { font-family: var(--fh); font-size: 1.7rem; font-weight: 800; line-height: 1; }
.kpi-lbl { font-size: .62rem; color: var(--muted); text-transform: uppercase; letter-spacing: .7px; margin-top: 2px; }
.c-or { color: #e07b00; } .c-bl { color: #1a7abf; } .c-gr { color: #2e8b57; }
.c-pu { color: #7b4fa6; } .c-re { color: #c0392b; }

/* Badges */
.badge {
  display: inline-block; padding: 2px 8px; border-radius: 20px;
  font-size: .7rem; font-weight: 700; font-family: var(--fh);
  text-transform: uppercase; letter-spacing: .4px;
}
.badge-bb    { background:#fff4e0; color:#b86000; border:1px solid #f5c57a; }
.badge-bo    { background:#e6f4fb; color:#1a7abf; border:1px solid #90cae8; }
.badge-tr    { background:#e6f5ec; color:#2e8b57; border:1px solid #7dc99a; }
.badge-st    { background:#f3f4f6; color:#6b7280; border:1px solid #d1d5db; }
.badge-low   { background:#fde8e8; color:#c0392b; border:1px solid #f5a5a5; }
.badge-pend  { background:#fef9ee; color:#92600a; border:1px solid #f5c57a; }
.badge-desp  { background:#e6f5ec; color:#2e8b57; border:1px solid #7dc99a; }

/* Cards resumen */
.sv-card {
  background: #fff; border: 1px solid var(--border); border-radius: 10px;
  padding: 12px 14px; border-top: 3px solid #e07b00;
  box-shadow: 0 1px 4px rgba(0,0,0,.08); margin-bottom: 8px;
}
.sv-variedad { font-family: var(--fh); font-size: .95rem; font-weight: 700; text-transform: uppercase; color: #1a2a4a; }
.sv-row { display: flex; justify-content: space-between; align-items: center; padding: 4px 0; border-bottom: 1px solid #edf0f5; font-size: .82rem; }
.sv-row:last-child { border-bottom: none; }
.sv-label { color: var(--muted); font-size: .68rem; text-transform: uppercase; letter-spacing: .4px; }

/* Login */
.login-wrap {
  min-height: 70vh; display: flex; align-items: center; justify-content: center;
}
.login-box {
  background: #fff; border-radius: 16px; padding: 40px 48px;
  width: 100%; max-width: 380px; text-align: center;
  box-shadow: 0 8px 40px rgba(0,0,0,.15);
}

/* Misc */
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

# ─── PERSISTENCIA ─────────────────────────────────────────────
def load_data():
    p = Path(DATA_FILE)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "stock": STOCK_INIT.copy(),
        "historial": [],
        "ordenes": [],
        "campañas": CAMPAÑAS_DEF.copy(),
        "especies": ESPECIES_DEF.copy(),
        "varMap": {k: list(v) for k, v in VARS_DEF.items()},
        "password": DEFAULT_PASS,
    }

def save_data():
    d = {
        "stock":    st.session_state.stock,
        "historial":st.session_state.historial,
        "ordenes":  st.session_state.ordenes,
        "campañas": st.session_state.campañas,
        "especies": st.session_state.especies,
        "varMap":   st.session_state.varMap,
        "password": st.session_state.password,
    }
    Path(DATA_FILE).write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

def init_state():
    if "initialized" not in st.session_state:
        d = load_data()
        st.session_state.stock     = d.get("stock",     STOCK_INIT.copy())
        st.session_state.historial = d.get("historial", [])
        st.session_state.ordenes   = d.get("ordenes",   [])
        st.session_state.campañas  = d.get("campañas",  CAMPAÑAS_DEF.copy())
        st.session_state.especies  = d.get("especies",  ESPECIES_DEF.copy())
        st.session_state.varMap    = d.get("varMap",    {k: list(v) for k, v in VARS_DEF.items()})
        st.session_state.password  = d.get("password",  DEFAULT_PASS)
        st.session_state.logged_in = False
        st.session_state.tab       = "resumen"
        st.session_state.modal     = None
        st.session_state.edit_item = None
        st.session_state.edit_oc   = None
        st.session_state.initialized = True

# ─── HELPERS ──────────────────────────────────────────────────
def fmt(n):
    try:
        return f"{int(n):,}".replace(",", ".")
    except Exception:
        return str(n)

def now_str():
    return datetime.now().strftime("%d/%m/%Y %H:%M")

def next_id(lst):
    return max((i.get("id", 0) for i in lst), default=0) + 1

def fmt_oc(n):
    return f"OC-{n:03d}"

def next_oc_num(ordenes):
    nums = []
    for o in ordenes:
        try:
            nums.append(int(o["numero"].replace("OC-", "")))
        except Exception:
            pass
    return max(nums, default=0) + 1

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
        pwd = st.text_input("Clave", type="password", label_visibility="collapsed",
                            placeholder="••••••••••")
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
    with col_f1:
        r_camp = st.selectbox("Campaña", ["Todas"] + st.session_state.campañas, key="r_camp")
    with col_f2:
        r_esp = st.selectbox("Especie", ["Todas"] + st.session_state.especies, key="r_esp")

    # Agrupar
    resumen = {}
    for i in stock:
        camp = i.get("campaña", "")
        esp  = i.get("especie", "")
        if r_camp != "Todas" and camp != r_camp:
            continue
        if r_esp != "Todas" and esp != r_esp:
            continue
        key = f"{i.get('variedad')}|||{i.get('tipo')}|||{i.get('tratada')}"
        if camp not in resumen:
            resumen[camp] = {}
        if esp not in resumen[camp]:
            resumen[camp][esp] = {}
        if key not in resumen[camp][esp]:
            resumen[camp][esp][key] = {"variedad": i.get("variedad"), "tipo": i.get("tipo"),
                                        "tratada": i.get("tratada"), "_uds": 0, "_kgs": 0}
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
                      <div class="sv-row"><span class="sv-label">Unidades</span>
                        <span style="font-family:'Barlow Condensed',sans-serif;font-size:1.1rem;font-weight:800;color:{uds_color}">{fmt(d["_uds"])}</span>
                      </div>
                      <div class="sv-row"><span class="sv-label">Kilogramos</span>
                        <span style="font-family:'Barlow Condensed',sans-serif;font-size:1rem;font-weight:800;color:#2e8b57">{fmt(d["_kgs"])} kg</span>
                      </div>
                      <div class="sv-row"><span class="sv-label">Toneladas</span>
                        <span style="font-family:'Barlow Condensed',sans-serif;font-size:1rem;font-weight:700;color:#6b7280">{d["_kgs"]/1000:.2f} t</span>
                      </div>
                    </div>"""
                    with cols[idx % 3]:
                        st.markdown(html, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 2 — TABLA
# ══════════════════════════════════════════════════════════════
with tabs[1]:
    # Filtros
    tf1, tf2, tf3, tf4, tf5, tf6 = st.columns([3, 2, 2, 2, 2, 1])
    with tf1:
        search = st.text_input("🔍 Buscar", placeholder="Variedad, lote, especie…", label_visibility="collapsed", key="t_search")
    with tf2:
        f_camp = st.selectbox("Campaña", ["Todas"] + st.session_state.campañas, key="t_camp", label_visibility="collapsed")
    with tf3:
        f_esp = st.selectbox("Especie", ["Todas"] + st.session_state.especies, key="t_esp", label_visibility="collapsed")
    with tf4:
        f_tipo = st.selectbox("Tipo", ["BB + Bolsa", "BigBag", "Bolsa"], key="t_tipo", label_visibility="collapsed")
    with tf5:
        f_trat = st.selectbox("Tratamiento", ["Tratada + S/T", "Solo Tratada", "Sin tratar"], key="t_trat", label_visibility="collapsed")
    with tf6:
        if st.button("＋ Nuevo", type="primary", use_container_width=True):
            st.session_state.modal = "new"
            st.session_state.edit_item = None
            st.rerun()

    # Filtrar
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

    # Botones CSV / Imprimir
    bc1, bc2, _ = st.columns([2, 2, 8])
    with bc1:
        rows = [["Campaña","Especie","Variedad","Tipo","Tratada","Cantidad","Kg Totales","PG (%)","PMIL (g)","Lote","Ubicación","Fecha","Observaciones"]]
        for i in filtered:
            rows.append([i.get("campaña",""), i.get("especie",""), i.get("variedad",""),
                         "BigBag" if i.get("tipo")=="bigbag" else "Bolsa",
                         "Sí" if i.get("tratada") else "No",
                         i.get("cantidad",""), kg_total(i),
                         i.get("pg",""), i.get("pmil",""),
                         i.get("lote",""), i.get("ubicacion",""),
                         i.get("fecha",""), i.get("obs","")])
        st.download_button("⬇ Excel/CSV", data=to_csv(rows),
                           file_name=f"stock_{date.today()}.csv", mime="text/csv")

    # Tabla
    if not filtered:
        st.info("Sin registros para los filtros seleccionados.")
    else:
        df_cols = ["Campaña","Especie","Variedad","Tipo","Tratada","Cantidad","Kg","PG %","PMIL g","Lote","Ubicación","Fecha","Obs."]
        rows_df = []
        for i in filtered:
            low = i.get("cantidad",0) <= LOW
            rows_df.append({
                "Campaña":   i.get("campaña",""),
                "Especie":   i.get("especie",""),
                "Variedad":  i.get("variedad","") + (" ⚠" if low else ""),
                "Tipo":      "BigBag" if i.get("tipo")=="bigbag" else "Bolsa",
                "Tratada":   "✅" if i.get("tratada") else "○",
                "Cantidad":  i.get("cantidad",0),
                "Kg":        kg_total(i),
                "PG %":      f"{i.get('pg','')}%" if i.get("pg") not in (None, "") else "—",
                "PMIL g":    f"{i.get('pmil','')} g" if i.get("pmil") not in (None, "") else "—",
                "Lote":      i.get("lote","—"),
                "Ubicación": i.get("ubicacion","—"),
                "Fecha":     i.get("fecha",""),
                "Obs.":      (str(i.get("obs",""))[:40] + "…") if len(str(i.get("obs",""))) > 40 else i.get("obs","—"),
                "_id":       i.get("id"),
                "_low":      low,
            })
        df = pd.DataFrame(rows_df)

        display_df = df[df_cols]
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            height=min(40 + 35 * len(display_df), 550),
        )

        # Total pie filtrado
        tot_kg_filt = sum(kg_total(i) for i in filtered)
        st.caption(f"**{len(filtered)} registro{'s' if len(filtered)!=1 else ''}** &nbsp;·&nbsp; "
                   f"**{fmt(tot_kg_filt)} kg** totales filtrados")

        # Acciones por registro
        st.markdown("**Acciones por registro:**")
        sel_variedad = st.selectbox(
            "Seleccionar registro",
            options=[(i.get("id"), f"{i.get('variedad')} | {i.get('tipo')} | {i.get('campaña')} | Lote: {i.get('lote','—')} | {fmt(i.get('cantidad',0))} uds") for i in filtered],
            format_func=lambda x: x[1],
            label_visibility="collapsed",
            key="sel_item_id"
        )
        if sel_variedad:
            sel_id = sel_variedad[0]
            sel_item = next((i for i in stock if i.get("id") == sel_id), None)
            if sel_item:
                ac1, ac2, ac3 = st.columns(3)
                with ac1:
                    if st.button("⇄ Mover / Orden", use_container_width=True):
                        st.session_state.modal = "move"
                        st.session_state.edit_item = sel_item
                        st.rerun()
                with ac2:
                    if st.button("✏ Editar", use_container_width=True):
                        st.session_state.modal = "edit"
                        st.session_state.edit_item = sel_item
                        st.rerun()
                with ac3:
                    if st.button("✕ Eliminar", use_container_width=True):
                        st.session_state.modal = "delete"
                        st.session_state.edit_item = sel_item
                        st.rerun()

# ══════════════════════════════════════════════════════════════
# TAB 3 — HISTORIAL
# ══════════════════════════════════════════════════════════════
with tabs[2]:
    historial = st.session_state.historial
    hf1, hf2, _ = st.columns([2, 2, 8])
    with hf1:
        h_camp = st.selectbox("Campaña", ["Todas"] + st.session_state.campañas, key="h_camp", label_visibility="collapsed")
    with hf2:
        h_op = st.selectbox("Operación", ["Egresos + Ingresos", "Solo Egresos", "Solo Ingresos"], key="h_op", label_visibility="collapsed")

    hist_filt = [h for h in historial
                 if (h_camp == "Todas" or h.get("campaña") == h_camp)
                 and (h_op == "Egresos + Ingresos"
                      or (h_op == "Solo Egresos"   and h.get("op") == "egreso")
                      or (h_op == "Solo Ingresos"  and h.get("op") == "ingreso"))]

    if not hist_filt:
        st.info("Sin movimientos para los filtros seleccionados." if historial else
                "Sin movimientos todavía. Usá ⇄ Mover en Tabla para registrar.")
    else:
        # CSV
        h_rows = [["Fecha","Campaña","Especie","Variedad","Tipo","Lote","Remito","N° Pedido","Operación","Cantidad","Kg Movidos","Stock Anterior","Stock Nuevo","Motivo"]]
        for h in hist_filt:
            h_rows.append([h.get("fecha",""), h.get("campaña",""), h.get("especie",""), h.get("variedad",""),
                            "BigBag" if h.get("tipo")=="bigbag" else "Bolsa",
                            h.get("lote",""), h.get("remito",""), h.get("nPedido",""),
                            "Egreso" if h.get("op")=="egreso" else "Ingreso",
                            h.get("delta",""), h.get("kgMovidos",""),
                            h.get("stockPrev",""), h.get("stockPost",""), h.get("motivo","")])
        st.download_button("⬇ Excel/CSV Historial", data=to_csv(h_rows),
                           file_name=f"historial_{date.today()}.csv", mime="text/csv")

        df_h = pd.DataFrame([{
            "Fecha":       h.get("fecha",""),
            "Campaña":     h.get("campaña",""),
            "Especie":     h.get("especie",""),
            "Variedad":    h.get("variedad",""),
            "Tipo":        "BigBag" if h.get("tipo")=="bigbag" else "Bolsa",
            "Lote":        h.get("lote","—"),
            "Remito":      h.get("remito","—"),
            "N° Pedido":   h.get("nPedido","—"),
            "Operación":   "⬇ Egreso" if h.get("op")=="egreso" else "⬆ Ingreso",
            "Cantidad":    f"{'-' if h.get('op')=='egreso' else '+'}{fmt(h.get('delta',0))}",
            "Kg":          f"{'-' if h.get('op')=='egreso' else '+'}{fmt(h.get('kgMovidos',0))} kg",
            "St. Anterior":fmt(h.get("stockPrev",0)),
            "St. Nuevo":   f"{fmt(h.get('stockPost',0))}{'⚠' if h.get('stockPost',0)<=LOW else ''}",
            "Motivo":      h.get("motivo","—"),
        } for h in hist_filt])
        st.dataframe(df_h, use_container_width=True, hide_index=True, height=min(40+35*len(df_h), 500))

        kg_egr = sum(h.get("kgMovidos",0) for h in hist_filt if h.get("op")=="egreso")
        kg_ing = sum(h.get("kgMovidos",0) for h in hist_filt if h.get("op")=="ingreso")
        st.caption(f"Egresos: **{fmt(kg_egr)} kg** &nbsp;·&nbsp; Ingresos: **{fmt(kg_ing)} kg** &nbsp;·&nbsp; {len(hist_filt)} movimientos")

# ══════════════════════════════════════════════════════════════
# TAB 4 — ÓRDENES DE CARGA
# ══════════════════════════════════════════════════════════════
with tabs[3]:
    ordenes = st.session_state.ordenes
    of1, of2, of3 = st.columns([2, 2, 3])
    with of1:
        oc_camp = st.selectbox("Campaña OC", ["Todas"] + st.session_state.campañas, key="oc_camp", label_visibility="collapsed")
    with of2:
        oc_status = st.selectbox("Estado", ["Todas", "Pendientes", "Despachadas"], key="oc_status", label_visibility="collapsed")
    with of3:
        oc_search = st.text_input("🔍 Buscar OC", placeholder="Número, variedad, destino…", label_visibility="collapsed", key="oc_search")

    oc_filt = []
    for o in ordenes:
        if oc_camp != "Todas" and o.get("campaña") != oc_camp: continue
        if oc_status == "Pendientes"  and o.get("estado") != "pendiente":  continue
        if oc_status == "Despachadas" and o.get("estado") != "despachada": continue
        if oc_search:
            lotes_str = " ".join(l.get("lote","") for l in o.get("lotes",[]))
            hay = " ".join([o.get("numero",""), o.get("remito",""), o.get("nPedido",""),
                            o.get("variedad",""), o.get("especie",""), lotes_str,
                            o.get("destino",""), o.get("obs","")]).lower()
            if oc_search.lower() not in hay: continue
        oc_filt.append(o)

    if not oc_filt:
        st.info("Sin órdenes para los filtros seleccionados." if ordenes else
                "Sin órdenes todavía. Creá una desde Tabla → ⇄ Mover → Orden de Carga.")
    else:
        # CSV
        oc_rows = [["N° OC","Remito","N° Pedido","Fecha","Campaña","Especie","Variedad","Tipo","Tratada","Cantidad","Kg","PG (%)","PMIL (g)","Lotes","Ubicaciones","Destino","Observaciones","Estado","Fecha Despacho"]]
        for o in oc_filt:
            lotes_s = "; ".join(l.get("lote","") for l in o.get("lotes",[]))
            ubics_s = "; ".join(l.get("ubicacion","") for l in o.get("lotes",[]))
            tc = sum(l.get("cantidad",0) for l in o.get("lotes",[]))
            oc_rows.append([o.get("numero",""), o.get("remito",""), o.get("nPedido",""),
                             o.get("fecha",""), o.get("campaña",""), o.get("especie",""),
                             o.get("variedad",""), "BigBag" if o.get("tipo")=="bigbag" else "Bolsa",
                             "Sí" if o.get("tratada") else "No", tc, tc*o.get("pesoUnit",0),
                             o.get("pg",""), o.get("pmil",""), lotes_s, ubics_s,
                             o.get("destino",""), o.get("obs",""),
                             "Pendiente" if o.get("estado")=="pendiente" else "Despachada",
                             o.get("fechaDespachada","")])
        st.download_button("⬇ Excel/CSV OCs", data=to_csv(oc_rows),
                           file_name=f"ordenes_{date.today()}.csv", mime="text/csv")

        df_oc = pd.DataFrame([{
            "N° OC":       o.get("numero",""),
            "Remito":      o.get("remito","—"),
            "N° Pedido":   o.get("nPedido","—"),
            "Fecha":       o.get("fecha",""),
            "Campaña":     o.get("campaña",""),
            "Especie":     o.get("especie",""),
            "Variedad":    o.get("variedad",""),
            "Tipo":        "BigBag" if o.get("tipo")=="bigbag" else "Bolsa",
            "Tratada":     "✅" if o.get("tratada") else "○",
            "Cant.":       sum(l.get("cantidad",0) for l in o.get("lotes",[])),
            "Kg":          f'{fmt(sum(l.get("cantidad",0) for l in o.get("lotes",[]))*o.get("pesoUnit",0))} kg',
            "PG %":        f'{o.get("pg","")}%' if o.get("pg") else "—",
            "Lotes":       ", ".join(l.get("lote","") for l in o.get("lotes",[])),
            "Destino":     o.get("destino","—"),
            "Obs.":        o.get("obs","—"),
            "Estado":      "⏳ Pendiente" if o.get("estado")=="pendiente" else "✓ Despachada",
            "F. Despacho": o.get("fechaDespachada","—"),
        } for o in oc_filt])
        st.dataframe(df_oc, use_container_width=True, hide_index=True, height=min(40+35*len(df_oc), 500))

        pend_n = sum(1 for o in oc_filt if o.get("estado")=="pendiente")
        desp_n = len(oc_filt) - pend_n
        kg_pend = sum(sum(l.get("cantidad",0) for l in o.get("lotes",[]))*o.get("pesoUnit",0)
                      for o in oc_filt if o.get("estado")=="pendiente")
        st.caption(f"Pendientes: **{pend_n}** &nbsp;·&nbsp; Despachadas: **{desp_n}** &nbsp;·&nbsp; Kg pendientes: **{fmt(kg_pend)} kg**")

        # Acciones OC
        st.markdown("**Acciones por OC:**")
        sel_oc_opt = st.selectbox(
            "Seleccionar OC",
            options=[(o.get("id"), f"{o.get('numero')} | {o.get('variedad')} | {o.get('destino','—')} | {o.get('estado','—')}") for o in oc_filt],
            format_func=lambda x: x[1],
            label_visibility="collapsed",
            key="sel_oc_id"
        )
        if sel_oc_opt:
            oc_id = sel_oc_opt[0]
            sel_oc = next((o for o in ordenes if o.get("id") == oc_id), None)
            if sel_oc:
                oa1, oa2, oa3 = st.columns(3)
                with oa1:
                    if sel_oc.get("estado") == "pendiente":
                        if st.button("✏ Editar OC", use_container_width=True):
                            st.session_state.modal = "editOC"
                            st.session_state.edit_oc = sel_oc
                            st.rerun()
                with oa2:
                    if sel_oc.get("estado") == "pendiente":
                        if st.button("✓ Despachar", use_container_width=True, type="primary"):
                            st.session_state.modal = "despachar"
                            st.session_state.edit_oc = sel_oc
                            st.rerun()
                with oa3:
                    if st.button("✕ Eliminar OC", use_container_width=True):
                        st.session_state.modal = "deleteOC"
                        st.session_state.edit_oc = sel_oc
                        st.rerun()

# ══════════════════════════════════════════════════════════════
# TAB 5 — CATÁLOGOS / ADMIN
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
            ea, cb = st.columns([4, 1])
            ea.write(e)
            if cb.button("✕", key=f"del_esp_{e}"):
                st.session_state.especies = [x for x in st.session_state.especies if x != e]
                st.session_state.varMap.pop(e, None)
                save_data(); st.rerun()
        new_e = st.text_input("Nueva especie", placeholder="Ej. Arveja", key="new_esp")
        if st.button("+ Agregar especie") and new_e.strip():
            if new_e.strip() not in st.session_state.especies:
                st.session_state.especies.append(new_e.strip())
                st.session_state.varMap[new_e.strip()] = []
                save_data(); st.rerun()

    st.markdown("---")
    st.markdown("**🌿 Variedades por Especie**")
    sel_e = st.selectbox("Seleccionar Especie para ver/gestionar variedades", st.session_state.especies, key="sel_esp_cat")
    if sel_e:
        vars_list = st.session_state.varMap.get(sel_e, [])
        for v in vars_list:
            v_col1, v_col2 = st.columns([4, 1])
            v_col1.write(v)
            if v_col2.button("✕", key=f"del_var_{sel_e}_{v}"):
                st.session_state.varMap[sel_e] = [x for x in vars_list if x != v]
                save_data(); st.rerun()
        new_v = st.text_input(f"Nueva variedad para {sel_e}", key="new_var_input", placeholder="Ej. Nidera 5009")
        if st.button("+ Agregar variedad") and new_v.strip():
            if new_v.strip() not in st.session_state.varMap[sel_e]:
                st.session_state.varMap[sel_e].append(new_v.strip())
                save_data(); st.rerun()

# ══════════════════════════════════════════════════════════════
# MOTORES DE ACCIÓN / MODALES
# ══════════════════════════════════════════════════════════════
if st.session_state.modal:
    st.markdown("---")
    m = st.session_state.modal

    if m == "new":
        st.markdown("<div class='section-title'>＋ Nuevo Registro de Stock</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        camp_in = c1.selectbox("Campaña *", st.session_state.campañas)
        esp_in = c2.selectbox("Especie *", st.session_state.especies)
        vars_disponibles = st.session_state.varMap.get(esp_in, [])
        var_in = c3.selectbox("Variedad *", vars_disponibles if vars_disponibles else ["—"])
        
        c4, c5, c6, c7 = st.columns(4)
        tipo_in = c4.selectbox("Tipo *", ["bigbag", "bolsa"])
        trat_in = c5.checkbox("¿Tratada?", value=False)
        cant_in = c6.number_input("Cantidad (Uds) *", min_value=0, value=0)
        peso_def = 800 if tipo_in == "bigbag" else 25
        peso_in = c7.number_input("Peso Unitario (kg) *", min_value=1, value=peso_def)
        
        c8, c9, c10 = st.columns(3)
        lote_in = c8.text_input("Lote *", placeholder="Ej. L-104")
        ubic_in = c9.text_input("Ubicación", placeholder="Ej. Celda A")
        f_in = c10.date_input("Fecha Ingreso", value=date.today())
        
        c11, c12 = st.columns(2)
        pg_in = c11.number_input("Poder Germinativo (%)", min_value=0, max_value=100, value=95)
        pmil_in = c12.number_input("Peso de Mil Granos (g)", min_value=0, value=150)
        obs_in = st.text_area("Observaciones")
        
        b1, b2 = st.columns(2)
        if b1.button("Guardar Registro", type="primary", use_container_width=True):
            if var_in == "—" or not lote_in.strip():
                st.error("Por favor completá los campos obligatorios (*).")
            else:
                new_item = {
                    "id": next_id(st.session_state.stock), "campaña": camp_in, "especie": esp_in,
                    "variedad": var_in, "tipo": tipo_in, "tratada": trat_in, "cantidad": int(cant_in),
                    "pesoUnit": int(peso_in), "lote": lote_in.strip(), "ubicacion": ubic_in.strip(),
                    "fecha": str(f_in), "pg": int(pg_in), "pmil": int(pmil_in), "obs": obs_in.strip()
                }
                st.session_state.stock.append(new_item)
                save_data(); st.session_state.modal = None; st.rerun()
        if b2.button("Cancelar", use_container_width=True):
            st.session_state.modal = None; st.rerun()

    elif m == "edit" and st.session_state.edit_item:
        item = st.session_state.edit_item
        st.markdown(f"<div class='section-title'>✏️ Editar Registro (ID: {item['id']})</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        camp_in = c1.selectbox("Campaña", st.session_state.campañas, index=st.session_state.campañas.index(item["campaña"]) if item["campaña"] in st.session_state.campañas else 0)
        esp_in = c2.selectbox("Especie", st.session_state.especies, index=st.session_state.especies.index(item["especie"]) if item["especie"] in st.session_state.especies else 0)
        vars_disponibles = st.session_state.varMap.get(esp_in, [])
        var_idx = vars_disponibles.index(item["variedad"]) if item["variedad"] in vars_disponibles else 0
        var_in = c3.selectbox("Variedad", vars_disponibles if vars_disponibles else ["—"], index=var_idx)
        
        c4, c5, c6, c7 = st.columns(4)
        tipo_in = c4.selectbox("Tipo", ["bigbag", "bolsa"], index=0 if item["tipo"]=="bigbag" else 1)
        trat_in = c5.checkbox("¿Tratada?", value=item["tratada"])
        cant_in = c6.number_input("Cantidad (Uds)", min_value=0, value=int(item["cantidad"]))
        peso_in = c7.number_input("Peso Unitario (kg)", min_value=1, value=int(item["pesoUnit"]))
        
        c8, c9, c10 = st.columns(3)
        lote_in = c8.text_input("Lote", value=item["lote"])
        ubic_in = c9.text_input("Ubicación", value=item["ubicacion"])
        try:
            val_f = datetime.strptime(item["fecha"], "%Y-%m-%d").date()
        except:
            val_f = date.today()
        f_in = c10.date_input("Fecha", value=val_f)
        
        c11, c12 = st.columns(2)
        pg_in = c11.number_input("PG (%)", min_value=0, max_value=100, value=int(item.get("pg", 95)))
        pmil_in = c12.number_input("PMIL (g)", min_value=0, value=int(item.get("pmil", 150)))
        obs_in = st.text_area("Observaciones", value=item["obs"])
        
        b1, b2 = st.columns(2)
        if b1.button("Actualizar Registro", type="primary", use_container_width=True):
            item.update({
                "campaña": camp_in, "especie": esp_in, "variedad": var_in, "tipo": tipo_in,
                "tratada": trat_in, "cantidad": int(cant_in), "pesoUnit": int(peso_in),
                "lote": lote_in, "ubicacion": ubic_in, "fecha": str(f_in), "pg": int(pg_in),
                "pmil": int(pmil_in), "obs": obs_in
            })
            save_data(); st.session_state.modal = None; st.rerun()
        if b2.button("Cancelar", use_container_width=True):
            st.session_state.modal = None; st.rerun()

    elif m == "delete" and st.session_state.edit_item:
        item = st.session_state.edit_item
        st.warning(f"⚠️ ¿Seguro que querés eliminar el lote **{item['lote']}** de **{item['variedad']}** ({item['campaña']})?")
        b1, b2 = st.columns(2)
        if b1.button("Sí, eliminar", type="primary", use_container_width=True):
            st.session_state.stock = [x for x in st.session_state.stock if x["id"] != item["id"]]
            save_data(); st.session_state.modal = None; st.rerun()
        if b2.button("Cancelar", use_container_width=True):
            st.session_state.modal = None; st.rerun()

    elif m == "move" and st.session_state.edit_item:
        item = st.session_state.edit_item
        st.markdown(f"<div class='section-title'>⇄ Gestión de Movimientos: {item['variedad']} (Lote: {item['lote']})</div>", unsafe_allow_html=True)
        acc_type = st.radio("Acción a realizar:", ["Ingreso Directo (Ajuste)", "Egreso Directo (Consumo/Baja)", "Generar Orden de Carga (Reserva)"])
        
        if acc_type in ["Ingreso Directo (Ajuste)", "Egreso Directo (Consumo/Baja)"]:
            c1, c2 = st.columns(2)
            qty_mov = c1.number_input("Cantidad de bultos (unidades)", min_value=1, value=1)
            rem_mov = c2.text_input("N° Remito Asociado")
            c3, c4 = st.columns(2)
            ped_mov = c3.text_input("N° Pedido Interno")
            mot_mov = c4.text_input("Motivo / Destino Interno")
            
            b1, b2 = st.columns(2)
            if b1.button("Confirmar Movimiento", type="primary", use_container_width=True):
                op = "ingreso" if "Ingreso" in acc_type else "egreso"
                old_qty = item["cantidad"]
                if op == "egreso" and qty_mov > old_qty:
                    st.error("Error: No podés egresar más de lo disponible en stock físico.")
                else:
                    item["cantidad"] = old_qty + qty_mov if op == "ingreso" else old_qty - qty_mov
                    st.session_state.historial.append({
                        "fecha": now_str(), "campaña": item["campaña"], "especie": item["especie"],
                        "variedad": item["variedad"], "tipo": item["tipo"], "lote": item["lote"],
                        "remito": rem_mov, "nPedido": ped_mov, "op": op, "delta": int(qty_mov),
                        "kgMovidos": int(qty_mov * item["pesoUnit"]), "stockPrev": old_qty,
                        "stockPost": item["cantidad"], "motivo": mot_mov
                    })
                    save_data(); st.session_state.modal = None; st.rerun()
            if b2.button("Cancelar", use_container_width=True):
                st.session_state.modal = None; st.rerun()
        else:
            c1, c2 = st.columns(2)
            qty_oc = c1.number_input("Cantidad para la Orden de Carga", min_value=1, max_value=int(item["cantidad"]), value=1)
            dest_oc = c2.text_input("Destino / Cliente Responsable")
            c3, c4 = st.columns(2)
            rem_oc = c3.text_input("Remito Previsto")
            ped_oc = c4.text_input("Pedido Vinculado")
            obs_oc = st.text_area("Observaciones de la Carga")
            
            b1, b2 = st.columns(2)
            if b1.button("Crear Orden de Carga Pendiente", type="primary", use_container_width=True):
                if not dest_oc.strip():
                    st.error("Debes ingresar un destino/cliente.")
                else:
                    oc_num = next_oc_num(st.session_state.ordenes)
                    st.session_state.ordenes.append({
                        "id": next_id(st.session_state.ordenes), "numero": fmt_oc(oc_num),
                        "remito": rem_oc, "nPedido": ped_oc, "fecha": now_str(),
                        "campaña": item["campaña"], "especie": item["especie"], "variedad": item["variedad"],
                        "tipo": item["tipo"], "pesoUnit": item["pesoUnit"], "pg": item.get("pg"), "pmil": item.get("pmil"),
                        "lotes": [{"lote": item["lote"], "ubicacion": item["ubicacion"], "cantidad": int(qty_oc), "stock_id": item["id"]}],
                        "destino": dest_oc, "obs": obs_oc, "estado": "pendiente", "fechaDespachada": ""
                    })
                    save_data(); st.session_state.modal = None; st.rerun()
            if b2.button("Cancelar", use_container_width=True):
                st.session_state.modal = None; st.rerun()

    elif m == "despachar" and st.session_state.edit_oc:
        oc = st.session_state.edit_oc
        st.markdown(f"<div class='section-title'>✓ Confirmar Despacho Físico: {oc['numero']}</div>", unsafe_allow_html=True)
        st.info(f"Se procesará el despacho de **{oc['variedad']}** con destino a **{oc['destino']}**.")
        
        b1, b2 = st.columns(2)
        if b1.button("Confirmar y Restar de Stock", type="primary", use_container_width=True):
            puede_despachar = True
            for l in oc.get("lotes", []):
                s_item = next((x for x in st.session_state.stock if x["id"] == l["stock_id"]), None)
                if not s_item or s_item["cantidad"] < l["cantidad"]:
                    puede_despachar = False
            
            if not puede_despachar:
                st.error("No se puede despachar: Stock físico insuficiente en los lotes asignados.")
            else:
                for l in oc.get("lotes", []):
                    s_item = next((x for x in st.session_state.stock if x["id"] == l["stock_id"]), None)
                    old_q = s_item["cantidad"]
                    s_item["cantidad"] -= l["cantidad"]
                    st.session_state.historial.append({
                        "fecha": now_str(), "campaña": oc["campaña"], "especie": oc["especie"],
                        "variedad": oc["variedad"], "tipo": oc["tipo"], "lote": l["lote"],
                        "remito": oc["remito"], "nPedido": oc["nPedido"], "op": "egreso",
                        "delta": l["cantidad"], "kgMovidos": l["cantidad"] * oc["pesoUnit"],
                        "stockPrev": old_q, "stockPost": s_item["cantidad"],
                        "motivo": f"Despacho {oc['numero']} -> {oc['destino']}"
                    })
                oc["estado"] = "despachada"
                oc["fechaDespachada"] = now_str()
                save_data()
                st.session_state.wa_pending = oc
                st.session_state.modal = None
                st.rerun()
        if b2.button("Cancelar", use_container_width=True):
            st.session_state.modal = None; st.rerun()

    elif m == "deleteOC" and st.session_state.edit_oc:
        oc = st.session_state.edit_oc
        st.warning(f"⚠️ ¿Seguro que querés eliminar permanentemente la orden **{oc['numero']}**?")
        b1, b2 = st.columns(2)
        if b1.button("Sí, eliminar orden", type="primary", use_container_width=True):
            st.session_state.ordenes = [x for x in st.session_state.ordenes if x["id"] != oc["id"]]
            save_data(); st.session_state.modal = None; st.rerun()
        if b2.button("Cancelar", use_container_width=True):
            st.session_state.modal = None; st.rerun()

# ══════════════════════════════════════════════════════════════
# VENTANA DE NOTIFICACIÓN WHATSAPP EMITIDA
# ══════════════════════════════════════════════════════════════
if "wa_pending" in st.session_state and st.session_state.wa_pending:
    wa_oc = st.session_state.wa_pending
    st.markdown("---")
    st.success(f"🎉 ¡Orden de Carga {wa_oc['numero']} despachada físicamente con éxito!")
    
    tot_cant_oc = sum(l.get("cantidad", 0) for l in wa_oc.get("lotes", []))
    w_msg = (
        f"🌱 *La Clementina · Planta de Semillas*\n"
        f"📦 *Orden de Carga Despachada: {wa_oc['numero']}*\n\n"
        f"🔹 *Especie:* {wa_oc['especie']}\n"
        f"🔹 *Variedad:* {wa_oc['variedad']}\n"
        f"🔹 *Tipo:* {wa_oc['tipo'].upper()}\n"
        f"🔹 *Cantidad:* {tot_cant_oc} bultos\n"
        f"⚖️ *Peso Neto:* {fmt(tot_cant_oc * wa_oc['pesoUnit'])} kg\n"
        f"📍 *Destino:* {wa_oc.get('destino','—')}\n"
        f"📄 *Remito:* {wa_oc.get('remito','—')} | *Pedido:* {wa_oc.get('nPedido','—')}\n"
        f"📅 *Despacho:* {wa_oc['fechaDespachada']}\n\n"
        f"¡Buen viaje! 🚛"
    )
    import urllib.parse
    wa_url = f"https://wa.me/?text={urllib.parse.quote(w_msg)}"
    
    st.link_button("📲 Enviar Comprobante por WhatsApp", wa_url, type="primary", use_container_width=True)
    if st.button("Cerrar panel de notificación", use_container_width=True):
        st.session_state.wa_pending = None
        st.rerun()

# ─── PIE DE PÁGINA ────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #6b7280; font-size: 0.8rem; padding: 10px 0 20px;'>"
    "La Clementina · Sistema de Gestión de Stock · Creado por Ignacio Diaz"
    "</div>", 
    unsafe_allow_html=True
)
