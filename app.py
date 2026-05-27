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
# 2. CONEXIÓN Y LÓGICA (BACKEND)
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
            stock = [r if str(r.get("ID")) != str(lote_data.get("ID")) else {**r, **lote_data, "Bolsas": int(lote_data.get("bolsas", 0)), "Kilos_Totales": int(lote_data.get("bolsas", 0)) * float(lote_data.get("kilosBolsa", r.get("Kilos_por_Bolsa", 40)))} for r in stock]
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
        historial = leer_pestana("Historial")
        ordenes = leer_pestana("Ordenes")
        mov = payload.get("mov", payload)
        lote_id = int(mov.get("loteId"))
        cant = int(mov.get("cantidad"))
        for lote in stock:
            if int(lote.get("ID", 0)) == lote_id:
                lote["Bolsas"] = int(lote["Bolsas"]) - cant
                lote["Kilos_Totales"] = int(lote["Bolsas"]) * float(lote.get("Kilos_por_Bolsa", 40))
                if mov.get("tipo") == "transfer":
                    next_id_t = max([int(r.get("ID", 0)) for r in stock]) + 1
                    lote_dest = {**lote, "ID": next_id_t, "Depósito": mov.get("destino"), "Bolsas": cant, "Kilos_Totales": cant * float(lote.get("Kilos_por_Bolsa", 40))}
                    stock.append(lote_dest)
                else:
                    proxima_oc = max([int(o.get("ID_Orden", 0)) for o in ordenes]) + 1 if ordenes else 5001
                    ordenes.append({"ID_Orden": proxima_oc, "Fecha": now_str, "Variedad": lote["Variedad"], "Depósito": lote["Depósito"], "Bolsas": cant, "Cliente": mov.get("cliente", "").upper(), "Patente_Chasis": mov.get("chasis", "").upper(), "Estado": "DESPACHADO"})
                    actualizar_pestana("Ordenes", ordenes)
        actualizar_pestana("Stock", stock)
        st.query_params.clear()
        st.rerun()

js_stock = json.dumps(leer_pestana("Stock"))
js_historial = json.dumps(leer_pestana("Historial"))
js_ordenes = json.dumps(leer_pestana("Ordenes"))
js_catalogos = json.dumps(leer_pestana("Catalogos"))

# ==============================================================================
# 3. FRONTEND INTEGRAL (HTML5 + REACT)
# ==============================================================================
html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.2/babel.min.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500&display=swap');
:root{{--bg:#f4f6f9;--panel:#fff;--card:#fff;--border:#dde1ea;--accent:#e07b00;--blue:#1a7abf;--green:#2e8b57;--red:#c0392b;--muted:#6b7280;--fh:'Barlow Condensed',sans-serif;--fb:'Barlow',sans-serif;}}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);font-family:var(--fb)}
.app{max-width:1300px;margin:0 auto}
.login-wrap{{min-height:100vh;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#1a2a4a,#1e3660)}}
.login-box{{background:#fff;border-radius:16px;padding:40px;width:300px;text-align:center;box-shadow:0 8px 40px rgba(0,0,0,.2)}}
.hdr{{background:#1a2a4a;padding:20px;display:flex;justify-content:space-between;color:#fff;align-items:center}}
.tab{{background:transparent;border:none;color:#fff;padding:10px;cursor:pointer;font-family:var(--fh);font-weight:700;text-transform:uppercase}}
.tab.active{{color:var(--accent)}}
.kpi-strip{{display:grid;grid-template-columns:repeat(4,1fr);background:var(--panel);border-bottom:1px solid var(--border)}}
.kpi{{padding:15px;text-align:center}}
.kpi-val{{font-size:1.5rem;font-weight:800;font-family:var(--fh)}}
.kpi-lbl{{font-size:0.7rem;text-transform:uppercase;color:var(--muted)}}
.table-wrap{{overflow-x:auto;padding:20px}}
table{{width:100%;border-collapse:collapse;background:#fff}}
th,td{{padding:12px;border:1px solid #eee;text-align:left}}
.overlay{{position:fixed;inset:0;background:rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;padding:20px}}
.modal{{background:#fff;padding:25px;border-radius:12px;width:100%;max-width:400px}}
.field{{margin-bottom:10px}}
.field label{{display:block;font-size:.7rem;text-transform:uppercase;color:var(--muted)}}
.field input,.field select{{width:100%;padding:8px;border:1px solid var(--border);border-radius:6px}}
.modal-btns{{display:flex;justify-content:flex-end;gap:10px;margin-top:15px}}
.btn{{padding:8px 16px;border-radius:6px;border:none;cursor:pointer;font-family:var(--fh);text-transform:uppercase}}
.btn-save{{background:var(--accent);color:#fff}}
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const DB_STOCK = {js_stock};
const DB_ORDENES = {js_ordenes};
const {{ useState, useEffect }} = React;

function App() {{
    const [user, setUser] = useState(null);
    const [tab, setTab] = useState("stock");
    const [modal, setModal] = useState(null);

    useEffect(() => {{ const sesion = localStorage.getItem("lc_session"); if(sesion) setUser(JSON.parse(sesion)); }}, []);
    
    const handleLogin = (p) => {{ if(p === "1234") {{ setUser({{name: "Admin"}}); localStorage.setItem("lc_session", JSON.stringify({{name: "Admin"}})); }} }};
    const handleLogout = () => {{ setUser(null); localStorage.removeItem("lc_session"); }};
    
    if(!user) return <div className="login-wrap"><div className="login-box"><h1>La Clementina</h1><input type="password" className="field" placeholder="Clave" onKeyDown={{e => e.key === "Enter" && handleLogin(e.target.value)}}/></div></div>;

    return (
        <div className="app">
            <header className="hdr">
                <h1>La Clementina</h1>
                <div>
                    <button className={{`tab ${{tab==="stock"?"active":""}}`}} onClick={{()=>setTab("stock")}}>Stock</button>
                    <button className={{`tab ${{tab==="ordenes"?"active":""}}`}} onClick={{()=>setTab("ordenes")}}>Órdenes</button>
                    <button className="tab" onClick={{handleLogout}}>Salir</button>
                </div>
            </header>

            {{tab === "stock" && (
                <div className="table-wrap">
                    <button className="btn btn-save" onClick={{()=>setModal({{mode:"new"}})}}>+ Nuevo Lote</button>
                    <table>
                        <thead><tr><th>ID</th><th>Variedad</th><th>Bolsas</th><th>Acciones</th></tr></thead>
                        <tbody>
                            {{DB_STOCK.map(s => (
                                <tr key={{s.ID}}>
                                    <td>{{s.ID}}</td>
                                    <td>{{s.Variedad}}</td>
                                    <td>{{s.Bolsas}}</td>
                                    <td><button onClick={{()=>setModal({{mode:"move", item:s}})}}>Despachar</button></td>
                                </tr>
                            ))}}
                        </tbody>
                    </table>
                </div>
            )}}

            {{tab === "ordenes" && (
                <div className="table-wrap">
                    <table>
                        <thead><tr><th>OC #</th><th>Cliente</th><th>Bolsas</th></tr></thead>
                        <tbody>
                            {{DB_ORDENES.map(o => (
                                <tr key={{o.ID_Orden}}>
                                    <td>{{o.ID_Orden}}</td>
                                    <td>{{o.Cliente}}</td>
                                    <td>{{o.Bolsas}}</td>
                                </tr>
                            ))}}
                        </tbody>
                    </table>
                </div>
            )}}

            {{modal?.mode === "new" && <ModalForm onSave={{i => window.parent.location.search = `?action=save_lote&payload=${{encodeURIComponent(JSON.stringify({{item:i}}))}}`}} onClose={{()=>setModal(null)}}/>}}
            {{modal?.mode === "move" && <MoveModal item={{modal.item}} onSave={{m => window.parent.location.search = `?action=move_lote&payload=${{encodeURIComponent(JSON.stringify({{mov:m}}))}}`}} onClose={{()=>setModal(null)}}/>}}
        </div>
    );
}}

function ModalForm({{ onClose, onSave }}) {{
    const [variedad, setVariedad] = useState("");
    const [bolsas, setBolsas] = useState(0);
    return (
        <div className="overlay">
            <form className="modal" onSubmit={{e => {{e.preventDefault(); onSave({{variedad, bolsas}});}}}}>
                <h2>Nuevo Lote</h2>
                <div className="field"><label>Variedad</label><input onChange={{e=>setVariedad(e.target.value)}} required/></div>
                <div className="field"><label>Bolsas</label><input type="number" onChange={{e=>setBolsas(e.target.value)}} required/></div>
                <div className="modal-btns">
                    <button type="button" onClick={{onClose}}>Cancelar</button>
                    <button type="submit" className="btn btn-save">Guardar</button>
                </div>
            </form>
        </div>
    );
}}

function MoveModal({{ item, onSave, onClose }}) {{
    const [tipo, setTipo] = useState("egreso");
    const [cantidad, setCantidad] = useState(1);
    const [destino, setDestino] = useState("");
    const [cliente, setCliente] = useState("");
    const [chasis, setChasis] = useState("");

    return (
        <div className="overlay">
            <form className="modal" onSubmit={{e => {{e.preventDefault(); onSave({{loteId: item.ID, cantidad, tipo, destino, cliente, chasis}});}}}}>
                <h2>Movimiento: {{item.Variedad}}</h2>
                <div className="field">
                    <label>Tipo</label>
                    <select value={{tipo}} onChange={{e=>setTipo(e.target.value)}}>
                        <option value="egreso">Egreso Comercial</option>
                        <option value="transfer">Transferencia</option>
                    </select>
                </div>
                <div className="field"><label>Cantidad</label><input type="number" value={{cantidad}} onChange={{e=>setCantidad(parseInt(e.target.value))}}/></div>
                {{tipo === "transfer" && <div className="field"><label>Destino</label><input value={{destino}} onChange={{e=>setDestino(e.target.value)}}/></div>}}
                {{tipo === "egreso" && (
                    <>
                        <div className="field"><label>Cliente</label><input value={{cliente}} onChange={{e=>setCliente(e.target.value)}}/></div>
                        <div className="field"><label>Chasis</label><input value={{chasis}} onChange={{e=>setChasis(e.target.value)}}/></div>
                    </>
                )}}
                <div className="modal-btns">
                    <button type="button" onClick={{onClose}}>Cancelar</button>
                    <button type="submit" className="btn btn-save">Confirmar</button>
                </div>
            </form>
        </div>
    );
}}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
</script>
</body>
</html>
"""

st.components.v1.html(html_content, height=1000)
