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
except Exception as e:
    st.error("⚠️ Error al conectar con Google Sheets.")
    st.stop()

def leer_pestana(sheet_name):
    try:
        df = conn.read(worksheet=sheet_name, ttl=0)
        return df.fillna("").to_dict(orient="records")
    except Exception:
        return []

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
            lote_id = lote_data.get("ID")
            stock = [r if str(r.get("ID")) != str(lote_id) else {
                "ID": int(lote_id), 
                "Campaña": lote_data.get("campaña", r.get("Campaña")), 
                "Especie": lote_data.get("especie", r.get("Especie")),
                "Variedad": lote_data.get("variedad", r.get("Variedad")), 
                "Categoría": lote_data.get("categoría", r.get("Categoría")), 
                "Depósito": lote_data.get("depósito", r.get("Depósito")),
                "Bolsas": int(lote_data.get("bolsas", 0)), 
                "Kilos_por_Bolsa": float(lote_data.get("kilosBolsa", r.get("Kilos_por_Bolsa", 40))),
                "Kilos_Totales": int(lote_data.get("bolsas", 0)) * float(lote_data.get("kilosBolsa", r.get("Kilos_por_Bolsa", 40))),
                "Estado": lote_data.get("estado", r.get("Estado", "DISPONIBLE")), 
                "Notas": lote_data.get("notas", r.get("Notas"))
            } for r in stock]
            historial.append({"Fecha": now_str, "Tipo": "EDICION", "Detalle": f"Se modificaron datos del lote ID {lote_id}", "Bolsas": int(lote_data.get("bolsas", 0)), "Kilos": int(lote_data.get("bolsas", 0)) * 40, "Operario": "Ignacio Diaz"})
        else:
            next_id = max([int(r.get("ID", 0)) for r in stock]) + 1 if stock else 1
            stock.append({
                "ID": next_id, "Campaña": lote_data.get("campaña"), "Especie": lote_data.get("especie"),
                "Variedad": lote_data.get("variedad"), "Categoría": lote_data.get("categoría"), "Depósito": lote_data.get("depósito"),
                "Bolsas": int(lote_data.get("bolsas", 0)), "Kilos_por_Bolsa": 40,
                "Kilos_Totales": int(lote_data.get("bolsas", 0)) * 40, "Estado": "DISPONIBLE", "Notas": lote_data.get("notas")
            })
            historial.append({"Fecha": now_str, "Tipo": "INGRESO", "Detalle": f"Alta lote ID {next_id}", "Bolsas": int(lote_data.get("bolsas", 0)), "Kilos": int(lote_data.get("bolsas", 0)) * 40, "Operario": "Ignacio Diaz"})
            
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
                    next_id_t = max([int(r.get("ID", 0)) for r in stock]) + 1
                    lote_dest = lote.copy()
                    lote_dest["ID"] = next_id_t
                    lote_dest["Depósito"] = mov.get("destino")
                    lote_dest["Bolsas"] = cant
                    lote_dest["Kilos_Totales"] = kg_movidos
                    lote_dest["Notas"] = f"Traspasado desde {lote['Depósito']}"
                    stock.append(lote_dest)
                    historial.append({"Fecha": now_str, "Tipo": "TRANSFERENCIA", "Detalle": f"Traspaso: {lote['Variedad']} ({lote['Depósito']} -> {mov.get('destino')})", "Bolsas": cant, "Kilos": kg_movidos, "Operario": "Ignacio Diaz"})
                else:
                    proxima_oc = max([int(o.get("ID_Orden", 0)) for o in ordenes]) + 1 if ordenes else 5001
                    ordenes.append({
                        "ID_Orden": proxima_oc, "Fecha": now_str, "Campaña": lote["Campaña"],
                        "Especie": lote["Especie"], "Variedad": lote["Variedad"], "Depósito": lote["Depósito"],
                        "Bolsas": cant, "Kilos": kg_movidos, "Cliente": mov.get("cliente", "").upper(),
                        "Patente_Chasis": mov.get("chasis", "").upper(), "Patente_Acoplado": mov.get("acoplado", "").upper(),
                        "Estado": "DESPACHADO"
                    })
                    historial.append({"Fecha": now_str, "Tipo": "EGRESO", "Detalle": f"Despacho OC #{proxima_oc}: {lote['Variedad']} para {mov.get('cliente', '').upper()}", "Bolsas": cant, "Kilos": kg_movidos, "Operario": "Ignacio Diaz"})
                break
        
        actualizar_pestana("Stock", stock)
        actualizar_pestana("Historial", historial)
        if mov.get("tipo") == "egreso": actualizar_pestana("Ordenes", ordenes)
        st.query_params.clear()
        st.rerun()

# ==============================================================================
# 5. FRONTEND INTEGRAL
# ==============================================================================
data_stock = json.dumps(leer_pestana("Stock"))
data_historial = json.dumps(leer_pestana("Historial"))
data_ordenes = json.dumps(leer_pestana("Ordenes"))
data_catalogos = json.dumps(leer_pestana("Catalogos"))

html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>La Clementina</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.2/babel.min.js"></script>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const DB_STOCK = {data_stock};
const DB_HISTORIAL = {data_historial};
const DB_ORDENES = {data_ordenes};
const DB_CATALOGOS = {data_catalogos};
const {{ useState, useMemo, useEffect }} = React;
const fmt = n => Number(n).toLocaleString("es-AR");

function App() {{
  const [user, setUser] = useState(null);
  const [tab, setTab] = useState("stock");
  const [stock] = useState(DB_STOCK);
  const [historial] = useState(DB_HISTORIAL);
  const [ordenes] = useState(DB_ORDENES);
  const [catalogos] = useState(DB_CATALOGOS);
  const [modal, setModal] = useState(null);

  useEffect(() => {{
    const sesion = localStorage.getItem("lc_session");
    if(sesion) setUser(JSON.parse(sesion));
  }}, []);

  const handleLogin = (pass) => {{
    if(pass === "1234") {{ setUser({{ name: "Ignacio Diaz" }}); localStorage.setItem("lc_session", JSON.stringify({{ name: "Ignacio Diaz" }})); }}
  }};

  const handleSave = (item) => {{ window.parent.location.search = `?action=save_lote&payload=${{encodeURIComponent(JSON.stringify(item))}}`; }};
  const handleMove = (mov) => {{ window.parent.location.search = `?action=move_lote&payload=${{encodeURIComponent(JSON.stringify(mov))}}`; }};

  if(!user) return (
      <div style={{{display:'flex',justifyContent:'center',paddingTop:'100px'}}}>
        <div style={{{padding:40,background:'#fff',borderRadius:10,boxShadow:'0 4px 10px rgba(0,0,0,0.1)'}}}>
           <h1>La Clementina</h1>
           <input type="password" placeholder="Clave" onKeyDown={{e=>e.key==='Enter' && handleLogin(e.target.value)}}/>
           <button onClick={{(e)=>handleLogin(e.target.previousSibling.value)}}>Ingresar</button>
        </div>
      </div>
  );

  return (
    <div className="app">
        <header className="hdr">
            <h1>La Clementina</h1>
            <div className="hdr-tabs">
                <button className={{`tab ${{tab === "stock" ? "active" : ""}}`}} onClick={() => setTab("stock")}>STOCK</button>
                <button className={{`tab ${{tab === "ordenes" ? "active" : ""}}`}} onClick={() => setTab("ordenes")}>ÓRDENES</button>
            </div>
        </header>

        {{tab === "stock" && (
            <div className="table-wrap">
                <table>
                    <thead><tr><th>Variedad</th><th>Bolsas</th><th>Acciones</th></tr></thead>
                    <tbody>
                        {{stock.map(s => (
                            <tr key={{s.ID}}>
                                <td>{{s.Variedad}}</td>
                                <td>{{fmt(s.Bolsas)}}</td>
                                <td>
                                    <button onClick={{() => setModal({{ mode: "move", item: s }})}}>🚚 Despachar/Mover</button>
                                </td>
                            </tr>
                        ))}}
                    </tbody>
                </table>
            </div>
        )}}

        {{tab === "ordenes" && (
             <div className="table-wrap">
                <table>
                    <thead><tr><th>OC #</th><th>Cliente</th><th>Info</th><th>WhatsApp</th></tr></thead>
                    <tbody>
                        {{ordenes.map(o => {{
                            const msg = encodeURIComponent(`📦 *La Clementina - OC #${{o.ID_Orden}}*
------------------------
👤 Cliente: ${{o.Cliente}}
🌱 Variedad: ${{o.Variedad}}
🛍 Bolsas: ${{fmt(o.Bolsas)}}
🚚 Patente: ${{o.Patente_Chasis}} ${{o.Patente_Acoplado ? `+ ${{o.Patente_Acoplado}}` : ''}}
------------------------
Creado por Ignacio Diaz`);
                            return (
                                <tr key={{o.ID_Orden}}>
                                    <td>{{o.ID_Orden}}</td>
                                    <td>{{o.Cliente}}</td>
                                    <td>{{o.Variedad}}</td>
                                    <td><a href={{"https://api.whatsapp.com/send?text=" + msg}} target="_blank">Enviar</a></td>
                                </tr>
                            )
                        }})}}
                    </tbody>
                </table>
             </div>
        )}}

        {{modal?.mode === "move" && <MoveModal item={{modal.item}} onSave={{handleMove}} onClose={{() => setModal(null)}} />}}
        <footer style={{{marginTop:20,fontSize:'0.7rem',color:'#999'}}}>Creado por Ignacio Diaz</footer>
    </div>
  );
}}

function MoveModal({{ item, onSave, onClose }}) {{
  const [tipo, setTipo] = useState("transfer");
  const [cantidad, setCantidad] = useState(1);
  const [destino, setDestino] = useState("Planta 1");
  const [cliente, setCliente] = useState("");
  const [chasis, setChasis] = useState("");
  const [acoplado, setAcoplado] = useState("");

  return (
    <div className="overlay" style={{{position:'fixed',inset:0,background:'rgba(0,0,0,0.5)',display:'flex',justifyContent:'center',alignItems:'center'}}}>
      <form className="modal" style={{{background:'#fff',padding:20,borderRadius:10}}} onSubmit={{e => {{ e.preventDefault(); onSave({{ mov: {{ loteId: item.ID, tipo, cantidad, destino, cliente, chasis, acoplado }} }}); onClose(); }}}}>
        <h2>{{"Mover: " + item.Variedad}}</h2>
        <select value={{tipo}} onChange={{e => setTipo(e.target.value)}}>
            <option value="transfer">Transferencia</option>
            <option value="egreso">Egreso Comercial</option>
        </select>
        <input type="number" value={{cantidad}} onChange={{e => setCantidad(e.target.value)}} max={{item.Bolsas}} />
        {{tipo === "transfer" ? (
            <input type="text" placeholder="Destino" value={{destino}} onChange={{e => setDestino(e.target.value)}} />
        ) : (
            <>
                <input type="text" placeholder="Cliente" value={{cliente}} onChange={{e => setCliente(e.target.value)}} />
                <input type="text" placeholder="Patente Chasis" value={{chasis}} onChange={{e => setChasis(e.target.value)}} />
                <input type="text" placeholder="Patente Acoplado" value={{acoplado}} onChange={{e => setAcoplado(e.target.value)}} />
            </>
        )}}
        <button type="submit">Guardar</button>
        <button type="button" onClick={{onClose}}>Cancelar</button>
      </form>
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
