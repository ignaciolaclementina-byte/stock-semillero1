import streamlit as st
import pandas as pd
import json
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# ==============================================================================
# 1. CONFIGURACIÓN Y CONEXIÓN ROBUSTA
# ==============================================================================
st.set_page_config(page_title="La Clementina · Stock", layout="wide", initial_sidebar_state="collapsed")

# Inicialización segura de la conexión
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
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
# 2. PROCESAMIENTO DE ACCIONES (BACKEND)
# ==============================================================================
params = st.query_params
action = params.get("action")

if action:
    raw_payload = params.get("payload", "{}")
    try:
        payload = json.loads(raw_payload)
    except: payload = {}
    
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # Lógica de Guardado (Save/Edit)
    if action == "save_lote":
        stock = leer_datos("Stock")
        historial = leer_datos("Historial")
        item = payload.get("item", {})
        
        # Actualización o Nuevo
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

    # Lógica de Movimientos
    elif action == "move_lote":
        stock = leer_datos("Stock")
        ordenes = leer_datos("Ordenes")
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
# 3. INTERFAZ (FRONTEND REACT)
# ==============================================================================
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <style>
        body {{ font-family: sans-serif; background: #f4f6f9; padding: 20px; }}
        .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.1); }}
    </style>
</head>
<body>
    <div id="root"></div>
    <script type="text/babel">
        function App() {{
            return (
                <div className="card">
                    <h1>La Clementina · Control de Semillas</h1>
                    <p>Creado por Ignacio Diaz</p>
                    <hr/>
                    <p>Estado del sistema: <b>Conectado</b></p>
                </div>
            );
        }}
        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
"""

st.components.v1.html(html_code, height=600)
