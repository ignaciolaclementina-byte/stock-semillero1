import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import json
from datetime import datetime

# Configuración básica
st.set_page_config(page_title="La Clementina", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>iframe { width: 100%; height: 100vh; border: none; } [data-testid='stHeader'] { display: none; }</style>", unsafe_allow_html=True)

# Conexión
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data(ws): 
    try: return conn.read(worksheet=ws, ttl=0).fillna("").to_dict(orient="records")
    except: return []

# Lógica de procesamiento (Backend)
if "action" in st.query_params:
    action = st.query_params["action"]
    payload = json.loads(st.query_params.get("payload", "{}"))
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    stock = get_data("Stock")
    historial = get_data("Historial")
    ordenes = get_data("Ordenes")

    if action == "save_lote":
        # (Tu lógica de guardado aquí)
        pass 
    elif action == "move_lote":
        # (Tu lógica de movimiento aquí)
        pass

    st.query_params.clear()
    st.rerun()

# Preparación de datos
js_data = json.dumps({
    "stock": get_data("Stock"),
    "historial": get_data("Historial"),
    "ordenes": get_data("Ordenes"),
    "catalogos": get_data("Catalogos")
})

# HTML/REACT BLINDADO
# Usamos un bloque de texto multilínea sin f-strings para evitar conflictos con %
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</head>
<body>
    <div id="root"></div>
    <script type="text/babel">
        const DB = {js_data};
        function App() {{
            return (
                <div style={{{{padding: '20px'}}}}>
                    <h1>La Clementina</h1>
                    <p>Sistema cargado con {{{{DB.stock.length}}}} lotes.</p>
                    <small>Creado por Ignacio Diaz</small>
                </div>
            );
        }}
        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
"""

st.components.v1.html(html_code, height=800)
