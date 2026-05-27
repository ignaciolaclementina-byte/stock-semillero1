import streamlit as st
import pandas as pd
from datetime import datetime
import json

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="La Clementina · Stock Semillas",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS CSS (Inspirados en tu HTML) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500&display=swap');
    
    :root {
        --accent: #e07b00;
        --blue: #1a7abf;
        --bg-dark: #1a2a4a;
    }

    /* Reset y fuentes */
    .main .block-container { padding-top: 2rem; }
    html, body, [data-testid="stSidebar"] {
        font-family: 'Barlow', sans-serif;
    }

    /* Header Estilo La Clementina */
    .custom-header {
        background: linear-gradient(135deg, #1a2a4a 60%, #1e3660);
        border-bottom: 3px solid var(--accent);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 25px;
    }
    .custom-header h1 {
        font-family: 'Barlow Condensed', sans-serif;
        font-weight: 800;
        text-transform: uppercase;
        margin: 0;
        font-size: 2.2rem;
    }
    .custom-header h1 span { color: #f5a623; }

    /* KPIs Cards */
    .kpi-container {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
    }
    .kpi-card {
        background: white;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #dde1ea;
        flex: 1;
        box-shadow: 0 1px 4px rgba(0,0,0,.08);
    }
    .kpi-val {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        line-height: 1;
        display: block;
    }
    .kpi-lbl {
        font-size: 0.7rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.7px;
    }

    /* Botones y Tabs */
    .stButton>button {
        background-color: var(--accent);
        color: white;
        font-family: 'Barlow Condensed', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA DE DATOS (Simulación de DB) ---
if 'db' not in st.session_state:
    st.session_state.db = {
        'stock': [
            {'id': 1, 'campaña': '23/24', 'especie': 'SOJA', 'variedad': 'NIDERA 5009', 'deposito': 'PLANTA 1', 'cantidad': 450, 'unidad': 'Bolsas', 'estado': 'Disponible'},
            {'id': 2, 'campaña': '23/24', 'especie': 'MAIZ', 'variedad': 'DK 72-10', 'deposito': 'PLANTA 2', 'cantidad': 120, 'unidad': 'Bolsas', 'estado': 'Disponible'}
        ],
        'historial': [],
        'ordenes': []
    }

# --- HEADER ---
st.markdown("""
    <div class="custom-header">
        <h1>LA CLEMENTINA · <span>STOCK SEMILLAS</span></h1>
        <p style="opacity:0.7">Gestión Profesional de Inventario Agrícola</p>
    </div>
""", unsafe_allow_html=True)

# --- TABS PRINCIPALES ---
tab_stock, tab_movimientos, tab_ordenes, tab_admin = st.tabs([
    "📊 RESUMEN STOCK", 
    "🔄 MOVIMIENTOS", 
    "📑 ÓRDENES DE CARGA", 
    "⚙️ CONFIGURACIÓN"
])

# --- TAB: RESUMEN STOCK ---
with tab_stock:
    # KPIs Rápidos
    total_bolsas = sum(item['cantidad'] for item in st.session_state.db['stock'] if item['unidad'] == 'Bolsas')
    total_especies = len(set(item['especie'] for item in st.session_state.db['stock']))
    
    cols = st.columns(4)
    cols[0].markdown(f'<div class="kpi-card"><span class="kpi-val" style="color:#e07b00">{total_bolsas}</span><span class="kpi-lbl">TOTAL BOLSAS</span></div>', unsafe_allow_html=True)
    cols[1].markdown(f'<div class="kpi-card"><span class="kpi-val" style="color:#1a7abf">{total_especies}</span><span class="kpi-lbl">ESPECIES</span></div>', unsafe_allow_html=True)
    cols[2].markdown(f'<div class="kpi-card"><span class="kpi-val" style="color:#2e8b57">OK</span><span class="kpi-lbl">ESTADO SISTEMA</span></div>', unsafe_allow_html=True)
    cols[3].markdown(f'<div class="kpi-card"><span class="kpi-val" style="color:#7b4fa6">0</span><span class="kpi-lbl">PENDIENTES</span></div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # Filtros
    f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
    search = f_col1.text_input("🔍 Buscar variedad o lote...")
    campana_filter = f_col2.selectbox("Campaña", ["Todas", "23/24", "24/25"])
    
    # Tabla de Stock
    df_stock = pd.DataFrame(st.session_state.db['stock'])
    if search:
        df_stock = df_stock[df_stock['variedad'].str.contains(search, case=False)]
    
    st.dataframe(df_stock, use_container_width=True, hide_index=True)

# --- TAB: MOVIMIENTOS (INGRESOS/EGRESOS) ---
with tab_movimientos:
    st.subheader("Registrar Movimiento de Stock")
    with st.form("form_movimiento"):
        m_col1, m_col2, m_col3 = st.columns(3)
        tipo = m_col1.selectbox("Tipo", ["Ingreso (+)", "Egreso (-)"])
        especie = m_col2.selectbox("Especie", ["SOJA", "MAIZ", "TRIGO", "GIRASOL"])
        variedad = m_col3.text_input("Variedad")
        
        cant = st.number_input("Cantidad", min_value=1)
        obs = st.text_area("Observaciones / Destino")
        
        submit = st.form_submit_button("REGISTRAR MOVIMIENTO")
        
        if submit:
            # Lógica para actualizar el stock (simplificada)
            nuevo_mov = {
                "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "tipo": tipo,
                "variedad": variedad,
                "cantidad": cant,
                "obs": obs
            }
            st.session_state.db['historial'].append(nuevo_mov)
            st.success("Movimiento registrado correctamente.")

# --- TAB: ÓRDENES DE CARGA ---
with tab_ordenes:
    st.subheader("Gestión de Órdenes de Carga")
    st.info("Aquí se visualizan las órdenes generadas para despacho.")
    if not st.session_state.db['ordenes']:
        st.write("No hay órdenes pendientes.")
    else:
        st.table(st.session_state.db['ordenes'])

# --- TAB: ADMIN ---
with tab_admin:
    st.subheader("Panel de Control")
    col_adm1, col_adm2 = st.columns(2)
    
    with col_adm1:
        st.markdown("### 📋 Catálogos")
        st.text_input("Agregar Nueva Variedad")
        st.button("Guardar en Catálogo")
        
    with col_adm2:
        st.markdown("### 🔒 Seguridad")
        st.text_input("Nueva Contraseña", type="password")
        if st.button("Actualizar Acceso"):
            st.toast("Contraseña actualizada")

# --- FOOTER ---
st.markdown(f"""
    <div style="text-align:center; color: #6b7280; font-size: 0.8rem; margin-top: 50px; padding: 20px; border-top: 1px solid #dde1ea;">
        Creado por Ignacio Diaz · {datetime.now().year} <br>
        Sistema de Gestión de Semillas v2.1
    </div>
""", unsafe_allow_html=True)
