import streamlit as st
from streamlit_gsheets import GSheetsConnection
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

# Estilos CSS personalizados para mantener la identidad visual de tu app
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght=600;700;800&family=Barlow:wght=400;500;600&display=swap');
    
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

# 2. CONEXIÓN SEGURA NATIVA A GOOGLE SHEETS
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("⚠️ Error al inicializar la conexión. Verificá que en los Secrets de Streamlit esté configurado '[connections.gsheets]' con la URL de tu planilla.")
    st.stop()

# Funciones de lectura y escritura adaptadas para st.connection
def get_dataframe(sheet_name):
    try:
        return conn.read(worksheet=sheet_name, ttl=0)
    except Exception as e:
        st.error(f"Error al leer la pestaña {sheet_name}: {e}")
        return pd.DataFrame()

def append_row(sheet_name, row_list, df_actual):
    nueva_fila = pd.DataFrame([row_list], columns=df_actual.columns)
    df_actualizado = pd.concat([df_actual, nueva_fila], ignore_index=True)
    conn.update(worksheet=sheet_name, data=df_actualizado)

# 3. CONTROL DE ACCESO
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
if not df_catalogos.empty and 'Tipo' in df_catalogos.columns and 'Valor' in df_catalogos.columns:
    campanas_list = df_catalogos[df_catalogos['Tipo'] == 'Campaña']['Valor'].dropna().unique().tolist()
    especies_list = df_catalogos[df_catalogos['Tipo'] == 'Especie']['Valor'].dropna().unique().tolist()
    depositos_list = df_catalogos[df_catalogos['Tipo'] == 'Deposito']['Valor'].dropna().unique().tolist()
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
tot_bolsas = int(df_stock['Bolsas'].sum()) if not df_stock.empty and 'Bolsas' in df_stock.columns else 0
tot_kilos = float(df_stock['Kilos_Totales'].sum()) if not df_stock.empty and 'Kilos_Totales' in df_stock.columns else 0.0
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
    
    if not df_ver.empty:
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
            
            tipo_var_catalogo = f"Variedad_{in_especie}"
            if not df_catalogos.empty and 'Tipo' in df_catalogos.columns and tipo_var_catalogo in df_catalogos['Tipo'].values:
                vars_filtradas = df_catalogos[df_catalogos['Tipo'] == tipo_var_catalogo]['Valor'].dropna().tolist()
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
            
        btn_alta = st.form_submit_button("✓ Guardar en Base de Datos Central", use_container_width=True)
        
        if btn_alta:
            kilos_t = in_bolsas * in_kilos_b
            next_id = int(df_stock['ID'].max()) + 1 if not df_stock.empty and 'ID' in df_stock.columns else 1
            now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
            
            append_row("Stock", [next_id, in_campana, in_especie, in_variedad, in_categoria, in_deposito, in_bolsas, in_kilos_b, kilos_t, in_estado, in_notas], df_stock)
            append_row("Historial", [now_str, "INGRESO", f"Alta lote ID {next_id}: {in_bolsas} bolsas de {in_variedad} en {in_deposito}", in_bolsas, kilos_t, "Ignacio Diaz"], df_historial)
            
            st.success(f"¡Lote de {in_variedad} ingresado y sincronizado correctamente!")
            st.rerun()

# ==========================================
# PESTAÑA 3: TRANSFERENCIA / EGRESO
# ==========================================
with tab_movimiento:
    st.subheader("Gestión Logística Interna y Despachos")
    if df_stock.empty or 'Bolsas' not in df_stock.columns or (df_stock['Bolsas'] == 0).all():
        st.warning("No hay existencias físicas en la base de datos para realizar movimientos.")
    else:
        opciones_lotes = []
        for idx, row in df_stock.iterrows():
            if int(row['Bolsas']) > 0:
                opciones_lotes.append(f"ID {row['ID']} | {row['Variedad']} ({row['Categoría']}) - Ubicación: {row['Depósito']} [Disp: {row['Bolsas']} bols]")
                
        lote_seleccionado = st.selectbox("Seleccione el Lote de Origen de la mercadería:", opciones_lotes)
        lote_id_real = int(lote_seleccionado.split(" | ")[0].replace("ID ", ""))
        datos_origen = df_stock[df_stock['ID'] == lote_id_real].iloc[0]
        
        m1, m2 = st.columns(2)
        with m1:
            modalidad = st.radio("Destino de la Operación:", ["Transferencia entre Plantas / Depósitos", "Egreso por Despacho (Genera Orden de Carga)"])
            cant_mover = st.number_input("Cantidad de Bolsas a Movilizar:", min_value=1, max_value=int(datos_origen['Bolsas']), value=1, step=1)
        with m2:
            if modalidad == "Transferencia entre Plantas / Depósitos":
                destino_dep = st.selectbox("Depósito de Destino:", [d for d in depositos_list if d != datos_origen['Depósito']])
                cliente_oc = "MOVIMIENTO INTERNO"
            else:
                destino_dep = "EGRESO DE DEPÓSITO"
                cliente_oc = st.text_input("Razón Social / Cliente Destinatario:").upper().strip()
                
            patente_c = st.text_input("Patente Chasis:").upper().strip()
            patente_a = st.text_input("Patente Acoplado:").upper().strip()
            
        if st.button("⚡ Ejecutar Operación y Actualizar Todas las PC", use_container_width=True):
            if modalidad == "Egreso por Despacho (Genera Orden de Carga)" and not cliente_oc:
                st.error("Por favor, ingrese el nombre del Cliente para autorizar la Orden de Carga.")
            else:
                now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
                kilogramos_mov = cant_mover * float(datos_origen['Kilos_por_Bolsa'])
                
                # Modificar stock local
                df_stock.loc[df_stock['ID'] == lote_id_real, 'Bolsas'] = int(datos_origen['Bolsas']) - cant_mover
                df_stock.loc[df_stock['ID'] == lote_id_real, 'Kilos_Totales'] = (int(datos_origen['Bolsas']) - cant_mover) * float(datos_origen['Kilos_por_Bolsa'])
                
                if modalidad == "Transferencia entre Plantas / Depósitos":
                    next_id_t = int(df_stock['ID'].max()) + 1 if 'ID' in df_stock.columns else 1
                    
                    nueva_fila_stock = pd.DataFrame([[
                        next_id_t, datos_origen['Campaña'], datos_origen['Especie'], 
                        datos_origen['Variedad'], datos_origen['Categoría'], destino_dep, 
                        cant_mover, datos_origen['Kilos_por_Bolsa'], kilogramos_mov, datos_origen['Estado'], f"Traspasado desde {datos_origen['Depósito']}"
                    ]], columns=df_stock.columns)
                    df_stock_final = pd.concat([df_stock, nueva_fila_stock], ignore_index=True)
                    conn.update(worksheet="Stock", data=df_stock_final)
                    
                    append_row("Historial", [now_str, "TRANSFERENCIA", f"Traspaso de {cant_mover} bols de {datos_origen['Variedad']} desde {datos_origen['Depósito']} hacia {destino_dep}", cant_mover, kilogramos_mov, "Ignacio Diaz"], df_historial)
                    st.success(f"¡Transferencia exitosa! Las existencias se reubicaron en {destino_dep}.")
                    st.rerun()
                else:
                    conn.update(worksheet="Stock", data=df_stock)
                    
                    proxima_oc = int(df_ordenes['ID_Orden'].max()) + 1 if not df_ordenes.empty and 'ID_Orden' in df_ordenes.columns else 5001
                    
                    append_row("Ordenes", [
                        proxima_oc, now_str, datos_origen['Campaña'], datos_origen['Especie'], 
                        datos_origen['Variedad'], datos_origen['Depósito'], cant_mover, 
                        kilogramos_mov, cliente_oc, patente_c, patente_a, "DESPACHADO"
                    ], df_ordenes)
                    
                    append_row("Historial", [now_str, "EGRESO", f"Despacho OC #{proxima_oc}: {cant_mover} bols entregadas a {cliente_oc}", cant_mover, kilogramos_mov, "Ignacio Diaz"], df_historial)
                    
                    # WhatsApp estructurado
                    texto_wa = (
                        f"🌱 *LA CLEMENTINA · ORDEN DE CARGA #{proxima_oc}*\n\n"
                        f"📅 *Fecha:* {now_str}\n"
                        f"🌾 *Variedad:* {datos_origen['Variedad']} ({datos_origen['Campaña']})\n"
                        f"📦 *Cantidad:* {cant_mover} Bolsas ({kilogramos_mov/1000:.2f} Tn)\n"
                        f"🏢 *Origen:* {datos_origen['Depósito']}\n"
                        f"👤 *Destino/Cliente:* {cliente_oc}\n"
                        f"🚛 *Transporte:* Chasis: {patente_c or 'N/C'} | Acoplado: {patente_a or 'N/C'}\n\n"
                        f"✅ *Despacho authorized por Ignacio Diaz*"
                    )
                    wa_url = f"https://wa.me/?text={urllib.parse.quote(texto_wa)}"
                    
                    st.success(f"¡Egreso sincronizado en la nube! Se emitió la Orden de Carga #{proxima_oc}")
                    st.markdown(f'<a href="{wa_url}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:12px 20px; border-radius:6px; cursor:pointer; font-weight:bold; width:100%; font-size:1.05rem;">💬 ENVIAR NOTIFICACIÓN POR WHATSAPP</button></a>', unsafe_allow_html=True)
                    st.write("")

# ==========================================
# PESTAÑA 4: AUDITORÍA (LOG)
# ==========================================
with tab_historial:
    st.subheader("Historial Completo de Operaciones en Tiempo Real")
    if df_historial.empty:
        st.info("No se registran movimientos en el historial todavía.")
    else:
        st.dataframe(df_historial.iloc[::-1], use_container_width=True, hide_index=True)

# ==========================================
# PESTAÑA 5: ÓRDENES DE CARGA
# ==========================================
with tab_ordenes:
    st.subheader("Registro Centralizado de Órdenes Emitidas")
    if df_ordenes.empty:
        st.info("No se emitieron Órdenes de Carga en este ciclo comercial.")
    else:
        st.dataframe(df_ordenes.iloc[::-1], use_container_width=True, hide_index=True)

# 8. PIE DE PÁGINA REQUERIDO
st.markdown("""
    <div class="footer">
        🔒 Panel de Gestión Conectado · Creado por Ignacio Diaz
    </div>
""", unsafe_allow_html=True)
