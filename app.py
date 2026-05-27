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
.login-box h1{font-family:var(--fh);font-size:1.5rem;font-weight:800;text-transform:uppercase;letter-spacing:1px;color:#1a2a4a;margin-bottom:6px}
.login-box p{font-size:.85rem;color:var(--muted);margin-bottom:24px}
.login-input{width:100%;padding:11px 14px;border:1.5px solid var(--border);border-radius:8px;font-family:var(--fb);font-size:1rem;outline:none;text-align:center;letter-spacing:3px;margin-bottom:8px;background:var(--bg)}
.login-input:focus{border-color:var(--accent)}
.login-input.err{border-color:var(--red);background:#fff5f5}
.err-msg{color:var(--red);font-size:.8rem;margin-bottom:12px}
.login-btn{width:100%;background:var(--accent);border:none;border-radius:8px;color:#fff;font-family:var(--fh);font-size:1rem;font-weight:800;text-transform:uppercase;padding:12px;cursor:pointer;margin-top:8px}

/* HEADER */
.hdr{background:linear-gradient(135deg,#1a2a4a 60%,#1e3660);border-bottom:3px solid var(--accent);padding:14px 24px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
.hdr h1{font-family:var(--fh);font-size:1.6rem;font-weight:800;text-transform:uppercase;letter-spacing:1px;color:#fff}
.hdr h1 span{color:#f5a623}
.hdr p{font-size:.7rem;color:rgba(255,255,255,.55);margin-top:2px}
.hdr-right{display:flex;flex-direction:column;align-items:flex-end;gap:8px}
.save-ind{font-size:.65rem;color:rgba(255,255,255,.45);height:14px}
.save-ok{color:#6ee7a0}.save-ing{color:#fbbf24}
.hdr-tabs{display:flex;gap:5px;flex-wrap:wrap}
.tab{font-family:var(--fh);font-size:.82rem;font-weight:700;text-transform:uppercase;padding:6px 13px;border-radius:6px;cursor:pointer;border:1.5px solid rgba(255,255,255,.22);background:transparent;color:rgba(255,255,255,.65)}
.tab.active{background:#f5a623;border-color:#f5a623;color:#1a1e2e}
.tab:hover:not(.active){border-color:rgba(255,255,255,.7);color:#fff}

/* KPIs */
.kpi-strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:1px;background:var(--border);border-bottom:1px solid var(--border)}
.kpi{background:var(--panel);padding:12px 16px}
.kpi-val{font-family:var(--fh);font-size:1.8rem;font-weight:800;line-height:1}
.kpi-lbl{font-size:.65rem;color:var(--muted);text-transform:uppercase;margin-top:2px}
.c-or{color:var(--accent)}.c-bl{color:var(--blue)}.c-gr{color:var(--green)}.c-pu{color:var(--purple)}

/* TOOLBAR Y TABLAS */
.toolbar{display:flex;gap:8px;padding:12px 16px;flex-wrap:wrap;align-items:center;border-bottom:1px solid var(--border);background:var(--panel);box-shadow:var(--shadow)}
.search-wrap{position:relative;flex:1;min-width:160px}
.search-icon{position:absolute;left:9px;top:50%;transform:translateY(-50%);color:var(--muted);font-size:.85rem}
.search-inp{width:100%;padding:7px 10px 7px 28px;background:var(--bg);border:1.5px solid var(--border);border-radius:8px;color:var(--text);font-family:var(--fb);font-size:.83rem;outline:none}
.search-inp:focus{border-color:var(--accent)}
.sel{background:var(--bg);border:1.5px solid var(--border);border-radius:8px;color:var(--text);font-family:var(--fb);font-size:.81rem;padding:7px 9px;outline:none;cursor:pointer}
.btn{font-family:var(--fh);font-size:.85rem;font-weight:700;text-transform:uppercase;padding:7px 14px;border-radius:8px;cursor:pointer;border:none;display:inline-flex;align-items:center;gap:5px;white-space:nowrap}
.btn-add{background:var(--accent);color:#fff}.btn-add:hover{background:#c86e00}
.btn-ol{background:var(--panel);border:1.5px solid var(--border)!important;color:var(--text)}
.btn-ol:hover{border-color:var(--blue)!important;color:var(--blue)}
.btn-ol.gnh:hover{border-color:var(--green)!important;color:var(--green)}
.btn-ol.rh:hover{border-color:var(--red)!important;color:var(--red)}
.btn-ol.oc:hover{border-color:var(--purple)!important;color:var(--purple)}
.btn-sm{padding:4px 9px;font-size:.75rem}

.table-wrap{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:.82rem}
thead tr{background:#f0f3f8;border-bottom:2px solid var(--border)}
th{font-family:var(--fh);font-size:.7rem;font-weight:700;text-transform:uppercase;color:var(--muted);padding:8px 10px;text-align:left}
tbody tr{border-bottom:1px solid #edf0f5;background:#fff}
tbody tr:hover{background:#f7f9fc}
tbody tr.low-row{background:#fff5f5}
td{padding:8px 10px;vertical-align:middle}

/* BADGES */
.badge{display:inline-flex;align-items:center;gap:3px;padding:2px 8px;border-radius:20px;font-size:.7rem;font-weight:700;font-family:var(--fh);text-transform:uppercase}
.bb{background:#fff4e0;color:#b86000;border:1px solid #f5c57a}
.bo{background:#e6f4fb;color:#1a7abf;border:1px solid #90cae8}
.tr-b{background:#e6f5ec;color:#2e8b57;border:1px solid #7dc99a}
.st-b{background:#f3f4f6;color:#6b7280;border:1px solid #d1d5db}
.egr{background:#fde8e8;color:#c0392b;border:1px solid #f5a5a5}
.ing{background:#e6f5ec;color:#2e8b57;border:1px solid #7dc99a}
.pend{background:#fef9ee;color:#92600a;border:1px solid #f5c57a}
.desp{background:#e6f5ec;color:#2e8b57;border:1px solid #7dc99a}

.cell-muted{color:var(--muted);font-size:.8rem}
.qty-big{font-family:var(--fh);font-size:1.1rem;font-weight:800}
.action-btn{background:transparent;border:1.5px solid var(--border);border-radius:6px;color:var(--muted);font-size:.75rem;padding:3px 8px;cursor:pointer;margin-right:3px}
.action-btn:hover{border-color:var(--blue);color:var(--blue)}
.action-btn.del:hover{border-color:var(--red);color:var(--red)}

/* VISTA TARJETAS (RESUMEN) */
.stock-view,.hist-view,.oc-view,.admin{padding:16px}
.sv-filters{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;align-items:center}
.camp-block{margin-bottom:26px}
.camp-title{font-family:var(--fh);font-size:1.25rem;font-weight:800;text-transform:uppercase;color:#1a2a4a;border-bottom:2px solid var(--accent);padding-bottom:5px;margin-bottom:12px;display:flex;justify-content:space-between;align-items:center}
.camp-sub{font-size:.82rem;font-weight:600;color:var(--muted)}
.esp-block{margin-bottom:18px}
.esp-title{font-family:var(--fh);font-size:.95rem;font-weight:700;text-transform:uppercase;color:var(--blue);margin-bottom:8px;border-left:3px solid var(--blue);padding-left:9px}
.sv-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:9px}
.sv-card{background:#fff;border:1px solid var(--border);border-radius:10px;padding:12px 14px;border-top:3px solid var(--accent);box-shadow:var(--shadow)}
.sv-head{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:9px;gap:8px}
.sv-variedad{font-family:var(--fh);font-size:.95rem;font-weight:700;text-transform:uppercase;color:#1a2a4a}
.sv-row{display:flex;justify-content:space-between;align-items:center;padding:4px 0;border-bottom:1px solid #edf0f5}
.sv-row:last-child{border-bottom:none}
.sv-label{font-size:.68rem;color:var(--muted);text-transform:uppercase}
.sv-val{font-family:var(--fh);font-size:1rem;font-weight:700}
.no-data{color:var(--muted);font-size:.88rem;padding:40px 0;text-align:center}
.dpos{font-family:var(--fh);font-size:1rem;font-weight:800;color:var(--green)}
.dneg{font-family:var(--fh);font-size:1rem;font-weight:800;color:var(--red)}

/* CONFIGURACIÓN */
.admin-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}
.admin-card{background:#fff;border:1px solid var(--border);border-radius:10px;padding:14px;box-shadow:var(--shadow)}
.admin-card h3{font-family:var(--fh);font-size:.85rem;font-weight:700;text-transform:uppercase;color:var(--muted);margin-bottom:9px}
.tag-list{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:10px;min-height:26px}
.tag{background:var(--bg);border:1.5px solid var(--border);border-radius:20px;padding:3px 10px;font-size:.76rem;display:flex;align-items:center;gap:5px}
.tag-del{background:none;border:none;color:var(--muted);cursor:pointer;font-size:.85rem}
.tag-del:hover{color:var(--red)}
.add-inline{display:flex;gap:5px}
.add-inline input{flex:1;background:var(--bg);border:1.5px solid var(--border);border-radius:8px;padding:6px 9px;outline:none;font-size:.83rem}
.add-inline button{background:var(--accent);border:none;border-radius:8px;color:#fff;font-family:var(--fh);font-weight:700;padding:6px 12px;cursor:pointer}
.pass-row{display:flex;gap:6px;margin-top:8px}
.pass-row input{flex:1;background:var(--bg);border:1.5px solid var(--border);border-radius:8px;padding:6px 9px;outline:none}

/* MODALES */
.overlay{position:fixed;inset:0;z-index:100;background:rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;padding:14px}
.modal{background:#fff;border:1px solid var(--border);border-radius:14px;padding:22px;width:100%;max-width:520px;max-height:90vh;overflow-y:auto;box-shadow:0 8px 32px rgba(0,0,0,.15)}
.modal-md{max-width:440px}
.modal h2{font-family:var(--fh);font-size:1.2rem;font-weight:800;text-transform:uppercase;color:#1a2a4a;margin-bottom:16px}
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.form-grid .full{grid-column:1/-1}
.field label,.move-row label{display:block;font-size:.66rem;color:var(--muted);text-transform:uppercase;margin-bottom:3px;letter-spacing:.5px}
.field input,.field select,.field textarea,.move-row input,.move-row select,.move-row textarea{width:100%;background:var(--bg);border:1.5px solid var(--border);border-radius:8px;color:var(--text);font-family:var(--fb);font-size:.86rem;padding:7px 10px;outline:none}
.field input:focus,.field select:focus,.move-row input:focus{border-color:var(--accent)}
.modal-btns{display:flex;justify-content:flex-end;gap:9px;margin-top:18px}
.btn-cancel{background:transparent;border:1.5px solid var(--border);border-radius:8px;color:var(--muted);font-family:var(--fh);font-weight:700;padding:8px 18px;cursor:pointer}
.btn-cancel:hover{border-color:var(--red);color:var(--red)}
.btn-save{background:var(--accent);border:none;border-radius:8px;color:#fff;font-family:var(--fh);font-weight:800;padding:8px 22px;cursor:pointer}
.btn-desp{background:var(--green);border:none;border-radius:8px;color:#fff;font-family:var(--fh);font-weight:800;padding:8px 22px;cursor:pointer}
.move-info{background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:10px 13px;margin-bottom:14px;font-size:.83rem;line-height:1.7}
.move-row{margin-bottom:10px}

@media print{
  .no-print{display:none!important}
  .app{max-width:100%!important;padding:0!important}
  .sv-card{box-shadow:none!important;break-inside:avoid}
}
</style>
</head>
<body>
<div id="root"></div>

<script type="text/babel">
const {useState, useMemo, useEffect} = React;

const LOW = 5;
const fmt = n => Number(n).toLocaleString("es-AR");
const today = () => new Date().toISOString().slice(0,10);
const nowStr = () => new Date().toLocaleString("es-AR",{day:"2-digit",month:"2-digit",year:"numeric",hour:"2-digit",minute:"2-digit"});

const defaultCampanas = ['24/25', '25/26'];
const defaultEspecies = ['Soja', 'Maíz', 'Trigo', 'Girasol'];
const defaultVarMap = {
  'Soja': ['DM 46E21', 'AW 4721', 'DM 40i25 Enlist'],
  'Maíz': ['DK 72-10 VT3P', 'DK 72-27'],
  'Trigo': ['Baguette 620', 'Algarrobo'],
  'Girasol': ['Syn 3970 CL']
};
const defaultStock = [
  { id: 1, campaña: '25/26', especie: 'Soja', variedad: 'DM 46E21', lote: 'L-201', origen: 'Propio', ubicacion: 'Galpón Norte', bolsas: 120, kg: 4800, tipo: 'Bolsas', tratamiento: 'Tratado', observaciones: 'Calidad excelente.' },
  { id: 2, campaña: '25/26', especie: 'Maíz', variedad: 'DK 72-10 VT3P', lote: 'L-409', origen: 'Don Pedro', ubicacion: 'Silo 2', bolsas: 3, kg: 2100, tipo: 'Granel', tratamiento: 'Original', observaciones: '' }
];
const defaultHistorial = [
  { id: 1, fecha: nowStr(), tipo: 'Ingreso', detalle: 'Carga inicial del sistema', campaña: '25/26', especie: 'Soja', variedad: 'DM 46E21', bolsas: 120, kg: 4800 }
];
const defaultOC = [
  { id: 1, numero: 'OC-5001', fecha: today(), cliente: 'Agroganadera San Jorge', especie: 'Soja', variedad: 'DM 46E21', bolsas: 30, estado: 'Pendiente', observaciones: 'Retira flete cliente.' }
];

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(() => localStorage.getItem('lc_auth') === 'true');
  const [password, setPassword] = useState('');
  const [savedPassword, setSavedPassword] = useState(() => localStorage.getItem('lc_pass') || '1234');
  const [loginError, setLoginError] = useState(false);

  const [tab, setTab] = useState('resumen');
  const [campañas, setCampañas] = useState(() => JSON.parse(localStorage.getItem('lc_campañas')) || defaultCampanas);
  const [especies, setEspecies] = useState(() => JSON.parse(localStorage.getItem('lc_especies')) || defaultEspecies);
  const [varMap, setVarMap] = useState(() => JSON.parse(localStorage.getItem('lc_varmap')) || defaultVarMap);
  const [stock, setStock] = useState(() => JSON.parse(localStorage.getItem('lc_stock')) || defaultStock);
  const [historial, setHistorial] = useState(() => JSON.parse(localStorage.getItem('lc_historial')) || defaultHistorial);
  const [ocList, setOcList] = useState(() => JSON.parse(localStorage.getItem('lc_oc')) || defaultOC);

  const [saveStatus, setSaveStatus] = useState('saved');
  const [search, setSearch] = useState('');
  const [fCampaña, setFCampaña] = useState('TODAS');
  const [fEspecie, setFEspecie] = useState('TODAS');
  const [fEstado, setFEstado] = useState('TODOS');
  const [modal, setModal] = useState(null);

  // Autoguardado reactivo
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
    }, 1500);
    return () => clearTimeout(timer);
  }, [campañas, especies, varMap, stock, historial, ocList, isAuthenticated]);

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
      alert('Clave actualizada.');
      document.getElementById('new_pass_input').value = '';
    }
  };

  const resetAll = () => {
    if (confirm('¿Resetear base de datos por completo?')) {
      localStorage.clear();
      window.location.reload();
    }
  };

  // Métricas KPIs
  const kpis = useMemo(() => {
    let totKg = 0, totBolsas = 0, alertasBajo = 0;
    stock.forEach(i => {
      totKg += Number(i.kg || 0);
      if (i.tipo === 'Bolsas') {
        totBolsas += Number(i.bolsas || 0);
        if (Number(i.bolsas || 0) <= LOW) alertasBajo++;
      } else {
        if (Number(i.kg || 0) <= LOW * 50) alertasBajo++;
      }
    });
    return { totKg, totBolsas, pendOC: ocList.filter(o => o.estado === 'Pendiente').length, alertasBajo };
  }, [stock, ocList]);

  const filteredStock = useMemo(() => {
    return stock.filter(i => {
      const matchSearch = !search || i.variedad.toLowerCase().includes(search.toLowerCase()) || i.lote.toLowerCase().includes(search.toLowerCase());
      const matchCamp = fCampaña === 'TODAS' || i.campaña === fCampaña;
      const matchEsp = fEspecie === 'TODAS' || i.especie === fEspecie;
      let matchEst = true;
      if (fEstado === 'ALERTA') matchEst = i.tipo === 'Bolsas' ? (i.bolsas <= LOW) : (i.kg <= LOW * 50);
      return matchSearch && matchCamp && matchEsp && matchEst;
    });
  }, [stock, search, fCampaña, fEspecie, fEstado]);

  // Handlers unificados de interacción ABM (Nombres exactos)
  const handleSave = (itemData) => {
    if (itemData.id) {
      setStock(prev => prev.map(x => x.id === itemData.id ? itemData : x));
    } else {
      const newItem = { ...itemData, id: Date.now() };
      setStock(prev => [newItem, ...prev]);
      setHistorial(h => [{ id: Date.now(), fecha: nowStr(), tipo: 'Ingreso', detalle: `Alta de lote ${newItem.lote}`, campaña: newItem.campaña, especie: newItem.especie, variedad: newItem.variedad, bolsas: newItem.bolsas, kg: newItem.kg }, ...h]);
    }
    setModal(null);
  };

  const handleMove = (movement) => {
    const { itemId, tipoMov, cantidadBolsas, cantidadKg, destino, observaciones } = movement;
    setStock(prev => prev.map(item => {
      if (item.id === itemId) {
        let nBolsas = Number(item.bolsas);
        let nKg = Number(item.kg);
        if (tipoMov === 'Egreso' || tipoMov === 'Despacho') {
          nBolsas = Math.max(0, nBolsas - Number(cantidadBolsas));
          nKg = Math.max(0, nKg - Number(cantidadKg));
        } else {
          nBolsas += Number(cantidadBolsas);
          nKg += Number(cantidadKg);
        }
        return { ...item, bolsas: nBolsas, kg: nKg };
      }
      return item;
    }));

    const ref = stock.find(x => x.id === itemId);
    setHistorial(h => [{ id: Date.now(), fecha: nowStr(), tipo: tipoMov, detalle: `${tipoMov} - Destino: ${destino || '-'}`, campaña: ref.campaña, especie: ref.especie, variedad: ref.variedad, bolsas: cantidadBolsas, kg: cantidadKg }, ...h]);
    
    // Integración de Alerta Profesional WhatsApp
    if (confirm('¿Enviar reporte de movimiento vía WhatsApp?')) {
      const msg = `*La Clementina · Logística Semillas*\n\nMovimiento: *${tipoMov}*\n• Insumo: ${ref.especie} (${ref.variedad})\n• Lote: ${ref.lote}\n• Cantidad: ${cantidadBolsas} Bolsas / ${cantidadKg} Kg\n• Destino: ${destino || '-'}\n• Info: ${observaciones || '-'}`;
      window.open(`https://api.whatsapp.com/send?text=${encodeURIComponent(msg)}`, '_blank');
    }
    setModal(null);
  };

  const handleCreateOC = (ocData) => {
    const newOC = { id: Date.now(), numero: `OC-${Math.floor(1000 + Math.random() * 9000)}`, fecha: today(), estado: 'Pendiente', ...ocData };
    setOcList(prev => [newOC, ...prev]);
  };

  const handleEditOC = (updatedOc) => {
    setOcList(prev => prev.map(o => o.id === updatedOc.id ? updatedOc : o));
    setModal(null);
  };

  const handleDeleteItem = (id) => {
    if (confirm('¿Eliminar este lote físico del inventario?')) {
      setStock(prev => prev.filter(x => x.id !== id));
    }
  };

  const handleAddTag = (category, value) => {
    if (!value.trim()) return;
    if (category === 'campaña' && !campañas.includes(value)) setCampañas([...campañas, value]);
    if (category === 'especie' && !especies.includes(value)) {
      setEspecies([...especies, value]);
      setVarMap({ ...varMap, [value]: [] });
    }
  };

  const handleRemoveTag = (category, value) => {
    if (category === 'campaña') setCampañas(campañas.filter(x => x !== value));
    if (category === 'especie') setEspecies(especies.filter(x => x !== value));
  };

  if (!isAuthenticated) {
    return (
      <div className="login-wrap">
        <form className="login-box" onSubmit={handleLogin}>
          <h1>La Clementina</h1>
          <p>Control de Existencias Semillas</p>
          <input type="password" className={`login-input ${loginError ? 'err' : ''}`} placeholder="Clave de acceso..." value={password} onChange={e => setPassword(e.target.value)}/>
          <button type="submit" className="login-btn">Ingresar</button>
        </form>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="hdr">
        <div>
          <h1>La Clementina · <span>Stock Semillas</span></h1>
          <p>Logística y Administración Interna</p>
        </div>
        <div className="hdr-right">
          <div className="save-ind">
            {saveStatus === 'saving' ? <span className="save-ing">⏳ Sincronizando...</span> : <span className="save-ok">✓ Base Sincronizada</span>}
          </div>
          <div className="hdr-tabs no-print">
            <button className={`tab ${tab === 'resumen' ? 'active' : ''}`} onClick={() => setTab('resumen')}>Resumen</button>
            <button className={`tab ${tab === 'stock' ? 'active' : ''}`} onClick={() => setTab('stock')}>Inventario</button>
            <button className={`tab ${tab === 'historial' ? 'active' : ''}`} onClick={() => setTab('historial')}>Tráfico</button>
            <button className={`tab ${tab === 'oc' ? 'active' : ''}`} onClick={() => setTab('oc')}>Órdenes (OC)</button>
            <button className={`tab ${tab === 'admin' ? 'active' : ''}`} onClick={() => setTab('admin')}>Config</button>
            <button className="tab" style={{color:'#ff9494'}} onClick={handleLogout}>Salir</button>
          </div>
        </div>
      </header>

      <section className="kpi-strip">
        <div className="kpi"><div className="kpi-val c-or">{fmt(kpis.totBolsas)}</div><div className="kpi-lbl">Bolsas</div></div>
        <div className="kpi"><div className="kpi-val c-bl">{fmt(kpis.totKg)}</div><div className="kpi-lbl">Kg Totales</div></div>
        <div className="kpi"><div className="kpi-val c-pu">{kpis.pendOC}</div><div className="kpi-lbl">OC Abiertas</div></div>
        <div className="kpi" style={{background: kpis.alertasBajo > 0 ? '#fff5f5' : ''}}><div className="kpi-val c-red">{kpis.alertasBajo}</div><div className="kpi-lbl">Lotes en Crítico</div></div>
      </section>

      {/* VISTA RESUMEN (CARDS) */}
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
          </div>
          {campañas.filter(c => fCampaña === 'TODAS' || c === fCampaña).map(camp => {
            const sc = stock.filter(s => s.campaña === camp && (fEspecie === 'TODAS' || s.especie === fEspecie));
            if (!sc.length) return null;
            return (
              <div key={camp} className="camp-block">
                <div className="camp-title"><span>Campaña {camp}</span></div>
                <div className="sv-grid">
                  {sc.map(item => (
                    <div key={item.id} className="sv-card">
                      <div className="sv-head">
                        <span className="sv-variedad">{item.variedad}</span>
                        <span className="badge bb">{item.tipo}</span>
                      </div>
                      <div className="sv-row"><span className="sv-label">Lote:</span><span className="sv-val">{item.lote}</span></div>
                      <div className="sv-row"><span className="sv-label">Ubicación:</span><span className="sv-val cell-muted">{item.ubicacion}</span></div>
                      <div className="sv-row"><span className="sv-label">Disponible:</span><span className="sv-val" style={{color:'var(--green)'}}>{item.tipo === 'Bolsas' ? `${fmt(item.bolsas)} b.` : `${fmt(item.kg)} kg`}</span></div>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* VISTA INVENTARIO (TABLA FÍSICA) */}
      {tab === 'stock' && (
        <div className="hist-view">
          <div className="toolbar no-print">
            <div className="search-wrap"><span className="search-icon">🔍</span><input type="text" className="search-inp" placeholder="Buscar..." value={search} onChange={e => setSearch(e.target.value)}/></div>
            <button className="btn btn-add" onClick={() => setModal({mode: 'new'})}>＋ Registrar Lote</button>
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Campaña</th><th>Especie</th><th>Variedad</th><th>Lote</th><th>Ubicación</th><th>Bolsas</th><th>Kg Netos</th><th style={{textAlign:'center'}}>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {filteredStock.map(item => (
                  <tr key={item.id}>
                    <td>{item.campaña}</td><td>{item.especie}</td><td><b>{item.variedad}</b></td><td><code>{item.lote}</code></td><td>{item.ubicacion}</td><td>{fmt(item.bolsas)}</td><td className="qty-big">{fmt(item.kg)}</td>
                    <td style={{textAlign:'center'}}>
                      <button className="action-btn" onClick={() => setModal({mode: 'move', item})}>📦 Mover</button>
                      <button className="action-btn" onClick={() => setModal({mode: 'edit', item})}>✏</button>
                      <button className="action-btn del" onClick={() => handleDeleteItem(item.id)}>🗑</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* VISTA HISTORIAL */}
      {tab === 'historial' && (
        <div className="hist-view">
          <table Kakao="true">
            <thead>
              <tr><th>Fecha</th><th>Tipo</th><th>Especie</th><th>Variedad</th><th>Detalle</th><th style={{textAlign:'right'}}>Bolsas</th>
            </tr>
            </thead>
            <tbody>
              {historial.map(h => (
                <tr key={h.id}>
                  <td>{h.fecha}</td><td><span className={`badge ${h.tipo === 'Ingreso' ? 'ing' : 'egr'}`}>{h.tipo}</span></td><td>{h.especie}</td><td>{h.variedad}</td><td>{h.detalle}</td><td style={{textAlign:'right'}} className={h.tipo === 'Ingreso' ? 'dpos' : 'dneg'}>{h.bolsas}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* VISTA ÓRDENES DE COMPRA (OC) */}
      {tab === 'oc' && (
        <div className="oc-view">
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Código</th><th>Cliente</th><th>Insumo</th><th>Bolsas</th><th>Estado</th><th>Observaciones</th><th style={{textAlign:'center'}}>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {ocList.map(o => (
                  <tr key={o.id}>
                    <td><b style={{color:'var(--purple)'}}>{o.numero}</b></td><td>{o.cliente}</td><td>{o.especie} · {o.variedad}</td><td>{o.bolsas}</td><td><span className={`badge ${o.estado==='Pendiente'?'pend':'desp'}`}>{o.estado}</span></td><td>{o.observaciones || '-'}</td>
                    <td style={{textAlign:'center'}}>
                      <button className="action-btn" onClick={() => setModal({mode: 'editOC', oc: o})}>✏ Editar OC</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* VISTA CONFIG */}
      {tab === 'admin' && (
        <div className="admin">
          <div className="admin-grid">
            <div className="admin-card">
              <h3>Campañas</h3>
              <div className="tag-list">{campañas.map(c => <span key={c} className="tag">{c} <button className="tag-del" onClick={() => handleRemoveTag('campaña', c)}>×</button></span>)}</div>
              <div className="add-inline"><input type="text" id="new_c"/><button onClick={() => handleAddTag('campaña', document.getElementById('new_c').value)}>＋</button></div>
            </div>
            <div className="admin-card">
              <h3>Seguridad</h3>
              <div className="pass-row"><input type="password" id="new_pass_input" placeholder="Nueva clave..."/><button className="btn btn-sm btn-ol gnh" onClick={handleChangePass}>Guardar</button></div>
            </div>
            <div className="admin-card" style={{borderColor:'#f5a5a5'}}>
              <h3>Zona Crítica</h3>
              <button className="btn btn-ol rh" onClick={resetAll}>Resetear Todo</button>
            </div>
          </div>
        </div>
      )}

      {/* FOOTER REQUERIDO */}
      <footer style={{textAlign:"center", padding:20, fontSize:".75rem", color:"var(--muted)", borderTop:"1px solid var(--border)", marginTop:40}}>
        La Clementina · Control Operativo Digital<br/>
        <strong>Creado por Ignacio Diaz</strong>
      </footer>

      {/* RENDER DE MODALES COMPLETOS */}
      {modal?.mode === 'new' && <ModalForm campañas={campañas} especies={especies} varMap={varMap} onSave={handleSave} onClose={() => setModal(null)}/>}
      {modal?.mode === 'edit' && <ModalForm item={modal.item} campañas={campañas} especies={especies} varMap={varMap} onSave={handleSave} onClose={() => setModal(null)}/>}
      {modal?.mode === 'move' && <MoveModal item={modal.item} onSave={handleMove} onCreateOC={handleCreateOC} onClose={() => setModal(null)}/>}
      {modal?.mode === 'editOC' && <OCModal editOC={modal.oc} onSave={handleEditOC} onClose={() => setModal(null)}/>}
    </div>
  );
}

/* COMPONENTE: MODAL ALTA/EDICIÓN */
function ModalForm({ item, campañas, especies, varMap, onSave, onClose }) {
  const [campaña, setCampaña] = useState(item ? item.campaña : campañas[0] || '');
  const [especie, setEspecie] = useState(item ? item.especie : especies[0] || '');
  const [variedad, setVariedad] = useState(item ? item.variedad : '');
  const [lote, setLote] = useState(item ? item.lote : '');
  const [ubicacion, setUbicacion] = useState(item ? item.ubicacion : '');
  const [bolsas, setBolsas] = useState(item ? item.bolsas : 0);
  const [kg, setKg] = useState(item ? item.kg : 0);

  const available = varMap[especie] || [];
  useEffect(() => { if (!item && available.length > 0) setVariedad(available[0]); }, [especie]);

  const sub = (e) => {
    e.preventDefault();
    onSave({ id: item?.id, campaña, especie, variedad, lote, ubicacion, bolsas: Number(bolsas), kg: Number(kg), tipo: 'Bolsas', tratamiento: 'Original', origen: 'Propio', observaciones: '' });
  };

  return (
    <div className="overlay">
      <form className="modal" onSubmit={sub}>
        <h2>{item ? 'Modificar Registro' : 'Alta de Insumo Físico'}</h2>
        <div className="form-grid">
          <div className="field"><label>Campaña</label><select value={campaña} onChange={e => setCampaña(e.target.value)}>{campañas.map(c => <option key={c} value={c}>{c}</option>)}</select></div>
          <div className="field"><label>Especie</label><select value={especie} onChange={e => setEspecie(e.target.value)}>{especies.map(e => <option key={e} value={e}>{e}</option>)}</select></div>
          <div className="field"><label>Variedad</label><select value={variedad} onChange={e => setVariedad(e.target.value)}>{available.map(v => <option key={v} value={v}>{v}</option>)}</select></div>
          <div className="field"><label>Lote</label><input type="text" value={lote} onChange={e => setLote(e.target.value)} required/></div>
          <div className="field"><label>Ubicación</label><input type="text" value={ubicacion} onChange={e => setUbicacion(e.target.value)}/></div>
          <div className="field"><label>Bolsas</label><input type="number" value={bolsas} onChange={e => setBolsas(e.target.value)}/></div>
          <div className="field"><label>Kg</label><input type="number" value={kg} onChange={e => setKg(e.target.value)}/></div>
        </div>
        <div className="modal-btns"><button type="button" className="btn-cancel" onClick={onClose}>Cerrar</button><button type="submit" className="btn-save">Guardar</button></div>
      </form>
    </div>
  );
}

/* COMPONENTE: MODAL MOVIMIENTOS */
function MoveModal({ item, onSave, onCreateOC, onClose }) {
  const [tipoMov, setTipoMov] = useState('Despacho');
  const [cantidadBolsas, setCantidadBolsas] = useState(0);
  const [cantidadKg, setCantidadKg] = useState(0);
  const [destino, setDestino] = useState('');

  const handleBChange = (v) => { setCantidadBolsas(v); setCantidadKg(Number(v) * 40); };

  return (
    <div className="overlay">
      <div className="modal modal-md">
        <h2>Transacción Operativa</h2>
        <div className="move-info"><b>Lote:</b> {item.lote} ({item.variedad})<br/><b>Disponible:</b> {item.bolsas} b.</div>
        <div className="move-row">
          <label>Naturaleza Tráfico</label>
          <select value={tipoMov} onChange={e => setTipoMov(e.target.value)}><option value="Despacho">Despacho Comercial</option><option value="Egreso">Egreso Interno</option><option value="Ingreso">Ingreso Adicional</option></select>
        </div>
        <div className="form-grid">
          <div className="move-row"><label>Bolsas</label><input type="number" value={cantidadBolsas} onChange={e => handleBChange(e.target.value)}/></div>
          <div className="move-row"><label>Kg</label><input type="number" value={cantidadKg} onChange={e => setCantidadKg(e.target.value)}/></div>
        </div>
        <div className="move-row"><label>Destino / Cliente</label><input type="text" value={destino} onChange={e => setDestino(e.target.value)} placeholder="Ej: San Jorge..."/></div>
        {tipoMov === 'Despacho' && (
          <div style={{margin:'10px 0', padding:8, background:'#f3ebff', borderRadius:6, border:'1px solid var(--purple)'}}>
            <button type="button" className="btn btn-sm btn-ol oc" onClick={() => { if(!destino) return alert('Ponga un cliente'); onCreateOC({ cliente: destino, especie: item.especie, variedad: item.variedad, bolsas: Number(cantidadBolsas), observaciones: `Desde Lote ${item.lote}` }); alert('Reserva de OC vinculada de forma pendiente.'); }}>📋 Pre-registrar Orden de Compra</button>
          </div>
        )}
        <div className="modal-btns"><button type="button" className="btn-cancel" onClick={onClose}>Cerrar</button><button type="button" className="btn-desp" onClick={() => onSave({ itemId: item.id, tipoMov, cantidadBolsas, cantidadKg, destino })}>Ejecutar</button></div>
      </div>
    </div>
  );
}

/* COMPONENTE INTERCONECTADO REPARADO: MODAL ORDEN DE COMPRA (OCModal) */
function OCModal({ editOC, onSave, onClose }) {
  const [cliente, setCliente] = useState(editOC ? editOC.cliente : '');
  const [bolsas, setBolsas] = useState(editOC ? editOC.bolsas : 0);
  const [estado, setEstado] = useState(editOC ? editOC.estado : 'Pendiente');
  const [observaciones, setObservaciones] = useState(editOC ? editOC.observaciones : '');

  const sub = (e) => {
    e.preventDefault();
    onSave({ ...editOC, cliente, bolsas: Number(bolsas), estado, observaciones });
  };

  return (
    <div className="overlay">
      <form className="modal modal-md" onSubmit={sub}>
        <h2>Modificar Orden de Compra ({editOC?.numero})</h2>
        <div className="move-row">
          <label>Cliente / Productor</label>
          <input type="text" value={cliente} onChange={e => setCliente(e.target.value)} required/>
        </div>
        <div className="form-grid">
          <div className="move-row">
            <label>Bolsas Reservadas</label>
            <input type="number" value={bolsas} onChange={e => setBolsas(e.target.value)} required/>
          </div>
          <div className="move-row">
            <label>Estado de Entrega</label>
            <select value={estado} onChange={e => setEstado(e.target.value)}>
              <option value="Pendiente">Pendiente (Reservado)</option>
              <option value="Despachado">Despachado (Entregado)</option>
            </select>
          </div>
        </div>
        <div className="move-row">
          <label>Notas de Flete / Despacho</label>
          <textarea rows="2" value={observaciones} onChange={e => setObservaciones(e.target.value)}/>
        </div>
        <div className="modal-btns">
          <button type="button" className="btn-cancel" onClick={onClose}>Cancelar</button>
          <button type="submit" className="btn-save">Guardar Cambios</button>
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
