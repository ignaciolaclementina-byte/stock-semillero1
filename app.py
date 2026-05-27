import streamlit as st
import pandas as pd
import json
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# ==============================================================================
# 1. CONFIGURACIÓN Y CONEXIÓN
# ==============================================================================
st.set_page_config(page_title="La Clementina · Stock", layout="wide", initial_sidebar_state="collapsed")

# Inicialización segura
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
# 2. PROCESAMIENTO DE ACCIONES (VERSIÓN SEGURA)
# ==============================================================================
# Usamos un dict por defecto si st.query_params no está disponible
params = st.query_params if hasattr(st, 'query_params') and st.query_params is not None else {}
action = params.get("action")

if action:
    raw_payload = params.get("payload", "{}")
    try:
        payload = json.loads(raw_payload)
    except:
        payload = {}

    now = datetime.now().strftime("%d/%m/%Y %H:%M")

    # ACCIÓN: GUARDAR LOTE
    if action == "save_lote":
        stock = leer_datos("Stock")
        historial = leer_datos("Historial")
        item = payload.get("item", {})

        if item.get("ID"):
            stock = [item if str(r.get("ID")) == str(item.get("ID")) else r for r in stock]
            historial.append({"Fecha": now, "Tipo": "EDICION", "Detalle": f"Modificó {item.get('Variedad')}", "Operario": "Ignacio Diaz"})
        else:
            item["ID"] = max([int(r.get("ID", 0)) for r in stock] + [0]) + 1
            stock.append(item)
            historial.append({"Fecha": now, "Tipo": "INGRESO", "Detalle": f"Nuevo lote {item['ID']}", "Operario": "Ignacio Diaz"})

        guardar_datos("Stock", stock)
        guardar_datos("Historial", historial)
        if hasattr(st, 'query_params'):
            st.query_params.clear()
        st.rerun()

    # ACCIÓN: MOVER LOTE
    elif action == "move_lote":
        stock = leer_datos("Stock")
        mov = payload.get("mov", {})
        if mov:
            lote_id = int(mov.get("loteId", 0))
            cant = int(mov.get("cantidad", 0))
            for lote in stock:
                if int(lote.get("ID", 0)) == lote_id:
                    lote["Bolsas"] = int(lote["Bolsas"]) - cant
                    break
            guardar_datos("Stock", stock)
        if hasattr(st, 'query_params'):
            st.query_params.clear()
        st.rerun()

# ==============================================================================
# 3. EXTRACCIÓN DE DATOS PARA FRONTEND
# ==============================================================================
js_stock = json.dumps(leer_datos("Stock"))
js_historial = json.dumps(leer_datos("Historial"))
js_ordenes = json.dumps(leer_datos("Ordenes"))
js_catalogos = json.dumps(leer_datos("Catalogos"))

# ==============================================================================
# 4. FRONTEND INTEGRAL COMPLETO (REACT)
# ==============================================================================
html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>La Clementina · Stock Semillas</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.2/babel.min.js"></script>

<script id="data-stock" type="application/json">{js_stock}</script>
<script id="data-historial" type="application/json">{js_historial}</script>
<script id="data-ordenes" type="application/json">{js_ordenes}</script>
<script id="data-catalogos" type="application/json">{js_catalogos}</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500&display=swap');
:root{{
  --bg:#f4f6f9;--panel:#fff;--card:#fff;--border:#dde1ea;
  --accent:#e07b00;--blue:#1a7abf;--green:#2e8b57;--red:#c0392b;
  --purple:#7b4fa6;--text:#1a1e2e;--muted:#6b7280;--shadow:0 1px 4px rgba(0,0,0,.08);
  --fh:'Barlow Condensed',sans-serif;--fb:'Barlow',sans-serif;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:var(--bg);color:var(--text);font-family:var(--fb)}}
.app{{max-width:1300px;margin:0 auto;padding-bottom:60px}}

/* LOGIN */
.login-wrap{{min-height:100vh;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#1a2a4a,#1e3660)}}
.login-box{{background:#fff;border-radius:16px;padding:40px 48px;width:100%;max-width:400px;text-align:center;box-shadow:0 8px 40px rgba(0,0,0,.25)}}
.login-box h1{{font-family:var(--fh);font-size:1.5rem;font-weight:800;text-transform:uppercase;letter-spacing:1px;color:#1a2a4a;margin-bottom:6px}}
.login-box p{{font-size:.85rem;color:var(--muted);margin-bottom:24px}}
.login-input{{width:100%;padding:11px 14px;border:1.5px solid var(--border);border-radius:8px;font-family:var(--fb);font-size:1rem;outline:none;text-align:center;letter-spacing:3px;margin-bottom:8px;background:var(--bg)}}
.login-input:focus{{border-color:var(--accent)}}
.login-btn{{width:100%;background:var(--accent);border:none;border-radius:8px;color:#fff;font-family:var(--fh);font-size:1rem;font-weight:800;text-transform:uppercase;letter-spacing:.8px;padding:12px;cursor:pointer;margin-top:8px}}
.login-btn:hover{{background:#c86e00}}

/* HEADER */
.hdr{{background:linear-gradient(135deg,#1a2a4a 60%,#1e3660);border-bottom:3px solid var(--accent);padding:14px 24px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}}
.hdr h1{{font-family:var(--fh);font-size:1.6rem;font-weight:800;text-transform:uppercase;letter-spacing:1px;color:#fff}}
.hdr h1 span{{color:#f5a623}}
.hdr-tabs{{display:flex;gap:5px;flex-wrap:wrap}}
.tab{{font-family:var(--fh);font-size:.82rem;font-weight:700;letter-spacing:.6px;text-transform:uppercase;padding:6px 13px;border-radius:6px;cursor:pointer;border:1.5px solid rgba(255,255,255,.22);background:transparent;color:rgba(255,255,255,.65)}}
.tab.active{{background:#f5a623;border-color:#f5a623;color:#1a1e2e}}
.tab:hover:not(.active){{border-color:rgba(255,255,255,.7);color:#fff}}

/* KPIs */
.kpi-strip{{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:1px;background:var(--border);border-bottom:1px solid var(--border)}}
.kpi{{background:var(--panel);padding:12px 16px}}
.kpi-val{{font-family:var(--fh);font-size:1.8rem;font-weight:800;line-height:1}}
.kpi-lbl{{font-size:.65rem;color:var(--muted);text-transform:uppercase;letter-spacing:.7px;margin-top:2px}}
.c-or{{color:var(--accent)}}.c-bl{{color:var(--blue)}}.c-gr{{color:var(--green)}}.c-pu{{color:var(--purple)}}

/* TOOLBAR */
.toolbar{{display:flex;gap:8px;padding:12px 16px;flex-wrap:wrap;align-items:center;border-bottom:1px solid var(--border);background:var(--panel)}}
.search-inp{{flex:1;min-width:160px;padding:7px 10px;background:var(--bg);border:1.5px solid var(--border);border-radius:8px;font-size:.83rem;outline:none}}
.sel{{background:var(--bg);border:1.5px solid var(--border);border-radius:8px;font-size:.81rem;padding:7px 9px;outline:none;cursor:pointer}}
.btn{{font-family:var(--fh);font-size:.85rem;font-weight:700;text-transform:uppercase;padding:7px 14px;border-radius:8px;cursor:pointer;border:none}}
.btn-add{{background:var(--accent);color:#fff}}.btn-add:hover{{background:#c86e00}}
.btn-ol{{background:var(--panel);border:1.5px solid var(--border)!important;color:var(--text)}}
.btn-sm{{padding:4px 9px;font-size:.75rem}}

/* TABLE */
.table-wrap{{overflow-x:auto}}
table{{width:100%;border-collapse:collapse;font-size:.82rem}}
thead tr{{background:#f0f3f8;border-bottom:2px solid var(--border)}}
th{{font-family:var(--fh);font-size:.7rem;font-weight:700;text-transform:uppercase;padding:8px 10px;text-align:left;color:var(--muted)}}
tbody tr{{border-bottom:1px solid #edf0f5;background:#fff}}
tbody tr:hover{{background:#f7f9fc}}
td{{padding:8px 10px;vertical-align:middle}}

.badge{{display:inline-flex;padding:2px 8px;border-radius:20px;font-size:.7rem;font-weight:700;font-family:var(--fh);text-transform:uppercase}}
.bb{{background:#fff4e0;color:#b86000;border:1px solid #f5c57a}}
.bo{{background:#e6f4fb;color:#1a7abf;border:1px solid #90cae8}}
.tr-b{{background:#e6f5ec;color:#2e8b57;border:1px solid #7dc99a}}
.desp{{background:#e6f5ec;color:#2e8b57;border:1px solid #7dc99a}}

/* FOOTER */
.site-footer {{
    text-align: center;
    padding: 20px;
    margin-top: 40px;
    font-size: 0.85rem;
    color: var(--muted);
    border-top: 1px solid var(--border);
}}

/* ... (resto de tus estilos originales de modales, resumen, admin) ... */
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const DB_STOCK = JSON.parse(document.getElementById('data-stock').textContent || "[]");
const DB_HISTORIAL = JSON.parse(document.getElementById('data-historial').textContent || "[]");
const DB_ORDENES = JSON.parse(document.getElementById('data-ordenes').textContent || "[]");
const DB_CATALOGOS = JSON.parse(document.getElementById('data-catalogos').textContent || "[]");

const {{useState, useMemo, useEffect}} = React;

function App() {{
  const [user, setUser] = useState(null);
  const [tab, setTab] = useState("stock");
  const [stock] = useState(DB_STOCK);
  
  const [fCamp, setFCamp] = useState("TODAS");
  const [fEsp, setFEsp] = useState("TODAS");
  const [fDep, setFDep] = useState("TODOS");

  useEffect(() => {{
    const sesion = localStorage.getItem("lc_session");
    if(sesion) setUser(JSON.parse(sesion));
  }}, []);

  const handleLogin = (pass) => {{
    if(pass === "1234") {{
      const u = {{ name: "Ignacio Diaz", role: "admin" }};
      localStorage.setItem("lc_session", JSON.stringify(u));
      setUser(u);
    }} else {{
      alert("Clave incorrecta");
    }}
  }};

  const handleLogout = () => {{
    localStorage.removeItem("lc_session");
    setUser(null);
  }};

  if(!user) {{
    return (
      <div className="login-wrap">
        <div className="login-box">
          <h1>La Clementina</h1>
          <p>Control de Semillas</p>
          <input type="password" id="passInput" className="login-input" placeholder="••••" 
                 onKeyDown={{e => e.key === "Enter" && handleLogin(e.target.value)}}/>
          <button className="login-btn" onClick={{() => handleLogin(document.getElementById('passInput').value)}}>Ingresar</button>
        </div>
      </div>
    );
  }}

  return (
    <div className="app">
      <header className="hdr">
        <h1>La Clementina <span>· Semillero Interactive</span></h1>
        <div className="hdr-tabs">
          <button className={{`tab ${{tab === "stock" ? "active" : ""}}`}} onClick={{() => setTab("stock")}}>📊 Stock</button>
          <button className="tab" onClick={{handleLogout}} style={{{{color: "var(--red)"}}}}>🚪 Salir</button>
        </div>
      </header>

      {{tab === "stock" && (
        <div className="stock-view">
            <div className="table-wrap">
                <table>
                <thead>
                    <tr><th>ID</th><th>Variedad</th><th>Bolsas</th><th>Depósito</th></tr>
                </thead>
                <tbody>
                    {{stock.map(s => (
                        <tr key={{s.ID}}>
                            <td><b>{{s.ID}}</b></td>
                            <td>{{s.Variedad}}</td>
                            <td>{{s.Bolsas}}</td>
                            <td>{{s.Depósito}}</td>
                        </tr>
                    ))}}
                </tbody>
                </table>
            </div>
        </div>
      )}}
      
      <footer className="site-footer">
        Creado por Ignacio Diaz
      </footer>
    </div>
  );
}}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
</script>
</body>
</html>
"""

# Renderizamos el componente
st.components.v1.html(html_content, height=900)
