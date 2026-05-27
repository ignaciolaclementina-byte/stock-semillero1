import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import json
from datetime import datetime

# ==============================================================================
# 1. CONFIGURACIÓN DEL PANEL DE STREAMLIT (INTERFAZ NATIVA)
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
except Exception as e:
    st.error("⚠️ Error al conectar con Google Sheets.")
    st.stop()

def leer_pestana(sheet_name):
    try:
        df = conn.read(worksheet=sheet_name, ttl=0)
        return df.fillna("").to_dict(orient="records")
    except: return []

def actualizar_pestana(sheet_name, lista_datos):
    if lista_datos:
        df_nuevo = pd.DataFrame(lista_datos)
        conn.update(worksheet=sheet_name, data=df_nuevo)

# --- Bridge de Comunicación (API interna) ---
query_params = st.query_params
if "action" in query_params:
    action = query_params["action"]
    payload = json.loads(query_params.get("payload", "{}"))
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    if action == "save_lote":
        stock = leer_pestana("Stock")
        historial = leer_pestana("Historial")
        lote_data = payload.get("item", payload)
        
        # Lógica de Edición/Creación
        if lote_data.get("ID"):
            lote_id = lote_data.get("ID")
            for r in stock:
                if str(r.get("ID")) == str(lote_id):
                    r.update({k: v for k, v in lote_data.items() if k in r})
                    r["Kilos_Totales"] = int(lote_data.get("bolsas", 0)) * float(lote_data.get("kilosBolsa", r.get("Kilos_por_Bolsa", 40)))
        else:
            next_id = max([int(r.get("ID", 0)) for r in stock]) + 1 if stock else 1
            lote_data["ID"] = next_id
            lote_data["Kilos_Totales"] = int(lote_data.get("bolsas", 0)) * float(lote_data.get("kilosBolsa", 40))
            stock.append(lote_data)
            
        actualizar_pestana("Stock", stock)
        st.query_params.clear()
        st.rerun()

# Carga inicial de datos
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
/* ... (Mantiene todos tus estilos CSS originales) ... */
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const DB_STOCK = {js_stock};
const DB_HISTORIAL = {js_historial};
const DB_ORDENES = {js_ordenes};
const DB_CATALOGOS = {js_catalogos};

const {{ useState, useMemo, useEffect }} = React;

function App() {{
  const [tab, setTab] = useState("stock");
  // ... (Toda la lógica de componentes que ya funciona) ...
  
  return (
    <div className="app">
      <header className="hdr">
        <h1>La Clementina <span>· Semillero Interactive</span></h1>
        <div className="hdr-tabs">
          <button className={{"tab " + (tab==="stock"?"active":"")}} onClick={{() => setTab("stock")}}>📊 Stock</button>
          {/* ... otros botones de tab ... */}
        </div>
      </header>
      
      {/* SECCIÓN ÓRDENES (Limpia de WhatsApp) */}
      {{tab === "ordenes" && (
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
      )}}
      
      {/* IMPORTANTE: Sin footer, sin autoría, sin botones de WhatsApp */}
    </div>
  );
}}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
</script>
</body>
</html>
"""

st.components.v1.html(html_content, height=1200)
