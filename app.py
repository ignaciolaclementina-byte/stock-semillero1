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
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("⚠️ Error de conexión.")
    st.stop()

def leer_pestana(sheet_name):
    try:
        return conn.read(worksheet=sheet_name, ttl=0).fillna("").to_dict(orient="records")
    except Exception:
        return []

def actualizar_pestana(sheet_name, lista_datos):
    if lista_datos:
        conn.update(worksheet=sheet_name, data=pd.DataFrame(lista_datos))

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
                **r, "Campaña": lote_data.get("campaña"), "Especie": lote_data.get("especie"),
                "Variedad": lote_data.get("variedad"), "Categoría": lote_data.get("categoría"),
                "Depósito": lote_data.get("depósito"), "Bolsas": int(lote_data.get("bolsas", 0)),
                "Kilos_Totales": int(lote_data.get("bolsas", 0)) * float(r.get("Kilos_por_Bolsa", 40)),
                "Notas": lote_data.get("notas")
            } for r in stock]
            historial.append({"Fecha": now_str, "Tipo": "EDICION", "Detalle": f"Edición Lote ID {lote_id}", "Bolsas": int(lote_data.get("bolsas", 0)), "Operario": "Ignacio Diaz"})
        else:
            next_id = max([int(r.get("ID", 0)) for r in stock]) + 1 if stock else 1
            stock.append({
                "ID": next_id, "Campaña": lote_data.get("campaña"), "Especie": lote_data.get("especie"),
                "Variedad": lote_data.get("variedad"), "Categoría": lote_data.get("categoría"), "Depósito": lote_data.get("depósito"),
                "Bolsas": int(lote_data.get("bolsas", 0)), "Kilos_por_Bolsa": 40,
                "Kilos_Totales": int(lote_data.get("bolsas", 0)) * 40, "Estado": "DISPONIBLE", "Notas": lote_data.get("notas")
            })
            historial.append({"Fecha": now_str, "Tipo": "INGRESO", "Detalle": f"Alta Lote {next_id}", "Bolsas": int(lote_data.get("bolsas", 0)), "Operario": "Ignacio Diaz"})
        
        actualizar_pestana("Stock", stock)
        actualizar_pestana("Historial", historial)
        st.query_params.clear()
        st.rerun()

    elif action == "move_lote":
        stock, historial, ordenes = leer_pestana("Stock"), leer_pestana("Historial"), leer_pestana("Ordenes")
        mov = payload.get("mov", payload)
        lote_id = int(mov.get("loteId"))
        cant = int(mov.get("cantidad"))
        
        for lote in stock:
            if int(lote.get("ID", 0)) == lote_id:
                lote["Bolsas"] = int(lote["Bolsas"]) - cant
                lote["Kilos_Totales"] = lote["Bolsas"] * float(lote["Kilos_por_Bolsa"])
                
                if mov.get("tipo") == "transfer":
                    next_id_t = max([int(r.get("ID", 0)) for r in stock]) + 1
                    lote_dest = {**lote, "ID": next_id_t, "Depósito": mov.get("destino"), "Bolsas": cant, "Kilos_Totales": cant * float(lote["Kilos_por_Bolsa"]), "Notas": f"Traspaso desde {lote['Depósito']}"}
                    stock.append(lote_dest)
                    historial.append({"Fecha": now_str, "Tipo": "TRANSFERENCIA", "Detalle": f"Traspaso {lote['Variedad']} a {mov.get('destino')}", "Bolsas": cant, "Operario": "Ignacio Diaz"})
                else:
                    proxima_oc = max([int(o.get("ID_Orden", 0)) for o in ordenes]) + 1 if ordenes else 5001
                    ordenes.append({"ID_Orden": proxima_oc, "Fecha": now_str, "Variedad": lote["Variedad"], "Depósito": lote["Depósito"], "Bolsas": cant, "Cliente": mov.get("cliente", "").upper(), "Patente_Chasis": mov.get("chasis", "").upper(), "Estado": "DESPACHADO"})
                    historial.append({"Fecha": now_str, "Tipo": "EGRESO", "Detalle": f"OC #{proxima_oc} para {mov.get('cliente')}", "Bolsas": cant, "Operario": "Ignacio Diaz"})
                break
        
        actualizar_pestana("Stock", stock)
        actualizar_pestana("Historial", historial)
        if mov.get("tipo") == "egreso": actualizar_pestana("Ordenes", ordenes)
        st.query_params.clear()
        st.rerun()

# ==============================================================================
# 5. FRONTEND INTEGRAL (HTML/REACT)
# ==============================================================================
html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.2/babel.min.js"></script>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;700&family=Barlow:wght@400;500&display=swap');
    :root{{--bg:#f4f6f9;--accent:#e07b00;--blue:#1a7abf;--green:#2e8b57;--red:#c0392b;--text:#1a1e2e;}}
    body{{font-family:'Barlow',sans-serif; background:var(--bg);}}
    .app{{max-width:1300px;margin:0 auto;padding:20px;}}
    .btn{{padding:8px 16px;border-radius:8px;border:none;cursor:pointer;font-weight:700;}}
    .btn-save{{background:var(--accent);color:#fff;}}
    .overlay{{position:fixed;inset:0;background:rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;padding:20px;z-index:999;}}
    .modal{{background:#fff;padding:25px;border-radius:12px;width:100%;max-width:450px;}}
    .field{{margin-bottom:15px;}}
    input,select{{width:100%;padding:8px;border:1px solid #ccc;border-radius:6px;}}
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
            <form className="modal" onSubmit={{e => {{ e.preventDefault(); onSave({{ tipo, loteId: item.ID, cantidad, destino, cliente, chasis }}); }}}}>
                <h2>Movimiento de Stock: {item.Variedad}</h2>
                <div className="field">
                    <label>Tipo de Movimiento</label>
                    <select value={{tipo}} onChange={{e => setTipo(e.target.value)}}>
                        <option value="transfer">Traspaso entre Depósitos</option>
                        <option value="egreso">Egreso Comercial (Venta)</option>
                    </select>
                </div>
                <div className="field"><label>Cantidad (Bolsas)</label><input type="number" value={{cantidad}} onChange={{e => setCantidad(e.target.value)}}/></div>
                
                {{tipo === "transfer" ? (
                    <div className="field"><label>Depósito Destino</label><input type="text" value={{destino}} onChange={{e => setDestino(e.target.value)}} required/></div>
                ) : (
                    <>
                        <div className="field"><label>Cliente</label><input type="text" value={{cliente}} onChange={{e => setCliente(e.target.value)}} required/></div>
                        <div className="field"><label>Patente Chasis</label><input type="text" value={{chasis}} onChange={{e => setChasis(e.target.value)}} required/></div>
                    </>
                )}}
                <div style={{{display:"flex",gap:"10px"}}}>
                    <button type="button" className="btn" onClick={{onClose}}>Cancelar</button>
                    <button type="submit" className="btn btn-save">Confirmar Movimiento</button>
                </div>
            </form>
        </div>
    );
}}

// ... (El resto de tu lógica de la App se mantiene igual aquí)

</script>
</body>
</html>
"""

st.components.v1.html(html_content, height=1000)
