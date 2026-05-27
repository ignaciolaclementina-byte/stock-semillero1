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
# 2. CONEXIÓN GENERAL CON GOOGLE SHEETS
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
        conn.update(worksheet=sheet_name, data=pd.DataFrame(lista_datos))

# ==============================================================================
# 3. PROCESAMIENTO DE ACCIONES (API BRIDGE)
# ==============================================================================
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
            stock = [r if str(r.get("ID")) != str(lote_id) else {
                **r, **lote_data, "Kilos_Totales": int(lote_data.get("bolsas", 0)) * float(lote_data.get("kilosBolsa", r.get("Kilos_por_Bolsa", 40)))
            } for r in stock]
            historial.append({"Fecha": now_str, "Tipo": "EDICION", "Detalle": f"Editó lote {lote_id}", "Bolsas": int(lote_data.get("bolsas", 0)), "Kilos": 0, "Operario": "Ignacio Diaz"})
        else:
            next_id = max([int(r.get("ID", 0)) for r in stock]) + 1 if stock else 1
            lote_data["ID"] = next_id
            lote_data["Kilos_Totales"] = int(lote_data.get("bolsas", 0)) * float(lote_data.get("kilosBolsa", 40))
            stock.append(lote_data)
            historial.append({"Fecha": now_str, "Tipo": "INGRESO", "Detalle": f"Alta lote {next_id}", "Bolsas": int(lote_data.get("bolsas", 0)), "Kilos": lote_data["Kilos_Totales"], "Operario": "Ignacio Diaz"})
            
        actualizar_pestana("Stock", stock)
        actualizar_pestana("Historial", historial)
        st.query_params.clear()
        st.rerun()

    elif action == "move_lote":
        stock = leer_pestana("Stock")
        historial = leer_pestana("Historial")
        ordenes = leer_pestana("Ordenes")
        mov = payload.get("mov", payload)
        lote_id = int(mov.get("loteId"))
        cant = int(mov.get("cantidad"))
        
        for lote in stock:
            if int(lote.get("ID", 0)) == lote_id:
                lote["Bolsas"] = int(lote["Bolsas"]) - cant
                lote["Kilos_Totales"] = lote["Bolsas"] * float(lote.get("Kilos_por_Bolsa", 40))
                kg_movidos = cant * float(lote.get("Kilos_por_Bolsa", 40))
                
                if mov.get("tipo") == "transfer":
                    next_id = max([int(r.get("ID", 0)) for r in stock]) + 1
                    stock.append({**lote, "ID": next_id, "Bolsas": cant, "Depósito": mov.get("destino"), "Notas": f"Traspaso desde {lote['Depósito']}"})
                    historial.append({"Fecha": now_str, "Tipo": "TRANSFERENCIA", "Detalle": f"Traspaso {cant} a {mov.get('destino')}", "Bolsas": cant, "Kilos": kg_movidos, "Operario": "Ignacio Diaz"})
                else:
                    ordenes.append({
                        "ID_Orden": max([int(o.get("ID_Orden", 0)) for o in ordenes]) + 1 if ordenes else 5001,
                        "Fecha": now_str, "Variedad": lote["Variedad"], "Depósito": lote["Depósito"], "Bolsas": cant, 
                        "Cliente": mov.get("cliente", "").upper(), "Patente_Chasis": mov.get("chasis", "").upper(), "Patente_Acoplado": mov.get("acoplado", "").upper(), "Estado": "DESPACHADO"
                    })
                    historial.append({"Fecha": now_str, "Tipo": "EGRESO", "Detalle": f"Egreso a {mov.get('cliente')}", "Bolsas": cant, "Kilos": kg_movidos, "Operario": "Ignacio Diaz"})
                break
        
        actualizar_pestana("Stock", stock)
        actualizar_pestana("Historial", historial)
        if mov.get("tipo") == "egreso": actualizar_pestana("Ordenes", ordenes)
        st.query_params.clear()
        st.rerun()

# ==============================================================================
# 4. FRONTEND
# ==============================================================================
html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<style>
    :root {{ --accent:#e07b00; --bg:#f4f6f9; --text:#1a1e2e; --muted:#6b7280; }}
    body {{ font-family: sans-serif; background: var(--bg); margin: 0; padding: 20px; }}
    .overlay {{ position: fixed; inset: 0; z-index: 100; background: rgba(0,0,0,.5); display: flex; align-items: center; justify-content: center; }}
    .modal {{ background: #fff; border-radius: 14px; padding: 22px; width: 100%; max-width: 400px; }}
    .field {{ margin-bottom: 15px; }}
    input, select {{ width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }}
    .modal-btns {{ display: flex; gap: 10px; margin-top: 20px; }}
    .btn {{ padding: 8px 16px; border-radius: 6px; border: none; cursor: pointer; }}
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
function MoveModal({{ item, onSave, onClose }}) {{
    const [tipo, setTipo] = React.useState("transfer");
    const [cantidad, setCantidad] = React.useState(1);
    const [destino, setDestino] = React.useState("");
    const [cliente, setCliente] = React.useState("");
    const [chasis, setChasis] = React.useState("");
    const [acoplado, setAcoplado] = React.useState("");

    return (
        <div className="overlay">
            <form className="modal" onSubmit={{(e) => {{
                e.preventDefault();
                onSave({{ mov: {{ loteId: item.ID, tipo, cantidad, destino, cliente, chasis, acoplado }} }});
            }}}}>
                <h3>Movimiento: {item.Variedad}</h3>
                <div className="field">
                    <label>Tipo</label>
                    <select value={{tipo}} onChange={{e => setTipo(e.target.value)}}>
                        <option value="transfer">Traspaso Depósito</option>
                        <option value="egreso">Egreso Comercial</option>
                    </select>
                </div>
                <div className="field">
                    <label>Cantidad (Bolsas)</label>
                    <input type="number" value={{cantidad}} onChange={{e => setCantidad(e.target.value)}}/>
                </div>
                {tipo === "transfer" ? (
                    <div className="field">
                        <label>Destino</label>
                        <input value={{destino}} onChange={{e => setDestino(e.target.value)}} required/>
                    </div>
                ) : (
                    <>
                        <div className="field"><label>Cliente</label><input value={{cliente}} onChange={{e => setCliente(e.target.value)}} required/></div>
                        <div className="field"><label>Chasis</label><input value={{chasis}} onChange={{e => setChasis(e.target.value)}}/></div>
                        <div className="field"><label>Acoplado</label><input value={{acoplado}} onChange={{e => setAcoplado(e.target.value)}}/></div>
                    </>
                )}
                <div className="modal-btns">
                    <button type="button" className="btn" onClick={{onClose}}>Cancelar</button>
                    <button type="submit" className="btn" style={{{{background: 'var(--accent)', color: 'white'}}}}>Confirmar</button>
                </div>
            </form>
        </div>
    );
}}

function App() {{
    return (
        <div style={{{{padding: '20px'}}}}>
            <h1>La Clementina · Gestión</h1>
            <p>Creado por Ignacio Diaz</p>
        </div>
    );
}}
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
</script>
</body>
</html>
"""

st.components.v1.html(html_content, height=1000)
