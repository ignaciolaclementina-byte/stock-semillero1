"""
La Clementina · Stock Semillas
App de gestión de stock de semillas para Streamlit
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime, date
import io

# ──────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="La Clementina · Stock Semillas",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────
# DATOS POR DEFECTO
# ──────────────────────────────────────────────
DEFAULT_PASS = "semillas2025"

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

LOW = 5  # umbral stock bajo

# ──────────────────────────────────────────────
# ESTILOS CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
  /* Header personalizado */
  .app-header {
    background: linear-gradient(135deg,#1a2a4a 60%,#1e3660);
    border-bottom: 3px solid #e07b00;
    padding: 16px 24px;
    border-radius: 10px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .app-header h1 {
    color: #fff;
    font-size: 1.6rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 0;
  }
  .app-header h1 span { color: #f5a623; }
  .app-header p { color: rgba(255,255,255,.55); font-size: .75rem; margin: 2px 0 0 0; }

  /* KPI cards */
  .kpi-card {
    background: #fff;
    border: 1px solid #dde1ea;
    border-radius: 10px;
    padding: 14px 18px;
    text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,.08);
  }
  .kpi-val { font-size: 2rem; font-weight: 800; line-height: 1; }
  .kpi-lbl { font-size: .65rem; color: #6b7280; text-transform: uppercase; letter-spacing: .7px; margin-top: 4px; }
  .kpi-or  { color: #e07b00; }
  .kpi-bl  { color: #1a7abf; }
  .kpi-gr  { color: #2e8b57; }
  .kpi-pu  { color: #7b4fa6; }
  .kpi-rd  { color: #c0392b; }

  /* Badges */
  .badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: .72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .4px;
  }
  .badge-tratada  { background:#e6f5ec; color:#2e8b57; border:1px solid #7dc99a; }
  .badge-notratar { background:#f3f4f6; color:#6b7280; border:1px solid #d1d5db; }
  .badge-bigbag   { background:#fff4e0; color:#b86000; border:1px solid #f5c57a; }
  .badge-bolsa    { background:#e6f4fb; color:#1a7abf; border:1px solid #90cae8; }
  .badge-low      { background:#fde8e8; color:#c0392b; border:1px solid #f5a5a5; }
  .badge-pend     { background:#fef9ee; color:#92600a; border:1px solid #f5c57a; }
  .badge-desp     { background:#e6f5ec; color:#2e8b57; border:1px solid #7dc99a; }
  .badge-egreso   { background:#fde8e8; color:#c0392b; border:1px solid #f5a5a5; }
  .badge-ingreso  { background:#e6f5ec; color:#2e8b57; border:1px solid #7dc99a; }

  /* Sección de título */
  .section-title {
    font-size: 1.1rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: #1a2a4a;
    border-bottom: 2px solid #e07b00;
    padding-bottom: 6px;
    margin-bottom: 14px;
  }

  /* Ajuste de tabla */
  div[data-testid="stDataFrame"] { border-radius: 8px; overflow: hidden; }

  /* Botones Streamlit */
  .stButton > button {
    border-radius: 8px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .4px;
    font-size: .82rem;
  }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────
def fmt(n):
    try:
        return f"{float(n):,.0f}".replace(",", ".")
    except Exception:
        return str(n)

def now_str():
    return datetime.now().strftime("%d/%m/%Y %H:%M")

def fmt_oc(n):
    return f"OC-{str(n).zfill(3)}"

def next_id(lst):
    return max((i["id"] for i in lst), default=0) + 1

def kg_total(item):
    return item["cantidad"] * item["pesoUnit"]

def peso_label(tipo):
    return "BigBags" if tipo == "bigbag" else "Bolsas"


# ──────────────────────────────────────────────
# SESSION STATE – inicialización
# ──────────────────────────────────────────────
def ss_init():
    defaults = {
        "logged_in":  False,
        "stock":      [dict(i) for i in STOCK_INIT],
        "historial":  [],
        "ordenes":    [],
        "campañas":   list(CAMPAÑAS_DEF),
        "especies":   list(ESPECIES_DEF),
        "var_map":    {k: list(v) for k, v in VARS_DEF.items()},
        "password":   DEFAULT_PASS,
        "tab":        "Resumen",
        # filtros tabla
        "f_camp": "Todas",
        "f_esp":  "Todas",
        "f_tipo": "Todos",
        "f_trat": "Todos",
        "f_search": "",
        # filtros historial
        "h_camp": "Todas",
        "h_op":   "Todos",
        # filtros OC
        "oc_camp":   "Todas",
        "oc_status": "Todos",
        "oc_search": "",
        # filtros resumen
        "r_camp": "Todas",
        "r_esp":  "Todas",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

ss_init()


# ──────────────────────────────────────────────
# LOGIN
# ──────────────────────────────────────────────
def render_login():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='background:linear-gradient(135deg,#1a2a4a,#1e3660);
                    border-radius:16px;padding:36px 40px;text-align:center;
                    box-shadow:0 8px 40px rgba(0,0,0,.25)'>
          <h2 style='color:#fff;font-weight:800;text-transform:uppercase;
                     letter-spacing:1px;margin-bottom:6px'>
            🌱 Planta de Semillas
          </h2>
          <p style='color:rgba(255,255,255,.55);font-size:.85rem;margin-bottom:0'>
            La Clementina · Stock Semillas
          </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        pw = st.text_input("Clave de acceso", type="password",
                           placeholder="••••••••", label_visibility="collapsed")
        if st.button("Ingresar →", use_container_width=True, type="primary"):
            if pw == st.session_state["password"]:
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("Clave incorrecta. Intentá de nuevo.")


# ──────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────
def render_header():
    st.markdown("""
    <div class='app-header'>
      <div>
        <h1>🌱 La <span>Clementina</span></h1>
        <p>Sistema de gestión de stock de semillas</p>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# KPIs
# ──────────────────────────────────────────────
def render_kpis(stock):
    total_items = len(stock)
    total_kg = sum(kg_total(i) for i in stock)
    stock_bajo = sum(1 for i in stock if i["cantidad"] <= LOW)
    total_oc_pend = sum(1 for o in st.session_state["ordenes"] if o["estado"] == "pendiente")
    especies_u = len({i["especie"] for i in stock})

    cols = st.columns(5)
    data = [
        (total_items,       "Registros",      "kpi-or"),
        (f"{fmt(total_kg)} kg", "Kg Totales", "kpi-bl"),
        (especies_u,        "Especies",        "kpi-gr"),
        (stock_bajo,        "Stock Bajo",      "kpi-rd"),
        (total_oc_pend,     "OC Pendientes",   "kpi-pu"),
    ]
    for col, (val, lbl, cls) in zip(cols, data):
        with col:
            st.markdown(f"""
            <div class='kpi-card'>
              <div class='kpi-val {cls}'>{val}</div>
              <div class='kpi-lbl'>{lbl}</div>
            </div>
            """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# TAB: RESUMEN
# ──────────────────────────────────────────────
def render_resumen():
    stock = st.session_state["stock"]
    campañas = ["Todas"] + st.session_state["campañas"]
    especies = ["Todas"] + st.session_state["especies"]

    st.markdown("<div class='section-title'>📋 Resumen de Stock por Variedad</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        r_camp = st.selectbox("Campaña", campañas, key="r_camp")
    with col2:
        r_esp = st.selectbox("Especie", especies, key="r_esp")

    filtered = [
        i for i in stock
        if (r_camp == "Todas" or i["campaña"] == r_camp)
        and (r_esp == "Todas" or i["especie"] == r_esp)
    ]

    if not filtered:
        st.info("Sin registros para los filtros seleccionados.")
        return

    # Agrupar por campaña → especie → variedad
    from collections import defaultdict
    tree = defaultdict(lambda: defaultdict(list))
    for i in filtered:
        tree[i["campaña"]][i["especie"]].append(i)

    for camp, esp_dict in sorted(tree.items()):
        st.markdown(f"<div style='font-size:1.15rem;font-weight:800;text-transform:uppercase;"
                    f"letter-spacing:1.2px;color:#1a2a4a;border-bottom:2px solid #e07b00;"
                    f"padding-bottom:5px;margin:18px 0 10px'>🌾 {camp}</div>", unsafe_allow_html=True)
        for esp, items in sorted(esp_dict.items()):
            st.markdown(f"<div style='font-size:.9rem;font-weight:700;text-transform:uppercase;"
                        f"color:#1a7abf;border-left:3px solid #1a7abf;padding-left:9px;"
                        f"margin-bottom:8px'>{esp}</div>", unsafe_allow_html=True)

            # agrupar por variedad
            var_dict = defaultdict(list)
            for i in items:
                var_dict[i["variedad"]].append(i)

            cards = []
            for var, vitems in sorted(var_dict.items()):
                cant_bb  = sum(v["cantidad"] for v in vitems if v["tipo"] == "bigbag")
                cant_bo  = sum(v["cantidad"] for v in vitems if v["tipo"] == "bolsa")
                kg_t     = sum(kg_total(v) for v in vitems)
                tratadas = sum(v["cantidad"] for v in vitems if v["tratada"])
                cards.append((var, cant_bb, cant_bo, kg_t, tratadas))

            cols = st.columns(min(len(cards), 3))
            for col, (var, bb, bo, kg_t, trat) in zip(cols, cards):
                with col:
                    st.markdown(f"""
                    <div style='background:#fff;border:1px solid #dde1ea;border-radius:10px;
                                padding:12px 14px;border-top:3px solid #e07b00;
                                box-shadow:0 1px 4px rgba(0,0,0,.08);margin-bottom:8px'>
                      <div style='font-weight:800;text-transform:uppercase;color:#1a2a4a;
                                  font-size:.92rem;margin-bottom:8px'>{var}</div>
                      <div style='display:flex;justify-content:space-between;padding:3px 0;
                                  border-bottom:1px solid #edf0f5'>
                        <span style='font-size:.68rem;color:#6b7280;text-transform:uppercase'>BigBags</span>
                        <b>{fmt(bb)}</b>
                      </div>
                      <div style='display:flex;justify-content:space-between;padding:3px 0;
                                  border-bottom:1px solid #edf0f5'>
                        <span style='font-size:.68rem;color:#6b7280;text-transform:uppercase'>Bolsas</span>
                        <b>{fmt(bo)}</b>
                      </div>
                      <div style='display:flex;justify-content:space-between;padding:3px 0;
                                  border-bottom:1px solid #edf0f5'>
                        <span style='font-size:.68rem;color:#6b7280;text-transform:uppercase'>Kg Totales</span>
                        <b>{fmt(kg_t)} kg</b>
                      </div>
                      <div style='display:flex;justify-content:space-between;padding:3px 0'>
                        <span style='font-size:.68rem;color:#6b7280;text-transform:uppercase'>Tratadas</span>
                        <b>{fmt(trat)}</b>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# TAB: TABLA DE STOCK
# ──────────────────────────────────────────────
def render_tabla():
    stock = st.session_state["stock"]
    campañas = ["Todas"] + st.session_state["campañas"]
    especies  = ["Todas"] + st.session_state["especies"]

    st.markdown("<div class='section-title'>📦 Tabla de Stock</div>", unsafe_allow_html=True)

    # Filtros
    c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 1])
    with c1:
        busq = st.text_input("🔍 Buscar variedad, lote, obs…", key="f_search", label_visibility="collapsed",
                             placeholder="🔍 Buscar variedad, lote, obs…")
    with c2:
        f_camp = st.selectbox("Campaña", campañas, key="f_camp", label_visibility="collapsed")
    with c3:
        f_esp = st.selectbox("Especie", especies, key="f_esp", label_visibility="collapsed")
    with c4:
        f_tipo = st.selectbox("Tipo", ["Todos", "BigBag", "Bolsa"], key="f_tipo", label_visibility="collapsed")
    with c5:
        f_trat = st.selectbox("Tratamiento", ["Todos", "Tratada", "Sin tratar"], key="f_trat", label_visibility="collapsed")

    def filtrar(i):
        if f_camp != "Todas" and i["campaña"] != f_camp: return False
        if f_esp  != "Todas" and i["especie"]  != f_esp:  return False
        if f_tipo != "Todos":
            t = "bigbag" if f_tipo == "BigBag" else "bolsa"
            if i["tipo"] != t: return False
        if f_trat != "Todos":
            s = (f_trat == "Tratada")
            if i["tratada"] != s: return False
        if busq:
            hay = " ".join([str(i.get(k,"")) for k in ["variedad","especie","lote","campaña","obs","ubicacion"]]).lower()
            if busq.lower() not in hay: return False
        return True

    filtrado = [i for i in stock if filtrar(i)]

    # Botón nuevo ingreso
    col_add, col_exp = st.columns([1, 5])
    with col_add:
        if st.button("➕ Nuevo ingreso", type="primary"):
            st.session_state["modal"] = "new"
    with col_exp:
        if st.button("📥 Exportar CSV"):
            rows = [["Campaña","Especie","Variedad","Tipo","Tratada","Cantidad",
                     "Kg Totales","PG (%)","PMIL (g)","Lote","Ubicación","Fecha","Observaciones"]]
            for i in filtrado:
                rows.append([i["campaña"],i["especie"],i["variedad"],
                             "BigBag" if i["tipo"]=="bigbag" else "Bolsa",
                             "Sí" if i["tratada"] else "No",
                             i["cantidad"], kg_total(i), i.get("pg",""),
                             i.get("pmil",""), i["lote"], i.get("ubicacion",""),
                             i["fecha"], i.get("obs","")])
            df_exp = pd.DataFrame(rows[1:], columns=rows[0])
            csv = df_exp.to_csv(index=False, sep=";").encode("utf-8-sig")
            st.download_button("⬇ Descargar", csv, "stock_semillas.csv", "text/csv")

    st.markdown("<br>", unsafe_allow_html=True)

    if not filtrado:
        st.info("Sin registros para los filtros seleccionados.")
    else:
        # Mostrar tabla editable
        for i in filtrado:
            bajo = i["cantidad"] <= LOW
            color = "#fff5f5" if bajo else "#fff"
            tipo_lbl = "BigBag" if i["tipo"] == "bigbag" else "Bolsa"
            trat_badge = ("<span class='badge badge-tratada'>✓ Tratada</span>"
                          if i["tratada"]
                          else "<span class='badge badge-notratar'>Sin tratar</span>")
            tipo_badge = (f"<span class='badge badge-bigbag'>{tipo_lbl}</span>"
                          if i["tipo"] == "bigbag"
                          else f"<span class='badge badge-bolsa'>{tipo_lbl}</span>")
            bajo_badge = "<span class='badge badge-low'>⚠ Bajo</span>" if bajo else ""

            with st.container():
                cols = st.columns([1.5, 1.5, 1, 1, 1, 1.2, 0.8, 0.8, 0.8, 0.8])
                cols[0].markdown(f"<b style='color:#1a2a4a'>{i['variedad']}</b><br>"
                                 f"<span style='font-size:.75rem;color:#6b7280'>{i['especie']} · {i['campaña']}</span>",
                                 unsafe_allow_html=True)
                cols[1].markdown(f"{tipo_badge} {trat_badge}", unsafe_allow_html=True)
                cols[2].markdown(f"<b style='font-size:1.1rem'>{fmt(i['cantidad'])}</b> "
                                 f"<span style='font-size:.72rem;color:#6b7280'>{peso_label(i['tipo'])}</span> "
                                 f"{bajo_badge}", unsafe_allow_html=True)
                cols[3].markdown(f"<span style='font-size:.78rem;color:#6b7280'>Kg totales</span><br>"
                                 f"<b>{fmt(kg_total(i))} kg</b>", unsafe_allow_html=True)
                cols[4].markdown(f"<span style='font-size:.78rem;color:#6b7280'>Lote</span><br>"
                                 f"{i.get('lote','—')}", unsafe_allow_html=True)
                cols[5].markdown(f"<span style='font-size:.78rem;color:#6b7280'>PG: {i.get('pg','—')}% · PMIL: {i.get('pmil','—')}g</span><br>"
                                 f"<span style='font-size:.75rem;color:#6b7280'>{i.get('fecha','')}</span>",
                                 unsafe_allow_html=True)
                with cols[6]:
                    if st.button("✏ Editar", key=f"edit_{i['id']}"):
                        st.session_state["modal"] = "edit"
                        st.session_state["modal_item"] = dict(i)
                with cols[7]:
                    if st.button("⇄ Mover", key=f"move_{i['id']}"):
                        st.session_state["modal"] = "move"
                        st.session_state["modal_item"] = dict(i)
                with cols[8]:
                    if st.button("📋 OC", key=f"oc_{i['id']}"):
                        st.session_state["modal"] = "oc"
                        st.session_state["modal_item"] = dict(i)
                with cols[9]:
                    if st.button("🗑", key=f"del_{i['id']}"):
                        st.session_state["confirm_del"] = i["id"]

            st.markdown(f"<hr style='margin:4px 0;border:none;border-top:1px solid #edf0f5'>",
                        unsafe_allow_html=True)

    # Confirmar eliminación
    if st.session_state.get("confirm_del"):
        cid = st.session_state["confirm_del"]
        item_del = next((x for x in stock if x["id"] == cid), None)
        if item_del:
            st.warning(f"⚠ ¿Eliminar registro **{item_del['variedad']}** (Lote {item_del.get('lote','—')})? Esta acción no se puede deshacer.")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Sí, eliminar", type="primary"):
                    st.session_state["stock"] = [x for x in stock if x["id"] != cid]
                    del st.session_state["confirm_del"]
                    st.rerun()
            with c2:
                if st.button("❌ Cancelar"):
                    del st.session_state["confirm_del"]
                    st.rerun()

    # Modals
    render_modals()


# ──────────────────────────────────────────────
# MODALS (formularios en expanders)
# ──────────────────────────────────────────────
def render_modals():
    modal = st.session_state.get("modal")
    if not modal:
        return

    campañas = st.session_state["campañas"]
    especies  = st.session_state["especies"]
    var_map   = st.session_state["var_map"]
    item = st.session_state.get("modal_item", {})

    # ── NUEVO / EDITAR ──
    if modal in ("new", "edit"):
        titulo = "Editar Registro" if modal == "edit" else "Nuevo Ingreso"
        st.subheader(titulo)
        with st.form("form_stock"):
            c1, c2 = st.columns(2)
            with c1:
                camp_sel = st.selectbox("Campaña *", campañas,
                    index=campañas.index(item.get("campaña", campañas[0])) if item.get("campaña") in campañas else 0)
            with c2:
                esp_sel = st.selectbox("Especie *", especies,
                    index=especies.index(item.get("especie", especies[0])) if item.get("especie") in especies else 0)

            vars_disp = var_map.get(esp_sel, [])
            var_sel = st.selectbox("Variedad *", vars_disp,
                index=vars_disp.index(item.get("variedad")) if item.get("variedad") in vars_disp else 0)

            c3, c4 = st.columns(2)
            with c3:
                tipo_opts = ["bigbag", "bolsa"]
                tipo_labels = ["BigBag", "Bolsa"]
                tipo_idx = tipo_opts.index(item.get("tipo", "bigbag"))
                tipo_sel_lbl = st.selectbox("Tipo de envase", tipo_labels, index=tipo_idx)
                tipo_sel = tipo_opts[tipo_labels.index(tipo_sel_lbl)]
            with c4:
                trat_sel = st.selectbox("Tratamiento", ["Sin tratar", "Tratada"],
                    index=1 if item.get("tratada") else 0)

            default_peso = item.get("pesoUnit", 800 if tipo_sel == "bigbag" else 25)
            c5, c6 = st.columns(2)
            with c5:
                cant_sel = st.number_input(f"Cantidad ({tipo_labels[tipo_opts.index(tipo_sel)]}) *",
                    min_value=0.0, step=0.5, value=float(item.get("cantidad", 0)))
            with c6:
                peso_sel = st.number_input("Peso unitario (kg)", min_value=1.0, step=1.0,
                    value=float(default_peso))

            c7, c8 = st.columns(2)
            with c7:
                pg_sel = st.number_input("PG – Poder Germinativo (%)", 0.0, 100.0, step=0.1,
                    value=float(item.get("pg", 0) or 0))
            with c8:
                pmil_sel = st.number_input("PMIL – Peso mil semillas (g)", 0.0, step=0.1,
                    value=float(item.get("pmil", 0) or 0))

            c9, c10 = st.columns(2)
            with c9:
                lote_sel = st.text_input("Lote", value=item.get("lote", ""), placeholder="Ej. L-001")
            with c10:
                ubic_sel = st.text_input("Ubicación", value=item.get("ubicacion", ""), placeholder="Ej. A-12")

            fecha_sel = st.date_input("Fecha", value=date.fromisoformat(item.get("fecha", date.today().isoformat())))
            obs_sel = st.text_area("Observaciones", value=item.get("obs", ""), height=60)

            submitted = st.form_submit_button("💾 Guardar", type="primary")
            cancelled = st.form_submit_button("Cancelar")

        if cancelled:
            st.session_state.pop("modal", None)
            st.session_state.pop("modal_item", None)
            st.rerun()

        if submitted:
            if not camp_sel or not esp_sel or not var_sel or cant_sel <= 0:
                st.error("Completá campaña, especie, variedad y cantidad.")
            else:
                new_item = {
                    "id":       item.get("id", next_id(st.session_state["stock"])),
                    "campaña":  camp_sel,
                    "especie":  esp_sel,
                    "variedad": var_sel,
                    "tipo":     tipo_sel,
                    "tratada":  trat_sel == "Tratada",
                    "cantidad": cant_sel,
                    "pesoUnit": peso_sel,
                    "pg":       pg_sel,
                    "pmil":     pmil_sel,
                    "lote":     lote_sel,
                    "ubicacion": ubic_sel,
                    "fecha":    fecha_sel.isoformat(),
                    "obs":      obs_sel,
                }
                if modal == "edit":
                    st.session_state["stock"] = [
                        new_item if x["id"] == new_item["id"] else x
                        for x in st.session_state["stock"]
                    ]
                else:
                    st.session_state["stock"].insert(0, new_item)
                st.session_state.pop("modal", None)
                st.session_state.pop("modal_item", None)
                st.success("✅ Guardado correctamente.")
                st.rerun()

    # ── MOVIMIENTO ──
    elif modal == "move":
        st.subheader(f"⇄ Mover Stock — {item.get('variedad', '')}")
        st.markdown(f"**Campaña:** {item.get('campaña','')} · **Especie:** {item.get('especie','')} · "
                    f"**Lote:** {item.get('lote','—')} · **Stock actual:** {fmt(item.get('cantidad',0))} "
                    f"{peso_label(item.get('tipo','bolsa'))}")

        with st.form("form_move"):
            op = st.selectbox("Operación", ["Egreso", "Ingreso"])
            delta = st.number_input("Cantidad a mover", min_value=0.0, step=0.5, value=0.0)
            motivo = st.text_input("Motivo / Remito", placeholder="Ej. Venta, Ajuste, Devolución…")

            nueva = item["cantidad"] - delta if op == "Egreso" else item["cantidad"] + delta
            if delta > 0:
                color_prev = "red" if nueva < 0 else ("orange" if nueva <= LOW else "green")
                st.markdown(f"**Stock resultante:** <span style='color:{color_prev};font-weight:800'>"
                            f"{fmt(nueva)} {peso_label(item.get('tipo','bolsa'))}</span>",
                            unsafe_allow_html=True)

            sub = st.form_submit_button("✅ Confirmar movimiento", type="primary")
            canc = st.form_submit_button("Cancelar")

        if canc:
            st.session_state.pop("modal", None)
            st.session_state.pop("modal_item", None)
            st.rerun()
        if sub:
            if delta <= 0:
                st.error("Ingresá una cantidad válida.")
            elif nueva < 0:
                st.error("El stock no puede quedar negativo.")
            else:
                op_key = "egreso" if op == "Egreso" else "ingreso"
                # actualizar stock
                st.session_state["stock"] = [
                    {**x, "cantidad": nueva} if x["id"] == item["id"] else x
                    for x in st.session_state["stock"]
                ]
                # registrar historial
                h_item = {
                    "id":        next_id(st.session_state["historial"]),
                    "fecha":     now_str(),
                    "campaña":   item["campaña"],
                    "especie":   item["especie"],
                    "variedad":  item["variedad"],
                    "tipo":      item["tipo"],
                    "tratada":   item["tratada"],
                    "lote":      item["lote"],
                    "op":        op_key,
                    "delta":     delta,
                    "stockPrev": item["cantidad"],
                    "stockPost": nueva,
                    "kgMovidos": delta * item["pesoUnit"],
                    "motivo":    motivo,
                }
                st.session_state["historial"].insert(0, h_item)
                st.session_state.pop("modal", None)
                st.session_state.pop("modal_item", None)
                st.success("✅ Movimiento registrado.")
                st.rerun()

    # ── ORDEN DE CARGA ──
    elif modal == "oc":
        st.subheader(f"📋 Nueva Orden de Carga — {item.get('variedad', '')}")
        st.markdown(f"**Campaña:** {item.get('campaña','')} · **Especie:** {item.get('especie','')} · "
                    f"**Lote:** {item.get('lote','—')} · **Stock disponible:** {fmt(item.get('cantidad',0))} "
                    f"{peso_label(item.get('tipo','bolsa'))}")

        with st.form("form_oc"):
            c1, c2 = st.columns(2)
            with c1:
                remito = st.text_input("N° Remito", placeholder="Ej. R-0001")
            with c2:
                n_pedido = st.text_input("N° Pedido", placeholder="Ej. P-2025-01")

            destino = st.text_input("Destino / Campo", placeholder="Ej. Campo La Esperanza")
            cant_oc = st.number_input("Cantidad a cargar", min_value=0.0, step=0.5, max_value=float(item.get("cantidad", 0)))
            obs_oc  = st.text_area("Observaciones", height=60)

            sub = st.form_submit_button("📋 Crear Orden de Carga", type="primary")
            canc = st.form_submit_button("Cancelar")

        if canc:
            st.session_state.pop("modal", None)
            st.session_state.pop("modal_item", None)
            st.rerun()
        if sub:
            if cant_oc <= 0:
                st.error("Ingresá una cantidad válida.")
            else:
                oc_id = next_id(st.session_state["ordenes"])
                oc_num_n = max((int(o["numero"].replace("OC-", "")) for o in st.session_state["ordenes"]), default=0) + 1
                lote_entry = {
                    "lote": item["lote"], "ubicacion": item.get("ubicacion", ""),
                    "cantidad": cant_oc, "stockId": item["id"]
                }
                nueva_oc = {
                    "id": oc_id, "numero": fmt_oc(oc_num_n), "fecha": now_str(),
                    "campaña": item["campaña"], "especie": item["especie"],
                    "variedad": item["variedad"], "tipo": item["tipo"],
                    "tratada": item["tratada"], "pesoUnit": item["pesoUnit"],
                    "pg": item.get("pg", ""), "pmil": item.get("pmil", ""),
                    "lotes": [lote_entry],
                    "destino": destino, "obs": obs_oc, "remito": remito,
                    "nPedido": n_pedido, "estado": "pendiente",
                    "fechaDespachada": None, "stockId": item["id"],
                }
                st.session_state["ordenes"].append(nueva_oc)
                st.session_state.pop("modal", None)
                st.session_state.pop("modal_item", None)
                st.success(f"✅ Orden {fmt_oc(oc_num_n)} creada.")
                st.session_state["tab"] = "Órdenes de Carga"
                st.rerun()


# ──────────────────────────────────────────────
# TAB: HISTORIAL
# ──────────────────────────────────────────────
def render_historial():
    historial = st.session_state["historial"]
    campañas = ["Todas"] + st.session_state["campañas"]

    st.markdown("<div class='section-title'>📜 Historial de Movimientos</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        h_camp = st.selectbox("Campaña", campañas, key="h_camp")
    with c2:
        h_op = st.selectbox("Operación", ["Todos", "Ingreso", "Egreso"], key="h_op")

    filtrado = [
        h for h in historial
        if (h_camp == "Todas" or h.get("campaña") == h_camp)
        and (h_op == "Todos" or h.get("op", "").lower() == h_op.lower())
    ]

    if st.button("📥 Exportar historial CSV"):
        rows = [["Fecha","Campaña","Especie","Variedad","Tipo","Lote","Operación",
                 "Cantidad","Kg Movidos","Stock Anterior","Stock Nuevo","Motivo"]]
        for h in filtrado:
            rows.append([h.get("fecha",""), h.get("campaña",""), h.get("especie",""),
                         h.get("variedad",""), h.get("tipo",""), h.get("lote",""),
                         h.get("op",""), h.get("delta",""), h.get("kgMovidos",""),
                         h.get("stockPrev",""), h.get("stockPost",""), h.get("motivo","")])
        df_exp = pd.DataFrame(rows[1:], columns=rows[0])
        csv = df_exp.to_csv(index=False, sep=";").encode("utf-8-sig")
        st.download_button("⬇ Descargar", csv, "historial_semillas.csv", "text/csv")

    st.markdown("<br>", unsafe_allow_html=True)

    if not filtrado:
        st.info("Sin movimientos para los filtros seleccionados. Usá ⇄ Mover en la Tabla para registrar movimientos.")
    else:
        for h in filtrado:
            is_ingreso = h.get("op") == "ingreso"
            op_badge = ("<span class='badge badge-ingreso'>↑ Ingreso</span>"
                        if is_ingreso
                        else "<span class='badge badge-egreso'>↓ Egreso</span>")
            delta_str = (f"<span style='color:#2e8b57;font-weight:800'>+{fmt(h.get('delta',0))}</span>"
                         if is_ingreso
                         else f"<span style='color:#c0392b;font-weight:800'>-{fmt(h.get('delta',0))}</span>")
            cols = st.columns([1.5, 1.5, 0.8, 1, 1, 1, 1.2])
            cols[0].markdown(f"<small style='color:#6b7280'>{h.get('fecha','')}</small><br>"
                             f"<b>{h.get('variedad','')}</b>", unsafe_allow_html=True)
            cols[1].markdown(f"{h.get('especie','')} · {h.get('campaña','')}<br>"
                             f"<small style='color:#6b7280'>Lote: {h.get('lote','—')}</small>",
                             unsafe_allow_html=True)
            cols[2].markdown(op_badge, unsafe_allow_html=True)
            cols[3].markdown(f"<b>Movido:</b> {delta_str} unid.", unsafe_allow_html=True)
            cols[4].markdown(f"<b>Kg:</b> {fmt(h.get('kgMovidos',0))} kg", unsafe_allow_html=True)
            cols[5].markdown(f"<small>{fmt(h.get('stockPrev',0))} → <b>{fmt(h.get('stockPost',0))}</b></small>",
                             unsafe_allow_html=True)
            cols[6].markdown(f"<small style='color:#6b7280'>{h.get('motivo','—')}</small>",
                             unsafe_allow_html=True)
            st.markdown("<hr style='margin:4px 0;border:none;border-top:1px solid #edf0f5'>",
                        unsafe_allow_html=True)


# ──────────────────────────────────────────────
# TAB: ÓRDENES DE CARGA
# ──────────────────────────────────────────────
def render_ordenes():
    ordenes = st.session_state["ordenes"]
    campañas = ["Todas"] + st.session_state["campañas"]

    st.markdown("<div class='section-title'>📋 Órdenes de Carga</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        oc_camp = st.selectbox("Campaña", campañas, key="oc_camp")
    with c2:
        oc_status = st.selectbox("Estado", ["Todos", "Pendiente", "Despachada"], key="oc_status")
    with c3:
        oc_search = st.text_input("🔍 Buscar OC, variedad…", key="oc_search",
                                  label_visibility="collapsed", placeholder="🔍 Buscar OC, variedad…")

    def filtrar_oc(o):
        if oc_camp != "Todas" and o.get("campaña") != oc_camp: return False
        if oc_status != "Todos" and o.get("estado","").lower() != oc_status.lower(): return False
        if oc_search:
            hay = " ".join([str(o.get(k,"")) for k in ["numero","variedad","especie","destino","remito","nPedido","obs"]]).lower()
            if oc_search.lower() not in hay: return False
        return True

    filtrado = [o for o in ordenes if filtrar_oc(o)]

    if st.button("📥 Exportar OC CSV"):
        rows = [["N° OC","Remito","N° Pedido","Fecha","Campaña","Especie","Variedad",
                 "Tipo","Tratada","Cantidad total","Kg","PG (%)","PMIL (g)","Destino","Observaciones","Estado","Fecha Despacho"]]
        for o in filtrado:
            total_cant = sum(l.get("cantidad", 0) for l in o.get("lotes", []))
            rows.append([o["numero"],o.get("remito",""),o.get("nPedido",""),o.get("fecha",""),
                         o.get("campaña",""),o.get("especie",""),o.get("variedad",""),
                         o.get("tipo",""),"Sí" if o.get("tratada") else "No",
                         total_cant,total_cant*o.get("pesoUnit",0),
                         o.get("pg",""),o.get("pmil",""),o.get("destino",""),
                         o.get("obs",""),o.get("estado",""),o.get("fechaDespachada","")])
        df_exp = pd.DataFrame(rows[1:], columns=rows[0])
        csv = df_exp.to_csv(index=False, sep=";").encode("utf-8-sig")
        st.download_button("⬇ Descargar", csv, "ordenes_carga.csv", "text/csv")

    st.markdown("<br>", unsafe_allow_html=True)

    if not filtrado:
        st.info("Sin órdenes para los filtros seleccionados. Creá una desde Tabla → 📋 OC.")
    else:
        for o in filtrado:
            is_desp = o.get("estado") == "despachada"
            estado_badge = ("<span class='badge badge-desp'>✓ Despachada</span>"
                            if is_desp
                            else "<span class='badge badge-pend'>⏳ Pendiente</span>")
            total_cant = sum(l.get("cantidad", 0) for l in o.get("lotes", []))

            cols = st.columns([1.2, 1.5, 1, 1, 1, 1, 0.8, 0.8])
            cols[0].markdown(f"<b style='font-size:1rem;color:#1a2a4a'>{o['numero']}</b><br>"
                             f"<small style='color:#6b7280'>{o.get('fecha','')}</small>",
                             unsafe_allow_html=True)
            cols[1].markdown(f"<b>{o.get('variedad','')}</b><br>"
                             f"<small>{o.get('especie','')} · {o.get('campaña','')}</small>",
                             unsafe_allow_html=True)
            cols[2].markdown(f"<b>{fmt(total_cant)}</b> {'BB' if o.get('tipo')=='bigbag' else 'bolsas'}<br>"
                             f"<small>{fmt(total_cant * o.get('pesoUnit', 0))} kg</small>",
                             unsafe_allow_html=True)
            cols[3].markdown(f"<small style='color:#6b7280'>Destino</small><br>{o.get('destino','—')}",
                             unsafe_allow_html=True)
            cols[4].markdown(f"<small style='color:#6b7280'>Remito</small><br>{o.get('remito','—')}",
                             unsafe_allow_html=True)
            cols[5].markdown(estado_badge, unsafe_allow_html=True)

            with cols[6]:
                if not is_desp:
                    if st.button("✅ Despachar", key=f"desp_{o['id']}"):
                        st.session_state["confirm_desp"] = o["id"]

            with cols[7]:
                if st.button("🗑 Eliminar", key=f"del_oc_{o['id']}"):
                    st.session_state["confirm_del_oc"] = o["id"]

            st.markdown("<hr style='margin:4px 0;border:none;border-top:1px solid #edf0f5'>",
                        unsafe_allow_html=True)

    # Confirmar despacho
    if st.session_state.get("confirm_desp"):
        oc_id = st.session_state["confirm_desp"]
        oc = next((o for o in ordenes if o["id"] == oc_id), None)
        if oc:
            total = sum(l.get("cantidad", 0) for l in oc.get("lotes", []))
            st.warning(f"⚠ ¿Despachar **{oc['numero']}**? Se generará un egreso de {fmt(total)} unidades de **{oc['variedad']}**.")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Confirmar despacho", type="primary"):
                    # aplicar egreso al stock
                    stock_upd = list(st.session_state["stock"])
                    hist_new = []
                    for lote in oc.get("lotes", []):
                        for idx, si in enumerate(stock_upd):
                            if si["id"] == lote.get("stockId"):
                                nueva_cant = si["cantidad"] - lote["cantidad"]
                                stock_upd[idx] = {**si, "cantidad": nueva_cant}
                                hist_new.append({
                                    "id": next_id(st.session_state["historial"]),
                                    "fecha": now_str(),
                                    "campaña": si["campaña"], "especie": si["especie"],
                                    "variedad": si["variedad"], "tipo": si["tipo"],
                                    "tratada": si["tratada"], "lote": si["lote"],
                                    "op": "egreso", "delta": lote["cantidad"],
                                    "stockPrev": si["cantidad"],
                                    "stockPost": nueva_cant,
                                    "kgMovidos": lote["cantidad"] * si["pesoUnit"],
                                    "motivo": f"Despacho {oc['numero']}",
                                })
                    st.session_state["stock"] = stock_upd
                    st.session_state["historial"] = hist_new + st.session_state["historial"]
                    st.session_state["ordenes"] = [
                        {**o, "estado": "despachada", "fechaDespachada": now_str()} if o["id"] == oc_id else o
                        for o in ordenes
                    ]
                    del st.session_state["confirm_desp"]
                    st.success(f"✅ {oc['numero']} despachada.")
                    st.rerun()
            with c2:
                if st.button("❌ Cancelar"):
                    del st.session_state["confirm_desp"]
                    st.rerun()

    # Confirmar eliminación OC
    if st.session_state.get("confirm_del_oc"):
        oc_id = st.session_state["confirm_del_oc"]
        oc = next((o for o in ordenes if o["id"] == oc_id), None)
        if oc:
            st.warning(f"⚠ ¿Eliminar la orden **{oc['numero']}**?")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Sí, eliminar OC", type="primary"):
                    st.session_state["ordenes"] = [o for o in ordenes if o["id"] != oc_id]
                    del st.session_state["confirm_del_oc"]
                    st.rerun()
            with c2:
                if st.button("❌ Cancelar eliminación OC"):
                    del st.session_state["confirm_del_oc"]
                    st.rerun()


# ──────────────────────────────────────────────
# TAB: CATÁLOGOS / ADMIN
# ──────────────────────────────────────────────
def render_admin():
    st.markdown("<div class='section-title'>⚙ Catálogos y Configuración</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # Campañas
    with col1:
        st.markdown("**📅 Campañas**")
        camps = st.session_state["campañas"]
        for c in camps:
            cc1, cc2 = st.columns([4, 1])
            cc1.markdown(f"`{c}`")
            if cc2.button("✕", key=f"del_camp_{c}"):
                if len(camps) > 1:
                    st.session_state["campañas"] = [x for x in camps if x != c]
                    st.rerun()
        with st.form("add_camp"):
            new_c = st.text_input("Nueva campaña", placeholder="Ej. 2026/2027")
            if st.form_submit_button("Agregar"):
                if new_c and new_c not in camps:
                    st.session_state["campañas"].append(new_c)
                    st.rerun()

    # Especies
    with col2:
        st.markdown("**🌿 Especies**")
        esps = st.session_state["especies"]
        for e in esps:
            ce1, ce2 = st.columns([4, 1])
            ce1.markdown(f"`{e}`")
            if ce2.button("✕", key=f"del_esp_{e}"):
                if len(esps) > 1:
                    st.session_state["especies"] = [x for x in esps if x != e]
                    if e in st.session_state["var_map"]:
                        del st.session_state["var_map"][e]
                    st.rerun()
        with st.form("add_esp"):
            new_e = st.text_input("Nueva especie", placeholder="Ej. Lino")
            if st.form_submit_button("Agregar"):
                if new_e and new_e not in esps:
                    st.session_state["especies"].append(new_e)
                    st.session_state["var_map"][new_e] = []
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**🌱 Variedades por especie**")
    esp_sel = st.selectbox("Especie", st.session_state["especies"])
    vars_esp = st.session_state["var_map"].get(esp_sel, [])
    for v in vars_esp:
        cv1, cv2 = st.columns([4, 1])
        cv1.markdown(f"`{v}`")
        if cv2.button("✕", key=f"del_var_{esp_sel}_{v}"):
            st.session_state["var_map"][esp_sel] = [x for x in vars_esp if x != v]
            st.rerun()
    with st.form("add_var"):
        new_v = st.text_input("Nueva variedad", placeholder="Ej. DM 5958")
        if st.form_submit_button("Agregar variedad"):
            if new_v and new_v not in vars_esp:
                st.session_state["var_map"].setdefault(esp_sel, []).append(new_v)
                st.rerun()

    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("**🔒 Cambiar contraseña**")
    with st.form("change_pass"):
        p1 = st.text_input("Nueva contraseña", type="password")
        p2 = st.text_input("Confirmar contraseña", type="password")
        if st.form_submit_button("Cambiar contraseña"):
            if not p1:
                st.error("La contraseña no puede estar vacía.")
            elif p1 != p2:
                st.error("Las contraseñas no coinciden.")
            else:
                st.session_state["password"] = p1
                st.success("✅ Contraseña actualizada.")

    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("**💾 Exportar / Importar datos (JSON)**")
    c1, c2 = st.columns(2)
    with c1:
        data_export = {
            "stock": st.session_state["stock"],
            "historial": st.session_state["historial"],
            "ordenes": st.session_state["ordenes"],
            "campañas": st.session_state["campañas"],
            "especies": st.session_state["especies"],
            "var_map": st.session_state["var_map"],
        }
        st.download_button("📤 Exportar todos los datos",
                           json.dumps(data_export, ensure_ascii=False, indent=2).encode("utf-8"),
                           "semillero_backup.json", "application/json")
    with c2:
        uploaded = st.file_uploader("📥 Importar backup JSON", type=["json"])
        if uploaded:
            try:
                data_import = json.load(uploaded)
                st.session_state["stock"]    = data_import.get("stock", [])
                st.session_state["historial"]= data_import.get("historial", [])
                st.session_state["ordenes"]  = data_import.get("ordenes", [])
                st.session_state["campañas"] = data_import.get("campañas", CAMPAÑAS_DEF)
                st.session_state["especies"] = data_import.get("especies", ESPECIES_DEF)
                st.session_state["var_map"]  = data_import.get("var_map", VARS_DEF)
                st.success("✅ Datos importados correctamente.")
                st.rerun()
            except Exception as e:
                st.error(f"Error al importar: {e}")

    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("**🔴 Zona de peligro**")
    if st.button("⚠ Borrar TODOS los datos y reiniciar", type="secondary"):
        st.session_state["confirm_reset"] = True
    if st.session_state.get("confirm_reset"):
        st.error("¿Estás SEGURO? Se borrarán todos los datos.")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Sí, borrar todo"):
                st.session_state["stock"]     = [dict(i) for i in STOCK_INIT]
                st.session_state["historial"] = []
                st.session_state["ordenes"]   = []
                st.session_state["campañas"]  = list(CAMPAÑAS_DEF)
                st.session_state["especies"]  = list(ESPECIES_DEF)
                st.session_state["var_map"]   = {k: list(v) for k, v in VARS_DEF.items()}
                del st.session_state["confirm_reset"]
                st.success("✅ Datos reiniciados.")
                st.rerun()
        with c2:
            if st.button("Cancelar reset"):
                del st.session_state["confirm_reset"]
                st.rerun()


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────
def main():
    if not st.session_state["logged_in"]:
        render_login()
        return

    render_header()
    render_kpis(st.session_state["stock"])

    st.markdown("<br>", unsafe_allow_html=True)

    tabs = ["📋 Resumen", "📦 Tabla", "📜 Historial", "🚚 Órdenes de Carga", "⚙ Catálogos"]
    tab = st.tabs(tabs)

    with tab[0]:
        render_resumen()
    with tab[1]:
        render_tabla()
    with tab[2]:
        render_historial()
    with tab[3]:
        render_ordenes()
    with tab[4]:
        render_admin()

    # Logout en sidebar
    with st.sidebar:
        st.markdown("### 🌱 La Clementina")
        st.markdown("---")
        if st.button("🔒 Cerrar sesión"):
            st.session_state["logged_in"] = False
            st.rerun()


main()
