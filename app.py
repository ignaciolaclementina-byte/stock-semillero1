import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import json
from datetime import datetime

# ==============================================================================
# 1. CONFIGURACIÓN DEL PANEL DE STREAMLIT (INTERFAZ COMPLETA E INVISIBLE)
# ==============================================================================
st.set_page_config(
    page_title="La Clementina · Stock Semillas",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inyección de estilos para ocultar componentes de Streamlit y dar aspecto nativo
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
    st.error("⚠️ Error al conectar con Google Sheets. Verificá tus credenciales en Secrets.")
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
# 3. PROCESAMIENTO DE ACCIONES (BRIDGE DE COMUNICACIÓN API DESDE EL FRONTEND)
# ==============================================================================
query_params = st.query_params

if "action" in query_params:
    action = query_params["action"]
    payload = json.loads(query_params.get("payload", "{}"))
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # ACCIÓN: GUARDAR / EDITAR LOTE
    if action == "save_lote":
        stock = leer_pestana("Stock")
        historial = leer_pestana("Historial")
        lote_data = payload.get("item", payload)
        
        # Si tiene ID es una edición, sino es un nuevo ingreso
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
            
            historial.append({
                "Fecha": now_str, "Tipo": "EDICION",
                "Detalle": f"Se modificaron datos del lote ID {lote_id} ({lote_data.get('variedad')})",
                "Bolsas": int(lote_data.get("bolsas", 0)), 
                "Kilos": int(lote_data.get("bolsas", 0)) * float(lote_data.get("kilosBolsa", 40)), 
                "Operario": "Ignacio Diaz"
            })
        else:
            next_id = max([int(r.get("ID", 0)) for r in stock]) + 1 if stock else 1
            kilos_t = int(lote_data.get("bolsas", 0)) * float(lote_data.get("kilosBolsa", 40))
            
            stock.append({
                "ID": next_id, "Campaña": lote_data.get("campaña"), "Especie": lote_data.get("especie"),
                "Variedad": lote_data.get("variedad"), "Categoría": lote_data.get("categoría"), "Depósito": lote_data.get("depósito"),
                "Bolsas": int(lote_data.get("bolsas", 0)), "Kilos_por_Bolsa": float(lote_data.get("kilosBolsa", 40)),
                "Kilos_Totales": kilos_t, "Estado": lote_data.get("estado", "DISPONIBLE"), "Notas": lote_data.get("notas")
            })
            
            historial.append({
                "Fecha": now_str, "Tipo": "INGRESO",
                "Detalle": f"Alta lote ID {next_id}: {lote_data.get('bolsas')} bolsas de {lote_data.get('variedad')} en {lote_data.get('depósito')}",
                "Bolsas": int(lote_data.get("bolsas", 0)), "Kilos": kilos_t, "Operario": "Ignacio Diaz"
            })
            
        actualizar_pestana("Stock", stock)
        actualizar_pestana("Historial", historial)
        st.query_params.clear()
        st.rerun()

    # ACCIÓN: MOVIMIENTOS (TRASPASOS Y EGRESOS COMERCIALES)
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
                lote["Kilos_Totales"] = lote["Bolsas"] * float(lote["Kilos_por_Bolsa"])
                kg_movidos = cant * float(lote["Kilos_por_Bolsa"])
                
                if mov.get("tipo") == "transfer":
                    next_id_t = max([int(r.get("ID", 0)) for r in stock]) + 1
                    lote_dest = lote.copy()
                    lote_dest["ID"] = next_id_t
                    lote_dest["Depósito"] = mov.get("destino")
                    lote_dest["Bolsas"] = cant
                    lote_dest["Kilos_Totales"] = kg_movidos
                    lote_dest["Notas"] = f"Traspasado desde {lote['Depósito']}"
                    stock.append(lote_dest)
                    
                    historial.append({
                        "Fecha": now_str, "Tipo": "TRANSFERENCIA",
                        "Detalle": f"Traspaso de {cant} bols de {lote['Variedad']} ({lote['Depósito']} -> {mov.get('destino')})",
                        "Bolsas": cant, "Kilos": kg_movidos, "Operario": "Ignacio Diaz"
                    })
                else:
                    proxima_oc = max([int(o.get("ID_Orden", 0)) for o in ordenes]) + 1 if ordenes else 5001
                    ordenes.append({
                        "ID_Orden": proxima_oc, "Fecha": now_str, "Campaña": lote["Campaña"],
                        "Especie": lote["Especie"], "Variedad": lote["Variedad"], "Depósito": lote["Depósito"],
                        "Bolsas": cant, "Kilos": kg_movidos, "Cliente": mov.get("cliente", "").upper(),
                        "Patente_Chasis": mov.get("chasis", "").upper(), "Patente_Acoplado": mov.get("acoplado", "").upper(),
                        "Estado": "DESPACHADO"
                    })
                    
                    historial.append({
                        "Fecha": now_str, "Tipo": "EGRESO",
                        "Detalle": f"Despacho OC #{proxima_oc}: {cant} bols para {mov.get('cliente', '').upper()}",
                        "Bolsas": cant, "Kilos": kg_movidos, "Operario": "Ignacio Diaz"
                    })
                break
                
        actualizar_pestana("Stock", stock)
        actualizar_pestana("Historial", historial)
        if mov.get("tipo") == "egreso":
            actualizar_pestana("Ordenes", ordenes)
            
        st.query_params.clear()
        st.rerun()

    # ACCIÓN: ELIMINAR / ACTUALIZAR CATÁLOGOS DIRECTAMENTE
    elif action == "update_catalogos":
        actualizar_pestana("Catalogos", payload.get("catalogos", []))
        st.query_params.clear()
        st.rerun()

# ==============================================================================
# 4. EXTRACCIÓN Y PREPARACIÓN DE DATOS DESDE GOOGLE SHEETS
# ==============================================================================
data_stock = leer_pestana("Stock")
data_historial = leer_pestana("Historial")
data_ordenes = leer_pestana("Ordenes")
data_catalogos = leer_pestana("Catalogos")

js_stock = json.dumps(data_stock) if data_stock else "[]"
js_historial = json.dumps(data_historial) if data_historial else "[]"
js_ordenes = json.dumps(data_ordenes) if data_ordenes else "[]"
js_catalogos = json.dumps(data_catalogos) if data_catalogos else "[]"

# ==============================================================================
# 5. CODIGO DEL FRONTEND INTEGRAL (HTML5 + REACT ENTERO)
# ==============================================================================
html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>La Clementina · Stock Semillas</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.2/babel.min.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500&display=swap');
:root{
  --bg:#f4f6f9;--panel:#fff;--card:#fff;--border:#dde1ea;
  --accent:#e07b00;--blue:#1a7abf;--green:#2e8b57;--red:#c0392b;
  --purple:#7b4fa6;--text:#1a1e2e;--muted:#6b7280;--shadow:0 1px 4px rgba(0,0,0,.08);
  --fh:'Barlow Condensed',sans-serif;--fb:'Barlow',sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:var(--bg);color:var(--text);font-family:var(--fb)}
.app{max-width:1300px;margin:0 auto;padding-bottom:60px}

/* LOGIN SCREEN */
.login-wrap{min-height:100vh;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#1a2a4a,#1e3660)}
.login-box{background:#fff;border-radius:16px;padding:40px 48px;width:100%;max-width:400px;text-align:center;box-shadow:0 8px 40px rgba(0,0,0,.25)}
.login-box h1{font-family:var(--fh);font-size:1.5rem;font-weight:800;text-transform:uppercase;letter-spacing:1px;color:#1a2a4a;margin-bottom:6px}
.login-box p{font-size:.85rem;color:var(--muted);margin-bottom:24px}
.login-input{width:100%;padding:11px 14px;border:1.5px solid var(--border);border-radius:8px;font-family:var(--fb);font-size:1rem;outline:none;text-align:center;letter-spacing:3px;margin-bottom:8px;background:var(--bg)}
.login-input:focus{border-color:var(--accent)}
.login-btn{width:100%;background:var(--accent);border:none;border-radius:8px;color:#fff;font-family:var(--fh);font-size:1rem;font-weight:800;text-transform:uppercase;letter-spacing:.8px;padding:12px;cursor:pointer;margin-top:8px}
.login-btn:hover{background:#c86e00}

/* ESTRUCTURA DASHBOARD */
.hdr{background:linear-gradient(135deg,#1a2a4a 60%,#1e3660);border-bottom:3px solid var(--accent);padding:14px 24px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
.hdr h1{font-family:var(--fh);font-size:1.6rem;font-weight:800;text-transform:uppercase;letter-spacing:1px;color:#fff}
.hdr h1 span{color:#f5a623}
.hdr p{font-size:.7rem;color:rgba(255,255,255,.55)}
.hdr-tabs{display:flex;gap:5px;flex-wrap:wrap}
.tab{font-family:var(--fh);font-size:.82rem;font-weight:700;letter-spacing:.6px;text-transform:uppercase;padding:6px 13px;border-radius:6px;cursor:pointer;border:1.5px solid rgba(255,255,255,.22);background:transparent;color:rgba(255,255,255,.65)}
.tab.active{background:#f5a623;border-color:#f5a623;color:#1a1e2e}
.tab:hover:not(.active){border-color:rgba(255,255,255,.7);color:#fff}

.kpi-strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:1px;background:var(--border);border-bottom:1px solid var(--border)}
.kpi{background:var(--panel);padding:12px 16px}
.kpi-val{font-family:var(--fh);font-size:1.8rem;font-weight:800;line-height:1}
.kpi-lbl{font-size:.65rem;color:var(--muted);text-transform:uppercase;letter-spacing:.7px;margin-top:2px}
.c-or{color:var(--accent)}.c-bl{color:var(--blue)}.c-gr{color:var(--green)}.c-pu{color:var(--purple)}

.toolbar{display:flex;gap:8px;padding:12px 16px;flex-wrap:wrap;align-items:center;border-bottom:1px solid var(--border);background:var(--panel)}
.search-inp{flex:1;min-width:160px;padding:7px 10px;background:var(--bg);border:1.5px solid var(--border);border-radius:8px;font-size:.83rem;outline:none}
.sel{background:var(--bg);border:1.5px solid var(--border);border-radius:8px;font-size:.81rem;padding:7px 9px;outline:none;cursor:pointer}
.btn{font-family:var(--fh);font-size:.85rem;font-weight:700;text-transform:uppercase;padding:7px 14px;border-radius:8px;cursor:pointer;border:none}
.btn-add{background:var(--accent);color:#fff}.btn-add:hover{background:#c86e00}
.btn-ol{background:var(--panel);border:1.5px solid var(--border)!important;color:var(--text)}
.btn-ol.gnh:hover{border-color:var(--green)!important;color:var(--green)}
.btn-sm{padding:4px 9px;font-size:.75rem}

.table-wrap{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:.82rem}
thead tr{background:#f0f3f8;border-bottom:2px solid var(--border)}
th{font-family:var(--fh);font-size:.7rem;font-weight:700;text-transform:uppercase;padding:8px 10px;text-align:left;color:var(--muted)}
tbody tr{border-bottom:1px solid #edf0f5;background:#fff}
tbody tr:hover{background:#f7f9fc}
td{padding:8px 10px;vertical-align:middle}

.badge{display:inline-flex;padding:2px 8px;border-radius:20px;font-size:.7rem;font-weight:700;font-family:var(--fh);text-transform:uppercase}
.bb{background:#fff4e0;color:#b86000;border:1px solid #f5c57a}
.bo{background:#e6f4fb;color:#1a7abf;border:1px solid #90cae8}
.tr-b{background:#e6f5ec;color:#2e8b57;border:1px solid #7dc99a}
.desp{background:#e6f5ec;color:#2e8b57;border:1px solid #7dc99a}
.egr{background:#fde8e8;color:#c0392b;border:1px solid #f5a5a5}
.ing{background:#e6f5ec;color:#2e8b57;border:1px solid #7dc99a}

.qty-big{font-family:var(--fh);font-size:1.1rem;font-weight:800}
.action-btn{background:transparent;border:1.5px solid var(--border);border-radius:6px;color:var(--muted);font-size:.75rem;padding:3px 8px;cursor:pointer;margin-right:3px}
.action-btn:hover{border-color:var(--blue);color:var(--blue)}
.action-btn.dep:hover{border-color:var(--green);color:var(--green)}

/* RESUMEN CARDS */
.stock-view{padding:16px;background:var(--bg)}
.sv-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:9px}
.sv-card{background:#fff;border:1px solid var(--border);border-radius:10px;padding:12px 14px;border-top:3px solid var(--accent);box-shadow:var(--shadow)}
.sv-head{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:9px}
.sv-variedad{font-family:var(--fh);font-size:.95rem;font-weight:700;text-transform:uppercase;color:#1a2a4a}
.sv-row{display:flex;justify-content:space-between;align-items:center;padding:4px 0;border-bottom:1px solid #edf0f5}
.sv-label{font-size:.68rem;color:var(--muted);text-transform:uppercase}
.sv-val{font-family:var(--fh);font-size:1rem;font-weight:700}

/* MODALES */
.overlay{position:fixed;inset:0;z-index:100;background:rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;padding:14px}
.modal{background:#fff;border-radius:14px;padding:22px;width:100%;max-width:520px;box-shadow:0 8px 32px rgba(0,0,0,.15)}
.modal h2{font-family:var(--fh);font-size:1.2rem;font-weight:800;text-transform:uppercase;color:#1a2a4a;margin-bottom:16px}
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.form-grid .full{grid-column:1/-1}
.field label{display:block;font-size:.66rem;color:var(--muted);text-transform:uppercase;margin-bottom:3px}
.field input,.field select,.field textarea{width:100%;background:var(--bg);border:1.5px solid var(--border);border-radius:8px;font-size:.86rem;padding:7px 10px;outline:none}
.modal-btns{display:flex;justify-content:flex-end;gap:9px;margin-top:18px}
.btn-cancel{background:transparent;border:1.5px solid var(--border);border-radius:8px;color:var(--muted);padding:8px 18px;cursor:pointer}
.btn-save{background:var(--accent);border:none;border-radius:8px;color:#fff;font-family:var(--fh);font-weight:800;padding:8px 22px;cursor:pointer}
.btn-desp{background:var(--green);border:none;border-radius:8px;color:#fff;font-family:var(--fh);font-weight:800;padding:8px 22px;cursor:pointer}
.move-info{background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:10px 13px;margin-bottom:14px;font-size:.83rem}

/* CATÁLOGOS */
.admin{padding:16px;background:var(--bg)}
.admin-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}
.admin-card{background:#fff;border:1px solid var(--border);border-radius:10px;padding:14px}
.admin-card h3{font-family:var(--fh);font-size:.85rem;font-weight:700;text-transform:uppercase;color:var(--muted);margin-bottom:9px}
.tag-list{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:10px}
.tag{background:var(--bg);border:1.5px solid var(--border);border-radius:20px;padding:3px 10px;font-size:.76rem}
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const DB_STOCK = %s;
const DB_HISTORIAL = %s;
const DB_ORDENES = %s;
const DB_CATALOGOS = %s;

const { useState, useMemo, useEffect } = React;
const LOW = 5;
const fmt = n => n === undefined || n === "" ? "0" : Number(n).toLocaleString("es-AR");

function App() {
  const [user, setUser] = useState(null);
  const [tab, setTab] = useState("stock");
  const [stock] = useState(DB_STOCK);
  const [historial] = useState(DB_HISTORIAL);
  const [ordenes] = useState(DB_ORDENES);
  const [catalogos] = useState(DB_CATALOGOS);

  const [fCamp, setFCamp] = useState("TODAS");
  const [fEsp, setFEsp] = useState("TODAS");
  const [fDep, setFDep] = useState("TODOS");
  const [fText, setFText] = useState("");
  const [modal, setModal] = useState(null);

  useEffect(() => {
    const sesion = localStorage.getItem("lc_session");
    if(sesion) setUser(JSON.parse(sesion));
  }, []);

  const handleLogin = (pass) => {
    if(pass === "1234") {
      const u = { name: "Ignacio Diaz", role: "admin" };
      localStorage.setItem("lc_session", JSON.stringify(u));
      setUser(u);
    } else {
      alert("Clave incorrecta");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("lc_session");
    setUser(null);
  };

  // Listas Dinámicas desde Catálogos
  const campañas = useMemo(() => ["TODAS", ...new Set(catalogos.filter(c => c.Tipo === "Campaña").map(c => c.Valor))], [catalogos]);
  const especies = useMemo(() => ["TODAS", ...new Set(catalogos.filter(c => c.Tipo === "Especie").map(c => c.Valor))], [catalogos]);
  const depositos = useMemo(() => ["TODOS", ...new Set(catalogos.filter(c => c.Tipo === "Depósito").map(c => c.Valor))], [catalogos]);

  // Funciones mandatorias restauradas para evitar errores de React
  const resetAll = () => { alert("Acción de reinicio bloqueada por el servidor."); };
  const handleChangePass = () => { alert("Cambio de clave inhabilitado."); };
  const addTag = () => { alert("Modifique la pestaña 'Catalogos' en su Google Sheets."); };
  const delTag = () => { alert("Modifique la pestaña 'Catalogos' en su Google Sheets."); };
  const handleEditOC = () => { alert("Las órdenes confirmadas se editan directo en Sheets."); };

  // Filtrado Seguro de Datos
  const filteredStock = useMemo(() => {
    return stock.filter(s => {
      if(fCamp !== "TODAS" && s.Campaña !== fCamp) return false;
      if(fEsp !== "TODAS" && s.Especie !== fEsp) return false;
      if(fDep !== "TODOS" && s.Depósito !== fDep) return false;
      if(fText) {
        const t = fText.toLowerCase();
        return s.Variedad.toLowerCase().includes(t) || s.Notas.toLowerCase().includes(t);
      }
      return true;
    });
  }, [stock, fCamp, fEsp, fDep, fText]);

  // KPIs de la cabecera
  const totals = useMemo(() => {
    let b = 0, k = 0, l = 0;
    stock.forEach(s => {
      const bags = parseInt(s.Bolsas) || 0;
      b += bags;
      k += parseFloat(s.Kilos_Totales) || 0;
      if(bags <= LOW) l++;
    });
    return { bolsas: fmt(b), kilos: fmt(Math.round(k)), low: l, ocs: ordenes.length };
  }, [stock, ordenes]);

  const handleSave = (item) => {
    window.parent.location.search = `?action=save_lote&payload=${encodeURIComponent(JSON.stringify(item))}`;
  };

  const handleMove = (mov) => {
    window.parent.location.search = `?action=move_lote&payload=${encodeURIComponent(JSON.stringify(mov))}`;
  };

  if(!user) {
    return (
      <div className="login-wrap">
        <div className="login-box">
          <h1>La Clementina</h1>
          <p>Control de Semillas & Logística</p>
          <input type="password" className="login-input" placeholder="••••" onKeyDown={e => e.key === "Enter" && handleLogin(e.target.value)}/>
          <button className="login-btn" onClick={(e) => handleLogin(e.target.previousSibling.value)}>Ingresar</button>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="hdr">
        <h1>La Clementina <span>· Semillero Interactive</span></h1>
        <div className="hdr-tabs">
          <button className={`tab ${tab === "stock" ? "active" : ""}`} onClick={() => setTab("stock")}>📊 Stock</button>
          <button className={`tab ${tab === "resumen" ? "active" : ""}`} onClick={() => setTab("resumen")}>🔍 Resumen</button>
          <button className={`tab ${tab === "historial" ? "active" : ""}`} onClick={() => setTab("historial")}>📜 Historial</button>
          <button className={`tab ${tab === "ordenes" ? "active" : ""}`} onClick={() => setTab("ordenes")}>🚚 Órdenes ({totals.ocs})</button>
          <button className={`tab ${tab === "admin" ? "active" : ""}`} onClick={() => setTab("admin")}>⚙ Catálogos</button>
          <button className="tab" onClick={handleLogout} style={{ color: "var(--red)" }}>🚪 Salir</button>
        </div>
      </header>

      <section className="kpi-strip">
        <div className="kpi"><div className="kpi-val c-or">{totals.bolsas}</div><div className="kpi-lbl">Bolsas Netas</div></div>
        <div className="kpi"><div className="kpi-val c-bl">{totals.kilos}</div><div className="kpi-lbl">Kilos Totales</div></div>
        <div className="kpi"><div className="kpi-val c-gr">{totals.ocs}</div><div className="kpi-lbl">Órdenes Activas</div></div>
        <div className="kpi"><div className="kpi-val c-pu">{totals.low}</div><div className="kpi-lbl">Stock Crítico</div></div>
      </section>

      {tab === "stock" && (
        <div className="stock-view">
          <div className="toolbar">
            <input type="text" className="search-inp" placeholder="Buscar por variedad..." value={fText} onChange={e => setFText(e.target.value)}/>
            <select className="sel" value={fCamp} onChange={e => setFCamp(e.target.value)}>
              {campañas.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
            <select className="sel" value={fEsp} onChange={e => setFEsp(e.target.value)}>
              {especies.map(e => <option key={e} value={e}>{e}</option>)}
            </select>
            <button className="btn btn-add" onClick={() => setModal({ mode: "new" })}>➕ Nuevo Lote</button>
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>ID</th><th>Campaña</th><th>Especie</th><th>Variedad</th><th>Categoría</th><th>Depósito</th><th>Bolsas</th><th>Kg Totales</th><th>Estado</th><th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {filteredStock.map(s => (
                  <tr key={s.ID}>
                    <td><b>{s.ID}</b></td><td>{s.Campaña}</td><td><span className="badge bb">{s.Especie}</span></td><td><b>{s.Variedad}</b></td><td>{s.Categoría}</td><td>{s.Depósito}</td><td className="qty-big">{fmt(s.Bolsas)}</td><td>{fmt(s.Kilos_Totales)}</td><td><span className="badge tr-b">{s.Estado}</span></td>
                    <td>
                      <button className="action-btn" onClick={() => setModal({ mode: "edit", item: s })}>✏️</button>
                      <button className="action-btn dep" onClick={() => setModal({ mode: "move", item: s })}>🚚 Despachar</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {tab === "resumen" && (
        <div className="stock-view">
          <div className="sv-grid">
            {filteredStock.map(s => (
              <div className="sv-card" key={s.ID}>
                <div className="sv-head"><div className="sv-variedad">{s.Variedad}</div><span className="badge bo">{s.Campaña}</span></div>
                <div className="sv-row"><span className="sv-label">Depósito</span><span className="sv-val">{s.Depósito}</span></div>
                <div className="sv-row"><span className="sv-label">Bolsas</span><span className="sv-val c-or">{fmt(s.Bolsas)}</span></div>
                <div className="sv-row"><span className="sv-label">Kilos</span><span className="sv-val">{fmt(s.Kilos_Totales)}</span></div>
              </div>
            ))}
          </div>
        </div>
      )}

      {tab === "historial" && (
        <div className="hist-view">
          <div className="table-wrap">
            <table>
              <thead>
                <tr><th>Fecha</th><th>Tipo</th><th>Detalle</th><th>Bolsas</th><th>Kilos</th><th>Operario</th></tr>
              </thead>
              <tbody>
                {historial.map((h, i) => (
                  <tr key={i}>
                    <td>{h.Fecha}</td><td><span className={`badge ${h.Tipo === "INGRESO" ? "ing" : "egr"}`}>{h.Tipo}</span></td><td>{h.Detalle}</td><td>{fmt(h.Bolsas)}</td><td>{fmt(h.Kilos)}</td><td><b>{h.Operario}</b></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {tab === "ordenes" && (
        <div className="oc-view">
          <div className="table-wrap">
            <table>
              <thead>
                <tr><th>OC #</th><th>Fecha</th><th>Variedad</th><th>Depósito</th><th>Bolsas</th><th>Cliente</th><th>Patentes</th><th>Estado</th><th>Notificar</th></tr>
              </thead>
              <tbody>
                {ordenes.map(o => {
                  const msg = `La Clementina - OC %23${o.ID_Orden}%0ACliente: ${o.Cliente}%0AVariedad: ${o.Variedad}%0ABolsas: ${o.Bolsas}%0APatente: ${o.Patente_Chasis}`;
                  return (
                    <tr key={o.ID_Orden}>
                      <td><b>#{o.ID_Orden}</b></td><td>{o.Fecha}</td><td>{o.Variedad}</td><td>{o.Depósito}</td><td className="qty-big">{fmt(o.Bolsas)}</td><td>{o.Cliente}</td><td>{o.Patente_Chasis}</td><td><span className="badge desp">{o.Estado}</span></td>
                      <td>
                        <a href={`https://api.whatsapp.com/send?text=${msg}`} target="_blank" rel="noreferrer" className="btn btn-ol gnh btn-sm">💬 WhatsApp</a>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {tab === "admin" && (
        <div className="admin">
          <div className="admin-grid">
            <div className="admin-card"><h3>Campañas</h3><div className="tag-list">{campañas.filter(c=>c!=="TODAS").map(t=><span className="tag" key={t}>{t}</span>)}</div></div>
            <div className="admin-card"><h3>Especies</h3><div className="tag-list">{especies.filter(e=>e!=="TODAS").map(t=><span className="tag" key={t}>{t}</span>)}</div></div>
            <div className="admin-card"><h3>Depósitos</h3><div className="tag-list">{depositos.filter(d=>d!=="TODOS").map(t=><span className="tag" key={t}>{t}</span>)}</div></div>
          </div>
        </div>
      )}

      {modal?.mode === "new" && <ModalForm campañas={campañas.filter(c=>c!=="TODAS")} especies={especies.filter(e=>e!=="TODAS")} onSave={handleSave} onClose={() => setModal(null)} />}
      {modal?.mode === "edit" && <ModalForm item={modal.item} campañas={campañas.filter(c=>c!=="TODAS")} especies={especies.filter(e=>e!=="TODAS")} onSave={handleSave} onClose={() => setModal(null)} />}
      {modal?.mode === "move" && <MoveModal item={modal.item} onSave={handleMove} onClose={() => setModal(null)} />}
      
      <footer style={{ position: "fixed", bottom: 10, right: 20, fontSize: "0.75rem", color: "#9ca3af" }}>
        Creado por Ignacio Diaz
      </footer>
    </div>
  );
}

function ModalForm({ item, campañas, especies, onSave, onClose }) {
  const [campaña, setCampaña] = useState(item?.Campaña || campañas[0] || "");
  const [especie, setEspecie] = useState(item?.Especie || especies[0] || "");
  const [variedad, setVariedad] = useState(item?.Variedad || "");
  const [categoría, setCategoría] = useState(item?.Categoría || "Original");
  const [depósito, setDepósito] = useState(item?.Depósito || "Planta 1");
  const [bolsas, setBolsas] = useState(item?.Bolsas || 0);
  const [notas, setNotas] = useState(item?.Notas || "");

  return (
    <div className="overlay">
      <form className="modal" onSubmit={e => { e.preventDefault(); onSave({ ID: item?.ID, campaña, especie, variedad, categoría, depósito, bolsas, notas }); }}>
        <h2>{item ? "Editar Lote" : "Nuevo Lote"}</h2>
        <div className="form-grid">
          <div className="field"><label>Campaña</label><select value={campaña} onChange={e => setCampaña(e.target.value)}>{campañas.map(c => <option key={c} value={c}>{c}</option>)}</select></div>
          <div className="field"><label>Especie</label><select value={especie} onChange={e => setEspecie(e.target.value)}>{especies.map(e => <option key={e} value={e}>{e}</option>)}</select></div>
          <div className="field full"><label>Variedad</label><input type="text" value={variedad} onChange={e => setVariedad(e.target.value)} required/></div>
          <div className="field"><label>Depósito</label><input type="text" value={depósito} onChange={e => setDepósito(e.target.value)} required/></div>
          <div className="field"><label>Bolsas</label><input type="number" value={bolsas} onChange={e => setBolsas(e.target.value)} required/></div>
          <div className="field full"><label>Notas</label><textarea value={notas} onChange={e => setNotas(e.target.value)}/></div>
        </div>
        <div className="modal-btns">
          <button type="button" className="btn-cancel" onClick={onClose}>Cancelar</button>
          <button type="submit" className="btn-save">💾 Guardar</button>
        </div>
      </form>
    </div>
  );
}

function MoveModal({ item, onSave, onClose }) {
  const [tipo, setTipo] = useState("transfer");
  const [cantidad, setCantidad] = useState(1);
  const [destino, setDestino] = useState("");
  const [cliente, setCliente] = useState("");
  const [chasis, setChasis] = useState("");

  return (
    <div className="overlay">
      <form className="modal" onSubmit={e => { e.preventDefault(); onSave({ loteId: item.ID, tipo, cantidad, destino, cliente, chasis }); }}>
        <h2>Registrar Egreso / Traspaso</h2>
        <div className="move-info"><b>Lote:</b> {item.Variedad}<br/><b>Bolsas Libres:</b> {item.Bolsas}</div>
        <div className="move-row">
          <label>Operación</label>
          <select value={tipo} onChange={e => setTipo(e.target.value)}>
            <option value="transfer">Traspaso Interno</option>
            <option value="egreso">Despacho Comercial (Genera OC)</option>
          </select>
        </div>
        <div className="move-row"><label>Cantidad</label><input type="number" min="1" max={item.Bolsas} value={cantidad} onChange={e => setCantidad(e.target.value)} required/></div>
        {tipo === "transfer" ? (
          <div className="move-row"><label>Depósito Destino</label><input type="text" value={destino} onChange={e => setDestino(e.target.value)} required/></div>
        ) : (
          <>
            <div className="move-row"><label>Cliente</label><input type="text" value={cliente} onChange={e => setCliente(e.target.value)} required/></div>
            <div className="move-row"><label>Patente</label><input type="text" value={chasis} onChange={e => setChasis(e.target.value)} required/></div>
          </>
        )}
        <div className="modal-btns">
          <button type="button" className="btn-cancel" onClick={onClose}>Cancelar</button>
          <button type="submit" className="btn-desp">✓ Confirmar</button>
        </div>
      </form>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
</script>
</body>
</html>
""" % (js_stock, js_historial, js_ordenes, js_catalogos)

# Renderizado de pantalla completa asegurado
st.components.v1.html(html_content, height=1200, scrolling=True)
