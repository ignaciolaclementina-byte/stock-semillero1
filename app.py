import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import json
from datetime import datetime
import streamlit.components.v1 as components

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
        
        if lote_data.get("ID") or lote_data.get("id"):
            lote_id = lote_data.get("ID") or lote_data.get("id")
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
            kilos_t = int(lote_data.get("bolsas", 0)) * 40
            stock.append({"ID": next_id, "Campaña": lote_data.get("campaña"), "Especie": lote_data.get("especie"), "Variedad": lote_data.get("variedad"), "Categoría": lote_data.get("categoría"), "Depósito": lote_data.get("depósito"), "Bolsas": int(lote_data.get("bolsas", 0)), "Kilos_por_Bolsa": 40, "Kilos_Totales": kilos_t, "Estado": "DISPONIBLE", "Notas": lote_data.get("notas")})
            historial.append({"Fecha": now_str, "Tipo": "INGRESO", "Detalle": f"Alta lote ID {next_id}", "Bolsas": int(lote_data.get("bolsas", 0)), "Kilos": kilos_t, "Operario": "Ignacio Diaz"})
            
        actualizar_pestana("Stock", stock)
        actualizar_pestana("Historial", historial)
        st.query_params.clear()
        st.rerun()

    elif action == "move_lote":
        stock = leer_pestana("Stock")
        historial = leer_pestana("Historial")
        ordenes = leer_pestana("Ordenes")
        mov = payload
        lote_id = int(mov.get("loteId"))
        cant = int(mov.get("cantidad"))
        
        for lote in stock:
            if int(lote.get("ID", 0)) == lote_id:
                lote["Bolsas"] = int(lote["Bolsas"]) - cant
                lote["Kilos_Totales"] = lote["Bolsas"] * 40
                kg_movidos = cant * 40
                
                if mov.get("tipo") == "transfer":
                    next_id_t = max([int(r.get("ID", 0)) for r in stock]) + 1
                    lote_dest = lote.copy()
                    lote_dest["ID"] = next_id_t
                    lote_dest["Depósito"] = mov.get("destino")
                    lote_dest["Bolsas"] = cant
                    lote_dest["Kilos_Totales"] = kg_movidos
                    lote_dest["Notas"] = f"Traspasado desde {lote['Depósito']}"
                    stock.append(lote_dest)
                    historial.append({"Fecha": now_str, "Tipo": "TRANSFERENCIA", "Detalle": f"Traspaso: {lote['Depósito']} -> {mov.get('destino')}", "Bolsas": cant, "Kilos": kg_movidos, "Operario": "Ignacio Diaz"})
                else:
                    proxima_oc = max([int(o.get("ID_Orden", 0)) for o in ordenes]) + 1 if ordenes else 5001
                    ordenes.append({"ID_Orden": proxima_oc, "Fecha": now_str, "Campaña": lote["Campaña"], "Especie": lote["Especie"], "Variedad": lote["Variedad"], "Depósito": lote["Depósito"], "Bolsas": cant, "Kilos": kg_movidos, "Cliente": mov.get("cliente", "").upper(), "Patente_Chasis": mov.get("chasis", "").upper(), "Estado": "DESPACHADO"})
                    historial.append({"Fecha": now_str, "Tipo": "EGRESO", "Detalle": f"Despacho OC #{proxima_oc}: {mov.get('cliente', '').upper()}", "Bolsas": cant, "Kilos": kg_movidos, "Operario": "Ignacio Diaz"})
                break
                
        actualizar_pestana("Stock", stock)
        actualizar_pestana("Historial", historial)
        if mov.get("tipo") == "egreso": actualizar_pestana("Ordenes", ordenes)
        st.query_params.clear()
        st.rerun()

# ==============================================================================
# 4. FRONTEND (HTML + REACT)
# ==============================================================================
# (El código JS sigue igual hasta el MoveModal)
html_content = """
... [INSERTAR AQUÍ TODO TU CÓDIGO HTML/JS ANTERIOR] ...
"""
# COMPLETANDO LA FUNCIÓN MoveModal QUE FALTABA
"""
function MoveModal({ item, onSave, onClose }) {
  const [tipo, setTipo] = useState("transfer");
  const [cantidad, setCantidad] = useState(1);
  const [destino, setDestino] = useState("");
  const [cliente, setCliente] = useState("");
  const [chasis, setChasis] = useState("");

  return (
    <div className="overlay">
      <form className="modal" onSubmit={e => { e.preventDefault(); onSave({ loteId: item.ID, tipo, cantidad, destino, cliente, chasis }); onClose(); }}>
        <h2>Movimiento: {item.Variedad}</h2>
        <div className="move-info">Stock actual: {item.Bolsas} bolsas</div>
        <div className="form-grid">
          <div className="field full">
            <label>Tipo de Movimiento</label>
            <select value={tipo} onChange={e => setTipo(e.target.value)}>
              <option value="transfer">Transferencia entre depósitos</option>
              <option value="egreso">Egreso Comercial (Despacho)</option>
            </select>
          </div>
          <div className="field full"><label>Cantidad (Bolsas)</label><input type="number" min="1" max={item.Bolsas} value={cantidad} onChange={e => setCantidad(e.target.value)} required/></div>
          {tipo === "transfer" && <div className="field full"><label>Depósito Destino</label><input type="text" value={destino} onChange={e => setDestino(e.target.value)} required/></div>}
          {tipo === "egreso" && (
            <>
              <div className="field full"><label>Cliente</label><input type="text" value={cliente} onChange={e => setCliente(e.target.value)} required/></div>
              <div className="field"><label>Chasis</label><input type="text" value={chasis} onChange={e => setChasis(e.target.value)}/></div>
            </>
          )}
        </div>
        <div className="modal-btns">
          <button type="button" className="btn-cancel" onClick={onClose}>Cancelar</button>
          <button type="submit" className="btn-save">Confirmar</button>
        </div>
      </form>
    </div>
  );
}
// Cierra el resto del código y el script (No olvidar cerrar todo correctamente)
"""

# IMPORTANTE: ESTA LÍNEA RENDERIZA EL FRONTEND
components.html(html_content, height=1000)
