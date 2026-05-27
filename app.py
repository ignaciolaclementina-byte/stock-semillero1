import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import json
from datetime import datetime

# ==============================================================================
# 1. CONFIGURACIÓN
# ==============================================================================
st.set_page_config(page_title="La Clementina · Stock Semillas", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""<style>.block-container{padding:0!important;max-width:100%!important;}[data-testid="stHeader"]{display:none!important;} footer{visibility:hidden!important;}</style>""", unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)

def leer_pestana(sheet_name):
    try: return conn.read(worksheet=sheet_name, ttl=0).fillna("").to_dict(orient="records")
    except: return []

def actualizar_pestana(sheet_name, lista_datos):
    if lista_datos: conn.update(worksheet=sheet_name, data=pd.DataFrame(lista_datos))

# ==============================================================================
# 2. PROCESAMIENTO DE ACCIONES
# ==============================================================================
query_params = st.query_params
if "action" in query_params:
    action = query_params["action"]
    payload = json.loads(query_params.get("payload", "{}"))
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    if action == "save_lote":
        stock = leer_pestana("Stock")
        lote_data = payload.get("item", payload)
        if lote_data.get("ID"):
            stock = [r if str(r.get("ID")) != str(lote_data["ID"]) else {**r, **lote_data} for r in stock]
        else:
            lote_data["ID"] = max([int(r.get("ID", 0)) for r in stock] + [0]) + 1
            stock.append(lote_data)
        actualizar_pestana("Stock", stock)
        st.query_params.clear()
        st.rerun()

    elif action == "move_lote":
        stock = leer_pestana("Stock")
        ordenes = leer_pestana("Ordenes")
        mov = payload.get("mov", payload)
        for lote in stock:
            if int(lote.get("ID", 0)) == int(mov.get("loteId")):
                lote["Bolsas"] = int(lote["Bolsas"]) - int(mov.get("cantidad"))
                if mov.get("tipo") == "transfer":
                    lote_dest = lote.copy()
                    lote_dest["ID"] = max([int(r.get("ID", 0)) for r in stock] + [0]) + 1
                    lote_dest["Depósito"] = mov.get("destino")
                    lote_dest["Bolsas"] = int(mov.get("cantidad"))
                    stock.append(lote_dest)
                else:
                    ordenes.append({"ID_Orden": len(ordenes)+5001, "Variedad": lote["Variedad"], "Bolsas": mov.get("cantidad"), "Cliente": mov.get("cliente")})
                    actualizar_pestana("Ordenes", ordenes)
        actualizar_pestana("Stock", stock)
        st.query_params.clear()
        st.rerun()

# ==============================================================================
# 3. FRONTEND
# ==============================================================================
js_stock = json.dumps(leer_pestana("Stock"))

html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.2/babel.min.js"></script>
    <style>
        body{{font-family:sans-serif; background:#f4f6f9; padding:20px;}}
        .modal{{background:white; padding:20px; border-radius:10px; position:fixed; top:20%; left:30%; width:40%; z-index:1000; box-shadow:0 0 10px rgba(0,0,0,0.2);}}
        .overlay{{position:fixed; inset:0; background:rgba(0,0,0,0.5); z-index:999;}}
    </style>
</head>
<body>
    <div id="root"></div>
    <script type="text/babel">
        const stock = {js_stock};
        const {{ useState }} = React;

        function App() {{
            const [modal, setModal] = useState(null);
            return (
                <div>
                    <h1>La Clementina</h1>
                    <table>
                        <thead><tr><th>Variedad</th><th>Bolsas</th><th>Acciones</th></tr></thead>
                        <tbody>
                            {{stock.map(item => (
                                <tr key={{item.ID}}>
                                    <td>{{item.Variedad}}</td>
                                    <td>{{item.Bolsas}}</td>
                                    <td><button onClick={{() => setModal({{mode:"move", item}})}} >Despachar</button></td>
                                </tr>
                            ))}}
                        </tbody>
                    </table>
                    {{modal && <MoveModal item={{modal.item}} onClose={{() => setModal(null)}} />}}
                </div>
            );
        }}

        function MoveModal({{ item, onClose }}) {{
            const [cant, setCant] = useState(1);
            const [tipo, setTipo] = useState("egreso");
            const handleSave = () => {{
                window.parent.location.search = `?action=move_lote&payload={{"{{"}} "mov": {{{"{{"}}} "loteId": {{item.ID}}, "cantidad": {{cant}}, "tipo": "{{tipo}}" {{{{"}}}}} }}}`;
            }};
            return (
                <div className="overlay">
                    <div className="modal">
                        <h2>Despachar {item.Variedad}</h2>
                        <input type="number" value={{cant}} onChange={{e => setCant(e.target.value)}} />
                        <button onClick={{handleSave}}>Confirmar</button>
                        <button onClick={{onClose}}>Cancelar</button>
                    </div>
                </div>
            );
        }}
        const container = document.getElementById('root');
        const root = ReactDOM.createRoot(container);
        root.render(<App />);
    </script>
</body>
</html>
"""
st.components.v1.html(html_content, height=800)
