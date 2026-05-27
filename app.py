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
@import url('https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;500;700&display=swap');
:root{--bg:#f4f6f9;--accent:#e07b00;--border:#dde1ea;--text:#1a1e2e;}
body{background:var(--bg);font-family:'Barlow',sans-serif;margin:0;padding:20px}
.app{max-width:1100px;margin:0 auto}
.tabs{display:flex;gap:10px;margin-bottom:20px}
.tab{padding:10px 20px;border-radius:8px;border:none;cursor:pointer;font-weight:700}
.tab.active{background:var(--accent);color:#fff}
table{width:100%;border-collapse:collapse;background:#fff;border-radius:8px;overflow:hidden}
th{background:#f0f3f8;padding:12px;text-align:left;text-transform:uppercase;font-size:0.8rem}
td{padding:12px;border-bottom:1px solid var(--border)}
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const STOCK = JSON.parse(document.getElementById('data-stock').textContent);
const HIST = JSON.parse(document.getElementById('data-historial').textContent);
const OC = JSON.parse(document.getElementById('data-ordenes').textContent);
const { useState } = React;

function App() {
  const [view, setView] = useState("stock");
  return (
    <div className="app">
      <div className="tabs">
        <button className={`tab ${view==="stock"?"active":""}`} onClick={()=>setView("stock")}>Stock</button>
        <button className={`tab ${view==="historial"?"active":""}`} onClick={()=>setView("historial")}>Historial</button>
        <button className={`tab ${view==="ordenes"?"active":""}`} onClick={()=>setView("ordenes")}>Órdenes</button>
      </div>
      
      {view === "stock" && (
        <table>
          <thead><tr><th>ID</th><th>Variedad</th><th>Bolsas</th><th>Depósito</th></tr></thead>
          <tbody>{STOCK.map(s => <tr key={s.ID}><td>{s.ID}</td><td>{s.Variedad}</td><td>{s.Bolsas}</td><td>{s.Depósito}</td></tr>)}</tbody>
        </table>
      )}
      {view === "historial" && (
        <table>
          <thead><tr><th>Fecha</th><th>Tipo</th><th>Detalle</th></tr></thead>
          <tbody>{HIST.map((h,i) => <tr key={i}><td>{h.Fecha}</td><td>{h.Tipo}</td><td>{h.Detalle}</td></tr>)}</tbody>
        </table>
      )}
      {view === "ordenes" && (
        <table>
          <thead><tr><th>OC</th><th>Cliente</th><th>Variedad</th><th>Bolsas</th></tr></thead>
          <tbody>{OC.map(o => <tr key={o.ID_Orden}><td>{o.ID_Orden}</td><td>{o.Cliente}</td><td>{o.Variedad}</td><td>{o.Bolsas}</td></tr>)}</tbody>
        </table>
      )}
    </div>
  );
}
ReactDOM.createRoot(document.getElementById('root')).render(<App />);
</script>
</body>
</html>
