import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import json
from datetime import datetime

# ==============================================================================
# 1. CONFIGURACIÓN DEL PANEL DE STREAMLIT (ESTILO INVISIBLE / NATIVO)
# ==============================================================================
st.set_page_config(
    page_title="La Clementina · Stock Semillas",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ocultamos la interfaz por defecto de Streamlit para que luzca 100% profesional
st.markdown("""
    <style>
        .block-container { padding: 0rem !important; max-width: 100% !important; }
        [data-testid="stHeader"] { display: none !important; }
        footer { visibility: hidden !important; }
        iframe { display: block; border: none; width: 100vw; height: 100vh; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. CONEXIÓN GENERAL Y ROBUSTA A GOOGLE SHEETS
# ==============================================================================
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("⚠️ Error de conexión con las credenciales de Google Sheets. Verificá tus Secrets.")
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
# 3. PROCESAMIENTO DE ACCIONES (API BRIDGE DESDE EL FRONTEND HTML)
# ==============================================================================
query_params = st.query_params

if "action" in query_params:
    action = query_params["action"]
    payload = json.loads(query_params.get("payload", "{}"))
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    if action == "save_lote":
        stock = leer_pestana("Stock")
        historial = leer_pestana("Historial")
        lote_data = payload.get("item", payload) # Tolerancia a estructura de envío
        
        # Mapeo y normalización para que coincida exactamente con las columnas de Google Sheets
        if lote_data.get("id") or lote_data.get("ID"):
            lote_id = lote_data.get("id") or lote_data.get("ID")
            # Modo Edición
            stock = [r if str(r.get("ID")) != str(lote_id) else {
                "ID": int(lote_id), 
                "Campaña": lote_data.get("campaña", r.get("Campaña")), 
                "Especie": lote_data.get("especie", r.get("Especie")),
                "Variedad": lote_data.get("variedad", r.get("Variedad")), 
                "Categoría": lote_data.get("categoría", r.get("Categoría")), 
                "Depósito": lote_data.get("depósito", r.get("Depósito")),
                "Bolsas": int(lote_data.get("bolsas", 0)), 
                "Kilos_por_Bolsa": float(lote_data.get("kilosBolsa", 0)),
                "Kilos_Totales": int(lote_data.get("bolsas", 0)) * float(lote_data.get("kilosBolsa", 0)),
                "Estado": lote_data.get("estado", r.get("Estado")), 
                "Notas": lote_data.get("notas", r.get("Notas"))
            } for r in stock]
            
            historial.append({
                "Fecha": now_str, "Tipo": "EDICION",
                "Detalle": f"Se modificaron datos del lote ID {lote_id} ({lote_data.get('variedad')})",
                "Bolsas": int(lote_data.get("bolsas", 0)), 
                "Kilos": int(lote_data.get("bolsas", 0)) * float(lote_data.get("kilosBolsa", 0)), 
                "Operario": "Ignacio Diaz"
            })
        else:
            # Modo Alta Nueva
            next_id = max([int(r.get("ID", 0)) for r in stock]) + 1 if stock else 1
            kilos_t = int(lote_data.get("bolsas", 0)) * float(lote_data.get("kilosBolsa", 0))
            
            stock.append({
                "ID": next_id, "Campaña": lote_data.get("campaña"), "Especie": lote_data.get("especie"),
                "Variedad": lote_data.get("variedad"), "Categoría": lote_data.get("categoría"), "Depósito": lote_data.get("depósito"),
                "Bolsas": int(lote_data.get("bolsas", 0)), "Kilos_por_Bolsa": float(lote_data.get("kilosBolsa", 0)),
                "Kilos_Totales": kilos_t, "Estado": lote_data.get("estado"), "Notas": lote_data.get("notas")
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
                    # Sumar lote en depósito de destino
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
                    # Emisión de una nueva Orden de Carga (OC)
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

# ==============================================================================
# 4. LECTURA DE DATOS DESDE GOOGLE SHEETS PARA INYECTAR EN LA INTERFAZ
# ==============================================================================
data_stock = leer_pestana("Stock")
data_historial = leer_pestana("Historial")
data_ordenes = leer_pestana("Ordenes")
data_catalogos = leer_pestana("Catalogos")

# Si las bases de datos de Sheets están vacías, inyectamos arrays vacíos limpios para React
js_stock = json.dumps(data_stock) if data_stock else "[]"
js_historial = json.dumps(data_historial) if data_historial else "[]"
js_ordenes = json.dumps(data_ordenes) if data_ordenes else "[]"
js_catalogos = json.dumps(data_catalogos) if data_catalogos else "[]"

# ==============================================================================
# 5. INTEGRACIÓN DIRECTA CON TU INTERFAZ HTML ORIGINAL (React Frontend)
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

/* LOGIN */
.login-wrap{min-height:100vh;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#1a2a4a,#1e3660)}
.login-box{background:#fff;border-radius:16px;padding:40px 48px;width:100%;max-width:400px;text-align:center;box-shadow:0 8px 40px rgba(0,0,0,.25)}
.login-logo{height:72px;margin-bottom:20px}
.login-box h1{font-family:var(--fh);font-size:1.5rem;font-weight:800;text-transform:uppercase;letter-spacing:1px;color:#1a2a4a;margin-bottom:6px}
.login-box p{font-size:.85rem;color:var(--muted);margin-bottom:24px}
.login-input{width:100%;padding:11px 14px;border:1.5px solid var(--border);border-radius:8px;font-family:var(--fb);font-size:1rem;outline:none;text-align:center;letter-spacing:3px;transition:border-color .18s;margin-bottom:8px;background:var(--bg)}
.login-input:focus{border-color:var(--accent)}
.login-input.err{border-color:var(--red);background:#fff5f5}
.err-msg{color:var(--red);font-size:.8rem;margin-bottom:12px}
.login-btn{width:100%;background:var(--accent);border:none;border-radius:8px;color:#fff;font-family:var(--fh);font-size:1rem;font-weight:800;text-transform:uppercase;letter-spacing:.8px;padding:12px;cursor:pointer;margin-top:8px;transition:background .15s}
.login-btn:hover{background:#c86e00}

/* HEADER */
.hdr{background:linear-gradient(135deg,#1a2a4a 60%,#1e3660);border-bottom:3px solid var(--accent);padding:14px 24px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
.hdr-left{display:flex;align-items:center;gap:14px}
.hdr-logo{height:52px;border-radius:5px}
.hdr h1{font-family:var(--fh);font-size:1.6rem;font-weight:800;text-transform:uppercase;letter-spacing:1px;line-height:1;color:#fff}
.hdr h1 span{color:#f5a623}
.hdr p{font-size:.7rem;color:rgba(255,255,255,.55);margin-top:2px}
.hdr-right{display:flex;flex-direction:column;align-items:flex-end;gap:8px}
.save-ind{font-size:.65rem;color:rgba(255,255,255,.45);height:14px;text-align:right}
.save-ok{color:#6ee7a0}.save-ing{color:#fbbf24}
.hdr-tabs{display:flex;gap:5px;flex-wrap:wrap}
.tab{font-family:var(--fh);font-size:.82rem;font-weight:700;letter-spacing:.6px;text-transform:uppercase;padding:6px 13px;border-radius:6px;cursor:pointer;border:1.5px solid rgba(255,255,255,.22);background:transparent;color:rgba(255,255,255,.65);transition:all .18s}
.tab.active{background:#f5a623;border-color:#f5a623;color:#1a1e2e}
.tab:hover:not(.active){border-color:rgba(255,255,255,.7);color:#fff}

/* KPIs */
.kpi-strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:1px;background:var(--border);border-bottom:1px solid var(--border)}
.kpi{background:var(--panel);padding:12px 16px}
.kpi-val{font-family:var(--fh);font-size:1.8rem;font-weight:800;line-height:1}
.kpi-lbl{font-size:.65rem;color:var(--muted);text-transform:uppercase;letter-spacing:.7px;margin-top:2px}
.c-or{color:var(--accent)}.c-bl{color:var(--blue)}.c-gr{color:var(--green)}.c-pu{color:var(--purple)}

/* TOOLBAR */
.toolbar{display:flex;gap:8px;padding:12px 16px;flex-wrap:wrap;align-items:center;border-bottom:1px solid var(--border);background:var(--panel);box-shadow:var(--shadow)}
.search-wrap{position:relative;flex:1;min-width:160px}
.search-icon{position:absolute;left:9px;top:50%;transform:translateY(-50%);color:var(--muted);font-size:.85rem}
.search-inp{width:100%;padding:7px 10px 7px 28px;background:var(--bg);border:1.5px solid var(--border);border-radius:8px;color:var(--text);font-family:var(--fb);font-size:.83rem;outline:none;transition:border-color .18s}
.search-inp:focus{border-color:var(--accent)}
.sel{background:var(--bg);border:1.5px solid var(--border);border-radius:8px;color:var(--text);font-family:var(--fb);font-size:.81rem;padding:7px 9px;outline:none;cursor:pointer}
.sel:focus{border-color:var(--accent)}
.btn{font-family:var(--fh);font-size:.85rem;font-weight:700;letter-spacing:.4px;text-transform:uppercase;padding:7px 14px;border-radius:8px;cursor:pointer;border:none;transition:all .15s;display:inline-flex;align-items:center;gap:5px;white-space:nowrap}
.btn-add{background:var(--accent);color:#fff}.btn-add:hover{background:#c86e00}
.btn-ol{background:var(--panel);border:1.5px solid var(--border)!important;color:var(--text)}
.btn-ol:hover{border-color:var(--blue)!important;color:var(--blue)}
.btn-ol.gnh:hover{border-color:var(--green)!important;color:var(--green)}
.btn-ol.rh:hover{border-color:var(--red)!important;color:var(--red)}
.btn-ol.ph:hover{border-color:var(--accent)!important;color:var(--accent)}
.btn-ol.oc:hover{border-color:var(--purple)!important;color:var(--purple)}
.btn-sm{padding:4px 9px;font-size:.75rem}

/* TABLE */
.table-wrap{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:.82rem}
thead tr{background:#f0f3f8;border-bottom:2px solid var(--border)}
th{font-family:var(--fh);font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.6px;color:var(--muted);padding:8px 10px;text-align:left;white-space:nowrap}
tbody tr{border-bottom:1px solid #edf0f5;transition:background .12s;background:#fff}
tbody tr:hover{background:#f7f9fc}
tbody tr.low-row{background:#fff5f5}
td{padding:8px 10px;vertical-align:middle}

/* BADGES */
.badge{display:inline-flex;align-items:center;gap:3px;padding:2px 8px;border-radius:20px;font-size:.7rem;font-weight:700;font-family:var(--fh);text-transform:uppercase;letter-spacing:.4px}
.bb{background:#fff4e0;color:#b86000;border:1px solid #f5c57a}
.bo{background:#e6f4fb;color:#1a7abf;border:1px solid #90cae8}
.tr-b{background:#e6f5ec;color:#2e8b57;border:1px solid #7dc99a}
.st-b{background:#f3f4f6;color:#6b7280;border:1px solid #d1d5db}
.low{background:#fde8e8;color:#c0392b;border:1px solid #f5a5a5}
.egr{background:#fde8e8;color:#c0392b;border:1px solid #f5a5a5}
.ing{background:#e6f5ec;color:#2e8b57;border:1px solid #7dc99a}
.pend{background:#fef9ee;color:#92600a;border:1px solid #f5c57a}
.desp{background:#e6f5ec;color:#2e8b57;border:1px solid #7dc99a}

.cell-muted{color:var(--muted);font-size:.8rem}
.qty-big{font-family:var(--fh);font-size:1.1rem;font-weight:800}
.action-btn{background:transparent;border:1.5px solid var(--border);border-radius:6px;color:var(--muted);font-size:.75rem;padding:3px 8px;cursor:pointer;margin-right:3px;transition:all .15s}
.action-btn:hover{border-color:var(--blue);color:var(--blue)}
.action-btn.del:hover{border-color:var(--red);color:var(--red)}
.action-btn.dep:hover{border-color:var(--green);color:var(--green)}
.action-btn.oc-btn:hover{border-color:var(--purple);color:var(--purple)}

/* RESUMEN */
.stock-view{padding:16px;background:var(--bg)}
.sv-filters{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;align-items:center}
.camp-block{margin-bottom:26px}
.camp-title{font-family:var(--fh);font-size:1.25rem;font-weight:800;text-transform:uppercase;letter-spacing:1.5px;color:#1a2a4a;border-bottom:2px solid var(--accent);padding-bottom:5px;margin-bottom:12px;display:flex;justify-content:space-between;align-items:center}
.camp-sub{font-size:.82rem;font-weight:600;color:var(--muted)}
.esp-block{margin-bottom:18px}
.esp-title{font-family:var(--fh);font-size:.95rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--blue);margin-bottom:8px;border-left:3px solid var(--blue);padding-left:9px}
.sv-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:9px}
.sv-card{background:#fff;border:1px solid var(--border);border-radius:10px;padding:12px 14px;border-top:3px solid var(--accent);transition:transform .15s;box-shadow:var(--shadow)}
.sv-card:hover{transform:translateY(-2px)}
.sv-head{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:9px;gap:8px}
.sv-variedad{font-family:var(--fh);font-size:.95rem;font-weight:700;text-transform:uppercase;color:#1a2a4a}
.sv-row{display:flex;justify-content:space-between;align-items:center;padding:4px 0;border-bottom:1px solid #edf0f5}
.sv-row:last-child{border-bottom:none}
.sv-label{font-size:.68rem;color:var(--muted);text-transform:uppercase;letter-spacing:.4px}
.sv-val{font-family:var(--fh);font-size:1rem;font-weight:700}
.no-data{color:var(--muted);font-size:.88rem;padding:40px 0;text-align:center}

/* HISTORIAL / OC view */
.hist-view,.oc-view{padding:16px;background:var(--bg)}
.hist-filters,.oc-filters{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;align-items:center}
.dpos{font-family:var(--fh);font-size:1rem;font-weight:800;color:var(--green)}
.dneg{font-family:var(--fh);font-size:1rem;font-weight:800;color:var(--red)}

/* ADMIN */
.admin{padding:16px;background:var(--bg)}
.admin h2{font-family:var(--fh);font-size:1.15rem;font-weight:800;text-transform:uppercase;letter-spacing:1px;color:#1a2a4a;margin-bottom:12px}
.admin-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}
.admin-card{background:#fff;border:1px solid var(--border);border-radius:10px;padding:14px;box-shadow:var(--shadow)}
.admin-card h3{font-family:var(--fh);font-size:.85rem;font-weight:700;text-transform:uppercase;letter-spacing:.6px;color:var(--muted);margin-bottom:9px}
.tag-list{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:10px;min-height:26px}
.tag{background:var(--bg);border:1.5px solid var(--border);border-radius:20px;padding:3px 10px;font-size:.76rem;display:flex;align-items:center;gap:5px;color:var(--text)}
.tag-del{background:none;border:none;color:var(--muted);cursor:pointer;font-size:.85rem;line-height:1;transition:color .15s;padding:0}
.tag-del:hover{color:var(--red)}
.add-inline{display:flex;gap:5px}
.add-inline input{flex:1;background:var(--bg);border:1.5px solid var(--border);border-radius:8px;color:var(--text);font-family:var(--fb);font-size:.83rem;padding:6px 9px;outline:none}
.add-inline input:focus{border-color:var(--accent)}
.add-inline button{background:var(--accent);border:none;border-radius:8px;color:#fff;font-family:var(--fh);font-weight:700;font-size:.83rem;padding:6px 12px;cursor:pointer;white-space:nowrap}
.add-inline button:hover{background:#c86e00}
.danger-zone{margin-top:18px;padding-top:14px;border-top:1px solid var(--border)}
.pass-row{display:flex;gap:6px;margin-top:8px}
.pass-row input{flex:1;background:var(--bg);border:1.5px solid var(--border);border-radius:8px;color:var(--text);font-family:var(--fb);font-size:.83rem;padding:6px 9px;outline:none}
.pass-row input:focus{border-color:var(--accent)}

/* MODAL */
.overlay{position:fixed;inset:0;z-index:100;background:rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;padding:14px}
.modal{background:#fff;border:1px solid var(--border);border-radius:14px;padding:22px;width:100%;max-width:520px;max-height:90vh;overflow-y:auto;animation:pop .18s ease;box-shadow:0 8px 32px rgba(0,0,0,.15)}
.modal-md{max-width:440px}
@keyframes pop{from{opacity:0;transform:scale(.95)}to{opacity:1;transform:scale(1)}}
.modal h2{font-family:var(--fh);font-size:1.2rem;font-weight:800;text-transform:uppercase;letter-spacing:1px;color:#1a2a4a;margin-bottom:16px}
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.form-grid .full{grid-column:1/-1}
.field label{display:block;font-size:.66rem;color:var(--muted);text-transform:uppercase;letter-spacing:.6px;margin-bottom:3px}
.field input,.field select,.field textarea{width:100%;background:var(--bg);border:1.5px solid var(--border);border-radius:8px;color:var(--text);font-family:var(--fb);font-size:.86rem;padding:7px 10px;outline:none;transition:border-color .18s}
.field input:focus,.field select:focus,.field textarea:focus{border-color:var(--accent)}
.modal-btns{display:flex;justify-content:flex-end;gap:9px;margin-top:18px}
.btn-cancel{background:transparent;border:1.5px solid var(--border);border-radius:8px;color:var(--muted);font-family:var(--fh);font-weight:700;font-size:.86rem;padding:8px 18px;cursor:pointer;transition:all .15s}
.btn-cancel:hover{border-color:var(--red);color:var(--red)}
.btn-save{background:var(--accent);border:none;border-radius:8px;color:#fff;font-family:var(--fh);font-weight:800;font-size:.86rem;padding:8px 22px;cursor:pointer}
.btn-save:hover{background:#c86e00}
.btn-desp{background:var(--green);border:none;border-radius:8px;color:#fff;font-family:var(--fh);font-weight:800;font-size:.86rem;padding:8px 22px;cursor:pointer}
.btn-desp:hover{background:#236b42}
.move-info{background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:10px 13px;margin-bottom:14px;font-size:.83rem;line-height:1.8}
.move-row{display:flex;flex-direction:column;gap:3px;margin-bottom:10px}
.move-row label{font-size:.66rem;color:var(--muted);text-transform:uppercase;letter-spacing:.6px}
.move-row select,.move-row input,.move-row textarea{width:100%;background:var(--bg);border:1.5px solid var(--border);border-radius:8px;color:var(--text);font-family:var(--fb);font-size:.86rem;padding:7px 10px;outline:none}
.move-row select:focus,.move-row input:focus,.move-row textarea:focus{border-color:var(--accent)}
.move-preview{background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:8px 12px;margin-top:5px;font-size:.81rem;color:var(--muted)}
.move-preview b{color:var(--text)}

/* PRINT */
@media print{
  *{-webkit-print-color-adjust:exact!important;print-color-adjust:exact!important}
  .no-print{display:none!important}
  .app{max-width:100%!important;padding:0!important}
  .hdr{background:#1a2a4a!important}
  .kpi-strip,.toolbar{display:none!important}
  .sv-filters,.hist-filters,.oc-filters{display:none!important}
  .table-wrap{overflow:visible!important}
  table{font-size:.73rem}
  thead tr{background:#f0f3f8!important}
  th{color:#444!important}
  tbody tr{background:#fff!important}
  tbody tr.low-row{background:#fff5f5!important}
  td{color:#111!important}
  .cell-muted{color:#555!important}
  .qty-big{color:#111!important}
  .badge{-webkit-print-color-adjust:exact}
  .sv-card{box-shadow:none!important;break-inside:avoid}
  .camp-title{color:#1a2a4a!important}
  .print-title{display:block!important;font-family:'Barlow Condensed',sans-serif;font-size:1.05rem;font-weight:800;text-transform:uppercase;color:#1a2a4a;border-bottom:2px solid #e07b00;padding-bottom:5px;margin:14px 0 10px}
}
.print-title{display:none}
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const {useState,useMemo,useCallback} = React;
const LOW = 5;
const fmt = n => Number(n).toLocaleString("es-AR");
const today = () => new Date().toISOString().slice(0,10);
const nowStr = () => new Date().toLocaleString("es-AR",{day:"2-digit",month:"2-digit",year:"numeric",hour:"2-digit",minute:"2-digit"});
const printDate = () => new Date().toLocaleDateString("es-AR",{day:"2-digit",month:"long",year:"numeric"});
const LOGO_SRC = "data:image/png;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJTEUAAQEAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAH4AABAAEAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAACRyWFlaAAABFAAAABRnWFlaAAABKAAAABRiWFlaAAABPAAAABR3dHB0AAABUAAAABRyVFJDAAABZAAAAChnVFJDAAABZAAAAChiVFJDAAABZAAAAChjcHJ0AAABjAAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEJYWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9YWVogAAAAAAAA9tYAAQAAAADTLXBhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACAAAAAcAEcAbwBvAGcAbABlACAASQBuAGMALgAgADIAMAAxADb/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wAARCACmAk8DASIAAhEBAxEB/8QAHQABAAMBAQEBAQEAAAAAAAAAAAYHCAQFAwkCAf/EAEsQAAEDAgICDAcQAAYCAwAAAAEAAgMEBQYRIZIHCBIVFjE1QVFUstITN1Nhc3SBFCIyNlVxcnWCkZOhsbPBwiMzQlJi0ZSiGCTw/8QAHAEBAAIDAQEBAAAAAAAAAAAAAAMEAgYHAQUI/8QAQBEAAQIDBAYGBwcEAgMAAAAAAAECAwQRBRITUQYUITEycRY0QVJToQcVFzNhscEiNXKBkdHhI0JDgvDxVKLi/9oADAMBAAIRAxEAPwAiKy7NaLXLaKKSSgp3PfTsc5xjGZJaMyvg27b0KxobIkRquvLTYXpGRdOOVrVpQrRFau8to+TaX8MJvLaPk2l/DC1n2iyfgu8j6PR+L308yqkVq7y2j5Npfwwm8to+TaX8MJ7RZPwXeQ6Pxe+nmVUitXeW0fJtフ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
