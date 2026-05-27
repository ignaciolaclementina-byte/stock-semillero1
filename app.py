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
:root {
  --bg: #f4f6f9; --panel: #fff; --card: #fff; --border: #dde1ea;
  --accent: #e07b00; --blue: #1a7abf; --green: #2e8b57; --red: #c0392b;
  --purple: #7b4fa6; --text: #1a1e2e; --muted: #6b7280; --shadow: 0 1px 4px rgba(0,0,0,.08);
  --fh: 'Barlow Condensed', sans-serif;
  --fb: 'Barlow', sans-serif;
}
body {
  background-color: var(--bg);
  color: var(--text);
  font-family: var(--fb);
  margin: 0;
  padding: 0;
}
.app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
h1, h2, h3, .brand { font-family: var(--fh); }
.header {
  background: var(--panel);
  padding: 20px;
  border-radius: 8px;
  box-shadow: var(--shadow);
  margin-bottom: 20px;
  border-bottom: 4px solid var(--accent);
}
.header h1 { margin: 0; font-size: 2rem; text-transform: uppercase; }
.header h1 span { color: var(--accent); }

/* Tabs */
.tabs { display: flex; gap: 10px; margin-bottom: 20px; }
.tab {
  padding: 10px 20px;
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 6px;
  cursor: pointer;
  font-family: var(--fh);
  font-weight: 600;
  text-transform: uppercase;
  color: var(--muted);
}
.tab.active {
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}

/* Cards & Tables */
.card {
  background: var(--card);
  padding: 20px;
  border-radius: 8px;
  box-shadow: var(--shadow);
  margin-bottom: 20px;
}
table { width: 100%; border-collapse: collapse; margin-top: 10px; }
th, td { padding: 12px; text-align: left; border-bottom: 1px solid var(--border); }
th { font-family: var(--fh); text-transform: uppercase; color: var(--muted); }
.badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
}
.badge-green { background: #e8f5e9; color: var(--green); }
.badge-blue { background: #e3f2fd; color: var(--blue); }

/* Buttons */
.btn {
  padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer;
  font-family: var(--fh); text-transform: uppercase; font-weight: bold;
  transition: all 0.2s;
}
.btn-primary { background: var(--accent); color: #fff; }
.btn-ol { background: transparent; border: 1px solid var(--border); color: var(--text); }
.gnh { color: var(--green); border-color: var(--green); }
.rh { color: var(--red); border-color: var(--red); }
.btn-wa { background: #25D366; color: white; border: none; }

/* Admin Area */
.admin-card { border: 1px solid var(--border); padding: 15px; margin-bottom: 15px; border-radius: 8px; }
.danger-zone { border: 1px solid #f5a5a5; padding: 15px; border-radius: 8px; background: #fffafa; }

/* Footer */
.footer {
  text-align: center;
  padding: 20px;
  margin-top: 40px;
  border-top: 1px solid var(--border);
  color: var(--muted);
  font-size: 0.9rem;
}
</style>
</head>
<body>
<div id="root"></div>

<script type="text/babel">
const { useState, useEffect } = React;

function App() {
  const [activeTab, setActiveTab] = useState("stock");
  const [stock, setStock] = useState([
    { id: 1, campaña: "23/24", especie: "SOJA", variedad: "NIDERA 5009", cantidad: 450 },
    { id: 2, campaña: "24/25", especie: "MAIZ", variedad: "DK 72-10", cantidad: 120 }
  ]);
  const [ordenes, setOrdenes] = useState([]);
  const [modal, setModal] = useState(null);

  // Funciones de admin
  const handleChangePass = () => {
    alert("Funcionalidad de cambio de clave (Blindada)");
  };
  const resetAll = () => {
    if(confirm("¿Estás seguro de resetear todos los datos?")) {
      setStock([]);
      setOrdenes([]);
    }
  };

  // Mensaje de WhatsApp Mejorado
  const enviarWhatsApp = (oc) => {
    const texto = `🚜 *LA CLEMENTINA - ÓRDEN DE CARGA* 🚜\n\n` +
                  `*ID de Órden:* #${oc.id}\n` +
                  `*Especie:* ${oc.especie} - ${oc.variedad}\n` +
                  `*Cantidad:* ${oc.cantidad} bolsas\n` +
                  `*Destino:* ${oc.destino}\n` +
                  `*Transporte:* ${oc.transporte || 'A confirmar'}\n\n` +
                  `_Gestionado vía Sistema Autogestión_`;
    const url = `https://api.whatsapp.com/send?text=${encodeURIComponent(texto)}`;
    window.open(url, '_blank');
  };

  // Renderizado Condicional de Tabs
  return (
    <div className="app-container">
      <div className="header">
        <h1>LA CLEMENTINA · <span>STOCK SEMILLAS</span></h1>
        <p style={{ margin: 0, color: "var(--muted)" }}>Gestión Profesional de Inventario Agrícola</p>
      </div>

      <div className="tabs">
        <div className={`tab ${activeTab === 'stock' ? 'active' : ''}`} onClick={() => setActiveTab('stock')}>📊 Stock</div>
        <div className={`tab ${activeTab === 'ordenes' ? 'active' : ''}`} onClick={() => setActiveTab('ordenes')}>📑 Órdenes</div>
        <div className={`tab ${activeTab === 'admin' ? 'active' : ''}`} onClick={() => setActiveTab('admin')}>⚙️ Configuración</div>
      </div>

      {/* TAB: STOCK */}
      {activeTab === "stock" && (
        <div className="card">
          <h2>Resumen de Inventario</h2>
          <table>
            <thead>
              <tr>
                <th>Campaña</th>
                <th>Especie</th>
                <th>Variedad</th>
                <th>Stock Disponible</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {stock.map(item => (
                <tr key={item.id}>
                  <td><span className="badge badge-blue">{item.campaña}</span></td>
                  <td><strong>{item.especie}</strong></td>
                  <td>{item.variedad}</td>
                  <td>{item.cantidad} bolsas</td>
                  <td>
                    <button className="btn btn-primary" onClick={() => alert("Mover/Despachar " + item.variedad)}>Mover</button>
                  </td>
                </tr>
              ))}
              {stock.length === 0 && <tr><td colSpan="5">No hay stock registrado.</td></tr>}
            </tbody>
          </table>
        </div>
      )}

      {/* TAB: ÓRDENES */}
      {activeTab === "ordenes" && (
        <div className="card">
          <h2>Órdenes de Carga Generadas</h2>
          <button className="btn btn-primary" onClick={() => setOrdenes([...ordenes, { id: Date.now(), especie: "SOJA", variedad: "Generica", cantidad: 100, destino: "Puerto", transporte: "Camión A" }])} style={{marginBottom: '15px'}}>
            + Simular Nueva Órden
          </button>
          <table>
            <thead>
              <tr>
                <th>ID Órden</th>
                <th>Detalle</th>
                <th>Destino</th>
                <th>Notificar</th>
              </tr>
            </thead>
            <tbody>
              {ordenes.map(oc => (
                <tr key={oc.id}>
                  <td>#{oc.id.toString().slice(-4)}</td>
                  <td>{oc.cantidad} bls - {oc.especie}</td>
                  <td>{oc.destino}</td>
                  <td>
                    <button className="btn btn-wa" onClick={() => enviarWhatsApp(oc)}>📱 WhatsApp</button>
                  </td>
                </tr>
              ))}
              {ordenes.length === 0 && <tr><td colSpan="4">No hay órdenes pendientes.</td></tr>}
            </tbody>
          </table>
        </div>
      )}

      {/* TAB: ADMIN */}
      {activeTab === "admin" && (
        <div className="card">
          <h2>Panel de Administración</h2>
          <div className="admin-card">
            <h3>Seguridad</h3>
            <button className="btn btn-ol gnh" onClick={handleChangePass}>✓ Guardar nueva clave</button>
          </div>
          <div className="admin-card danger-zone">
            <h3 style={{color:"var(--red)", marginBottom:8}}>⚠ Zona de peligro</h3>
            <p style={{fontSize:".8rem", color:"var(--muted)", marginBottom:10}}>Borra todo el stock, historial, órdenes y catálogos, volviendo al estado inicial de demostración.</p>
            <button className="btn btn-ol rh" onClick={resetAll}>🗑 Resetear todos los datos</button>
          </div>
        </div>
      )}

      <div className="footer">
        Creado por Ignacio Diaz
      </div>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
</script>
</body>
</html>
