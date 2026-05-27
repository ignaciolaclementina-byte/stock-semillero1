import streamlit as st
import gspread
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. CONFIGURACIÓN PREMIUM DE LA PÁGINA (Tema Corporativo Agro)
st.set_page_config(
    page_title="La Clementina · Stock Semillas",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para mantener la identidad visual de tu app original
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Barlow', sans-serif;
    }
    h1, h2, h3, [data-testid="stHeader"] {
        font-family: 'Barlow Condensed', sans-serif;
    }
    
    /* Encabezado Principal */
    .main-header {
        background: linear-gradient(135deg, #1a2a4a 0%, #111c33 100%);
        border-bottom: 3px solid #e07b00;
        padding: 24px;
        border-radius: 8px;
        color: white;
        margin-bottom: 25px;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.4rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .main-header h1 span {
        color: #f5a623;
    }
    
    /* Tarjetas de Métricas */
    .kpi-card {
        background-color: #ffffff;
        border: 1px solid #dde1ea;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,.04);
        text-align: center;
    }
    
    /* Pie de página blindado */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #1a2a4a;
        color: rgba(255,255,255,0.7);
        text-align: center;
        padding: 10px;
        font-size: 0.9rem;
        font-weight: 600;
        border-top: 3px solid #e07b00;
        z-index: 100;
    }
    </style>
""", unsafe_allow_html=True)

# 2. CONEXIÓN SEGURA A GOOGLE SHEETS
@st.cache_resource
def init_connection():
    credentials = st.secrets["gspread_credentials"]
    gc = gspread.service_account_from_dict(credentials)
    return gc.open("Base_Datos_Semillero")

try:
    sh = init_connection()
except Exception as e:
    st.error("⚠️ Error de conexión con Google Sheets. Verificá que hayas pegado las credenciales en 'Secrets' y que le hayas compartido la planilla al mail del bot como Editor.")
    st.stop()

# Funciones de lectura y escritura optimizadas para evitar retrasos
def get_dataframe(sheet_name):
    worksheet = sh.worksheet(sheet_name)
    data = worksheet.get_all_records()
    if not data:
        return pd.DataFrame()
    return pd.DataFrame(data)

def append_row(sheet_name, row_list):
    worksheet = sh.worksheet(sheet_name)
    worksheet.append_row(row_list)

# 3. CONTROL DE ACCESO (Mismo sistema de login)
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown("<div style='max-width: 450px; margin: 80px auto; padding: 30px; background:#fff; border-radius:8px; border:1px solid #dde1ea; box-shadow: 0 4px 12px rgba(0,0,0,0.05);'>", unsafe_allow_html=True)
    st.subheader("🔑 INGRESO AL SISTEMA · LA CLEMENTINA")
    clavelog = st.text_input("Introduzca Clave Operativa:", type="password")
    if st.button("Ingresar Sistema", use_container_width=True):
        if clavelog == "lcagro2026":
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("❌ Clave incorrecta")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# 4. CARGA DE BASE DE DATOS EN TIEMPO REAL
df_stock = get_dataframe("Stock")
df_historial = get_dataframe("Historial")
df_ordenes = get_dataframe("Ordenes")
df_catalogos = get_dataframe("Catalogos")

# Procesamiento de catálogos dinámicos vinculados
if not df_catalogos.empty:
    campanas_list = df_catalogos[df_catalogos['Tipo'] == 'Campaña']['Valor'].unique().tolist()
    especies_list = df_catalogos[df_catalogos['Tipo'] == 'Especie']['Valor'].unique().tolist()
    depositos_list = df_catalogos[df_catalogos['Tipo'] == 'Deposito']['Valor'].unique().tolist()
else:
    campanas_list = ["24/25", "23/24"]
    especies_list = ["SOJA", "TRIGO"]
    depositos_list = ["Planta 1", "Planta 2", "Planta 3", "Cámara Semillas"]

# 5. ENCABEZADO CORPORATIVO
st.markdown("""
    <div class="main-header">
        <h1>La Clementina · <span>Control de Semillero</span></h1>
        <p style="margin:4px 0 0 0; opacity:0.8; font-size:0.95rem;">Módulo centralizado de existencias, logística y distribución en la nube</p>
    </div>
""", unsafe_allow_html=True)

# 6. PANEL DE MÉTRICAS GENERALES
tot_bolsas = int(df_stock['Bolsas'].sum()) if not df_stock.empty else 0
tot_kilos = float(df_stock['Kilos_Totales'].sum()) if not df_stock.empty else 0.0
tot_ocs = len(df_ordenes) if not df_ordenes.empty else 0

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f'<div class="kpi-card"><span style="color:#e07b00; font-size:2rem; font-weight:800;">{tot_bolsas:,}</span><br><small style="color:#6b7280; font-weight:600;">BOLSAS EN STOCK TOTAL</small></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="kpi-card"><span style="color:#1a7abf; font-size:2rem; font-weight:800;">{tot_kilos/1000:,.2f} Tn</span><br><small style="color:#6b7280; font-weight:600;">MERCADERÍA DISPONIBLE</small></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="kpi-card"><span style="color:#2e8b57; font-size:2rem; font-weight:800;">{tot_ocs}</span><br><small style="color:#6b7280; font-weight:600;">ÓRDENES DE DESPACHO</small></div>', unsafe_allow_html=True)

st.write("")

# 7. MENÚ OPERATIVO POR PESTAÑAS
tab_resumen, tab_ingreso, tab_movimiento, tab_historial, tab_ordenes = st.tabs([
    "📋 PANEL DE EXISTENCIAS", 
    "📥 INGRESO DE LOTES", 
    "🔄 TRANSFERENCIA / EGRESO", 
    "⏳ AUDITORÍA (LOG)", 
    "🚚 ÓRDENES DE CARGA"
])

# ==========================================
# PESTAÑA 1: PANEL DE EXISTENCIAS
# ==========================================
with tab_resumen:
    st.subheader("Filtros de Búsqueda de Semillas")
    f1, f2, f3 = st.columns([2, 1, 1])
    with f1:
        search_q = st.text_input("🔍 Buscador rápido (Variedad o Categoría):", "").strip().lower()
    with f2:
        filtro_esp = st.selectbox("Especie:", ["TODAS"] + especies_list)
    with f3:
        filtro_dep = st.selectbox("Depósito:", ["TODOS"] + depositos_list)
        
    df_ver = df_stock.copy() if not df_stock.empty else pd.DataFrame(columns=['ID','Campaña','Especie','Variedad','Categoría','Depósito','Bolsas','Kilos_por_Bolsa','Kilos_Totales','Estado','Notas'])
    
    # Aplicar filtros en memoria
    if search_q:
        df_ver = df_ver[df_ver['Variedad'].astype(str).str.lower().str.contains(search_q) | df_ver['Categoría'].astype(str).str.lower().str.contains(search_q)]
    if filtro_esp != "TODAS":
        df_ver = df_ver[df_ver['Especie'] == filtro_esp]
    if filtro_dep != "TODOS":
        df_ver = df_ver[df_ver['Depósito'] == filtro_dep]
        
    if df_ver.empty:
        st.info("No se registran lotes con los criterios seleccionados.")
    else:
        st.dataframe(
            df_ver[['Campaña', 'Especie', 'Variedad', 'Categoría', 'Depósito', 'Bolsas', 'Kilos_por_Bolsa', 'Kilos_Totales', 'Estado', 'Notas']],
            use_container_width=True,
            hide_index=True
        )

# ==========================================
# PESTAÑA 2: INGRESO DE LOTES
# ==========================================
with tab_ingreso:
    st.subheader("Carga de Nueva Mercadería al Semillero")
    with st.form("form_alta_lote", clear_on_submit=True):
        i1, i2, i3 = st.columns(3)
        with i1:
            in_campana = st.selectbox("Seleccione Campaña:", campanas_list)
            in_especie = st.selectbox("Seleccione Especie:", especies_list)
            
            # Filtro dinámico de variedades según la especie seleccionada
            tipo_var_catalogo = f"Variedad_{in_especie}"
            if not df_catalogos.empty and tipo_var_catalogo in df_catalogos['Tipo'].values:
                vars_filtradas = df_catalogos[df_catalogos['Tipo'] == tipo_var_catalogo]['Valor'].tolist()
                in_variedad = st.selectbox("Variedad / Híbrido:", vars_filtradas)
            else:
                in_variedad = st.text_input("Variedad / Híbrido (Manual):").upper().strip()
                
        with i2:
            in_categoria = st.text_input("Categoría de la Semilla (Ej: R1, Original):").strip()
            in_deposito = st.selectbox("Asignar Depósito:", depositos_list)
            in_estado = st.selectbox("Estado Operativo del Lote:", ["Disponible", "Bloqueado", "Muestra"])
        with i3:
            in_bolsas = st.number_input("Cantidad de Bolsas:", min_value=1, value=100, step=1)
            in_kilos_b = st.number_input("Kilos netos por Bolsa:", min_value=1.0, value=40.0, step=0.5)
            in_notas = st.text_input("Observaciones / Nro Documento:")
            
        btn_alta = st.form_submit_button
