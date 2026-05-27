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
.login-btn{width:100%;background:var(--accent);border:none;border-radius:8px;color:#fff;font-family:var(--fh);font-size:1rem;font-weight:800;text-transform:uppercase;letter-spacing:.8px;padding:12px;cursor:pointer;margin-top:8px;transition:background .15s}
.login-btn:hover{background:#c86e00}

/* HEADER */
.hdr{background:linear-gradient(135deg,#1a2a4a 60%,#1e3660);border-bottom:3px solid var(--accent);padding:14px 24px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
.hdr-left{display:flex;align-items:center;gap:14px}
.hdr h1{font-family:var(--fh);font-size:1.6rem;font-weight:800;text-transform:uppercase;letter-spacing:1px;line-height:1;color:#fff}
.hdr h1 span{color:#f5a623}
.hdr-right{display:flex;flex-direction:column;align-items:flex-end;gap:4px}
.creator-tag{font-size:.65rem;color:rgba(255,255,255,.6);text-transform:uppercase;letter-spacing:.5px}
.hdr-tabs{display:flex;gap:5px;flex-wrap:wrap}
.tab{font-family:var(--fh);font-size:.82rem;font-weight:700;letter-spacing:.6px;text-transform:uppercase;padding:6px 13px;border-radius:6px;cursor:pointer;border:1.5px solid rgba(255,255,255,.22);background:transparent;color:rgba(255,255,255,.65);transition:all .18s}
.tab.active{background:#f5a623;border-color:#f5a623;color:#1a1e2e}
.tab:hover:not(.active){border-color:rgba(255,255,255,.7);color:#fff}

/* KPI, TOOLBAR, TABLE, ETC - (Mismos estilos que el original) */
.kpi-strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:1px;background:var(--border);border-bottom:1px solid var(--border)}
.kpi{background:var(--panel);padding:12px 16px}
.kpi-val{font-family:var(--fh);font-size:1.8rem;font-weight:800;line-height:1}
.kpi-lbl{font-size:.65rem;color:var(--muted);text-transform:uppercase;letter-spacing:.7px;margin-top:2px}
.c-or{color:var(--accent)}.c-bl{color:var(--blue)}.c-gr{color:var(--green)}.c-pu{color:var(--purple)}
.toolbar{display:flex;gap:8px;padding:12px 16px;flex-wrap:wrap;align-items:center;border-bottom:1px solid var(--border);background:var(--panel);box-shadow:var(--shadow)}
.btn{font-family:var(--fh);font-size:.85rem;font-weight:700;letter-spacing:.4px;text-transform:uppercase;padding:7px 14px;border-radius:8px;cursor:pointer;border:none;transition:all .15s;display:inline-flex;align-items:center;gap:5px}
.btn-add{background:var(--accent);color:#fff}
.table-wrap{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:.82rem}
th{font-family:var(--fh);font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.6px;color:var(--muted);padding:8px 10px;text-align:left}
tbody tr{border-bottom:1px solid #edf0f5;background:#fff}
td{padding:8px 10px}
.badge{display:inline-flex;align-items:center;gap:3px;padding:2px 8px;border-radius:20px;font-size:.7rem;font-weight:700;font-family:var(--fh);text-transform:uppercase}
</style>
</head>
<body>
<div id="root"></div>

<script type="text/babel">
const {useState} = React;

function App() {
  const [user, setUser] = useState(false);

  if (!user) return (
    <div className="login-wrap">
      <div className="login-box">
        <h1>La Clementina</h1>
        <p>Control de Stock</p>
        <button className="login-btn" onClick={() => setUser(true)}>Ingresar</button>
      </div>
    </div>
  );

  return (
    <div className="app">
      <header className="hdr">
        <div className="hdr-left">
          <h1>La Clementina <span>Stock</span></h1>
        </div>
        <div className="hdr-right">
          <div className="creator-tag">Creado por Ignacio Diaz</div>
        </div>
      </header>
      <div style={{padding: '20px'}}>
        <h2>Panel de Control</h2>
        <p>Sistema cargado correctamente.</p>
        {/* Aquí iría el resto de tu lógica de componentes */}
      </div>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
</script>
</body>
</html>
