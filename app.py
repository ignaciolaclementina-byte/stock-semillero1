<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>La Clementina · Stock Semillas</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.2/babel.min.js"></script>

<script id="data-stock" type="application/json">""" + js_stock + """</script>
<script id="data-historial" type="application/json">""" + js_historial + """</script>
<script id="data-ordenes" type="application/json">""" + js_ordenes + """</script>
<script id="data-catalogos" type="application/json">""" + js_catalogos + """</script>

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
.app{max-width:1300px;margin:0 auto;padding-bottom:20px}

/* Estilos de cabecera y navegación */
.hdr{background:linear-gradient(135deg,#1a2a4a 60%,#1e3660);border-bottom:3px solid var(--accent);padding:14px 24px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap}
.hdr h1{font-family:var(--fh);font-size:1.6rem;font-weight:800;text-transform:uppercase;color:#fff}
.hdr-tabs{display:flex;gap:5px}
.tab{font-family:var(--fh);font-size:.82rem;font-weight:700;text-transform:uppercase;padding:6px 13px;border-radius:6px;cursor:pointer;border:1.5px solid rgba(255,255,255,.22);background:transparent;color:rgba(255,255,255,.65)}
.tab.active{background:#f5a623;border-color:#f5a623;color:#1a1e2e}

/* Tablas y botones */
.table-wrap{overflow-x:auto;background:white}
table{width:100%;border-collapse:collapse;font-size:.82rem}
th{padding:10px;text-align:left;background:#f0f3f8;color:var(--muted);text-transform:uppercase}
td{padding:10px;border-bottom:1px solid #edf0f5}
.btn{cursor:pointer;border:none;border-radius:6px;padding:6px 12px;font-family:var(--fh)}
.btn-add{background:var(--accent);color:white}
.action-btn{background:transparent;border:1px solid var(--border);padding:3px 8px;border-radius:4px;cursor:pointer}
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const DB_STOCK = JSON.parse(document.getElementById('data-stock').textContent);
const DB_ORDENES = JSON.parse(document.getElementById('data-ordenes').textContent);
const { useState } = React;

function App() {
  const [tab, setTab] = useState("stock");
  
  return (
    <div className="app">
      <header className="hdr">
        <h1>La Clementina</h1>
        <div className="hdr-tabs">
          <button className={`tab ${tab === "stock" ? "active" : ""}`} onClick={() => setTab("stock")}>Stock</button>
          <button className={`tab ${tab === "ordenes" ? "active" : ""}`} onClick={() => setTab("ordenes")}>Órdenes</button>
        </div>
      </header>

      {tab === "stock" && (
        <div className="table-wrap">
          <table>
            <thead><tr><th>ID</th><th>Variedad</th><th>Bolsas</th><th>Acciones</th></tr></thead>
            <tbody>
              {DB_STOCK.map(s => (
                <tr key={s.ID}>
                  <td>{s.ID}</td><td>{s.Variedad}</td><td>{s.Bolsas}</td>
                  <td><button className="action-btn">Editar</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {tab === "ordenes" && (
        <div className="table-wrap">
          <table>
            <thead><tr><th>OC #</th><th>Variedad</th><th>Bolsas</th><th>Estado</th></tr></thead>
            <tbody>
              {DB_ORDENES.map(o => (
                <tr key={o.ID_Orden}>
                  <td>{o.ID_Orden}</td><td>{o.Variedad}</td><td>{o.Bolsas}</td><td>{o.Estado}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
ReactDOM.createRoot(document.getElementById('root')).render(<App />);
</script>
</body>
</html>
