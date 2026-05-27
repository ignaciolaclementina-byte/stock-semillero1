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
        lote_data = payload.get("item", payload)
        
        if lote_data.get("id") or lote_data.get("ID"):
            lote_id = lote_data.get("id") or lote_data.get("ID")
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

# ==============================================================================
# 4. LECTURA DE DATOS DESDE GOOGLE SHEETS
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
# 5. INTEGRACIÓN DIRECTA CON TU INTERFAZ HTML ORIGINAL COMPLETA
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
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const {useState,useMemo,useCallback,useEffect} = React;
const LOW = 5;
const fmt = n => n===undefined||n===""?"0":Number(n).toLocaleString("es-AR");
const today = () => new Date().toISOString().slice(0,10);

function App() {
  const [user, setUser] = useState(null);
  const [tab, setTab] = useState("stock");
  const [stock, setStock] = useState(DB_STOCK);
  const [historial, setHistorial] = useState(DB_HISTORIAL);
  const [ordenes, setOrdenes] = useState(DB_ORDENES);
  const [catalogos, setCatalogos] = useState(DB_CATALOGOS);

  // Filtros de búsqueda local
  const [fCamp, setFCamp] = useState("TODAS");
  const [fEsp, setFEsp] = useState("TODAS");
  const [fDep, setFDep] = useState("TODOS");
  const [fText, setFText] = useState("");
  const [fTextHist, setFTextHist] = useState("");
  const [fTextOC, setFTextOC] = useState("");

  const [modal, setModal] = useState(null);

  // Cargar sesión persistente para evitar bloqueos
  useEffect(() => {
    const s = localStorage.getItem("lc_session");
    if(s) setUser(JSON.parse(s));
  }, []);

  const handleLogin = (pass) => {
    if(pass==="1234") {
      const u = {name:"Ignacio Diaz", role:"admin"};
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

  // Extracción dinámica de listas desde los catálogos
  const campañas = useMemo(() => ["TODAS", ...new Set(catalogos.filter(c=>c.Tipo==="Campaña").map(c=>c.Valor))], [catalogos]);
  const especies = useMemo(() => ["TODAS", ...new Set(catalogos.filter(c=>c.Tipo==="Especie").map(c=>c.Valor))], [catalogos]);
  const depositos = useMemo(() => ["TODOS", ...new Set(catalogos.filter(c=>c.Tipo==="Depósito").map(c=>c.Valor))], [catalogos]);
  const categorias = useMemo(() => catalogos.filter(c=>c.Tipo==="Categoría").map(c=>c.Valor), [catalogos]);
  const estados = useMemo(() => catalogos.filter(c=>c.Tipo==="Estado").map(c=>c.Valor), [catalogos]);

  const varMap = useMemo(() => {
    const m = {};
    catalogos.filter(c=>c.Tipo==="Variedad").forEach(c => {
      const esp = c.Padre || "SOJA";
      if(!m[esp]) m[esp] = [];
      m[esp].push(c.Valor);
    });
    return m;
  }, [catalogos]);

  // Totales dinámicos (KPIs)
  const totals = useMemo(() => {
    let b=0, k=0, l=0;
    stock.forEach(s => {
      const bags = parseInt(s.Bolsas)||0;
      b += bags;
      k += parseFloat(s.Kilos_Totales)||0;
      if(bags<=LOW) l++;
    });
    return {bolsas:fmt(b), kilos:fmt(Math.round(k)), low:l, ocs:ordenes.length};
  }, [stock, ordenes]);

  // Controladores de acciones (Inyección limpia a Streamlit)
  const handleSave = (item) => {
    window.parent.location.search = `?action=save_lote&payload=${encodeURIComponent(JSON.stringify(item))}`;
  };

  const handleMove = (mov) => {
    window.parent.location.search = `?action=move_lote&payload=${encodeURIComponent(JSON.stringify(mov))}`;
  };

  const handleCreateOC = (mov) => {
    window.parent.location.search = `?action=move_lote&payload=${encodeURIComponent(JSON.stringify(mov))}`;
  };

  // Funciones complementarias obligatorias para evitar que React falle
  const handleEditOC = (oc) => { alert("Acción delegada a Google Sheets de forma automática."); };
  const addTag = (tipo, valor, padre="") => { alert("Para agregar un catálogo modifique la pestaña 'Catalogos' de su Sheets."); };
  const delTag = (tipo, valor) => { alert("Para eliminar un catálogo modifique la pestaña 'Catalogos' de su Sheets."); };
  const handleChangePass = () => { alert("Función de clave administrativa de solo lectura."); };
  const resetAll = () => { alert("Función deshabilitada en el servidor para protección de datos."); };

  // Filtrado avanzado en frontend
  const filteredStock = useMemo(() => {
    return stock.filter(s => {
      if(fCamp!=="TODAS" && s.Campaña!==fCamp) return false;
      if(fEsp!=="TODAS" && s.Especie!==fEsp) return false;
      if(fDep Pall!== "TODOS" && fDep!=="TODOS" && s.Depósito!==fDep) return false;
      if(fText) {
        const t = fText.toLowerCase();
        return s.Variedad.toLowerCase().includes(t) || s.Notas.toLowerCase().includes(t) || String(s.ID).includes(t);
      }
      return true;
    });
  }, [stock, fCamp, fEsp, fDep, fText]);

  if(!user) {
    return (
      <div className="login-wrap">
        <div className="login-box">
          <h1>La Clementina</h1>
          <p>Control de Semillas & Logística</p>
          <input type="password" className="login-input" placeholder="••••" onKeyDown={e=>e.key==="Enter"&&handleLogin(e.target.value)}/>
          <button className="login-btn" onClick={(e)=>handleLogin(e.target.previousSibling.value)}>Ingresar</button>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="hdr no-print">
        <div className="hdr-left">
          <div>
            <h1>La Clementina <span>· Semillero Interactive</span></h1>
            <p>Panel de Administración de Stock y Despachos</p>
          </div>
        </div>
        <div className="hdr-tabs">
          <button className={`tab ${tab==="stock"?"active":""}`} onClick={()=>setTab("stock")}>📊 Stock</button>
          <button className={`tab ${tab==="resumen"?"active":""}`} onClick={()=>setTab("resumen")}>🔍 Resumen</button>
          <button className={`tab ${tab==="historial"?"active":""}`} onClick={()=>setTab("historial")}>📜 Historial</button>
          <button className={`tab ${tab==="ordenes"?"active":""}`} onClick={()=>setTab("ordenes")}>🚚 Órdenes ({totals.ocs})</button>
          <button className={`tab ${tab==="admin"?"active":""}`} onClick={()=>setTab("admin")}>⚙ Catálogos</button>
          <button className="tab" onClick={handleLogout} style={{color:"var(--red)"}}>🚪 Salir</button>
        </div>
      </header>

      <section className="kpi-strip no-print">
        <div className="kpi"><div className="kpi-val c-or">{totals.bolsas}</div><div className="kpi-lbl">Bolsas Netas</div></div>
        <div className="kpi"><div className="kpi-val c-bl">{totals.kilos}</div><div className="kpi-lbl">Kilos Totales</div></div>
        <div className="kpi"><div className="kpi-val c-gr">{totals.ocs}</div><div className="kpi-lbl">Órdenes Activas</div></div>
        <div className="kpi"><div className="kpi-val c-pu">{totals.low}</div><div className="kpi-lbl">Stock Crítico</div></div>
      </section>

      {tab==="stock" && (
        <div className="stock-view">
          <div className="toolbar no-print">
            <input type="text" className="search-inp" placeholder="Buscar Variedad o ID..." value={fText} onChange={e=>setFText(e.target.value)}/>
            <select className="sel" value={fCamp} onChange={e=>setFCamp(e.target.value)}>
              {campañAs.map(c=><option key={c} value={c}>{c}</option>)}
            </select>
            <select className="sel" value={fEsp} onChange={e=>setFEsp(e.target.value)}>
              {especies.map(e=><option key={e} value={e}>{e}</option>)}
            </select>
            <button className="btn btn-add" onClick={()=>setModal({mode:"new"})}>➕ Nuevo Lote</button>
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>ID</th><th>Campaña</th><th>Especie</th><th>Variedad</th><th>Categoría</th><th>Depósito</th><th>Bolsas</th><th>Kg/Bolsa</th><th>Kg Totales</th><th>Estado</th><th className="no-print">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {filteredStock.map(s=>(
                  <tr key={s.ID} className={parseInt(s.Bolsas)<=LOW?"low-row":""}>
                    <td><b>{s.ID}</b></td><td>{s.Campaña}</td><td><span className="badge bb">{s.Especie}</span></td><td><b>{s.Variedad}</b></td><td>{s.Categoría}</td><td>{s.Depósito}</td><td className="qty-big">{fmt(s.Bolsas)}</td><td>{s.Kilos_por_Bolsa}</td><td>{fmt(s.Kilos_Totales)}</td><td><span className="badge tr-b">{s.Estado}</span></td>
                    <td className="no-print">
                      <button className="action-btn" onClick={()=>setModal({mode:"edit", item:s})}>✏️</button>
                      <button className="action-btn dep" onClick={()=>setModal({mode:"move", item:s})}>🚚 Despachar</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {tab==="resumen" && (
        <div className="stock-view">
          <div className="sv-grid">
            {filteredStock.map(s=>(
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

      {tab==="historial" && (
        <div className="hist-view">
          <div className="table-wrap">
            <table>
              <thead>
                <tr><th>Fecha</th><th>Tipo</th><th>Detalle</th><th>Bolsas</th><th>Kilos</th><th>Operario</th></tr>
              </thead>
              <tbody>
                {historial.map((h,i)=>(
                  <tr key={i}>
                    <td className="cell-muted">{h.Fecha}</td><td><span className={`badge ${h.Tipo==="INGRESO"?"ing":"egr"}`}>{h.Tipo}</span></td><td>{h.Detalle}</td><td>{fmt(h.Bolsas)}</td><td>{fmt(h.Kilos)}</td><td><b>{h.Operario}</b></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {tab==="ordenes" && (
        <div className="oc-view">
          <div className="table-wrap">
            <table>
              <thead>
                <tr><th>OC #</th><th>Fecha</th><th>Variedad</th><th>Depósito</th><th>Bolsas</th><th>Cliente</th><th>Patentes</th><th>Estado</th><th className="no-print">Notificar</th></tr>
              </thead>
              <tbody>
                {ordenes.map(o => {
                  const msg = `La Clementina - OC %23${o.ID_Orden}%0ACliente: ${o.Cliente}%0AVariedad: ${o.Variedad}%0ABolsas: ${o.Bolsas}%0APatente: ${o.Patente_Chasis} / ${o.Patente_Acoplado}`;
                  return (
                    <tr key={o.ID_Orden}>
                      <td><b>#{o.ID_Orden}</b></td><td>{o.Fecha}</td><td>{o.Variedad}</td><td>{o.Depósito}</td><td className="qty-big">{fmt(o.Bolsas)}</td><td>{o.Cliente}</td><td>{o.Patente_Chasis} / {o.Patente_Acoplado}</td><td><span className="badge desp">{o.Estado}</span></td>
                      <td className="no-print">
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

      {tab==="admin" && (
        <div className="admin">
          <h2>Panel de Catálogos Existentes (Lectura Directa)</h2>
          <div className="admin-grid">
            <div className="admin-card"><h3>Campañas</h3><div className="tag-list">{campañas.map(t=><span className="tag" key={t}>{t}</span>)}</div></div>
            <div className="admin-card"><h3>Especies</h3><div className="tag-list">{especies.map(t=><span className="tag" key={t}>{t}</span>)}</div></div>
            <div className="admin-card"><h3>Depósitos</h3><div className="tag-list">{depositos.map(t=><span className="tag" key={t}>{t}</span>)}</div></div>
          </div>
        </div>
      )}

      {modal?.mode==="new" && <ModalForm campañas={campañas.filter(c=>c!=="TODAS")} especies={especies.filter(e=>e!=="TODAS")} varMap={varMap} onSave={handleSave} onClose={()=>setModal(null)} />}
      {modal?.mode==="edit" && <ModalForm item={modal.item} campañas={campañas.filter(c=>c!=="TODAS")} especies={especies.filter(e=>e!=="TODAS")} varMap={varMap} onSave={handleSave} onClose={()=>setModal(null)} />}
      {modal?.mode==="move" && <MoveModal item={modal.item} depositos={depositos.filter(d=>d!=="TODOS")} onSave={handleMove} onClose={()=>setModal(null)} />}
      
      <footer style={{position:"fixed", bottom:10, right:20, fontSize:"0.75rem", color:"#9ca3af"}} className="no-print">
        Creado por Ignacio Diaz
      </footer>
    </div>
  );
}

function ModalForm({ item, campañas, especies, varMap, onSave, onClose }) {
  const [campaña, setCampaña] = useState(item?.Campaña || campañas[0] || "25/26");
  const [especie, setEspecie] = useState(item?.Especie || especies[0] || "SOJA");
  const [variedad, setVariedad] = useState(item?.Variedad || "");
  const [categoría, setCategoría] = useState(item?.Categoría || "Original");
  const [depósito, setDepósito] = useState(item?.Depósito || "Planta 1");
  const [bolsas, setBolsas] = useState(item?.Bolsas || 0);
  const [kilosBolsa, setKilosBolsa] = useState(item?.Kilos_por_Bolsa || 40);
  const [estado, setEstado] = useState(item?.Estado || "DISPONIBLE");
  const [notas, setNotas] = useState(item?.Notas || "");

  return (
    <div className="overlay">
      <form className="modal" onSubmit={e=>{e.preventDefault(); onSave({ID:item?.ID, campaña, especie, variedad, categoría, depósito, bolsas, kilosBolsa, estado, notas})}}>
        <h2>{item ? "Editar Lote" : "Nuevo Lote"}</h2>
        <div className="form-grid">
          <div className="field"><label>Campaña</label><select value={campaña} onChange={e=>setCampaña(e.target.value)}>{campañas.map(c=><option key={c} value={c}>{c}</option>)}</select></div>
          <div className="field"><label>Especie</label><select value={especie} onChange={e=>setEspecie(e.target.value)}>{especies.map(e=><option key={e} value={e}>{e}</option>)}</select></div>
          <div className="field full"><label>Variedad</label><input type="text" value={variedad} onChange={e=>setVariedad(e.target.value)} required/></div>
          <div className="field"><label>Depósito</label><input type="text" value={depósito} onChange={e=>setDepósito(e.target.value)} required/></div>
          <div className="field"><label>Categoría</label><input type="text" value={categoría} onChange={e=>setCategoría(e.target.value)}/></div>
          <div className="field"><label>Bolsas</label><input type="number" value={bolsas} onChange={e=>setBolsas(e.target.value)} required/></div>
          <div className="field"><label>Kg por Bolsa</label><input type="number" value={kilosBolsa} onChange={e=>setKilosBolsa(e.target.value)} required/></div>
          <div className="field full"><label>Notas</label><textarea value={notas} onChange={e=>setNotas(e.target.value)}/></div>
        </div>
        <div className="modal-btns">
          <button type="button" className="btn-cancel" onClick={onClose}>Cancelar</button>
          <button type="submit" className="btn-save">💾 Guardar</button>
        </div>
      </form>
    </div>
  );
}

function MoveModal({ item, depositos, onSave, onClose }) {
  const [tipo, setTipo] = useState("transfer");
  const [cantidad, setCantidad] = useState(1);
  const [destino, setDestino] = useState("");
  const [cliente, setCliente] = useState("");
  const [chasis, setChasis] = useState("");
  const [acoplado, setAcoplado] = useState("");

  return (
    <div className="overlay">
      <form className="modal modal-md" onSubmit={e=>{e.preventDefault(); onSave({loteId:item.ID, tipo, cantidad, destino, cliente, chasis, acoplado})}}>
        <h2>Registrar Egreso / Traspaso</h2>
        <div className="move-info"><b>Lote:</b> {item.Variedad} ({item.Depósito})<br/><b>Bolsas Libres:</b> {item.Bolsas}</div>
        <div className="move-row">
          <label>Operación</label>
          <select value={tipo} onChange={e=>setTipo(e.target.value)}>
            <option value="transfer">Traspaso Interno</option>
            <option value="egreso">Despacho Comercial (Genera OC)</option>
          </select>
        </div>
        <div className="move-row"><label>Bolsas a Extraer</label><input type="number" min="1" max={item.Bolsas} value={cantidad} onChange={e=>setCantidad(e.target.value)} required/></div>
        {tipo==="transfer" ? (
          <div className="move-row"><label>Depósito Destino</label><input type="text" value={destino} onChange={e=>setDestino(e.target.value)} required/></div>
        ) : (
          <>
            <div className="move-row"><label>Cliente</label><input type="text" value={cliente} onChange={e=>setCliente(e.target.value)} required/></div>
            <div className="move-row"><label>Patente Chasis</label><input type="text" value={chasis} onChange={e=>setChasis(e.target.value)} required/></div>
            <div className="move-row"><label>Patente Acoplado</label><input type="text" value={acoplado} onChange={e=>setAcoplado(e.target.value)}/></div>
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

# Despliegue limpio ocupando la pantalla completa de Streamlit
st.components.v1.html(html_content, height=1200, scrolling=True)
