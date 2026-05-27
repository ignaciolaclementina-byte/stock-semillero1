import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import json
from datetime import datetime

# ==============================================================================
# 1. CONFIGURACIÓN DEL PANEL
# ==============================================================================
st.set_page_config(
    page_title="La Clementina · Stock Semillas",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        .block-container { padding: 0rem !important; max-width: 100% !important; }
        [data-testid="stHeader"] { display: none !important; }
        footer { visibility: hidden !important; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. CONEXIÓN Y PROCESAMIENTO (BACKEND)
# ==============================================================================
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    st.error("⚠️ Error al conectar con Google Sheets.")
    st.stop()

def leer_pestana(sheet_name):
    try:
        return conn.read(worksheet=sheet_name, ttl=0).fillna("").to_dict(orient="records")
    except: return []

def actualizar_pestana(sheet_name, lista_datos):
    if lista_datos:
        df_nuevo = pd.DataFrame(lista_datos)
        conn.update(worksheet=sheet_name, data=df_nuevo)

# --- Bridge de Comunicación ---
query_params = st.query_params
if "action" in query_params:
    action = query_params["action"]
    payload = json.loads(query_params.get("payload", "{}"))
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    if action == "save_lote":
        stock = leer_pestana("Stock")
        historial = leer_pestana("Historial")
        lote_data = payload.get("item", payload)
        
        if lote_data.get("ID"):
            lote_id = lote_data.get("ID")
            for r in stock:
                if str(r.get("ID")) == str(lote_id):
                    r.update(lote_data)
                    r["Kilos_Totales"] = int(lote_data.get("bolsas", 0)) * float(lote_data.get("kilosBolsa", 40))
        else:
            next_id = max([int(r.get("ID", 0)) for r in stock]) + 1 if stock else 1
            lote_data["ID"] = next_id
            lote_data["Kilos_Totales"] = int(lote_data.get("bolsas", 0)) * float(lote_data.get("kilosBolsa", 40))
            stock.append(lote_data)
            
        actualizar_pestana("Stock", stock)
        st.query_params.clear()
        st.rerun()

    elif action == "move_lote":
        stock = leer_pestana("Stock")
        ordenes = leer_pestana("Ordenes")
        mov = payload.get("mov", payload)
        lote_id = int(mov.get("loteId"))
        cant = int(mov.get("cantidad"))
        
        for lote in stock:
            if int(lote.get("ID", 0)) == lote_id:
                lote["Bolsas"] = int(lote["Bolsas"]) - cant
                lote["Kilos_Totales"] = int(lote["Bolsas"]) * float(lote.get("Kilos_por_Bolsa", 40))
                
                if mov.get("tipo") == "egreso":
                    proxima_oc = max([int(o.get("ID_Orden", 0)) for o in ordenes]) + 1 if ordenes else 5001
                    ordenes.append({
                        "ID_Orden": proxima_oc, "Fecha": now_str, "Variedad": lote["Variedad"],
                        "Bolsas": cant, "Cliente": mov.get("cliente", ""), "Estado": "DESPACHADO"
                    })
                    actualizar_pestana("Ordenes", ordenes)
        
        actualizar_pestana("Stock", stock)
        st.query_params.clear()
        st.rerun()

# Carga de datos
js_stock = json.dumps(leer_pestana("Stock"))
js_historial = json.dumps(leer_pestana("Historial"))
js_ordenes = json.dumps(leer_pestana("Ordenes"))
js_catalogos = json.dumps(leer_pestana("Catalogos"))

# ==============================================================================
# 3. FRONTEND INTEGRAL (REACT + HTML5)
# ==============================================================================
html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.2/babel.min.js"></script>
    <style>
        /* (Estilos intactos de tu base original) */
        :root{{--bg:#f4f6f9;--accent:#e07b00;--border:#dde1ea;}}
        .app{{max-width:1300px;margin:0 auto;}}
        .table-wrap{{overflow-x:auto}}
        table{{width:100%;border-collapse:collapse;}}
        th,td{{padding:10px;text-align:left;border-bottom:1px solid #ddd;}}
    </style>
</head>
<body>
    <div id="root"></div>
    <script type="text/babel">
        const DB_STOCK = {js_stock};
        const DB_ORDENES = {js_ordenes};
        const {{ useState }} = React;

        function App() {{
            const [tab, setTab] = useState("stock");
            
            return (
                <div className="app">
                    <header className="hdr" style={{{{background:'#1a2a4a', padding:'20px', color:'#fff'}}}}>
                        <h1>La Clementina · Gestión</h1>
                        <button onClick={{() => setTab("stock")}}>Stock</button>
                        <button onClick={{() => setTab("ordenes")}}>Órdenes</button>
                    </header>

                    {{tab === "stock" && (
                        <div className="table-wrap">
                            <table>
                                <thead><tr><th>Variedad</th><th>Bolsas</th></tr></thead>
                                <tbody>
                                    {{DB_STOCK.map(s => <tr key={{s.ID}}><td>{{s.Variedad}}</td><td>{{s.Bolsas}}</td></tr>)}}
                                </tbody>
                            </table>
                        </div>
                    )}}

                    {{tab === "ordenes" && (
                        <div className="table-wrap">
                            <table>
                                <thead><tr><th>OC #</th><th>Cliente</th><th>Estado</th></tr></thead>
                                <tbody>
                                    {{DB_ORDENES.map(o => (
                                        <tr key={{o.ID_Orden}}>
                                            <td>{{o.ID_Orden}}</td>
                                            <td>{{o.Cliente}}</td>
                                            <td>{{o.Estado}}</td>
                                        </tr>
                                    ))}}
                                </tbody>
                            </table>
                        </div>
                    )}}
                    {/* FOOTER Y WHATSAPP ELIMINADOS */}
                </div>
            );
        }}
        ReactDOM.createRoot(document.getElementById('root')).render(<App />);
    </script>
</body>
</html>
"""

st.components.v1.html(html_content, height=1200)
