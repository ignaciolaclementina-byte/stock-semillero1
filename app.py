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

<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500&display=swap');
:root{
  --bg:#f4f6f9;--panel:#fff;--border:#dde1ea;--accent:#e07b00;
  --text:#1a1e2e;--muted:#6b7280;--fh:'Barlow Condensed',sans-serif;--fb:'Barlow',sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);font-family:var(--fb);color:var(--text);padding:20px}
.app{max-width:1200px;margin:0 auto}
.hdr{display:flex;justify-content:space-between;margin-bottom:20px}
.tabs{display:flex;gap:10px}
.tab{padding:8px 16px;border-radius:6px;cursor:pointer;background:#ddd;border:none}
.tab.active{background:var(--accent);color:white}
table{width:100%;border-collapse:collapse;background:white;margin-top:10px}
th,td{padding:12px;border:1px solid var(--border);text-align:left}
.btn{padding:8px 16px;background:var(--accent);color:white;border:none;border-radius:4px;cursor:pointer}
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const STOCK = JSON.parse(document.getElementById('data-stock').textContent);
const HISTORIAL = JSON.parse(document.getElementById('data-historial').textContent);
const ORDENES = JSON.parse(document.getElementById('data-ordenes').textContent);
const { useState } = React;

function App() {
  const [tab, setTab] = useState("stock");
  return (
    <div className="app">
      <div className="hdr">
        <h1>Gestión de Stock</h1>
        <div className="tabs">
          <button className={`tab ${tab === "stock" ? "active" : ""}`} onClick={() => setTab("stock")}>Stock</button>
          <button className={`tab ${tab === "historial" ? "active" : ""}`} onClick={() => setTab("historial")}>Historial</button>
          <button className={`tab ${tab === "ordenes" ? "active" : ""}`} onClick={() => setTab("ordenes")}>Órdenes</button>
        </div>
      </div>
      
      {tab === "stock" && (
        <table>
          <thead><tr><th>ID</th><th>Variedad</th><th>Bolsas</th><th>Kg Totales</th></tr></thead>
          <tbody>{STOCK.map(s => <tr key={s.ID}><td>{s.ID}</td><td>{s.Variedad}</td><td>{s.Bolsas}</td><td>{s.Kilos_Totales}</td></tr>)}</tbody>
        </table>
      )}
      {tab === "historial" && (
        <table>
          <thead><tr><th>Fecha</th><th>Tipo</th><th>Detalle</th></tr></thead>
          <tbody>{HISTORIAL.map((h,i) => <tr key={i}><td>{h.Fecha}</td><td>{h.Tipo}</td><td>{h.Detalle}</td></tr>)}</tbody>
        </table>
      )}
      {tab === "ordenes" && (
        <table>
          <thead><tr><th>OC</th><th>Cliente</th><th>Variedad</th><th>Bolsas</th></tr></thead>
          <tbody>{ORDENES.map(o => <tr key={o.ID_Orden}><td>{o.ID_Orden}</td><td>{o.Cliente}</td><td>{o.Variedad}</td><td>{o.Bolsas}</td></tr>)}</tbody>
        </table>
      )}
    </div>
  );
}
ReactDOM.createRoot(document.getElementById('root')).render(<App />);
</script>
</body>
</html>
