import streamlit as st
import pandas as pd
import json
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# ==============================================================================
# 1. CONFIGURACIÓN Y CONEXIÓN SEGURA
# ==============================================================================
st.set_page_config(page_title="La Clementina · Stock", layout="wide", initial_sidebar_state="collapsed")

# Inicialización segura
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    conn = None

def leer_datos(sheet_name):
    if conn is None: return []
    try:
        df = conn.read(worksheet=sheet_name, ttl=0)
        return df.fillna("").to_dict(orient="records") if df is not None else []
    except: return []

def guardar_datos(sheet_name, lista_datos):
    if conn is not None and lista_datos:
        conn.update(worksheet=sheet_name, data=pd.DataFrame(lista_datos))

# ==============================================================================
# 2. PROCESAMIENTO DE ACCIONES (CORREGIDO)
# ==============================================================================
# USAMOS .get() PARA EVITAR EL ERROR DE NoneType
params = st.query_params
action = params.get("action") 

if action:
    raw_payload = params.get("payload", "{}")
    try:
        payload = json.loads(raw_payload)
    except: payload = {}
    
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    if action == "save_lote":
        stock = leer_datos("Stock")
        historial = leer_datos("Historial")
        item = payload.get("item", {})
        
        if item.get("ID"):
            stock = [item if str(r.get("ID")) == str(item.get("ID")) else r for r in stock]
            historial.append({"Fecha": now, "Tipo": "EDICION", "Detalle": f"Modificó {item.get('Variedad')}", "Operario": "Ignacio Diaz"})
        else:
            item["ID"] = max([int(r.get("ID", 0)) for r in stock] + [0]) + 1
            stock.append(item)
            historial.append({"Fecha": now, "Tipo": "INGRESO", "Detalle": f"Nuevo lote {item['ID']}", "Operario": "Ignacio Diaz"})
            
        guardar_datos("Stock", stock)
        guardar_datos("Historial", historial)
        st.query_params.clear()
        st.rerun()

    elif action == "move_lote":
        stock = leer_datos("Stock")
        mov = payload.get("mov", {})
        if mov:
            lote_id = int(mov.get("loteId", 0))
            cant = int(mov.get("cantidad", 0))
            for lote in stock:
                if int(lote.get("ID", 0)) == lote_id:
                    lote["Bolsas"] = int(lote["Bolsas"]) - cant
                    break
            guardar_datos("Stock", stock)
        st.query_params.clear()
        st.rerun()

# ==============================================================================
# 3. INTERFAZ FRONTEND
# ==============================================================================
# Cargamos los datos para inyectar en el JS
data_stock = json.dumps(leer_datos("Stock"))

html_code = f"""
<!DOCTYPE html>
<html>
<body>
    <div id="root"></div>
    <script>
        const DB_STOCK = {data_stock};
    </script>
    <script type="text/babel">
        function App() {{
            return (
                <div style={{{{padding: "20px", background: "white", borderRadius: "8px"}}}}>
                    <h1>La Clementina · Control de Semillas</h1>
                    <p>Estado del sistema: <b>Conectado</b></p>
                    <p>Lotes actuales: {{DB_STOCK.length}}</p>
                </div>
            );
        }}
        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</body>
</html>
"""

st.components.v1.html(html_code, height=600)
