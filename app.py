import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA Y ESTILOS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="La Clementina · Stock Semillas",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS para replicar la interfaz profesional (Barlow, colores corporativos y cards)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500&display=swap');
    
    * { font-family: 'Barlow', sans-serif; }
    h1, h2, h3, .titulos-condensed { font-family: 'Barlow Condensed', sans-serif; text-transform: uppercase; }
    
    /* Header Personalizado */
    .header-box {
        background: linear-gradient(135deg, #1a2a4a 60%, #1e3660);
        border-bottom: 3px solid #e07b00;
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 25px;
    }
    .header-box h1 { margin: 0; font-size: 2.2rem; font-weight: 800; letter-spacing: 1px; }
    .header-box h1 span { color: #f5a623; }
    .header-box p { margin: 5px 0 0 0; font-size: 0.85rem; color: rgba(255,255,255,0.7); }
    
    /* Métrica / KPIs */
    .kpi-container {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #dde1ea;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        text-align: center;
    }
    .kpi-val { font-family: 'Barlow Condensed', sans-serif; font-size: 2rem; font-weight: 800; line-height: 1; }
    .kpi-lbl { font-size: 0.75rem; color: #6b7280; text-transform: uppercase; margin-top: 4px; font-weight: 600; }
    
    /* Cards de Resumen */
    .sv-card {
        background: white;
        border: 1px solid #dde1ea;
        border-radius: 10px;
        padding: 15px;
        border-top: 3px solid #e07b00;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        margin-bottom: 15px;
    }
    .sv-variedad { font-family: 'Barlow Condensed', sans-serif; font-size: 1.1rem; font-weight: 700; color: #1a2a4a; }
    .sv-row { display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid #edf0f5; }
    .sv-row:last-child { border-bottom: none; }
    .sv-label { font-size: 0.75rem; color: #6b7280; text-transform: uppercase; }
    .sv-val { font-family: 'Barlow Condensed', sans-serif; font-size: 1.1rem; font-weight: 700; }
    
    /* Footer */
    .footer-box {
        text-align: center;
        padding: 20px;
        font-size: 0.8rem;
        color: #6b7280;
        border-top: 1px solid #dde1ea;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# VALORES POR DEFECTO E INICIALIZACIÓN DEL ESTADO (LOCAL STORAGE EN PYTHON)
# -----------------------------------------------------------------------------
LOW_STOCK_LIMIT = 5

if 'lc_pass' not in st.session_state:
    st.session_state.lc_pass = '1234'
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'campanas' not in st.session_state:
    st.session_state.campanas = ['24/25', '25/26']
if 'especies' not in st.session_state:
    st.session_state.especies = ['Soja', 'Maíz', 'Trigo', 'Girasol']
if 'varmap' not in st.session_state:
    st.session_state.varmap = {
        'Soja': ['DM 46E21', 'AW 4721', 'DM 40i25 Enlist'],
        'Maíz': ['DK 72-10 VT3P', 'DK 72-27'],
        'Trigo': ['Baguette 620', 'Algarrobo'],
        'Girasol': ['Syn 3970 CL']
    }

if 'stock' not in st.session_state:
    st.session_state.stock = [
        { 'id': 1, 'campana': '25/26', 'especie': 'Soja', 'variedad': 'DM 46E21', 'lote': 'L-201', 'origen': 'Propio', 'ubicacion': 'Galpón Norte', 'bolsas': 120, 'kg': 4800, 'tipo': 'Bolsas', 'tratamiento': 'Tratado', 'observaciones': 'Calidad excelente.' },
        { 'id': 2, 'campana': '25/26', 'especie': 'Maíz', 'variedad': 'DK 72-10 VT3P', 'lote': 'L-409', 'origen': 'Don Pedro', 'ubicacion': 'Silo 2', 'bolsas': 3, 'kg': 2100, 'tipo': 'Granel', 'tratamiento': 'Original', 'observaciones': '' }
    ]

if 'historial' not in st.session_state:
    st.session_state.historial = [
        { 'id': 1, 'fecha': datetime.now().strftime("%d/%m/%Y %H:%M"), 'tipo': 'Ingreso', 'detalle': 'Carga inicial del sistema', 'campana': '25/26', 'especie': 'Soja', 'variedad': 'DM 46E21', 'bolsas': 120, 'kg': 4800 }
    ]

if 'oc_list' not in st.session_state:
    st.session_state.oc_list = [
        { 'id': 1, 'numero': 'OC-5001', 'fecha': datetime.now().strftime("%Y-%m-%d"), 'cliente': 'Agroganadera San Jorge', 'especie': 'Soja', 'variedad': 'DM 46E21', 'bolsas': 30, 'estado': 'Pendiente', 'observaciones': 'Retira flete cliente.' }
    ]

# -----------------------------------------------------------------------------
# MÓDULO DE AUTENTICACIÓN
# -----------------------------------------------------------------------------
if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
    with col_l2:
        st.markdown("""
            <div style='background: white; padding: 40px; border-radius: 16px; box-shadow: 0 8px 40px rgba(0,0,0,0.15); text-align: center; border: 1px solid #dde1ea;'>
                <h2 style='color: #1a2a4a; margin-bottom: 0;'>La Clementina</h2>
                <p style='color: #6b7280; font-size: 0.85rem; margin-top: 5px; margin-bottom: 25px;'>Control de Existencias Semillas</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=True):
            input_pass = st.text_input("Clave de acceso...", type="password")
            btn_login = st.form_submit_button("Ingresar", use_container_width=True)
            
            if btn_login:
                if input_pass == st.session_state.lc_pass:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Clave incorrecta")
    st.stop()

# -----------------------------------------------------------------------------
# LOGICA DE CONTROLADORES Y FUNCIONES DE NEGOCIO
# -----------------------------------------------------------------------------
def fmt(n):
    return f"{int(n):,}".replace(",", ".")

# Cálculos de Métricas KPIs
tot_bolsas = sum(int(i['bolsas']) for i in st.session_state.stock if i['tipo'] == 'Bolsas')
tot_kg = sum(int(i['kg']) for i in st.session_state.stock)
oc_abiertas = len([o for o in st.session_state.oc_list if o['estado'] == 'Pendiente'])

alertas_critico = 0
for i in st.session_state.stock:
    if i['tipo'] == 'Bolsas' and int(i['bolsas']) <= LOW_STOCK_LIMIT:
        alertas_critico += 1
    elif i['tipo'] != 'Bolsas' and int(i['kg']) <= (LOW_STOCK_LIMIT * 50):
        alertas_critico += 1

# -----------------------------------------------------------------------------
# INTERFAZ PRINCIPAL (HEADER Y NAV TABS)
# -----------------------------------------------------------------------------
st.markdown("""
    <div class="header-box">
        <h1>La Clementina · <span>Stock Semillas</span></h1>
        <p>Logística y Administración Interna · Base de Datos Sincronizada</p>
    </div>
""", unsafe_allow_html=True)

# Barra Superior de Métricas KPIs
c_kpi1, c_kpi2, c_kpi3, c_kpi4 = st.columns(4)
with c_kpi1:
    st.markdown(f'<div class="kpi-container"><div class="kpi-val" style="color:#e07b00;">{fmt(tot_bolsas)}</div><div class="kpi-lbl">Bolsas</div></div>', unsafe_allow_html=True)
with c_kpi2:
    st.markdown(f'<div class="kpi-container"><div class="kpi-val" style="color:#1a7abf;">{fmt(tot_kg)}</div><div class="kpi-lbl">Kg Totales</div></div>', unsafe_allow_html=True)
with c_kpi3:
    st.markdown(f'<div class="kpi-container"><div class="kpi-val" style="color:#7b4fa6;">{oc_abiertas}</div><div class="kpi-lbl">OC Abiertas</div></div>', unsafe_allow_html=True)
with c_kpi4:
    bg_alert = "background-color: #fff5f5;" if alertas_critico > 0 else ""
    st.markdown(f'<div class="kpi-container" style="{bg_alert}"><div class="kpi-val" style="color:#c0392b;">{alertas_critico}</div><div class="kpi-lbl">Lotes en Crítico</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Tabs de navegación de la app
tab_resumen, tab_inventario, tab_trafico, tab_oc, tab_config = st.tabs([
    "📊 Resumen", "📦 Inventario Físico", "🔄 Tráfico / Historial", "📑 Órdenes (OC)", "⚙️ Configuración"
])

# -----------------------------------------------------------------------------
# TAB 1: VISTA RESUMEN (CARDS)
# -----------------------------------------------------------------------------
with tab_resumen:
    st.markdown("### Resumen Consolidado de Existencias")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        f_campana = st.selectbox("Filtrar por Campaña", ["TODAS"] + st.session_state.campanas)
    with col_f2:
        f_especie = st.selectbox("Filtrar por Especie", ["TODAS"] + st.session_state.especies)
        
    campanas_visibles = st.session_state.campanas if f_campana == "TODAS" else [f_campana]
    
    for camp in campanas_visibles:
        items_camp = [i for i in st.session_state.stock if i['campana'] == camp and (f_especie == "TODAS" or i['especie'] == f_especie)]
        if not items_camp:
            continue
            
        st.markdown(f"<h3 style='color: #1a2a4a; border-bottom: 2px solid #e07b00; padding-bottom: 5px; margin-top: 20px;'>Campaña {camp}</h3>", unsafe_allow_html=True)
        
        # Grid layout dinámico usando columnas de Streamlit
        cols_grid = st.columns(3)
        for index, item in enumerate(items_camp):
            col_target = cols_grid[index % 3]
            with col_target:
                disponible_str = f"{fmt(item['bolsas'])} b." if item['tipo'] == "Bolsas" else f"{fmt(item['kg'])} kg"
                st.markdown(f"""
                    <div class="sv-card">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                            <span class="sv-variedad">{item['variedad']}</span>
                            <span style="background:#fff4e0; color:#b86000; border:1px solid #f5c57a; padding:2px 8px; border-radius:20px; font-size:0.7rem; font-weight:700;">{item['tipo']}</span>
                        </div>
                        <div class="sv-row"><span class="sv-label">Especie:</span><span class="sv-val" style="color:#1a7abf;">{item['especie']}</span></div>
                        <div class="sv-row"><span class="sv-label">Lote:</span><span class="sv-val"><code>{item['lote']}</code></span></div>
                        <div class="sv-row"><span class="sv-label">Ubicación:</span><span class="sv-val" style="color:#6b7280;">{item['ubicacion']}</span></div>
                        <div class="sv-row"><span class="sv-label">Disponible:</span><span class="sv-val" style="color:#2e8b57;">{disponible_str}</span></div>
                    </div>
                """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 2: INVENTARIO FÍSICO (ABM Y MOVIMIENTOS)
# -----------------------------------------------------------------------------
with tab_inventario:
    st.markdown("### Gestión del Inventario de Semillas")
    
    # Barra de herramientas superior
    c_tool1, c_tool2 = st.columns([2, 1])
    with c_tool1:
        search_query = st.text_input("🔍 Buscar por Variedad o Lote...", placeholder="Escribe para buscar...")
    with c_tool2:
        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
        exp_alta = st.expander("＋ Registrar Nuevo Lote Físico")

    # Formulario para dar de alta un lote
    with exp_alta:
        with st.form("form_alta_lote", clear_on_submit=True):
            st.markdown("##### Datos del Lote")
            c_al1, c_al2, c_al3 = st.columns(3)
            with c_al1:
                alt_campana = st.selectbox("Campaña *", st.session_state.campanas)
                alt_lote = st.text_input("Lote *")
            with c_al2:
                alt_especie = st.selectbox("Especie *", st.session_state.especies)
                alt_ubicacion = st.text_input("Ubicación")
            with c_al3:
                lista_var = st.session_state.varmap.get(alt_especie, ["Genérica"])
                alt_variedad = st.selectbox("Variedad *", lista_var)
                alt_tipo = st.selectbox("Tipo de Almacenamiento", ["Bolsas", "Granel"])
                
            c_al4, c_al5 = st.columns(2)
            with c_al4:
                alt_bolsas = st.number_input("Cantidad Bolsas", min_value=0, step=1)
            with c_al5:
                alt_kg = st.number_input("Kg Netos Totales", min_value=0, step=10)
                
            submit_alta = st.form_submit_button("✓ Confirmar Registro de Lote")
            if submit_alta:
                if alt_lote and alt_variedad:
                    new_id = int(datetime.now().timestamp())
                    new_item = {
                        'id': new_id, 'campana': alt_campana, 'especie': alt_especie, 'variedad': alt_variedad,
                        'lote': alt_lote, 'origen': 'Propio', 'ubicacion': alt_ubicacion, 'bolsas': int(alt_bolsas),
                        'kg': int(alt_kg), 'tipo': alt_tipo, 'tratamiento': 'Original', 'observaciones': ''
                    }
                    st.session_state.stock.insert(0, new_item)
                    
                    # Añadir al historial / tráfico
                    st.session_state.historial.insert(0, {
                        'id': new_id, 'fecha': datetime.now().strftime("%d/%m/%Y %H:%M"), 'tipo': 'Ingreso',
                        'detalle': f"Alta de lote {alt_lote}", 'campana': alt_campana, 'especie': alt_especie,
                        'variedad': alt_variedad, 'bolsas': int(alt_bolsas), 'kg': int(alt_kg)
                    })
                    st.success(f"Lote {alt_lote} registrado correctamente.")
                    st.rerun()
                else:
                    st.error("Por favor completa los campos obligatorios.")

    # Filtrado del Stock en base a la búsqueda
    stock_filtrado = st.session_state.stock
    if search_query:
        stock_filtrado = [i for i in stock_filtrado if search_query.lower() in i['variedad'].lower() or search_query.lower() in i['lote'].lower()]

    # Visualización de la Tabla Física Principal
    if stock_filtrado:
        df_stock = pd.DataFrame(stock_filtrado)
        df_display = df_stock[['campana', 'especie', 'variedad', 'lote', 'ubicacion', 'bolsas', 'kg', 'tipo']].copy()
        df_display.columns = ['Campaña', 'Especie', 'Variedad', 'Lote', 'Ubicación', 'Bolsas', 'Kg Netos', 'Tipo']
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.info("No se encontraron lotes en el inventario.")

    # Sección de Operaciones Logísticas rápidas (Mover / Despachar / Eliminar)
    st.markdown("---")
    st.markdown("##### 📦 Panel de Acciones Operativas")
    if st.session_state.stock:
        lista_lotes_op = [f"{i['lote']} - {i['variedad']} ({i['campana']})" for i in st.session_state.stock]
        dict_lotes_op = {f"{i['lote']} - {i['variedad']} ({i['campana']})": i for i in st.session_state.stock}
        
        c_op1, c_op2 = st.columns([1, 1])
        with c_op1:
            lote_seleccionado = st.selectbox("Seleccione el Lote a Operar o Modificar", lista_lotes_op)
            item_ref = dict_lotes_op[lote_seleccionado]
            
            st.markdown(f"""
                <div style="background:#f4f6f9; padding:12px; border-radius:8px; font-size:0.85rem; border:1px solid #dde1ea;">
                    <strong>Estado actual del lote seleccionado:</strong><br>
                    • Ubicación: {item_ref['ubicacion']} | Tipo: {item_ref['tipo']}<br>
                    • Stock Disponible: <b>{fmt(item_ref['bolsas'])} bolsas</b> / <b>{fmt(item_ref['kg'])} Kg</b>
                </div>
            """, unsafe_allow_html=True)
            
            # Botón rápido para eliminar lote físico
            if st.button("🗑 Eliminar este Lote por Completo del Inventario", use_container_width=True):
                st.session_state.stock = [x for x in st.session_state.stock if x['id'] != item_ref['id']]
                st.warning(f"Lote {item_ref['lote']} eliminado físicamente.")
                st.rerun()

        with c_op2:
            st.markdown("<div style='font-size:0.85rem; font-weight:bold; text-transform:uppercase; color:#6b7280;'>Registrar Movimiento</div>", unsafe_allow_html=True)
            with st.form("form_movimiento"):
                tipo_mov = st.selectbox("Tipo de Movimiento", ["Egreso", "Despacho", "Ingreso"])
                c_mov1, c_mov2 = st.columns(2)
                with c_mov1:
                    mov_bolsas = st.number_input("Bolsas a mover", min_value=0, step=1)
                with c_mov2:
                    mov_kg = st.number_input("Kg a mover", min_value=0, step=10)
                mov_destino = st.text_input("Destino / Cliente / Destinatario")
                mov_obs = st.text_input("Observaciones operativas")
                
                btn_movimiento = st.form_submit_button("Confirmar Movimiento y Generar Reporte")
                if btn_movimiento:
                    # Actualizar valores del stock
                    for i in st.session_state.stock:
                        if i['id'] == item_ref['id']:
                            if tipo_mov in ["Egreso", "Despacho"]:
                                i['bolsas'] = max(0, int(i['bolsas']) - int(mov_bolsas))
                                i['kg'] = max(0, int(i['kg']) - int(mov_kg))
                            else:
                                i['bolsas'] = int(i['bolsas']) + int(mov_bolsas)
                                i['kg'] = int(i['kg']) + int(mov_kg)
                    
                    # Registrar en Tráfico
                    st.session_state.historial.insert(0, {
                        'id': int(datetime.now().timestamp()), 'fecha': datetime.now().strftime("%d/%m/%Y %H:%M"),
                        'tipo': tipo_mov, 'detalle': f"{tipo_mov} - Destino: {mov_destino if mov_destino else '-'}",
                        'campana': item_ref['campana'], 'especie': item_ref['especie'], 'variedad': item_ref['variedad'],
                        'bolsas': int(mov_bolsas), 'kg': int(mov_kg)
                    })
                    
                    # Preparación de Alerta Profesional WhatsApp
                    msg_wa = (
                        f"*La Clementina · Logística Semillas*\n\n"
                        f"Movimiento: *{tipo_mov}*\n"
                        f"• Insumo: {item_ref['especie']} ({item_ref['variedad']})\n"
                        f"• Lote: {item_ref['lote']}\n"
                        f"• Cantidad: {mov_bolsas} Bolsas / {mov_kg} Kg\n"
                        f"• Destino: {mov_destino if mov_destino else '-'}\n"
                        f"• Info: {mov_obs if mov_obs else '-'}"
                    )
                    wa_url = f"https://api.whatsapp.com/send?text={urllib.parse.quote(msg_wa)}"
                    
                    st.success("Movimiento procesado de manera interna.")
                    st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; padding:10px; background-color:#25D366; color:white; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">📲 Enviar Reporte de Movimiento vía WhatsApp</button></a>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 3: TRÁFICO / HISTORIAL
# -----------------------------------------------------------------------------
with tab_trafico:
    st.markdown("### Registro Histórico de Tráfico de Semillas")
    if st.session_state.historial:
        df_hist = pd.DataFrame(st.session_state.historial)
        df_hist_display = df_hist[['fecha', 'tipo', 'especie', 'variedad', 'detalle', 'bolsas', 'kg']].copy()
        df_hist_display.columns = ['Fecha / Hora', 'Tipo', 'Especie', 'Variedad', 'Detalle Operación', 'Bolsas', 'Kg Netos']
        st.dataframe(df_hist_display, use_container_width=True, hide_index=True)
    else:
        st.info("No se registran movimientos en el historial.")

# -----------------------------------------------------------------------------
# TAB 4: ÓRDENES DE COMPRA (OC)
# -----------------------------------------------------------------------------
with tab_oc:
    st.markdown("### Control de Órdenes de Compra (OC)")
    
    # Formulario para agregar una nueva OC abierta
    with st.expander("＋ Generar Nueva Orden de Compra (OC)"):
        with st.form("form_alta_oc", clear_on_submit=True):
            c_oc1, c_oc2 = st.columns(2)
            with c_oc1:
                new_oc_cliente = st.text_input("Cliente / Razón Social *")
                new_oc_especie = st.selectbox("Especie Requerida", st.session_state.especies)
            with c_oc2:
                new_oc_bolsas = st.number_input("Cantidad de Bolsas Asignadas *", min_value=1, step=1)
                lista_var_oc = st.session_state.varmap.get(new_oc_especie, ["Genérica"])
                new_oc_variedad = st.selectbox("Variedad Requerida", lista_var_oc)
            new_oc_obs = st.text_input("Observaciones / Datos del Flete")
            
            submit_oc = st.form_submit_button("✓ Crear Orden de Compra Abierta")
            if submit_oc:
                if new_oc_cliente:
                    num_rand = int(datetime.now().timestamp()) % 10000
                    st.session_state.oc_list.insert(0, {
                        'id': int(datetime.now().timestamp()),
                        'numero': f"OC-{num_rand}",
                        'fecha': datetime.now().strftime("%Y-%m-%d"),
                        'cliente': new_oc_cliente,
                        'especie': new_oc_especie,
                        'variedad': new_oc_variedad,
                        'bolsas': int(new_oc_bolsas),
                        'estado': 'Pendiente',
                        'observaciones': new_oc_obs
                    })
                    st.success("Orden de compra agregada exitosamente.")
                    st.rerun()
                else:
                    st.error("El campo Cliente es requerido.")

    # Listado de OCs vigentes
    if st.session_state.oc_list:
        df_oc = pd.DataFrame(st.session_state.oc_list)
        df_oc_disp = df_oc[['numero', 'fecha', 'cliente', 'especie', 'variedad', 'bolsas', 'estado', 'observaciones']].copy()
        df_oc_disp.columns = ['Código OC', 'Fecha', 'Cliente', 'Especie', 'Variedad', 'Bolsas', 'Estado', 'Observaciones']
        st.dataframe(df_oc_disp, use_container_width=True, hide_index=True)
        
        # Cambios rápidos de estado de OC
        st.markdown("##### Cambiar Estado de Órdenes")
        c_st_oc1, c_st_oc2 = st.columns(2)
        with c_st_oc1:
            oc_seleccionada = st.selectbox("Seleccione la OC", [o['numero'] for o in st.session_state.oc_list])
        with c_st_oc2:
            nuevo_estado_oc = st.selectbox("Nuevo Estado", ["Pendiente", "Despachado"])
            if st.button("Actualizar Estado de Orden", use_container_width=True):
                for o in st.session_state.oc_list:
                    if o['numero'] == oc_seleccionada:
                        o['estado'] = nuevo_estado_oc
                st.success(f"Estado de {oc_seleccionada} modificado a {nuevo_estado_oc}.")
                st.rerun()
    else:
        st.info("No hay órdenes de compra registradas.")

# -----------------------------------------------------------------------------
# TAB 5: CONFIGURACIÓN Y SEGURIDAD
# -----------------------------------------------------------------------------
with tab_config:
    st.markdown("### Configuración y Parámetros del Sistema")
    
    col_cfg1, col_cfg2, col_cfg3 = st.columns(3)
    
    with col_cfg1:
        st.markdown("##### Campañas Activas")
        st.write(st.session_state.campanas)
        new_camp_val = st.text_input("Nueva Campaña (Ej: 26/27)", key="input_new_camp")
        if st.button("＋ Añadir Campaña"):
            if new_camp_val and new_camp_val not in st.session_state.campanas:
                st.session_state.campanas.append(new_camp_val)
                st.success("Campaña añadida.")
                st.rerun()
                
    with col_cfg2:
        st.markdown("##### Seguridad")
        new_pass_val = st.text_input("Nueva clave de acceso", type="password")
        if st.button("Guardar Nueva Clave"):
            if new_pass_val.strip():
                st.session_state.lc_pass = new_pass_val.strip()
                st.success("Clave de acceso modificada correctamente.")
            else:
                st.error("Clave inválida.")
                
    with col_cfg3:
        st.markdown("##### Zona Crítica de Datos")
        st.markdown("<p style='color:#6b7280; font-size:0.8rem;'>Elimina la base de datos temporal en memoria y reinicia el sistema al estado por defecto.</p>", unsafe_allow_html=True)
        if st.button("🗑 Resetear Todo"):
            st.session_state.clear()
            st.rerun()

    # Cierre de sesión seguro
    st.markdown("---")
    if st.button("🔒 Salir de la Aplicación (Cerrar Sesión)", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# -----------------------------------------------------------------------------
# FOOTER REQUERIDO
# -----------------------------------------------------------------------------
st.markdown("""
    <div class="footer-box">
        La Clementina · Control Operativo Digital<br>
        <strong>Creado por Ignacio Diaz</strong>
    </div>
""", unsafe_allow_html=True)
