import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import json
from datetime import datetime

# ==============================================================================
# 1. CONFIGURACIÓN DEL PANEL DE STREAMLIT
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
        iframe { display: block; border: none; width: 100vw; height: 100vh; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. CONEXIÓN Y LÓGICA DE BACKEND
# ==============================================================================
conn = st.connection("gsheets", type=GSheetsConnection)

def leer_pestana(sheet_name):
    try:
        return conn.read(worksheet=sheet_name, ttl=0).fillna("").to_dict(orient="records")
    except: return []

def actualizar_pestana(sheet_name, lista_datos):
    if lista_datos: conn.update(worksheet=sheet_name, data=pd.DataFrame(lista_datos))

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
            stock = [r if str(r.get("ID")) != str(lote_data.get("ID")) else {
                "ID": int(lote_data["ID"]), "Campaña": lote_data["campaña"], "Especie": lote_data["especie"],
                "Variedad": lote_data["variedad"], "Categoría": lote_data["categoría"], "Depósito": lote_data["depósito"],
                "Bolsas": int(lote_data["bolsas"]), "Kilos_por_Bolsa": float(lote_data.get("kilosBolsa", 40)),
                "Kilos_Totales": int(lote_data["bolsas"]) * float(lote_data.get("kilosBolsa", 40)),
                "Estado": "DISPONIBLE", "Notas": lote_data["notas"]
            } for r in stock]
        else:
            next_id = max([int(r.get("ID", 0)) for r in stock]) + 1 if stock else 1
            stock.append({
                "ID": next_id, "Campaña": lote_data["campaña"], "Especie": lote_data["especie"],
                "Variedad": lote_data["variedad"], "Categoría": lote_data["categoría"], "Depósito": lote_data["depósito"],
                "Bolsas": int(lote_data["bolsas"]), "Kilos_por_Bolsa": 40.0,
                "Kilos_Totales": int(lote_data["bolsas"]) * 40.0, "Estado": "DISPONIBLE", "Notas": lote_data["notas"]
            })
        actualizar_pestana("Stock", stock)
        st.query_params.clear()
        st.rerun()

    elif action == "move_lote":
        stock = leer_pestana("Stock")
        ordenes = leer_pestana("Ordenes")
        mov = payload
        lote_id = int(mov.get("loteId"))
        cant = int(mov.get("cantidad"))
        
        for lote in stock:
            if int(lote.get("ID", 0)) == lote_id:
                lote["Bolsas"] = int(lote["Bolsas"]) - cant
                lote["Kilos_Totales"] = lote["Bolsas"] * float(lote.get("Kilos_por_Bolsa", 40))
                
                if mov.get("tipo") == "egreso":
                    proxima_oc = max([int(o.get("ID_Orden", 0)) for o in ordenes]) + 1 if ordenes else 5001
                    ordenes.append({
                        "ID_Orden": proxima_oc, "Fecha": now_str, "Variedad": lote["Variedad"],
                        "Depósito": lote["Depósito"], "Bolsas": cant, "Cliente": mov.get("cliente", "").upper(),
                        "Patente_Chasis": mov.get("chasis", "").upper(), "Estado": "DESPACHADO"
                    })
                    actualizar_pestana("Ordenes", ordenes)
                break
        actualizar_pestana("Stock", stock)
        st.query_params.clear()
        st.rerun()

# ==============================================================================
# 3. FRONTEND INTEGRAL (Inyectando datos al JS)
# ==============================================================================
data_stock = json.dumps(leer_pestana("Stock"))
data_ordenes = json.dumps(leer_pestana("Ordenes"))

html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.2/babel.min.js"></script>
<style>
    :root {{ --accent:#e07b00; --bg:#f4f6f9; }}
    body {{ font-family: sans-serif; background: var(--bg); }}
    .overlay {{ position:fixed; inset:0; background:rgba(0,0,0,.5); display:flex; align-items:center; justify-content:center; }}
    .modal {{ background:#fff; padding:20px; border-radius:10px; width:400px; }}
    footer {{ position:fixed; bottom:10px; right:20px; font-size:0.8rem; color:#888; }}
</style>
</head>
<body>
<div id="root"></div>
<footer>Creado por Ignacio Diaz</footer>
<script type="text/babel">
    const STOCK = {data_stock};
    const ORDENES = {data_ordenes};
    
    function App() {{
        const [modal, setModal] = React.useState(null);
        return (
            <div>
                <h1>Gestión La Clementina</h1>
                <button onClick={() => setModal("new")}>Nuevo Lote</button>
                <div style={{{marginTop: "20px"}}}>
                    {ORDENES.map(o => (
                        <div key={{o.ID_Orden}} style={{{background: "#fff", padding: "10px", margin: "5px 0", borderRadius: "5px"}}}>
                            OC #{o.ID_Orden} - {o.Variedad} ({o.Bolsas} bolsas) 
                            <a href={`https://api.whatsapp.com/send?text=Hola, te informo sobre la OC #{o.ID_Orden} de {o.Variedad}. Cantidad: {o.Bolsas} bolsas.`} target="_blank" style={{{marginLeft: "10px"}}}>
                                💬 Enviar WhatsApp
                            </a>
                        </div>
                    ))}
                </div>
            </div>
        );
    }}
    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(<App />);
</script>
</body>
</html>
"""

import streamlit.components.v1 as components
components.html(html_content, height=1000)
