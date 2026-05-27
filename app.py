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
const {useState,useMemo,useCallback,useEffect} = React;

const LOW = 5;
const fmt = n => Number(n).toLocaleString("es-AR");
const today = () => new Date().toISOString().slice(0,10);
const nowStr = () => new Date().toLocaleString("es-AR",{day:"2-digit",month:"2-digit",year:"numeric",hour:"2-digit",minute:"2-digit"});
const printDate = () => new Date().toLocaleDateString("es-AR",{day:"2-digit",month:"long",year:"numeric"});

// Set de datos iniciales demo por defecto
const defaultCampanas = ['24/25', '25/26'];
const defaultEspecies = ['Soja', 'Maíz', 'Trigo', 'Girasol'];
const defaultVarMap = {
  'Soja': ['DM 46E21', 'AW 4721', 'DM 40i25 Enlist'],
  'Maíz': ['DK 72-10 VT3P', 'DK 72-27', 'AX 7761'],
  'Trigo': ['Baguette 620', 'Algarrobo', 'Catalpa'],
  'Girasol': ['Syn 3970 CL', 'DK 4045 CL']
};
const defaultStock = [
  { id: 1, campaña: '25/26', especie: 'Soja', variedad: 'DM 46E21', lote: 'L-201', origen: 'Propio', ubicacion: 'Galpón Norte', bolsas: 120, kg: 4800, tipo: 'Bolsas', tratamiento: 'Tratado', observaciones: 'Calidad excelente, curado completo.' },
  { id: 2, campaña: '25/26', especie: 'Maíz', variedad: 'DK 72-10 VT3P', lote: 'L-409', origen: 'Don Pedro', ubicacion: 'Silo 2', bolsas: 3, kg: 2100, tipo: 'Granel', tratamiento: 'Original', observaciones: 'Verificar humedad antes de despachar.' },
  { id: 3, campaña: '24/25', especie: 'Trigo', variedad: 'Baguette 620', lote: 'L-112', origen: 'La Colorada', ubicacion: 'Galpón Central', bolsas: 4, kg: 160, tipo: 'Bolsas', tratamiento: 'Original', observaciones: 'Remanente campaña anterior.' }
];
const defaultHistorial = [
  { id: 1, fecha: nowStr(), tipo: 'Ingreso', detalle: 'Carga inicial en sistema de Lote L-201', campaña: '25/26', especie: 'Soja', variedad: 'DM 46E21', bolsas: 120, kg: 4800 }
];
const defaultOC = [
  { id: 1, numero: 'OC-5001', fecha: today(), cliente: 'Agroganadera San Jorge', especie: 'Soja', variedad: 'DM 46E21', bolsas: 30, estado: 'Pendiente', observaciones: 'Coordinar flete propio cliente.' }
];

// Función mejorada y profesional para armado de mensajes de WhatsApp
const sendWhatsAppMessage = (text) => {
  const cleanText = encodeURIComponent(text);
  window.open(`https://api.whatsapp.com/send?text=${cleanText}`, '_blank');
};

function App() {
  // Autenticación y Seguridad
  const [isAuthenticated, setIsAuthenticated] = useState(() => localStorage.getItem('lc_auth') === 'true');
  const [password, setPassword] = useState('');
  const [savedPassword, setSavedPassword] = useState(() => localStorage.getItem('lc_pass') || '1234');
  const [loginError, setLoginError] = useState(false);

  // Estados Core de la App
  const [tab, setTab] = useState('resumen');
  const [campañas, setCampañas] = useState(() => JSON.parse(localStorage.getItem('lc_campañas')) || defaultCampanas);
  const [especies, setEspecies] = useState(() => JSON.parse(localStorage.getItem('lc_especies')) || defaultEspecies);
  const [varMap, setVarMap] = useState(() => JSON.parse(localStorage.getItem('lc_varmap')) || defaultVarMap);
  const [stock, setStock] = useState(() => JSON.parse(localStorage.getItem('lc_stock')) || defaultStock);
  const [historial, setHistorial] = useState(() => JSON.parse(localStorage.getItem('lc_historial')) || defaultHistorial);
  const [ocList, setOcList] = useState(() => JSON.parse(localStorage.getItem('lc_oc')) || defaultOC);

  // Estado del indicador de autoguardado
  const [saveStatus, setSaveStatus] = useState('saved'); // 'saved' | 'saving'

  // Estados de Filtros Comunes
  const [search, setSearch] = useState('');
  const [fCampaña, setFCampaña] = useState('TODAS');
  const [fEspecie, setFEspecie] = useState('TODAS');
  const [fEstado, setFEstado] = useState('TODOS');

  // Control de Modales
  const [modal, setModal] = useState(null); // { mode: 'new'|'edit'|'move'|'editOC', item: ... , oc: ... }

  // Sincronización automática con LocalStorage simulando Backend reactivo
  useEffect(() => {
    if (!isAuthenticated) return;
    setSaveStatus('saving');
    const timer = setTimeout(() => {
      localStorage.setItem('lc_campañas', JSON.stringify(campañas));
      localStorage.setItem('lc_especies', JSON.stringify(especies));
      localStorage.setItem('lc_varmap', JSON.stringify(varMap));
      localStorage.setItem('lc_stock', JSON.stringify(stock));
      localStorage.setItem('lc_historial', JSON.stringify(historial));
      localStorage.setItem('lc_oc', JSON.stringify(ocList));
      setSaveStatus('saved');
    }, 4000);
    return () => clearTimeout(timer);
  }, [campañas, especies, varMap, stock, historial, ocList, isAuthenticated]);

  // Handler Login
  const handleLogin = (e) => {
    e.preventDefault();
    if (password === savedPassword) {
      localStorage.setItem('lc_auth', 'true');
      setIsAuthenticated(true);
      setLoginError(false);
    } else {
      setLoginError(true);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('lc_auth');
    setIsAuthenticated(false);
    setPassword('');
  };

  const handleChangePass = () => {
    const newPass = document.getElementById('new_pass_input').value.trim();
    if (newPass) {
      localStorage.setItem('lc_pass', newPass);
      setSavedPassword(newPass);
      alert('Contraseña actualizada correctamente.');
      document.getElementById('new_pass_input').value = '';
    }
  };

  const resetAll = () => {
    if (confirm('¿Está absolutamente seguro de resetear todos los datos del inventario? Esta acción borrará el almacenamiento local.')) {
      localStorage.clear();
      setCampañas(defaultCampanas);
      setEspecies(defaultEspecies);
      setVarMap(defaultVarMap);
      setStock(defaultStock);
      setHistorial(defaultHistorial);
      setOcList(defaultOC);
      setSavedPassword('1234');
      alert('Sistema restaurado al estado de demostración inicial.');
      window.location.reload();
    }
  };

  // KPIs Calculados
  const kpis = useMemo(() => {
    let totKg = 0;
    let totBolsas = 0;
    let alertasBajo = 0;
    stock.forEach(i => {
      totKg += Number(i.kg || 0);
      if (i.tipo === 'Bolsas') {
        totBolsas += Number(i.bolsas || 0);
        if (Number(i.bolsas || 0) <= LOW) alertasBajo++;
      } else {
        if (Number(i.kg || 0) <= LOW * 50) alertasBajo++;
      }
    });
    const pendOC = ocList.filter(o => o.estado === 'Pendiente').length;
    return { totKg, totBolsas, pendOC, alertasBajo };
  }, [stock, ocList]);

  // Filtro de Datos para tabla de Stock
  const filteredStock = useMemo(() => {
    return stock.filter(i => {
      const matchSearch = !search || 
        i.variedad.toLowerCase().includes(search.toLowerCase()) ||
        i.lote.toLowerCase().includes(search.toLowerCase()) ||
        i.ubicacion.toLowerCase().includes(search.toLowerCase()) ||
        i.origen.toLowerCase().includes(search.toLowerCase());
      const matchCamp = fCampaña === 'TODAS' || i.campaña === fCampaña;
      const matchEsp = fEspecie === 'TODAS' || i.especie === fEspecie;
      
      let matchEst = true;
      if (fEstado === 'ALERTA') {
        matchEst = i.tipo === 'Bolsas' ? (i.bolsas <= LOW) : (i.kg <= LOW * 50);
      } else if (fEstado === 'TRATADO') {
        matchEst = i.tratamiento === 'Tratado';
      } else if (fEstado === 'ORIGINAL') {
        matchEst = i.tratamiento === 'Original';
      }

      return matchSearch && matchCamp && matchEsp && matchEst;
    });
  }, [stock, search, fCampaña, fEspecie, fEstado]);

  // ABM Acciones Stock
  const handleSaveItem = (itemData) => {
    if (itemData.id) {
      // Editar
      setStock(prev => prev.map(x => x.id === itemData.id ? itemData : x));
    } else {
      // Crear Nuevo
      const newItem = { ...itemData, id: Date.now() };
      setStock(prev => [newItem, ...prev]);
      // Registrar en historial automáticamente
      setHistorial(h => [{
        id: Date.now(),
        fecha: nowStr(),
        tipo: 'Ingreso',
        detalle: `Alta manual de lote ${newItem.lote}`,
        campaña: newItem.campaña,
        especie: newItem.especie,
        variedad: newItem.variedad,
        bolsas: newItem.bolsas,
        kg: newItem.kg
      }, ...h]);
    }
    setModal(null);
  };

  const handleDeleteItem = (id) => {
    const target = stock.find(x => x.id === id);
    if (!target) return;
    if (confirm(`¿Eliminar por completo el lote ${target.lote} (${target.variedad}) del stock?`)) {
      setStock(prev => prev.filter(x => x.id !== id));
      setHistorial(h => [{
        id: Date.now(),
        fecha: nowStr(),
        tipo: 'Egreso',
        detalle: `Eliminación de lote: ${target.lote}`,
        campaña: target.campaña,
        especie: target.especie,
        variedad: target.variedad,
        bolsas: target.bolsas,
        kg: target.kg
      }, ...h]);
    }
  };

  // Movimientos e Interacciones Avanzadas (Despacho / Transferencias)
  const handleMoveStock = (movement) => {
    const { itemId, tipoMov, cantidadBolsas, cantidadKg, destino, observaciones } = movement;
    setStock(prev => {
      return prev.map(item => {
        if (item.id === itemId) {
          let nBolsas = Number(item.bolsas);
          let nKg = Number(item.kg);
          if (tipoMov === 'Egreso' || tipoMov === 'Despacho') {
            nBolsas = Math.max(0, nBolsas - Number(cantidadBolsas));
            nKg = Math.max(0, nKg - Number(cantidadKg));
          } else if (tipoMov === 'Ingreso') {
            nBolsas += Number(cantidadBolsas);
            nKg += Number(cantidadKg);
          }
          return { ...item, bolsas: nBolsas, kg: nKg, observaciones: observaciones || item.observaciones };
        }
        return item;
      });
    });

    const refItem = stock.find(x => x.id === itemId);
    // Agregar registro al historial
    setHistorial(h => [{
      id: Date.now(),
      fecha: nowStr(),
      tipo: tipoMov,
      detalle: `${tipoMov} - Destino/Motivo: ${destino || 'No especificado'}`,
      campaña: refItem.campaña,
      especie: refItem.especie,
      variedad: refItem.variedad,
      bolsas: cantidadBolsas,
      kg: cantidadKg
    }, ...h]);

    // Armar notificación para WhatsApp automatizada
    const whatsMessage = `*La Clementina · Notificación Stock Semillas*\n\n` +
      `Se registró un movimiento de tipo *${tipoMov}*.\n` +
      `• *Especie/Var:* ${refItem.especie} - ${refItem.variedad}\n` +
      `• *Lote:* ${refItem.lote}\n` +
      `• *Cantidad:* ${cantidadBolsas} Bolsas (${cantidadKg} Kg)\n` +
      `• *Destino/Notas:* ${destino || '-'}\n` +
      `• *Fecha/Hora:* ${nowStr()}\n\n` +
      `_Monitoreo de stock en tiempo real._`;
    
    setModal(null);
    setTimeout(() => {
      if (confirm('¿Desea enviar la notificación de movimiento por WhatsApp?')) {
        sendWhatsAppMessage(whatsMessage);
      }
    }, 100);
  };

  const handleCreateOCFromMove = (ocData) => {
    const newOC = {
      id: Date.now(),
      numero: `OC-${Math.floor(1000 + Math.random() * 9000)}`,
      fecha: today(),
      cliente: ocData.cliente,
      especie: ocData.especie,
      variedad: ocData.variedad,
      bolsas: ocData.bolsas,
      estado: 'Pendiente',
      observaciones: ocData.observaciones
    };
    setOcList(prev => [newOC, ...prev]);
    alert(`Orden de Compra ${newOC.numero} para ${newOC.cliente} creada de manera pendiente.`);
  };

  const handleEditOCStatus = (id, newStatus) => {
    setOcList(prev => prev.map(o => o.id === id ? { ...o, estado: newStatus } : o));
    
    // Si se despacha, sugerir armar reporte
    if (newStatus === 'Despachado') {
      const itemOC = ocList.find(o => o.id === id);
      const msg = `*La Clementina · Orden de Compra Despachada*\n\n` +
        `• *Nro:* ${itemOC.numero}\n` +
        `• *Cliente:* ${itemOC.cliente}\n` +
        `• *Detalle:* ${itemOC.bolsas} Bolsas de ${itemOC.especie} (${itemOC.variedad})\n` +
        `• *Estado:* ¡DESPACHADO!\n\n` +
        `Saludos.`;
      setTimeout(() => {
        if (confirm('¿Desea enviar el aviso de despacho de OC por WhatsApp?')) {
          sendWhatsAppMessage(msg);
        }
      }, 500);
    }
  };

  // Configuración de Tags (Admin)
  const handleAddTag = (category, value) => {
    if (!value.trim()) return;
    if (category === 'campaña') {
      if (!campañas.includes(value)) setCampañas([...campañas, value]);
    } else if (category === 'especie') {
      if (!especies.includes(value)) {
        setEspecies([...especies, value]);
        setVarMap({ ...varMap, [value]: [] });
      }
    }
  };

  const handleRemoveTag = (category, value) => {
    if (category === 'campaña') {
      setCampañas(campañas.filter(x => x !== value));
    } else if (category === 'especie') {
      setEspecies(especies.filter(x => x !== value));
    }
  };

  const handleAddVariedad = (especie, variedad) => {
    if (!variedad.trim()) return;
    const currentList = varMap[especie] || [];
    if (!currentList.includes(variedad)) {
      setVarMap({
        ...varMap,
        [especie]: [...currentList, variedad]
      });
    }
  };

  const handleRemoveVariedad = (especie, variedad) => {
    const currentList = varMap[especie] || [];
    setVarMap({
      ...varMap,
      [especie]: currentList.filter(x => x !== variedad)
    });
  };

  // Render Pantalla de Logueo Completa
  if (!isAuthenticated) {
    return (
      <div className="login-wrap">
        <form className="login-box" onSubmit={handleLogin}>
          <h1>La Clementina</h1>
          <p>Control Interno · Stock de Semillas</p>
          <input 
            type="password" 
            className={`login-input ${loginError ? 'err' : ''}`}
            placeholder="••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {loginError && <div className="err-msg">Contraseña incorrecta. Intente de nuevo.</div>}
          <button type="submit" className="login-btn">Ingresar al Sistema</button>
        </form>
      </div>
    );
  }

  return (
    <div className="app">
      {/* HEADER DE APLICACIÓN */}
      <header className="hdr">
        <div className="hdr-left">
          <div>
            <h1>La Clementina · <span>Stock Semillas</span></h1>
            <p>Monitoreo y Logística Primaria de Semilleros</p>
          </div>
        </div>
        <div className="hdr-right">
          <div className="save-ind">
            {saveStatus === 'saving' ? (
              <span className="save-ing">⏳ Sincronizando cambios locales...</span>
            ) : (
              <span className="save-ok">✓ Base Blindada y Sincronizada</span>
            )}
          </div>
          <div className="hdr-tabs no-print">
            <button className={`tab ${tab === 'resumen' ? 'active' : ''}`} onClick={() => setTab('resumen')}>Resumen General</button>
            <button className={`tab ${tab === 'stock' ? 'active' : ''}`} onClick={() => setTab('stock')}>Inventario Físico</button>
            <button className={`tab ${tab === 'historial' ? 'active' : ''}`} onClick={() => setTab('historial')}>Historial Tráfico</button>
            <button className={`tab ${tab === 'oc' ? 'active' : ''}`} onClick={() => setTab('oc')}>Órdenes (OC)</button>
            <button className={`tab ${tab === 'admin' ? 'active' : ''}`} onClick={() => setTab('admin')}>Configuración</button>
            <button className="tab" style={{borderColor:'var(--red)', color:'#ff9494'}} onClick={handleLogout}>Salir</button>
          </div>
        </div>
      </header>

      {/* KPI STRIP */}
      <section className="kpi-strip">
        <div className="kpi">
          <div className="kpi-val c-or">{fmt(kpis.totBolsas)}</div>
          <div className="kpi-lbl">Bolsas Totales</div>
        </div>
        <div className="kpi">
          <div className="kpi-val c-bl">{fmt(kpis.totKg)}</div>
          <div className="kpi-lbl">Kilogramos Netos</div>
        </div>
        <div className="kpi">
          <div className="kpi-val c-pu">{kpis.pendOC}</div>
          <div className="kpi-lbl">OC Pendientes</div>
        </div>
        <div className="kpi">
          <div className="kpi-val c-gr">{(kpis.totKg / 1000).toFixed(1)} t</div>
          <div className="kpi-lbl">Métricas de Volumen</div>
        </div>
        <div className="kpi" style={{background: kpis.alertasBajo > 0 ? '#fff0f0' : ''}}>
          <div className="kpi-val c-red">{kpis.alertasBajo}</div>
          <div className="kpi-lbl" style={{color: kpis.alertasBajo > 0 ? 'var(--red)' : ''}}>Alertas Stock Crítico</div>
        </div>
      </section>

      {/* VISTA: RESUMEN DE STOCK (CARDS) */}
      {tab === 'resumen' && (
        <div className="stock-view">
          <div className="sv-filters no-print">
            <select className="sel" value={fCampaña} onChange={e => setFCampaña(e.target.value)}>
              <option value="TODAS">Todas las Campañas</option>
              {campañas.map(c => <option key={c} value={c}>Campaña {c}</option>)}
            </select>
            <select className="sel" value={fEspecie} onChange={e => setFEspecie(e.target.value)}>
              <option value="TODAS">Todas las Especies</option>
              {especies.map(e => <option key={e} value={e}>{e}</option>)}
            </select>
            <button className="btn btn-ol" onClick={() => window.print()}>🖨 Imprimir Reporte Consolidado</button>
          </div>

          <h2 className="print-title">La Clementina · Reporte General de Existencias - {printDate()}</h2>

          {campañas.filter(c => fCampaña === 'TODAS' || c === fCampaña).map(camp => {
            // Verificar si hay stock en esta campaña
            const stockCamp = stock.filter(s => s.campaña === camp && (fEspecie === 'TODAS' || s.especie === fEspecie));
            if (stockCamp.length === 0) return null;

            return (
              <div key={camp} className="camp-block">
                <div className="camp-title">
                  <span>Campaña {camp}</span>
                  <span className="camp-sub">{stockCamp.reduce((a, b) => a + Number(b.bolsas), 0)} Bolsas Totales</span>
                </div>

                {especies.filter(e => fEspecie === 'TODAS' || e === fEspecie).map(esp => {
                  const stockEsp = stockCamp.filter(s => s.especie === esp);
                  if (stockEsp.length === 0) return null;

                  return (
                    <div key={esp} className="esp-block">
                      <h3 className="esp-title">{esp}</h3>
                      <div className="sv-grid">
                        {stockEsp.map(item => {
                          const isLow = item.tipo === 'Bolsas' ? (item.bolsas <= LOW) : (item.kg <= LOW * 50);
                          return (
                            <div key={item.id} className="sv-card" style={{borderTopColor: isLow ? 'var(--red)' : 'var(--accent)'}}>
                              <div className="sv-head">
                                <span className="sv-variedad">{item.variedad}</span>
                                <span className={`badge ${item.tipo === 'Bolsas' ? 'bb' : 'bo'}`}>{item.tipo}</span>
                              </div>
                              <div className="sv-row">
                                <span className="sv-label">Lote / Identificador:</span>
                                <span className="sv-val" style={{color:'var(--blue)'}}>{item.lote}</span>
                              </div>
                              <div className="sv-row">
                                <span className="sv-label">Ubicación Física:</span>
                                <span className="sv-val cell-muted">{item.ubicacion}</span>
                              </div>
                              <div className="sv-row">
                                <span className="sv-label">Tratamiento:</span>
                                <span className={`badge ${item.tratamiento === 'Tratado' ? 'tr-b' : 'st-b'}`}>{item.tratamiento}</span>
                              </div>
                              <div className="sv-row" style={{background: isLow ? '#fff5f5' : '', padding:'4px 2px'}}>
                                <span className="sv-label">Stock Neto:</span>
                                <span className="sv-val" style={{color: isLow ? 'var(--red)' : 'var(--green)'}}>
                                  {item.tipo === 'Bolsas' ? `${fmt(item.bolsas)} Bolsas` : `${fmt(item.kg)} Kg`}
                                </span>
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  );
                })}
              </div>
            );
          })}
        </div>
      )}

      {/* VISTA: INVENTARIO FÍSICO DETALLADO (TABLA) */}
      {tab === 'stock' && (
        <div className="hist-view">
          <div className="toolbar no-print">
            <div className="search-wrap">
              <span className="search-icon">🔍</span>
              <input 
                type="text" 
                className="search-inp" 
                placeholder="Buscar por lote, variedad, ubicación u origen..."
                value={search}
                onChange={e => setSearch(e.target.value)}
              />
            </div>
            <select className="sel" value={fCampaña} onChange={e => setFCampaña(e.target.value)}>
              <option value="TODAS">Campaña: Todas</option>
              {campañas.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
            <select className="sel" value={fEspecie} onChange={e => setFEspecie(e.target.value)}>
              <option value="TODAS">Especie: Todas</option>
              {especies.map(e => <option key={e} value={e}>{e}</option>)}
            </select>
            <select className="sel" value={fEstado} onChange={e => setFEstado(e.target.value)}>
              <option value="TODOS">Todos los Estados</option>
              <option value="ALERTA">⚠ Stock Mínimo Crítico</option>
              <option value="TRATADO">Solo Tratados</option>
              <option value="ORIGINAL">Solo Originales</option>
            </select>
            <button className="btn btn-add" onClick={() => setModal({mode: 'new'})}>＋ Dar de Alta Lote</button>
          </div>

          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Campaña</th>
                  <th>Especie</th>
                  <th>Variedad / Genética</th>
                  <th>Lote</th>
                  <th>Ubicación</th>
                  <th>Tipo</th>
                  <th>Tratamiento</th>
                  <th style={{textAlign:'right'}}>Bolsas</th>
                  <th style={{textAlign:'right'}}>Kg Netos</th>
                  <th className="no-print" style={{textAlign:'center'}}>Acciones Operativas</th>
                </tr>
              </thead>
              <tbody>
                {filteredStock.length === 0 ? (
                  <tr>
                    <td colSpan="10" className="no-data">Ningún lote físico coincide con los criterios de filtrado.</td>
                  </tr>
                ) : (
                  filteredStock.map(item => {
                    const isLow = item.tipo === 'Bolsas' ? (item.bolsas <= LOW) : (item.kg <= LOW * 50);
                    return (
                      <tr key={item.id} className={isLow ? 'low-row' : ''}>
                        <td><b>{item.campaña}</b></td>
                        <td><span style={{color:'var(--blue)', fontWeight:600}}>{item.especie}</span></td>
                        <td>{item.variedad} {isLow && <span style={{color:'var(--red)'}}>⚠</span>}</td>
                        <td><code style={{background:'#eef1f6', padding:'2px 5px', borderRadius:4}}>{item.lote}</code></td>
                        <td className="cell-muted">{item.ubicacion}</td>
                        <td><span className={`badge ${item.tipo === 'Bolsas' ? 'bb' : 'bo'}`}>{item.tipo}</span></td>
                        <td><span className={`badge ${item.tratamiento === 'Tratado' ? 'tr-b' : 'st-b'}`}>{item.tratamiento}</span></td>
                        <td style={{textAlign:'right', fontWeight:700}}>{fmt(item.bolsas)}</td>
                        <td style={{textAlign:'right'} } className="qty-big">{fmt(item.kg)}</td>
                        <td className="no-print" style={{textAlign:'center', whiteSpace:'nowrap'}}>
                          <button className="action-btn dep" title="Registrar Movimiento / Despacho" onClick={() => setModal({mode: 'move', item})}>📦 Mover</button>
                          <button className="action-btn" title="Editar Parámetros Lote" onClick={() => setModal({mode: 'edit', item})}>✏</button>
                          <button className="action-btn del" title="Eliminar de Registro" onClick={() => handleDeleteItem(item.id)}>🗑</button>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* VISTA: HISTORIAL DE TRAFICO */}
      {tab === 'historial' && (
        <div className="hist-view">
          <div className="sv-filters no-print">
            <button className="btn btn-ol" onClick={() => {
              if (confirm('¿Limpiar el log de historial?')) setHistorial([]);
            }}>Limpiar Registro Histórico</button>
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Fecha/Hora</th>
                  <th>Operación</th>
                  <th>Campaña</th>
                  <th>Especie</th>
                  <th>Variedad</th>
                  <th>Detalle / Destinatario</th>
                  <th style={{textAlign:'right'}}>Bolsas</th>
                  <th style={{textAlign:'right'}}>Kg Movidos</th>
                </tr>
              </thead>
              <tbody>
                {historial.length === 0 ? (
                  <tr>
                    <td colSpan="8" className="no-data">No hay registros de tráfico recientes en la base blindada.</td>
                  </tr>
                ) : (
                  historial.map(h => (
                    <tr key={h.id}>
                      <td className="cell-muted">{h.fecha}</td>
                      <td>
                        <span className={`badge ${h.tipo === 'Ingreso' ? 'ing' : 'egr'}`}>{h.tipo}</span>
                      </td>
                      <td>{h.campaña}</td>
                      <td>{h.especie}</td>
                      <td>{h.variedad}</td>
                      <td className="cell-muted">{h.detalle}</td>
                      <td style={{textAlign:'right', fontWeight:600}} className={h.tipo === 'Ingreso' ? 'dpos' : 'dneg'}>
                        {h.tipo === 'Ingreso' ? `+${h.bolsas}` : `-${h.bolsas}`}
                      </td>
                      <td style={{textAlign:'right', fontWeight:600}} className={h.tipo === 'Ingreso' ? 'dpos' : 'dneg'}>
                        {h.tipo === 'Ingreso' ? `+${fmt(h.kg)}` : `-${fmt(h.kg)}`}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* VISTA: ÓRDENES DE COMPRA (OC) */}
      {tab === 'oc' && (
        <div className="oc-view">
          <div className="toolbar no-print">
            <h3 style={{fontFamily:'var(--fh)', fontSize:'1.1rem'}}>Logística de Ventas y Reservas</h3>
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Código OC</th>
                  <th>Fecha Emisión</th>
                  <th>Cliente Solicitante</th>
                  <th>Insumo / Variedad</th>
                  <th style={{textAlign:'right'}}>Cant. Bolsas</th>
                  <th>Estado Reserva</th>
                  <th>Observaciones</th>
                  <th className="no-print" style={{textAlign:'center'}}>Gestión de Estado</th>
                </tr>
              </thead>
              <tbody>
                {ocList.length === 0 ? (
                  <tr>
                    <td colSpan="8" className="no-data">No hay órdenes registradas.</td>
                  </tr>
                ) : (
                  ocList.map(o => (
                    <tr key={o.id}>
                      <td><b style={{color:'var(--purple)'}}>{o.numero}</b></td>
                      <td className="cell-muted">{o.fecha}</td>
                      <td>{o.cliente}</td>
                      <td><b>{o.especie}</b> · {o.variedad}</td>
                      <td style={{textAlign:'right', fontWeight:700}}>{o.bolsas} b.</td>
                      <td>
                        <span className={`badge ${o.estado === 'Pendiente' ? 'pend' : 'desp'}`}>{o.estado}</span>
                      </td>
                      <td className="cell-muted">{o.observaciones || '-'}</td>
                      <td className="no-print" style={{textAlign:'center'}}>
                        {o.estado === 'Pendiente' ? (
                          <button className="btn btn-sm btn-ol gnh" onClick={() => handleEditOCStatus(o.id, 'Despachado')}>✓ Despachar Insumo</button>
                        ) : (
                          <span style={{color:'var(--green)', fontSize:'.75rem', fontWeight:'bold'}}>Entrega Concluida</span>
                        )}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* VISTA: CONFIGURACION Y PARAMETRIZACION */}
      {tab === 'admin' && (
        <div className="admin">
          <div className="admin-grid">
            
            <div className="admin-card">
              <h3>Campañas Activas</h3>
              <div className="tag-list">
                {campañas.map(c => (
                  <span key={c} className="tag">{c} <button className="tag-del" onClick={() => handleRemoveTag('campaña', c)}>×</button></span>
                ))}
              </div>
              <div className="add-inline">
                <input type="text" id="new_camp" placeholder="Ej: 26/27"/>
                <button onClick={() => {
                  const val = document.getElementById('new_camp').value;
                  handleAddTag('campaña', val);
                  document.getElementById('new_camp').value = '';
                }}>Añadir</button>
              </div>
            </div>

            <div className="admin-card">
              <h3>Especies Estructuradas</h3>
              <div className="tag-list">
                {especies.map(e => (
                  <span key={e} className="tag">{e} <button className="tag-del" onClick={() => handleRemoveTag('especie', e)}>×</button></span>
                ))}
              </div>
              <div className="add-inline">
                <input type="text" id="new_esp" placeholder="Ej: Sorgo"/>
                <button onClick={() => {
                  const val = document.getElementById('new_esp').value;
                  handleAddTag('especie', val);
                  document.getElementById('new_esp').value = '';
                }}>Añadir</button>
              </div>
            </div>

            <div className="admin-card" style={{gridColumn: '1 / -1'}}>
              <h3>Variedades por Catálogo de Especie</h3>
              <div style={{display:'grid', gridTemplateColumns:'repeat(auto-fit, minmax(240px, 1fr))', gap:12, marginTop:10}}>
                {especies.map(esp => (
                  <div key={esp} style={{background:'var(--bg)', padding:10, borderRadius:8, border:'1px solid var(--border)'}}>
                    <h4 style={{fontSize:'.8rem', textTransform:'uppercase', color:'var(--blue)', marginBottom:6}}>{esp}</h4>
                    <div className="tag-list">
                      {(varMap[esp] || []).map(v => (
                        <span key={v} className="tag" style={{background:'#fff'}}>{v} 
                          <button className="tag-del" onClick={() => handleRemoveVariedad(esp, v)}>×</button>
                        </span>
                      ))}
                    </div>
                    <div className="add-inline">
                      <input type="text" id={`new_var_${esp}`} placeholder="Nueva variedad..."/>
                      <button onClick={() => {
                        const val = document.getElementById(`new_var_${esp}`).value;
                        handleAddVariedad(esp, val);
                        document.getElementById(`new_var_${esp}`).value = '';
                      }}>＋</button>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="admin-card">
              <h3>Seguridad Administrativa</h3>
              <p style={{fontSize:'.75rem', color:'var(--muted)', marginBottom:8}}>Cambiar la clave maestra de acceso al panel:</p>
              <div className="pass-row">
                <input type="password" id="new_pass_input" placeholder="Nueva clave..."/>
                <button className="btn btn-ol gnh" onClick={handleChangePass}>✓ Guardar</button>
              </div>
            </div>

            <div className="admin-card" style={{borderColor:"#f5a5a5"}}>
              <div className="danger-zone" style={{margin:0,padding:0,border:"none"}}>
                <h3 style={{color:"var(--red)",marginBottom:8}}>⚠ Zona de peligro</h3>
                <p style={{fontSize:\".8rem\",color:\"var(--muted)\",marginBottom:10}}>Borra todo el stock, historial, órdenes y catálogos, volviendo al estado inicial de demostración.</p>
                <button className="btn btn-ol rh" onClick={resetAll}>🗑 Resetear todos los datos</button>
              </div>
            </div>

          </div>
        </div>
      )}

      {/* PIE DE PÁGINA OBLIGATORIO - BLINDADO */}
      <footer className="no-print" style={{textAlign:"center", padding:20, fontSize:".75rem", color:"var(--muted)", borderTop:"1px solid var(--border)", marginTop:40}}>
        La Clementina · Sistema de Control de Stock de Semillas<br/>
        <strong>Creado por Ignacio Diaz</strong>
      </footer>

      {/* MODALES INTERACTIVOS */}
      {modal?.mode === 'new' && (
        <ModalForm campañas={campañas} especies={especies} varMap={varMap} onSave={handleSaveItem} onClose={() => setModal(null)}/>
      )}
      {modal?.mode === 'edit' && (
        <ModalForm item={modal.item} campañas={campañas} especies={especies} varMap={varMap} onSave={handleSaveItem} onClose={() => setModal(null)}/>
      )}
      {modal?.mode === 'move' && (
        <MoveModal stock={stock} item={modal.item} onSave={handleMoveStock} onCreateOC={handleCreateOCFromMove} onClose={() => setModal(null)}/>
      )}
    </div>
  );
}

// FORMULARIO MODAL: ALTA Y EDICIÓN
function ModalForm({ item, campañas, especies, varMap, onSave, onClose }) {
  const [campaña, setCampaña] = useState(item ? item.campaña : campañas[0] || '');
  const [especie, setEspecie] = useState(item ? item.especie : especies[0] || '');
  const [variedad, setVariedad] = useState(item ? item.variedad : '');
  const [lote, setLote] = useState(item ? item.lote : '');
  const [origen, setOrigen] = useState(item ? item.origen : '');
  const [ubicacion, setUbicacion] = useState(item ? item.ubicacion : '');
  const [bolsas, setBolsas] = useState(item ? item.bolsas : 0);
  const [kg, setKg] = useState(item ? item.kg : 0);
  const [tipo, setTipo] = useState(item ? item.tipo : 'Bolsas');
  const [tratamiento, setTratamiento] = useState(item ? item.tratamiento : 'Original');
  const [observaciones, setObservaciones] = useState(item ? item.observaciones : '');

  // Sincronizar variedad por defecto si cambia la especie elegida
  const availableVarieties = varMap[especie] || [];
  useEffect(() => {
    if (!item && availableVarieties.length > 0) {
      setVariedad(availableVarieties[0]);
    }
  }, [especie]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!lote || !variedad) {
      alert('Por favor complete Lote y Variedad de forma obligatoria.');
      return;
    }
    onSave({
      id: item?.id,
      campaña, especie, variedad, lote, origen, ubicacion,
      bolsas: Number(bolsas), kg: Number(kg), tipo, tratamiento, observaciones
    });
  };

  return (
    <div className="overlay">
      <form className="modal" onSubmit={handleSubmit}>
        <h2>{item ? 'Editar Parámetros de Lote' : 'Alta de Insumo / Lote Físico'}</h2>
        <div className="form-grid">
          <div className="field">
            <label>Campaña</label>
            <select value={campaña} onChange={e => setCampaña(e.target.value)}>
              {campañas.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
          <div className="field">
            <label>Especie</label>
            <select value={especie} onChange={e => setEspecie(e.target.value)}>
              {especies.map(e => <option key={e} value={e}>{e}</option>)}
            </select>
          </div>
          <div className="field">
            <label>Variedad / Genética</label>
            <select value={variedad} onChange={e => setVariedad(e.target.value)}>
              {availableVarieties.map(v => <option key={v} value={v}>{v}</option>)}
              {availableVarieties.length === 0 && <option value="">- Configurar variedad primero -</option>}
            </select>
          </div>
          <div className="field">
            <label>Código de Lote</label>
            <input type="text" value={lote} onChange={e => setLote(e.target.value)} placeholder="Ej: L-7712"/>
          </div>
          <div className="field">
            <label>Origen / Productor</label>
            <input type="text" value={origen} onChange={e => setOrigen(e.target.value)} placeholder="Ej: Don Pedro"/>
          </div>
          <div className="field">
            <label>Ubicación Depósito</label>
            <input type="text" value={ubicacion} onChange={e => setUbicacion(e.target.value)} placeholder="Ej: Silo 3 / Galpón A"/>
          </div>
          <div className="field">
            <label>Presentación</label>
            <select value={tipo} onChange={e => setTipo(e.target.value)}>
              <option value="Bolsas">Bolsas</option>
              <option value="Granel">Granel</option>
            </select>
          </div>
          <div className="field">
            <label>Tratamiento Semilla</label>
            <select value={tratamiento} onChange={e => setTratamiento(e.target.value)}>
              <option value="Original">Original (Limpia)</option>
              <option value="Tratado">Tratado (Curada)</option>
            </select>
          </div>
          <div className="field">
            <label>Cantidad de Bolsas</label>
            <input type="number" disabled={tipo==='Granel'} value={bolsas} onChange={e => setBolsas(e.target.value)}/>
          </div>
          <div className="field">
            <label>Kilogramos Totales</label>
            <input type="number" value={kg} onChange={e => setKg(e.target.value)}/>
          </div>
          <div className="field full">
            <label>Observaciones de Calidad Logística</label>
            <textarea rows="2" value={observaciones} onChange={e => setObservaciones(e.target.value)} placeholder="Detalles de pureza, poder germinativo..."></textarea>
          </div>
        </div>
        <div className="modal-btns">
          <button type="button" className="btn-cancel" onClick={onClose}>Cancelar</button>
          <button type="submit" className="btn-save">Guardar Registro</button>
        </div>
      </form>
    </div>
  );
}

// MODAL OPERATIVO: CONTROL DE MOVIMIENTOS Y FLUJOS
function MoveModal({ item, onSave, onCreateOC, onClose }) {
  const [tipoMov, setTipoMov] = useState('Despacho'); // 'Despacho' | 'Ingreso' | 'Egreso'
  const [cantidadBolsas, setCantidadBolsas] = useState(0);
  const [cantidadKg, setCantidadKg] = useState(0);
  const [destino, setDestino] = useState('');
  const [observaciones, setObservaciones] = useState('');

  // Proponer cálculo automático del peso si es en bolsas (aprox 40kg estándar por bolsa de semilla)
  const handleBolsasChange = (val) => {
    setCantidadBolsas(val);
    if (item.tipo === 'Bolsas') {
      setCantidadKg(Number(val) * 40);
    }
  };

  const handleExecute = () => {
    if (Number(cantidadKg) <= 0 && Number(cantidadBolsas) <= 0) {
      alert('Defina una cantidad válida para mover.');
      return;
    }
    if ((tipoMov === 'Despacho' || tipoMov === 'Egreso') && Number(cantidadBolsas) > item.bolsas) {
      if (!confirm('La cantidad solicitada supera las existencias físicas del lote. ¿Desea forzar el egreso de igual modo?')) {
        return;
      }
    }
    onSave({
      itemId: item.id,
      tipoMov,
      cantidadBolsas: Number(cantidadBolsas),
      cantidadKg: Number(cantidadKg),
      destino,
      observaciones
    });
  };

  const handleTriggerOC = () => {
    if (!destino) {
      alert('Escriba el nombre del cliente en el campo "Destino / Cliente / Notas" para generar la orden correctamente.');
      return;
    }
    onCreateOC({
      cliente: destino,
      especie: item.especie,
      variedad: item.variedad,
      bolsas: Number(cantidadBolsas),
      observaciones: `Generada desde Lote: ${item.lote}. ${observaciones}`
    });
  };

  return (
    <div className="overlay">
      <div className="modal modal-md">
        <h2>Transacción Operativa de Stock</h2>
        <div className="move-info">
          <b>Lote Origen:</b> <code style={{color:'var(--accent)'}}>{item.lote}</code> ({item.variedad})<br/>
          <b>Disponible Real:</b> {item.bolsas} Bolsas / {item.kg} Kg Netos<br/>
          <b>Ubicación actual:</b> {item.ubicacion}
        </div>

        <div className="move-row">
          <label>Naturaleza del Tráfico</label>
          <select value={tipoMov} onChange={e => setTipoMov(e.target.value)}>
            <option value="Despacho">Despacho Comercial (Retira Cliente)</option>
            <option value="Egreso">Egreso Interno / Consumo Propio</option>
            <option value="Ingreso">Ingreso Adicional / Ajuste Positivo</option>
          </select>
        </div>

        <div className="form-grid" style={{margin:'0 0 10px 0'}}>
          <div className="move-row">
            <label>Bolsas a Mover</label>
            <input type="number" value={cantidadBolsas} onChange={e => handleBolsasChange(e.target.value)} min="0"/>
          </div>
          <div className="move-row">
            <label>Kilogramos Equivalentes</label>
            <input type="number" value={cantidadKg} onChange={e => setCantidadKg(e.target.value)} min="0"/>
          </div>
        </div>

        <div className="move-row">
          <label>Destino / Cliente / Notas</label>
          <input type="text" value={destino} onChange={e => setDestino(e.target.value)} placeholder="Ej: Agronexo S.A. / Campo San Jorge"/>
        </div>

        <div className="move-row">
          <label>Notas Internas</label>
          <textarea rows="2" value={observaciones} onChange={e => setObservaciones(e.target.value)} placeholder="Datos de transporte, chofer, patente..."></textarea>
        </div>

        {tipoMov === 'Despacho' && (
          <div style={{marginTop:12, padding:8, background:'#f3ebff', borderRadius:8, border:'1px solid var(--purple)'}}>
            <p style={{fontSize:'.75rem', color:'var(--purple)', marginBottom:4}}><b>Vínculo de Logística Comercial</b></p>
            <button type="button" className="btn btn-sm btn-ol oc" onClick={handleTriggerOC}>📋 Pre-registrar Orden de Compra Pendiente</button>
          </div>
        )}

        <div className="modal-btns">
          <button type="button" className="btn-cancel" onClick={onClose}>Cerrar</button>
          <button type="button" className="btn-desp" onClick={handleExecute}>Ejecutar y Notificar</button>
        </div>
      </div>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
</script>
</body>
</html>
