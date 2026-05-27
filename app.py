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
# 2. CONEXIÓN Y LÓGICA DE DATOS
# ==============================================================================
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    st.error("⚠️ Error al conectar con Google Sheets.")
    st.stop()

def leer_pestana(sheet_name):
    try:
        df = conn.read(worksheet=sheet_name, ttl=0)
        return df.fillna("").to_dict(orient="records")
    except: return []

def actualizar_pestana(sheet_name, lista_datos):
    if lista_datos:
        conn.update(worksheet=sheet_name, data=pd.DataFrame(lista_datos))

# ==============================================================================
# 3. PROCESAMIENTO DE ACCIONES
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
            lote_id = int(lote_data["ID"])
            stock = [r if str(r.get("ID")) != str(lote_id) else {
                **r, 
                "Campaña": lote_data.get("campaña"), "Especie": lote_data.get("especie"),
                "Variedad": lote_data.get("variedad"), "Categoría": lote_data.get("categoría"),
                "Depósito": lote_data.get("depósito"), "Bolsas": int(lote_data.get("bolsas", 0)),
                "Kilos_Totales": int(lote_data.get("bolsas", 0)) * float(r.get("Kilos_por_Bolsa", 40)),
                "Notas": lote_data.get("notas")
            } for r in stock]
            historial.append({"Fecha": now_str, "Tipo": "EDICION", "Detalle": f"Modificado ID {lote_id}", "Bolsas": 0, "Kilos": 0, "Operario": "Ignacio Diaz"})
        else:
            next_id = max([int(r.get("ID", 0)) for r in stock]) + 1 if stock else 1
            stock.append({"ID": next_id, **lote_data, "Kilos_Totales": int(lote_data.get("bolsas", 0)) * 40})
            historial.append({"Fecha": now_str, "Tipo": "INGRESO", "Detalle": f"Alta ID {next_id}", "Bolsas": int(lote_data.get("bolsas", 0)), "Kilos": int(lote_data.get("bolsas", 0))*40, "Operario": "Ignacio Diaz"})
            
        actualizar_pestana("Stock", stock)
        actualizar_pestana("Historial", historial)
        st.query_params.clear()
        st.rerun()

    elif action == "move_lote":
        stock = leer_pestana("Stock")
        historial = leer_pestana("Historial")
        ordenes = leer_pestana("Ordenes")
        mov = payload.get("mov")
        lote_id = int(mov.get("loteId"))
        cant = int(mov.get("cantidad"))
        
        for lote in stock:
            if int(lote.get("ID", 0)) == lote_id:
                lote["Bolsas"] = int(lote["Bolsas"]) - cant
                lote["Kilos_Totales"] = int(lote["Bolsas"]) * float(lote.get("Kilos_por_Bolsa", 40))
                kg_movidos = cant * float(lote.get("Kilos_por_Bolsa", 40))
                
                if mov.get("tipo") == "transfer":
                    next_id_t = max([int(r.get("ID", 0)) for r in stock]) + 1
                    nuevo_lote = {**lote, "ID": next_id_t, "Depósito": mov.get("destino"), "Bolsas": cant, "Kilos_Totales": kg_movidos, "Notas": f"Traspaso"}
                    stock.append(nuevo_lote)
                    historial.append({"Fecha": now_str, "Tipo": "TRANSFERENCIA", "Detalle": f"De {lote['Depósito']} a {mov['destino']}", "Bolsas": cant, "Kilos": kg_movidos, "Operario": "Ignacio Diaz"})
                else:
                    proxima_oc = max([int(o.get("ID_Orden", 0)) for o in ordenes]) + 1 if ordenes else 5001
                    ordenes.append({"ID_Orden": proxima_oc, "Fecha": now_str, "Variedad": lote["Variedad"], "Depósito": lote["Depósito"], "Bolsas": cant, "Kilos": kg_movidos, "Cliente": mov.get("cliente", ""), "Patente_Chasis": mov.get("chasis", ""), "Estado": "DESPACHADO"})
                    historial.append({"Fecha": now_str, "Tipo": "EGRESO", "Detalle": f"OC {proxima_oc} para {mov.get('cliente', '')}", "Bolsas": cant, "Kilos": kg_movidos, "Operario": "Ignacio Diaz"})
                break
        
        actualizar_pestana("Stock", stock)
        actualizar_pestana("Historial", historial)
        if mov.get("tipo") == "egreso": actualizar_pestana("Ordenes", ordenes)
        st.query_params.clear()
        st.rerun()

# ==============================================================================
# 4. FRONTEND (HTML/REACT)
# ==============================================================================
html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.2/babel.min.js"></script>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;700&family=Barlow:wght@400;500&display=swap');
    :root {{ --bg:#f4f6f9; --accent:#e07b00; --text:#1a1e2e; --border:#dde1ea; --panel:#fff; }}
    body {{ font-family: 'Barlow', sans-serif; background: var(--bg); margin:0; padding:20px; }}
    .overlay {{ position:fixed; inset:0; background:rgba(0,0,0,0.5); display:flex; align-items:center; justify-content:center; }}
    .modal {{ background:white; padding:20px; border-radius:10px; width:400px; }}
    .form-grid {{ display:grid; gap:10px; }}
    input, select {{ width:100%; padding:8px; margin:5px 0; border:1px solid var(--border); }}
    .btn {{ padding:10px; cursor:pointer; border:none; border-radius:5px; }}
    .btn-save {{ background:var(--accent); color:white; }}
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const {{ useState }} = React;

function MoveModal({{ item, onSave, onClose }}) {{
    const [tipo, setTipo] = useState("transfer");
    const [cantidad, setCantidad] = useState(1);
    const [destino, setDestino] = useState("");
    const [cliente, setCliente] = useState("");
    const [chasis, setChasis] = useState("");

    return (
        <div className="overlay">
            <form className="modal" onSubmit={{(e) => {{
                e.preventDefault();
                onSave({{ mov: {{ loteId: item.ID, tipo, cantidad, destino, cliente, chasis }} }});
            }}}}>
                <h2>Movimiento: {{item.Variedad}}</h2>
                <div className="form-grid">
                    <label>Tipo</label>
                    <select value={{tipo}} onChange={{e => setTipo(e.target.value)}}>
                        <option value="transfer">Traspaso</option>
                        <option value="egreso">Egreso Comercial</option>
                    </select>
                    <label>Cantidad (bolsas)</label>
                    <input type="number" value={{cantidad}} onChange={{e => setCantidad(e.target.value)}} required />
                    
                    {{tipo === "transfer" ? (
                        <>
                            <label>Depósito Destino</label>
                            <input value={{destino}} onChange={{e => setDestino(e.target.value)}} required />
                        </>
                    ) : (
                        <>
                            <label>Cliente</label>
                            <input value={{cliente}} onChange={{e => setCliente(e.target.value)}} required />
                            <label>Patente Chasis</label>
                            <input value={{chasis}} onChange={{e => setChasis(e.target.value)}} />
                        </>
                    )}}
                </div>
                <div style={{{marginTop: 20, display:'flex', gap:10}}}>
                    <button type="button" className="btn" onClick={{onClose}}>Cancelar</button>
                    <button type="submit" className="btn btn-save">Confirmar</button>
                </div>
            </form>
        </div>
    );
}}

function App() {{
    const [modal, setModal] = useState(null);
    return (
        <div>
            <h1>La Clementina</h1>
            <button onClick={{() => setModal({{ mode: "move", item: {{ ID: 1, Variedad: "Test" }} }})}}>Probar Modal Movimiento</button>
            
            {{modal?.mode === "move" && (
                <MoveModal 
                    item={{modal.item}} 
                    onSave={{(mov) => {{ 
                        window.parent.location.search = `?action=move_lote&payload=${{encodeURIComponent(JSON.stringify(mov))}}`; 
                    }}}} 
                    onClose={{() => setModal(null)}} 
                />
            )}}
            <footer style={{{marginTop: 50, color:'#666'}}}>Creado por Ignacio Diaz</footer>
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
