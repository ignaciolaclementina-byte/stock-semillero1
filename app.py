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
const LOGO_SRC = "data:image/png;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJTEUAAQEAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAH4AABAAEAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAACRyWFlaAAABFAAAABRnWFlaAAABKAAAABRiWFlaAAABPAAAABR3dHB0AAABUAAAABRyVFJDAAABZAAAAChnVFJDAAABZAAAAChiVFJDAAABZAAAAChjcHJ0AAABjAAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEJYWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9YWVogAAAAAAAA9tYAAQAAAADTLXBhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACAAAAAcAEcAbwBvAGcAbABlACAASQBuAGMALgAgADIAMAAxADb/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wAARCACmAk8DASIAAhEBAxEB/8QAHQABAAMBAQEBAQEAAAAAAAAAAAYHCAQFAwkCAf/EAEsQAAEDAgICDAcQAAYCAwAAAAEAAgMEBQYRIZIHCBIVFjE1QVFUstITN1Nhc3SBFCIyNlVxcnWCkZOhsbPBwiMzQlJi0ZSiGCTw/8QAHAEBAAIDAQEBAAAAAAAAAAAAAAMEAgYHAQUI/8QAQBEAAQIDBAYGBwcEAgMAAAAAAAECAwQRBRITUQYUITEycRY0QVJToQcVFzNhscEiNXKBkdHhI0JDgvDxVKLi/9oADAMBAAIRAxEAPwAiKy7NaLXLaKKSSgp3PfTsc5xjGZJaMyvg27b0KxobIkRquvLTYXpGRdOOVrVpQrRFau8to+TaX8MJvLaPk2l/DC1n2iyfgu8j6PR+L308yqkVq7y2j5Npfwwm8to+TaX8MJ7RZPwXeQ6Pxe+nmVUitXeW0fJtL+GE3ltHybS/hhPaLJ+C7yHR+L308yqkVq7y2j5Npfwwm8to+TaX8MJ7RZPwXeQ6Pxe+nmVUitXeW0fJtL+GE3ltHybS/hhPaLJ+C7yHR+L308yqkVq7y2j5Npfwwm8to+TaX8MJ7RZPwXeQ6Pxe+nmVUitXeW0fJtL+GE3ltHybS/hhPaLJ+C7yHR+L308yqkVq7y2j5Npfwwm8to+TaX8MJ7RZPwXeQ6Pxe+nmVUitXeW0fJtL+GFHce2+ipLbA+lpYYXGbIljQCRkVes3TeWn5pksyG5FctKrQhmLGiQISxFcmwhiLy8UzS09lllgkdG8Obk5pyPGFC99rn1+o1yt8hwVelUU+BEjIxaKhZCKt99rn1+o1ym+1z6/Ua5UmquzI9abkWQirffa59fqNcpvtc+v1GuU1V2Y1puRZCKt99rn1+o1ym+1z6/Ua5TVXZjWm5FkIq332ufX6jXKb7XPr9RrlNVdmNabkWQirffa59fqNcpvtc+v1GuU1V2Y1puRZCKt99rn1+o1ym+1z6/Ua5TVXZjWm5FkIq332ufX6jXKb7XPr9RrlNVdmNabkWQirffa59fqNcpvtc+v1GuU1V2Y1puRZCKt99rn1+o1ym+1z6/Ua5TVXZjWm5FkIq332ufX6jXKb7XPr9RrlNVdmNabkWQirffa59fqNcpvtc+v1GuU1V2Y1puRZCKt99rn1+o1ym+1z6/Ua5TVXZjWm5FkIq332ufX6jXKb7XPr9RrlNVdmNabkWQirffa59fqNcpvtc+v1GuU1V2Y1puRZCKt99rn1+o1ym+1z6/Ua5TVXZjWm5FkIq332ufX6jXKb7XPr9RrlNVdmNabkWQirffa59fqNcpvtc+v1GuU1V2Y1puRZCKt99rn1+o1ym+1z6/Ua5TVXZjWm5FkIq332ufX6jXKb7XPr9RrlNVdmNabkWQirffa59fqNcpvtc+v1GuU1V2Y1puRZCKt99rn1+o1ym+1z6/Ua5TVXZjWm5FkIq332ufX6jXKb7XPr9RrlNVdmNabkWQirffa59fqNcpvtc+v1GuU1V2Y1puRZCKt99rn1+o1ym+1z6/Ua5TVXZjWm5FkIq332ufX6jXKb7XPr9RrlNVdmNabkWQuK98lzfZ7QUbwnX1tRd2xz1U0jNw47lziQpJe+S5vs9oKCIxWLRSeG9HpVDtVsWLkSg9Wj7IVTq2LFyJQerR9kLm3pG6tB/EvyNj0f94/kdqIi5KbUEREAREQBERAEREAREQBERAEREAUW2SOSqb0/wDUqUqLbJHJVN6f+pWwaK/e8Dn9FKFqdUfyKrxjyDN9JvaCgSnuMeQZvpN7QUCX6OluA5tM8YREVgrhERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQHt4L5cb6Nylt75Lm+z2golgvlxvo3KW3vkub7PaCozPGXpbgO1WxYuRKD1aPshVOrYsXIlB6tH2QuY+kbq0H8S/I2jR/3j+R2oiLkptQXu4Iooq69bmeJssUcTnua4Zg8QH6rwlNNjSD3tZUkc7Y2n7yf4X39F5RJq1YMNyVStV/JFX6FC04qwpV7k3/uSLeS0fJtL+GF8q21Weno56g22lyijc//ACxzDNeqvHxnP4DDlUQci8Bg9pGf5ZrtNoS0nLSkWNhN+y1V4U7E5GnwIkWJFay8u1U7VKxREX53N/CIiAIiIAiIgCIiAKLbJHJVN6f+pUpUW2SOSqb0/wDUrYNFfveBz+ilC1OqP5FV4x5Bm+k3tBQJT3GPIM30m9oKBL9HS3Ac2meMIiKwVwiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiID28F8uN9G5S298lzfZ7QUSwXy430blLb3yXN9ntBUZnjL0twHarYsXIlB6tH2QqnVsWLkSg9Wj7IXMfSN1aD+JfkbRo/wC8fyO1ERclNqCsfAMHgcOxvy0zSOf+e5/hVwrbssHua0UkGWRZC0H58tP5rf8A0eS1+eiRl/tb5qv7Ip8G34lIDWZr8jrUT2Sp9zb6Wnz/AMyUv1Rl/ZSxQDZGn3d3hgB0RQjP5yT/ABkt300mcCyIidrqJ+q7fJFPjWPDvzbfhVSMIiLhJu4REQBF6tuw7dq4B0dK6OM/65fej89J9gXtU+B5yAai4RsPOGRl35khfblNHLUnG3oUFaZrsTzoUotoS0JaOenz+REEU4bgemy99Xyk+ZgC+M2BjlnDcQT0Pi/kFX3aF2y1K4Vf9m/uQJbEmq0veS/sQ1F6t7sNdaWNlqPBPic7ch7Hc/RkdPMvKWuzUpHlIiwo7Va5OxT6EKKyK28xaoFFtkjkqm9P/UqUqLbJHJVN6f8AqV9jRX73gc/opUtTqj+RVeMeQZvpN7QUCU9xjyDN9JvaCgS/R0twHNpnjCIisFcIi03sQ7C+CMTbHFnvl0grnVlXG90pjqS1pIkc0ZDLRoAWD3oxKqZsYr1ohmRFZW2KwbZMD42o7TYY52U0ttZUOEshed2ZJWnT0ZMCrVZNcjkqhi5qtWihERengREQBERAEUr2NsA4gx7dzQ2aBrYosjU1UuiKBp4szzk8zRpPzAkaMw5tccFUNO3fiquN2qMvfnwngY/Y1uke1xUb4rWbFJGQnP2oZIRac2ZthvAGHNj26Ygt0FdRVFHG0xBtUXte9z2tAcH56M3DiIXLtXMD4TxLsf11ffrFSXCpjuskLZJQSQwRREN4+LNxPtXmM27eMsB166ZtRX7trcIYZwvb8PyYfs1LbnVEs4lMII3YAZlnp5syqCWbHo9KoRvarFooREWRiEREAREQBERAEREAREQBERAEREARF6NisV6vtT7mstqrbhLztpoXSZfPkNA85QbzzkRX5tXdjXDmKbZcMRYipRXtgqfctPTOeQxrg1rnPcARuvhgAHRx8ejLF70YlVMmMV60QoNFdu2h2O7DhCotd2w9B7jp65z4pqUPJa17QCHNzJIzBOY4hkOlUkjHI9KoHtVi0UIiLIxCIiAIiIAiIgCIiA9vBfLjfRuUtvfJc32e0FEsF8uN9G5S298lzfZ7QVGZ4y9LcB2q2LFyJQerR9kKp1bFi5EoPVo+yFzH0jdWg/iX5G0aP+8fyO1ERclNqOi2we6bhT0/lJWsPtKt5VpgeDw2I4CeKMOefYMh+ZCstde9Hctck4sbvOp+ifypqdvxKxmsyT5/9BVbiuf3RiKsfnobJuB9kbn+FaEr2xxOkecmtaXH5gqenkdLM+V3wnuLj85Kh9I0zdl4MDNVX9Ep9TPR+HV735JT9f8Ao/hEX0poZamojghYXySODWgc5XKWtV6o1qVVTaFVESqn2tlBU3GqbTUse6edJJ4mjpJ6FYNhw3Q2xrZHtFRU8ZkcNDT/AMRzfPxrqsFqhtNC2CMB0jtMsmWlx/66F6K7Ro1ojAs9jY8y29FXPc3l8fj+nx0+0bVfHcrIa0b8wi+dVUQUsDp6iVkUbeNzjkFFrhjanY4toqV83/OQ7kfdx/otjtG2ZGzURZmIjVXs3r+ibT58vJxpj3baktRQPhvX9Upv/b/tdNLjj3wFVQaOd0b/AOD/ANr40PTax3uu4ipzav7Ft1jTaJW75ofDZIrN3W09E06Imbt3zni/Ifmomuu81hr7pUVenKR5LQeMN4gPuyXIuQ27P6/aEWYRdirs5JsTyQ2ySgYEBrMk8+0KLbJHJVN6f+pUpUW2SOSqb0/9SrWiv3vA5/RSK1OqP5FV4x5Bm+k3tBQJT3GPIM30m9oKBL9HS3Ac2meMIiKwVwtw7XfxMYc9DJ+69YeW4drv4mMOehk/deq81woWJbiUorbk+M62/UsX786pNXZtyfGdbfqWL9+dUmpIPAhHG41A0nIKS2/AON7hTioo8JXuaFwzbIKKTcuHmJGn2KV7WS9Wmy7J0cl5NFHTTUkzG1FVuQ2ne0eEDw53wTkwtz/5LQNVs87GkFf7k35nlaHbl08dJIYx7csyPOAVjEiOatGpUyhw2uSrloZFv2GMR2BrXXuxXK3MccmvqaZ7GuPQCRkV5C/REttOIrGN02muVrroQ4BwD45o3DMHToIKw/sy4SZgvZCuNkp917jBE1IXHM+CeMwM+fI5tz59ykKNfWi7xFg3Eqm4hy+tJTzVdVDS00Zknme2ONg43OJyA+8r5KebX23suWzHhynkaHNjqXVGnmMTHSA/ewKVy0RVImpVUQ19sZYRosE4OorHSMZ4RjA+qlaNM0xA3bz7dA6AAOZVds6bONRhe9SYawrDTTV8Girqpm7tkTiM9wwA6XDnJ0DiyzzyvKtqGUlHPVSfAhjdI75gMyvztulbPcrnVXGqfu6iqmfPK7pc5xcT95VOAy+5VcXI71Y1EaTfF+y9jLFmF5sPXyopJ6aWVkrpGQCOT3pzDfe5DLPTxcw0q9Npt4sbl9dS/sQLJa1ptNvFjcvrqX9iBSx2o2HsIoDldE2nibdXkvDHpqjsxrMy0zt1eS8MemqOzGq62uOx3BjjFE1Xdoy+zWwNfOzSPDyOz3EefRoJOXMAOfNewnI2FVTyK1XRaIQjDuDsVYij8LZMP3KvhzI8LFTuMeY5t38HP2r44iwxiHDsjWX2y19u3ZIY6ogcxrz/AMXHQfYtwY2xhhfY7sdLNdXikpnOENLTU0OZOQ4mtGQAA+YDR0hdpbh3HeD2lzILpZrlDm3dN0OB59OlrgfmII5iFhrC71TYZ6um5F2n59r2o8J4qkjbJHhq9PY4Atc2hlIIPEQdyvvsjYblwjja6YekeZBSTZRPI0vjcA5jj5y0jPzrdGCpTPg2yTEAGS307iBzZxtKkixbiIqdpHChX1VF7DBNkw/fL3XvoLRaK6uqo/8AMiggc5zNOXvsh73T0rqxJg7FOHI2y3ywXCgiccmyywkRk9G64s/NmtqR3HAeAqyGxurqC1VV1qHziJ7vfzSPfpe48wJOQLshoyHEpJeLbQ3i11NsuVNHU0lTGY5YnjMOB/8A3HzFRLMrXdsJUlkpv2mAMO4axBiKV0Vis1dcXMy3Zp4XPDM+LdEaB7V/WJML4jw29jb9ZK63eEOTHTwlrXnzO4j7CtsWm5YDwPNbMCUlxobfUua1tPSF3v5HO4i45fCcenIk8S9rF+H7dijDtZY7pC2Wmqoy3MjMsd/pe3ocDpHzL3WVRd2w81ZFTftPz1X9wRSzzMhgifLK8hrGMaS5xPMAOMr63GkmoLhU0NQNzNTyuikHQ5pIP5hbC2vWxnQ4QwzTXi4UscmIK6ISyyPbm6nY4AiJvRo+ERxnMcQCmiREYlSGHDV60MxN2M9kB1H7rbg69GPLPL3K7d6uW6/JRaohmp53wTxPiljcWvY9pa5pHGCDxFbpt2yfg2vxzLg2luRfc43OjH+GRE+Rue6Y1/EXDI+bRkM1CdtPgOivOD58V0dMxl2tYD5ZGtyM0HE4O6dznugTxAEc6ibHW9RyEroCXatUylbLbcbpO6ntlBVVszW7t0dPC6RwbmBnk0E5ZkafOvvc7FfLXA2oudmuNFC524bJUUr42l2ROWbgBnkDo8ytPag+Nab6rm7ca1TiGx2m+wU0V4pI6qGkqW1UccnwPCNBDSRzgZnQdCyiR7jqUMYcC+2tTCtrwJjS6UTK234VvFTTSDOOVlI8teOkHLSPOF4dfR1dBVyUldSz0tTEdzJDNGWPYegtOkLf+GsV4bxJLUw2G80dwfSO3MzYJN1uOg+caDpGhVfttMJ0lzwHwnjga24WqRm6ka33z4XuDS09IDnNcOj33SViyYVXUVDJ8uiNqimfNh/D1Xecd2KSSyVFfat8Yo6p5pXSQZZgua85FuWRGYPMVuaho6SgpmUtDSwUsDNDYoYwxjfmA0BZ02qWOsN2XD5wpcKySO63C8OdTRCF7g4PjiY3NwGQ0tPGtJKKYcquopLLtRG1Q/PWrwziSjppKmrw/dqeCMZvllo5GtaOkkjIKa7CmNMcYQFY/DdhnvNuqHj3RCKWSRjZANBDmfBdkdPSMtHEre2VdmXAF/2O73Z7ZdZ5ayrpjHCx1JI0F2Y5yMgv62mXxEvH1mf2mKZ0RVYquQhbDRHojVKV2ZsVY1xdX0tdimzVNqpYQ5lJA6mkijaTkXEF/wAJxyGZ8wUOtljvV0hdNbLPcK6Njty59PTPka08eRLQdK0lt0fixh/12TsL6bTCUnCF9hyGTLg1wPPpjA/qvUiUh3kQLDrEuqpmeus92oauKkrbXXUtRNkYopqdzHvzOQyBGZ06NC9mXY9x1FSGrkwhfGwhu6LjQyaB05ZZrbt8pMN224nGV5FJBPRU3gRW1BAEEZcScieIkuy6eYcZz7cP3q1X+1xXSzV8NdRy57iWJ2YzHGDzgjoOlRrMrSqIZpLJWiqfneQQSCCCOMFf7Gx8sjY42Oe9xya1ozJPQArx23mE6Oz4ot+IrfAyFl2bIKljG5DwzCCX/O4OGfnaTzrl2qOJLDYMR3oX2ego430Qmiq6nctLCx2RY1x0++D+Ice5U+JVl5EIMOj7qqV9SbHmO6uATQYPvjo3cTjRSDPzjMaR515V9w/fbDK2K92evtr3/AFTTuj3XzZjT7Fr5mzzsaPuLaMXmcNc7cioNJIIvaSMwPPkp7iCz2nEtjmtd1pYa2hqWZFrtIII0OaeYjjBHEodYc1ftITJLtcn2VPzxRe3juwSYXxhdcPyvMhoqh0bXkZF7ONrva0g+1eIrSLXaVVSmwIiID28F8uN9G5S298lzfZ7QUSwXy430blLb3yXN9ntBUZnjL0twHarYsXIlB6tH2QqnVsWLkSg9Wj7IXMfSN1aD+JfkbRo/wC8fyO1ERclNqJfsaQZ1VZUkfBY1gPznM/oFN1G9jyDwdjdKRplmJB8wyH6gqSLvmiMtq9kQU7VSv6qq/KhotqxMSbeuWz9DzcUz+58P1smeRMZYPte9/lVWrlc0OGTgCOghfz4GLyTNUKlpHoq+2o7IuNdRqUpSvbWu9Caz7TSTYrblarn/BTil+xzbw+ea4yNBEf+HHn/ALjxn7svvU08DF5JmqF/TWtaMmtAHQAqNj6DNs+cZMxIt+7tRLtNvYu9d28nm7aWPCWG1tK/H+D/AFf5I9scbpHuDWtBLieYL/V4WOqp1Nh+RrDk6dwi9h0n8gR7VudoTjZKViTDv7UVf4/M+RLwljRWw07VIZia8y3asJDi2mYcomfyfOV5KIvzpNzcacjOjxlq52//AJlkdAhQmQmIxiURAiIqxIEREAUW2SOSqb0/9SpSotskclU3p/6lbBor97wOf0UoWp1R/IqvGPIM30m9oKBKe4x5Bm+k3tBQJfo6W4Dm0zxhERWCuFuHa7+JjDnoZP3XrDy3Dtd/Exhz0Mn7r1XmuFCxLcSlFbcnxnW36li/fnVJq7NuT4zrb9Sxfvzqk1JB4EI43Gp7ODcM3nF1+hstjpTUVUukk6GRtHG955mjp+YDMkBaKwttaLHBTsfiS91tZU5Zujo9zFED0ZuBc75/e/Mu3aeWWnpcBV178GDVV9a6Mvy0+DjADW6xefu6FwbbHHeIbBPbMO2Ssnt0dXA6oqKiBxbI8brchgcNLQMiTlpOY9sL4jnPuN2EzIbWsvu2l2YWsdBhrD9JY7YJRR0jSyISP3TgCSdJ59JWXduQ1rdk+3kNALrNESQOM+GmH8BXntcp6qq2GbDUVk0087/dBdJK4uc7/wCxLkSTpOjJUbtyfGdbfqWL9+dYQUpFVDOMtYVSk1Z21elbHs1WZrs85I6hjfn8A8/wqxUh2Nb2zDmPrJe5XFsNLWMdMRzRk5P/APUlW3pVqoVGLRyKbyv8ElTYrhTRDOSWlkY0ectIC/Oxfo+xzXtD2ODmuGYIOYIWINnPAtdgvG1aPczxaayZ01DOGncblxJ8Hn/ubxZceQB51VlXIiqhammqqIpX61ptNvFjcvrqX9iBZLWtNpt4sbl9dS/sQKWY4CKX4zxNuryXhj01R2Y1KtqXb4aTYljqmAeErq2aWQ8/vSIwPuZ+ZUV26vJeGPTVHZjUv2qFXDUbD9LDG4F9LVzxSDPicXbv9HhQr7lCZvvlOPZ72KcRbId/t9Xbrtb6Wjo6UxiKoL914QvJc4blpGRG4HsUy2GcKXLBWBKfD1zrIKuWCaRzXwl24DXO3WQzAPGSfaojs97KGJdju726O3Wi31VvrYCRNUB+Yla47pvvXAZbksPtKrT/AOTWLPkCyfdL314jIj2Iibj1Xw2PVV3nn7cCmZBsq08rQM6i1QyuyHOHyM/RgWoMA/ETD/1ZTftNWJNk7G9xx9iKO93Omp6aaOmbTtjg3W5DWuc7/USeNxW28A/ETD/1ZTftNXsZFRjUUxgqjnuVDIO2Uq5anZovpe45QmGKMZ/BAhZxe3M+1bStznPt9M97i5zomkk85yCxLtifHPiP00f7TFti18mUvoWdkJH4GnsHjcYs2YaicbPV3qBI7wsdzj3DucbncBv3ZBbcWHtmLx5Xv6zb/VbhSPwtEDicYhqrZDc9sVU2qRjfc8+KpInsy0bj3Ucx92a23UCU08ggLRLuDuC7i3WWjP2rFL62K3bZaetnIEUWLZDIT/pb7qIJ9g0ra03hPAv8DufCbk7jdcWfNn5kmP7RL/3GbsJ7X/F9mxha7/JiC0Suo66KqkydKXPDXhzh8HnGY9qv3GsEdVg2900ozjmt88bx5jG4FZxrdshjSirJqOrw3Z4aiCR0csb2yhzHNORB9/xgrhue2PxVX22qoXWSzRtqIXxF7RJm0OaRmM3ZZ6V66HEeqKp42JCYiohy7ULxrS/Vk3bjWjdmupmpNifEs1O8sk9wSMDhxgOG5P5ErOW1C8a0v1ZN241ofZ38UGJfUj+oXkb3qHsH3Sme9p/LIzZTqY2vIbJa5Q8cxyfGQtB7PLWu2H8ShzQ4e4yciOcOBCzztQvGtL9WTduNaH2d/FBiX1I/qF7F96gg+6UyFsNeNfC/1nB2wt5rBew45rdlbC5c4NG+kAzJ5y8ALeiTXEgleFT831qvaZfES8fWZ/aYsrzRyQzPhlYWSMcWuaRkQRoIWqNpl8RLx9Zn9pimmOAgl+M5tuj8WMP+uydhNpd8WMQeux9hNuj8WMP+uydhNpd8WMQeux9hQ/4Cb/Od23Jnmj2PbXCyQtjlujfCNH+rKN5Ga5dphPK7B98py4mOO4Ne1vQXRgHshfXbm/ESz/WY/aeubaXfFjEHrsfYXn+A9/zjbo/FjD/rsnYVB7HWB79ju9b22SBpEYDqiokOUUDTxFx8+nIDMnI9Byvzbo/FjD/rsnYUs2rlmprZsRW+rjYz3RcpJaid4GkkPLGjPoDWjR0krJsS5Cqhi6Hfiqikew9tasK00DHXu8XO41GXvhCWwRfdk53/ALK6bRQwWu1Udspd34CkgZBFu3bp25Y0NGZ5zkONZu21WPcS0OLo8L2q5VNuoYqVksvueQxvme/PjcNO5AyGXFx556Mrz2JHTv2MMMyVL3vlfbIHuc92bnZsBzJPHnmooiOVqOcpLDVqOVrUMrbaONjNmm7uaMi+Knc7znwLB+gCrBWjtpvHPdPQ0/7TVVyuw+BClE41CIizMD28F8uN9G5S298lzfZ7QUSwXy430blLb3yXN9ntBUZnjL0twHarYsXIlB6tH2QqnVsWLkSg9Wj7IXMfSN1aD+JfkbRo/wC8fyO1ERclNqLWw1B7msNFFlkfBBxHndpP6r0FTnhZfKP1inhpfKv1iumS3pBhy8FkFsvsaiJxZJTumuRLBdEer1ib1ru/kuNFTnhpfKv1inhpfKv1ipvaQ3/x/wD2/wDkw6PL4nl/JcaKnPDS+VfrFWph2b3RYqKXPM+Ba0nzgZH8wth0e0qZbUZ8JIdxWpXfWu2mSFCfsxZNiOvVr8DvUT2Ss976Xj3PhTn9yli8jF9vfcbLJHE3dSxkSMHSRxj7iV9PSOWiTVlxoUNKqqbPy2/QrWfEbDmWOduqVgiEEHI6Ci/PJvwREQBERAFFtkjkqm9P/UqUqLbJHJVN6f8AqVsGiv3vA5/RShanVH8iq8Y8gzfSb2goEp7jHkGb6Te0FAl+jpbgObTPGERFYK4W4drv4mMOehk/desPLuprxd6aFsFPda6GJnwWR1D2tHzAFRxYeIlCSFEw1qfoDc7FY7pO2ouVmt1bM1u4bJUUzJHBuZOWbgTlmTo86huy3hfDVLsY4kqKbDtogmjtszmSR0UbXNIaciCBmCsab/335auX/lP/AO1/E16vM8T4ZrtXyRvGTmPqXkOHQQTpUKS6ou8mWYRU3GgdqDjW309JWYLuFQyColqDU0BechKXNAfGPONyCBz5noV145wJhfGsdKzEdtFWaVxML2yOjc3PjGbSDkcho8ywKxzmOD2OLXNOYIORBXuz40xhPQe4J8VXyWlI3JhfXylhGWWRG60jRxcSyfAVXXmrQxZHRG3XJU3RhGtw9NQzWvDctMaW0S+4Xx0/wInNa07kHnyDhmenMcYKzXty4C3ZDtNTmcn2lrBo0e9mlPH9pUxRXO40Ubo6K4VdMxxzLYpnMBPTkCv4ra6trnNfW1lRUuaMmmaQvIHmzXrIFx1anj499tKHOiIpyA0/tddmK3S2elwliutZS1dMBFRVczsmTR8TWOcdAcOIE6CMufjvqspaO4Ujqerp4KumkAzjlYHscObQdBX5zL17TijEtoh8BasRXegi/wBlNWyRN+5pCrPl0VaopZZMKiUVDVW2QwxZqXYbus1qs9BRup5oJj7mpmRk/wCK1p+COhxXFtNvFjcvrqX9iBZeu+IL9eG7m73u53AZ55VVU+XT9olc9FdLlRRGKjuNXTRl26LYpnMBPTkDx6AssFbl1VMcZL95ENHbdXkvDHpqjsxqA7W3ZIpcE36otl6lMdmuW53cuRIp5RxPIH+kjQfYeZVdW3G4VwaK2uqqkMz3Imlc/c59GZ0LlWTYSIy4pg6KqvvofoVc7bh7F1jbDXU1DeLbOBJGTlIx3Q5rhxHj0gqM27Yd2NKCo8PBhKje/PPKokknbqyOI/JYss9+vlmJNovNxtxJzPuWqfFnqkLouWK8U3KMx3HEl5rGEZFtRXSSDL5nOPSVEku5NiOJlmGrtVp/eyBbo7Rjq+2yENbDTXCaOINGQ3Aedzl7MlunAPxEw/8AVlN+01fn0vQjvl7jjbHHeLgxjQA1ral4AA4gBmpIkK+iJUihRbiqtCX7Ynxz4j9NH+0xbYtfJlL6FnZC/OypnmqZnT1E0k0r/hPkcXOPzkruF+voAAvVxAHEBVP/AO15Eg3kRK7jKHGuqq03kt2YvHle/rNv9VuFfnHNPNNO6eaaSSZxzdI9xLiekk6V3b/335auX/lP/wC0iQb6IldwhxriqtN56Wyno2T8VEfLVZ++9ar2CdlK2YzsFLbbhWRw4ipoxHPFK4A1OQy8Iz/dnxkDSDnoyyKxlLJJLK+WV7pJHuLnOccy4njJPOV/jSWuDmkgg5gjjCzfCR7aKYMiqx1UN44r2NMC4przX3zDtNU1bst3Mx74XvyGQ3Rjc0u0aNOarDbFbHeErBsSz1lgsdDb5qWshkMrRnK9pJYW7t2biPfg5Z82fMs+U+N8aU8IhgxfiCKIDIMZcpmtHsDl5NxuNwuUwmuNfVVkgGQfPM6Rw9pJUbILmqn2iR8ZrkX7JbO1C8a0v1ZN241ofZ38UGJfUj+oWG6OrqqOXw1HUzU8mWW7ieWHLozC6Z7zeKiF0M92r5YnjJzH1D3NcPOCVk+DefeqYsjXWXaFqbULxrS/Vk3bjWh9nfxQYl9SP6hYbo6uqo5fDUdTNTyZZbuJ5YcujMLpnvN4qIXQz3avlieMnMfUPc1w84JR8G8+9UMjXWXaH+WC4y2e+2+7QNDpaKqjqWA87mODh+i3/he/WvEtjprzZ6plTSVDA5rmnS087XDmcOIjmX55Lvs96vFmkdLZ7tX26R3wnUtQ+In5y0hexYWIeQouGam2zeE8M0mxveL/AEtioIbrJUQufVshAkJdK0OOfSczmedcu0y+Il4+sz+0xZqu+JsR3iHwN3xBdrhFo95VVkkrdHFocSuSiudxoo3R0Vwq6ZjjmWxTOYCenIFY4K3LqqZYyX7yIaX26PxYw/67J2E2l3xYxB67H2FmetuVxrmtZW19VUtac2iaZzwD5sylFcrjQtcyir6qma45uEMzmAnz5Fe4P9O5U8xv6l+hqHbm/ESz/WY/aeubaXfFjEHrsfYWaK253GtjbHW3CrqWNOYbNM54B6ciV/lFcrjQtcyir6qma45uEMzmAnz5FMH+ncqMb+pfoaY26PxYw/67J2F3bUzGlDcMHNwhU1DI7lbXvdBG52maFzi/NvSWkuBHMNyss1tyuNc1rK2vqqlrTm0TTOeAfNmV8aeaannZPBK+KWNwcx7HFrmkcRBHEUwfsXVGN9u8hvDGux5g7F1wprniK0sqailbuWyeFfHmwHPcu3JG6GefH0npXtYbulou9qbUWKogqKGN7qdjof8ALzjJYQ3mIGWgjRlxLBtyxhi250PuG44nvNXSkZGGaukexw84JyPHzrgpLrdKOHwNJcqyniBz3EU7mtz+YFR6sqpRVJNZRFqiFj7amNzNmS4OdllJT07m/N4MD9QVVa+1ZV1VZL4asqZqiTLLdyvLzl0ZlfFWWpdREKzlvKqhERenh7eC+XG+jcpbe+S5vs9oKJYL5cb6Nylt75Lm+z2gqMzxl6W4DtVsWLkSg9Wj7IVTq2LFyJQerR9kLmPpG6tB/EvyNo0f94/kdqIi5KbUEREAREQBTjY6uIfTSW2R3v4yXx587Txj2HT7VB19aOpmpKqOpp3lkkZzaV9iwbVdZU6yYTam5UzRd/7p8UKc9KpNQVh9vZzLhReRh2+0t2hA3TY6oD38RP5jpC9dd/lJyDOQUjQHXmr2/wDO34GixYT4L1Y9KKhH77hWiuEjqiFxpZ3aXFrc2uPSR0/Mo/Lgq6Nd7yeleOndOB/RWAi+FPaI2XOxFivh0cu+6tK/lu8i7AtWZgtuo6qfEgkGCK4u/wAespmDpYHO/UBeVii0ss9bFTxyvlDog8ucMtOZH8K0FB9ktmVZRyZfCjc37iP+1rGk2i9n2dZb40uz7SKm1VVdirTl25H0rOtKPMTKMiLs2kRREXLDZwotskclU3p/6lSlRbZI5KpvT/1K2DRX73gc/opQtTqj+RVeMeQZvpN7QUCU9xjyDN9JvaCgS/R0twHNpnjCIisFcIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiA9vBfLjfRuUtvfJc32e0FEsF8uN9G5S298lzfZ7QVGZ4y9LcB2q2LFyJQerR9kKp1bFi5EoPVo+yFzH0jdWg/iX5G0aP+8fyO1ERclNqCIiAIiIAiIgP9Y5zHh7HFrmnMEHIgqQW7F10pQGTFlUweUGTvvH85qPIrslaU3IuvS0RWr8O3mm5fzII0vCjpSI2pOIccU5A8NQStPPuHh365L6OxvQ5e9o6knz7kfyoGi2Bum9sIlFiIv8Aqn7FFbFlFXh81JlUY5ORFPbwDzF8n8Afyo7e7xWXeRjqoxgR57hrG5AZ5Z+fmC89F8yf0itK0GLDmIqq1ezYieSJX8yzAs+XgLeht2hERfFLgUW2SOSqb0/9SpSotskclU3p/wCpWwaK/e8Dn9FKFqdUfyKrxjyDN9JvaCgSnuMeQZvpN7QUCX6OluA5tM8YREVgrhERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQHt4L5cb6Nylt75Lm+z2golgvlxvo3KW3vkub7PaCozPGXpbgO1WxYuRKD1aPshVOpvbcXW2mt1NTSQVZfFCxji1jciQANHvlz7Tmzpqel4TZZiuVFWtORsVizEKBEcsRaVQlyKM8NbV1et1G95OGtq6vW6je8ubdF7X8BxsXrKV76EmRRnhraur1uo3vJw1tXV63Ub3k6L2v4Dh6yle+hJkUZ4a2rq9bqN7ycNbV1et1G95Oi9r+A4espXvoSZFGeGtq6vW6je8nDW1dXrdRveTova/gOHrKV76EmRRnhraur1uo3vJw1tXV63Ub3k6L2v4Dh6yle+hJkUZ4a2rq9bqN7ycNbV1et1G95Oi9r+A4espXvoSZFGeGtq6vW6je8nDW1dXrdRveTova/gOHrKV76EmRRnhraur1uo3vJw1tXV63Ub3k6L2v4Dh6yle+hJlFtkjkqm9P/Ur++Gtq6vW6je8vGxbf6O70UUFNFUMcyTdkyNAGWRHMT0r7Wjuj9pS1pwYsWCqNRdq/kpTtCel4ks9rXoqqQHGPIM30m9oKBKxr9Ry19skpYXMa9xBBeSBoOfMozwTuPlqTWd3V3SBEa1tFU0OPDc51UQj6KQcE7j5ak1nd1OCdx8tSazu6psZmZDgvyI+ikHBO4+WpNZ3dTgncfLUms7upjMzGC/Ij6KQcE7j5ak1nd1OCdx8tSazu6mMzMYL8iPopBwTuPlqTWd3U4J3Hy1JrO7qYzMxgvyI+ikHBO4+WpNZ3dTgncfLUms7upjMzGC/Ij6KQcE7j5ak1nd1OCdx8tSazu6mMzMYL8iPopBwTuPlqTWd3U4J3Hy1JrO7qYzMxgvyI+ikHBO4+WpNZ3dTgncfLUms7upjMzGC/Ij6KQcE7j5ak1nd1OCdx8tSazu6mMzMYL8iPopBwTuPlqTWd3U4J3Hy1JrO7qYzMxgvyI+ikHBO4+WpNZ3dTgncfLUms7upjMzGC/Ij6KQcE7j5ak1nd1OCdx8tSazu6mMzMYL8iPopBwTuPlqTWd3U4J3Hy1JrO7qYzMxgvyI+ikHBO4+WpNZ3dTgncfLUms7upjMzGC/Ij6KQcE7j5ak1nd1OCdx8tSazu6mMzMYL8iPopBwTuPlqTWd3U4J3Hy1JrO7qYzMxgvyI+ikHBO4+WpNZ3dTgncfLUms7upjMzGC/Ij6KQcE7j5ak1nd1OCdx8tSazu6mMzMYL8iPopBwTuPlqTWd3U4J3Hy1JrO7qYzMxgvyI+ikHBO4+WpNZ3dTgncfLUms7upjMzGC/Ij6KQcE7j5ak1nd1OCdx8tSazu6mMzMYL8iPopBwTuPlqTWd3U4J3Hy1JrO7qYzMxgvyI+ikHBO4+WpNZ3dTgncfLUms7upjMzGC/Ij6KQcE7j5ak1nd1OCdx8tSazu6mMzMYL8iPopBwTuPlqTWd3U4J3Hy1JrO7qYzMxgvyPlgvlxvo3KW3vkub7PaC8jD1hrLfcRUzSQOYGkZMcSdPzheve+S5vs9oKnHcjnVQuQGq1tFO1ERQkwREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAFxXvkub7PaCIgP/Z";

const CAMPAÑAS_DEF = ["2024/2025","2025/2026"];
const ESPECIES_DEF = ["Soja","Trigo","Maíz","Girasol","Sorgo","Cebada"];
const VARS_DEF = {
  Soja:["DM 4612","SY 3x8","NA 5009"],
  Trigo:["Klein Proteo","Buck Meteoro","SY 100"],
  Maíz:["DK 7210","AX 7784","P1815W"],
  Girasol:["SY 4045","Paraíso 20"],
  Sorgo:["NK 300","DK 35"],
  Cebada:["Shakira","Lissette"],
};
const STOCK_INIT = [
  {id:1,campaña:"2024/2025",especie:"Soja",variedad:"DM 4612",tipo:"bigbag",tratada:false,cantidad:14,pesoUnit:800,lote:"L-001",fecha:"2025-04-01",pg:95,pmil:140,obs:""},
  {id:2,campaña:"2024/2025",especie:"Soja",variedad:"DM 4612",tipo:"bolsa",tratada:true,cantidad:320,pesoUnit:25,lote:"L-001",fecha:"2025-04-01",pg:95,pmil:140,obs:"Curasemillas MaximXL"},
  {id:3,campaña:"2024/2025",especie:"Maíz",variedad:"DK 7210",tipo:"bigbag",tratada:true,cantidad:8,pesoUnit:800,lote:"L-002",fecha:"2025-04-02",pg:92,pmil:280,obs:"Tratado"},
  {id:4,campaña:"2024/2025",especie:"Trigo",variedad:"Klein Proteo",tipo:"bolsa",tratada:false,cantidad:480,pesoUnit:25,lote:"L-003",fecha:"2025-04-03",pg:88,pmil:32,obs:""},
  {id:5,campaña:"2025/2026",especie:"Soja",variedad:"SY 3x8",tipo:"bigbag",tratada:false,cantidad:20,pesoUnit:800,lote:"L-010",fecha:"2025-04-04",pg:97,pmil:155,obs:""},
];
const BLANK = {campaña:"",especie:"",variedad:"",tipo:"bigbag",tratada:false,cantidad:"",pesoUnit:800,lote:"",ubicacion:"",fecha:today(),pg:"",pmil:"",obs:""};
const DEFAULT_PASS = "semillas2025";

function lsGet(k,fb){try{const v=localStorage.getItem(k);return v?JSON.parse(v):fb;}catch{return fb;}}
function lsSet(k,v){try{localStorage.setItem(k,JSON.stringify(v));}catch{}}

function downloadCSV(rows,filename){
  const sep=";";
  const csv=rows.map(r=>r.map(c=>{const s=String(c==null?"":c);return s.includes(sep)||s.includes('"')||s.includes('\n')?`"${s.replace(/"/g,'""')}"`:`${s}`;}).join(sep)).join("\r\n");
  const a=document.createElement("a");
  a.href="data:text/csv;charset=utf-8,\uFEFF"+encodeURIComponent(csv);
  a.download=filename;a.click();
}

function fmtOCNum(n){return "OC-"+String(n).padStart(3,"0");}

function printOCWindow(ocs){
  if(!ocs.length)return;
  const win=window.open("","_blank","width=900,height=700");
  if(!win){alert("Habilitá las ventanas emergentes para poder imprimir.");return;}
  const pages=ocs.map((o,idx)=>{
    const totalCant=o.lotes.reduce((s,l)=>s+l.cantidad,0);
    const lotesHtml=o.lotes.map(l=>`
      <tr>
        <td>${l.lote||"—"}</td>
        <td>${l.ubicacion||"—"}</td>
        <td style="text-align:center">${l.cantidad}</td>
        <td style="text-align:right">${fmt(l.cantidad*o.pesoUnit)} kg</td>
      </tr>
    `).join("");
    return `
    <div class="page">
      <div class="hdr">
        <img src="${LOGO_SRC}" alt="La Clementina" style="height:70px"/>
        <div>
          <h1>ORDEN DE CARGA</h1>
          <p>N° <b>${o.numero}</b> &nbsp;|&nbsp; Emitida: ${o.fecha}</p>
          ${o.remito?`<p style="margin-top:4px">🎫 Remito: <b>${o.remito}</b></p>`:""}
          ${o.nPedido?`<p style="margin-top:4px">📦 Pedido: <b>${o.nPedido}</b></p>`:""}
          ${o.estado==="despachada"?`<p style="color:#2e8b57;margin-top:3px">✓ DESPACHADA: ${o.fechaDespachada}</p>`:""}
        </div>
      </div>
      <table>
        <tr><th>Especie</th><td>${o.especie}</td><th>Variedad</th><td><b>${o.variedad}</b></td></tr>
        <tr><th>Campaña</th><td>${o.campaña}</td><th>Tratamiento</th><td><b>${o.tratada?"✓ TRATADA":"Sin tratar"}</b></td></tr>
        <tr><th>Tipo envase</th><td>${o.tipo==="bigbag"?"BigBag":"Bolsa"}</td><th>Total cantidad</th><td><b>${totalCant} ${o.tipo==="bigbag"?"BB":"bolsas"}</b></td></tr>
        <tr><th>PG (%)</th><td>${o.pg||"—"}</td><th>PMIL (g)</th><td>${o.pmil||"—"}</td></tr>
        <tr><th colspan="4" style="background:#f0f3f8">📦 DETALLE DE LOTES</th></tr>
      </table>

      <table style="margin-bottom:12px">
        <tr style="background:#f0f3f8">
          <th>Lote</th>
          <th>Ubicación</th>
          <th style="text-align:center">Cantidad</th>
          <th style="text-align:right">Kg totales</th>
        </tr>
        ${lotesHtml}
        <tr style="background:#fffaeb;font-weight:700">
          <td colspan="2"><b>TOTAL</b></td>
          <td style="text-align:center;border-top:2px solid #ccc"><b>${totalCant}</b></td>
          <td style="text-align:right;border-top:2px solid #ccc"><b>${fmt(totalCant*o.pesoUnit)} kg</b></td>
        </tr>
      </table>

      <table>
        <tr><th colspan="4" style="background:#f0f3f8">📋 INFORMACIÓN</th></tr>
        <tr><th>Destino / Campo</th><td colspan="3"><b>${o.destino||"—"}</b></td></tr>
        <tr><th>Observaciones</th><td colspan="3">${o.obs||"—"}</td></tr>
      </table>

      <div class="firmas">
        <div><div class="line"></div><p>Responsable despacho</p></div>
        <div><div class="line"></div><p>Transportista / Receptor</p></div>
        <div><div class="line"></div><p>Fecha y hora de despacho</p></div>
      </div>
      ${idx<ocs.length-1?'<div style="page-break-after:always"></div>':""}
    </div>`;
  }).join("");
  win.document.write(`<!DOCTYPE html><html lang="es"><head>
    <meta charset="UTF-8"/><title>Órdenes de Carga</title>
    <style>
      *{box-sizing:border-box;margin:0;padding:0}
      body{font-family:Arial,sans-serif;padding:15mm;color:#111;font-size:13px}
      .page{max-width:185mm;margin:0 auto 0}
      .hdr{display:flex;align-items:center;gap:20px;border-bottom:3px solid #e07b00;padding-bottom:12px;margin-bottom:18px}
      .hdr h1{font-size:1.3rem;font-weight:800;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px}
      .hdr p{color:#555;font-size:.83rem;margin-top:2px}
      table{width:100%;border-collapse:collapse;margin-bottom:24px}
      th{background:#f0f3f8;padding:7px 11px;border:1px solid #ccc;font-size:.73rem;text-transform:uppercase;letter-spacing:.5px;color:#444;text-align:left;width:130px;white-space:nowrap}
      td{padding:7px 11px;border:1px solid #ccc;font-size:.88rem}
      .firmas{display:flex;gap:28px;margin-top:50px}
      .firmas>div{flex:1;text-align:center}
      .line{border-bottom:1.5px solid #333;height:55px;margin-bottom:6px}
      .firmas p{font-size:.72rem;color:#555}
      @media print{body{padding:10mm}}
    </style>
  </head><body>${pages}<script>window.onload=function(){window.print()}<\/script></body></html>`);
  win.document.close();
}

/* ─── LOGIN ─────────────────────────────────────────────────── */
function LoginScreen({onLogin}){
  const [pass,setPass]=useState("");
  const [err,setErr]=useState(false);
  const doLogin=()=>{
    if(pass===lsGet("ss:password",DEFAULT_PASS)){onLogin();}
    else{setErr(true);setPass("");setTimeout(()=>setErr(false),2500);}
  };
  return(
    <div className="login-wrap">
      <div className="login-box">
        <img src={LOGO_SRC} alt="La Clementina" className="login-logo"/>
        <h1>Planta de Semillas</h1>
        <p>Ingresá tu clave para continuar</p>
        <input className={`login-input${err?" err":""}`} type="password"
          placeholder="••••••••" value={pass}
          onChange={e=>setPass(e.target.value)}
          onKeyDown={e=>e.key==="Enter"&&doLogin()} autoFocus/>
        {err&&<p className="err-msg">Clave incorrecta. Intentá de nuevo.</p>}
        <button className="login-btn" onClick={doLogin}>Ingresar →</button>
      </div>
    </div>
  );
}

/* ─── MODAL FORMULARIO STOCK ─────────────────────────────────── */
function ModalForm({item,campañas,especies,varMap,onSave,onClose}){
  const [f,setF]=useState(item?{...item}:{...BLANK});
  const set=(k,v)=>setF(p=>({...p,[k]:v}));
  const vars=varMap[f.especie]||[];
  const save=()=>{
    if(!f.campaña||!f.especie||!f.variedad||!f.cantidad)return alert("Completá campaña, especie, variedad y cantidad.");
    onSave({...f,cantidad:Number(f.cantidad),pesoUnit:Number(f.pesoUnit),pg:f.pg===""?"":Number(f.pg),pmil:f.pmil===""?"":Number(f.pmil)});
  };
  return(
    <div className="overlay" onClick={e=>e.target===e.currentTarget&&onClose()}>
      <div className="modal">
        <h2>{item?"Editar Registro":"Nuevo Ingreso"}</h2>
        <div className="form-grid">
          <div className="field"><label>Campaña</label>
            <select value={f.campaña} onChange={e=>set("campaña",e.target.value)}>
              <option value="">— Seleccionar —</option>
              {campañas.map(c=><option key={c}>{c}</option>)}
            </select>
          </div>
          <div className="field"><label>Especie</label>
            <select value={f.especie} onChange={e=>{set("especie",e.target.value);set("variedad","");}}>
              <option value="">— Seleccionar —</option>
              {especies.map(e=><option key={e}>{e}</option>)}
            </select>
          </div>
          <div className="field full"><label>Variedad</label>
            <select value={f.variedad} onChange={e=>set("variedad",e.target.value)} disabled={!f.especie}>
              <option value="">— Seleccionar variedad —</option>
              {(varMap[f.especie]||[]).map(v=><option key={v}>{v}</option>)}
            </select>
          </div>
          <div className="field"><label>Tipo de envase</label>
            <select value={f.tipo} onChange={e=>{set("tipo",e.target.value);set("pesoUnit",e.target.value==="bigbag"?800:25);}}>
              <option value="bigbag">BigBag</option>
              <option value="bolsa">Bolsa</option>
            </select>
          </div>
          <div className="field"><label>Tratamiento</label>
            <select value={f.tratada?"si":"no"} onChange={e=>set("tratada",e.target.value==="si")}>
              <option value="no">Sin tratar</option>
              <option value="si">Tratada</option>
            </select>
          </div>
          <div className="field"><label>Cantidad ({f.tipo==="bigbag"?"BigBags":"Bolsas"})</label>
            <input type="number" min="0" step="0.01" value={f.cantidad} onChange={e=>set("cantidad",e.target.value)} placeholder="Ej. 10.5"/>
          </div>
          <div className="field"><label>Peso unitario (kg)</label>
            <input type="number" min="1" value={f.pesoUnit} onChange={e=>set("pesoUnit",e.target.value)}/>
          </div>
          <div className="field"><label>PG — Poder Germinativo (%)</label>
            <input type="number" min="0" max="100" step="0.1" value={f.pg} onChange={e=>set("pg",e.target.value)} placeholder="Ej. 95"/>
          </div>
          <div className="field"><label>PMIL — Peso mil semillas (g)</label>
            <input type="number" min="0" step="0.1" value={f.pmil} onChange={e=>set("pmil",e.target.value)} placeholder="Ej. 145"/>
          </div>
          <div className="field"><label>Lote</label>
            <input type="text" value={f.lote} onChange={e=>set("lote",e.target.value)} placeholder="Ej. L-001"/>
          </div>
          <div className="field"><label>Ubicación (Pasillo/Rack)</label>
            <input type="text" value={f.ubicacion} onChange={e=>set("ubicacion",e.target.value)} placeholder="Ej. A-12, Estantería 3"/>
          </div>
          <div className="field"><label>Fecha</label>
            <input type="date" value={f.fecha} onChange={e=>set("fecha",e.target.value)}/>
          </div>
          <div className="field full"><label>Observaciones</label>
            <textarea rows={2} value={f.obs} onChange={e=>set("obs",e.target.value)} style={{resize:"vertical"}}/>
          </div>
        </div>
        <div className="modal-btns">
          <button className="btn-cancel" onClick={onClose}>Cancelar</button>
          <button className="btn-save" onClick={save}>Guardar</button>
        </div>
      </div>
    </div>
  );
}

/* ─── MODAL MOVIMIENTO ───────────────────────────────────────── */
function MoveModal({stock,item,onSave,onCreateOC,onClose}){
  const [op,setOp]=useState("egreso");
  const [delta,setDelta]=useState("");
  const [motivo,setMotivo]=useState("");
  const d=Number(delta)||0;
  const nueva=op==="egreso"?item.cantidad-d:item.cantidad+d;

  if(op==="oc"){
    return <OCModal stock={stock} item={item} onSave={onCreateOC} onClose={onClose}/>;
  }

  const save=()=>{
    if(!d||d<=0)return alert("Ingresá una cantidad válida.");
    if(nueva<0)return alert("El stock no puede quedar negativo.");
    onSave({item,op,delta:d,nueva,motivo});
  };
  return(
    <div className="overlay" onClick={e=>e.target===e.currentTarget&&onClose()}>
      <div className="modal modal-md">
        <h2>Movimiento de Stock</h2>
        <div className="move-info">
          <b>{item.variedad}</b> · {item.especie}<br/>
          Campaña: {item.campaña} · Lote: {item.lote||"—"}<br/>
          {item.tipo.toUpperCase()} · {item.tratada?"✅ Tratada":"○ Sin tratar"}
          {(item.pg||item.pmil)?<><br/>PG: {item.pg||"—"}% &nbsp;·&nbsp; PMIL: {item.pmil||"—"} g</>:null}<br/>
          Stock actual: <b style={{fontFamily:"Barlow Condensed",fontSize:"1.15rem"}}>{fmt(item.cantidad)}</b> unidades
          &nbsp;·&nbsp;<span style={{color:"var(--green)",fontFamily:"Barlow Condensed",fontWeight:700}}>{fmt(item.cantidad*item.pesoUnit)} kg</span>
        </div>
        <div className="move-row"><label>Operación</label>
          <select value={op} onChange={e=>setOp(e.target.value)}>
            <option value="egreso">⬇ Egreso / Retiro</option>
            <option value="ingreso">⬆ Ingreso / Ajuste +</option>
            <option value="oc">📋 Orden de Carga</option>
          </select>
        </div>
        <div className="move-row"><label>Cantidad</label>
          <input type="number" min="0" step="0.01" placeholder="Ej. 5.5" value={delta} onChange={e=>setDelta(e.target.value)}/>
          {d>0&&(
            <div className="move-preview">
              {op==="egreso"
                ?<span>Retirás <b>{fmt(d)}</b> uds ({fmt(d*item.pesoUnit)} kg) → quedan <b style={{color:nueva<=LOW?"var(--red)":"var(--green)"}}>{fmt(nueva)}</b></span>
                :<span>Sumás <b>{fmt(d)}</b> uds → nuevo stock: <b style={{color:"var(--green)"}}>{fmt(nueva)}</b></span>
              }
            </div>
          )}
        </div>
        <div className="move-row"><label>Motivo / Destino (opcional)</label>
          <input type="text" placeholder="Ej. Campo El Ombú" value={motivo} onChange={e=>setMotivo(e.target.value)}/>
        </div>
        <div className="modal-btns">
          <button className="btn-cancel" onClick={onClose}>Cancelar</button>
          <button className="btn-save" onClick={save}>Confirmar</button>
        </div>
      </div>
    </div>
  );
}

/* ─── MODAL ORDEN DE CARGA ───────────────────────────────────── */
function OCModal({stock,item,onSave,onClose,editOC}){
  const src=editOC||item;
  if(!src)return null;
  
  const [remito,setRemito]=useState(editOC?editOC.remito||"":"");
  const [nPedido,setNPedido]=useState(editOC?editOC.nPedido||"":"");
  const [destino,setDestino]=useState(editOC?editOC.destino||"":"");
  const [obs,setObs]=useState(editOC?editOC.obs||"":"");
  const [lotesSeleccionados,setLotesSeleccionados]=useState(editOC?editOC.lotes||[]:[]);

  const isEdit=!!editOC;
  
  // Filtrar items del stock que coincidan con especie, variedad, campaña, tipo, tratada
  const itemsCoincidentes=(stock||[]).filter(i=>
    i.especie===src.especie&&
    i.variedad===src.variedad&&
    i.campaña===src.campaña&&
    i.tipo===src.tipo&&
    i.tratada===src.tratada&&
    i.cantidad>0
  );

  const updateCantidadLote=(stockId,lote,ubicacion,nueva)=>{
    const cantidad=Number(nueva);
    setLotesSeleccionados(prev=>{
      const existe=prev.findIndex(l=>l.stockId===stockId&&l.lote===lote&&l.ubicacion===ubicacion);
      if(existe>=0){
        if(cantidad<=0){
          return prev.filter((l,i)=>i!==existe);
        }else{
          const copia=[...prev];
          copia[existe]={...copia[existe],cantidad};
          return copia;
        }
      }else if(cantidad>0){
        return [...prev,{stockId,lote,ubicacion,cantidad}];
      }
      return prev;
    });
  };

  const totalCantidad=lotesSeleccionados.reduce((s,l)=>s+l.cantidad,0);

  const save=()=>{
    if(lotesSeleccionados.length===0)return alert("Selecciona al menos un lote e ingresa cantidad.");
    if(lotesSeleccionados.some(l=>l.cantidad<=0))return alert("Todas las cantidades deben ser mayores a 0.");
    if(!destino.trim())return alert("Ingresá el destino o campo.");
    
    // Guardar con stockId para poder hacer egreso individual de cada lote
    const lotes=lotesSeleccionados.map(({stockId,lote,ubicacion,cantidad})=>({stockId,lote,ubicacion,cantidad}));
    onSave({lotes,destino,obs,remito,nPedido});
  };

  return(
    <div className="overlay" onClick={e=>e.target===e.currentTarget&&onClose()}>
      <div className="modal" style={{maxHeight:"85vh",overflowY:"auto"}}>
        <h2>{isEdit?`Editar ${editOC.numero}`:"Nueva Orden de Carga"}</h2>
        <div className="move-info">
          <b>{src.variedad}</b> · {src.especie} · Campaña {src.campaña}<br/>
          {src.tipo==="bigbag"?"BigBag":"Bolsa"} · {src.tratada?"✅ Tratada":"○ Sin tratar"}
          {(src.pg||src.pmil)?<><br/>PG: <b>{src.pg||"—"}%</b> &nbsp;·&nbsp; PMIL: <b>{src.pmil||"—"} g</b></>:null}
        </div>

        <div style={{marginBottom:16,padding:12,background:"#f9f3e6",borderRadius:8,borderLeft:"4px solid var(--accent)"}}>
          <label style={{display:"block",marginBottom:12,fontWeight:700,fontSize:".95rem"}}>📦 Selecciona lotes para cargar:</label>
          
          {itemsCoincidentes.length===0?(
            <div style={{padding:10,background:"#fff",borderRadius:6,color:"var(--muted)",textAlign:"center"}}>
              No hay lotes disponibles de este tipo
            </div>
          ):(
            <div style={{display:"flex",flexDirection:"column",gap:8}}>
              {itemsCoincidentes.map(it=>{
                const sel=lotesSeleccionados.find(l=>l.stockId===it.id&&l.lote===it.lote&&l.ubicacion===it.ubicacion);
                return(
                  <div key={it.id} style={{background:"#fff",border:"1px solid var(--border)",borderRadius:6,padding:10}}>
                    <div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start",gap:10}}>
                      <div>
                        <b style={{display:"block",marginBottom:4}}>📍 Lote: {it.lote}</b>
                        <span style={{fontSize:".8rem",color:"var(--muted)"}}>Ubicación: {it.ubicacion||"—"}</span><br/>
                        <span style={{fontSize:".75rem",color:"var(--muted)"}}>Stock disponible: <b>{fmt(it.cantidad)}</b> {it.tipo==="bigbag"?"BB":"bolsas"} ({fmt(it.cantidad*it.pesoUnit)} kg)</span>
                      </div>
                      <input 
                        type="number" 
                        min="0" 
                        step="0.01"
                        max={it.cantidad}
                        value={sel?.cantidad||0}
                        onChange={e=>updateCantidadLote(it.id,it.lote,it.ubicacion,e.target.value)}
                        placeholder="Cantidad"
                        style={{width:90,padding:"6px 8px",border:"1.5px solid var(--border)",borderRadius:4,fontSize:".9rem",fontWeight:600}}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        <div className="form-grid">
          <div className="field"><label>Total a cargar ({src.tipo==="bigbag"?"BigBags":"Bolsas"})</label>
            <input type="text" value={fmt(totalCantidad)} disabled style={{background:"#f0f3f8",fontWeight:700,color:"var(--blue)"}}/>
          </div>
          <div className="field"><label>Kg totales</label>
            <input type="text" value={fmt(totalCantidad*src.pesoUnit)+" kg"} disabled style={{background:"#f0f3f8",fontWeight:700,color:"var(--green)"}}/>
          </div>
          <div className="field"><label>🎫 Número de Remito</label>
            <input type="text" value={remito} onChange={e=>setRemito(e.target.value)} placeholder="Ej. REM-2024-001"/>
          </div>
          <div className="field"><label>📦 N° Pedido de Venta</label>
            <input type="text" value={nPedido} onChange={e=>setNPedido(e.target.value)} placeholder="Ej. PED-2024-001"/>
          </div>
          <div className="field full"><label>Destino / Campo *</label>
            <input type="text" value={destino} onChange={e=>setDestino(e.target.value)} placeholder="Ej. Campo El Ombú, Ruta 8 km 200"/>
          </div>
          <div className="field full"><label>Observaciones</label>
            <textarea rows={2} value={obs} onChange={e=>setObs(e.target.value)} style={{resize:"vertical"}} placeholder="Notas adicionales..."/>
          </div>
        </div>

        {lotesSeleccionados.length>0&&(
          <div style={{marginBottom:12,padding:10,background:"#e6f5ec",borderRadius:6,fontSize:".85rem"}}>
            <b>✓ Lotes a cargar:</b> {lotesSeleccionados.length} | <b>Total:</b> {fmt(totalCantidad)} {src.tipo==="bigbag"?"BB":"bolsas"} = {fmt(totalCantidad*src.pesoUnit)} kg
          </div>
        )}

        <div className="modal-btns">
          <button className="btn-cancel" onClick={onClose}>Cancelar</button>
          <button className="btn-save" onClick={save}>{isEdit?"Guardar cambios":"Crear Orden"}</button>
        </div>
      </div>
    </div>
  );
}

/* ─── APP PRINCIPAL ──────────────────────────────────────────── */
function App(){
  const [loggedIn,setLoggedIn]=useState(()=>!!sessionStorage.getItem("ss:session"));
  const [stock,setStock]       =useState(()=>lsGet("ss:stock",STOCK_INIT));
  const [historial,setHistorial]=useState(()=>lsGet("ss:historial",[]));
  const [ordenes,setOrdenes]   =useState(()=>lsGet("ss:ordenes",[]));
  const [campañas,setCampañas] =useState(()=>lsGet("ss:campañas",CAMPAÑAS_DEF));
  const [especies,setEspecies] =useState(()=>lsGet("ss:especies",ESPECIES_DEF));
  const [varMap,setVarMap]     =useState(()=>lsGet("ss:varMap",VARS_DEF));
  const [saveMsg,setSaveMsg]   =useState("");

  const [tab,setTab]=useState("resumen");
  const [modal,setModal]=useState(null);
  const [search,setSearch]=useState("");
  const [fCamp,setFCamp]=useState("todas");
  const [fEsp,setFEsp]=useState("todas");
  const [fTipo,setFTipo]=useState("todos");
  const [fTrat,setFTrat]=useState("todos");
  const [rCamp,setRCamp]=useState("todas");
  const [rEsp,setREsp]=useState("todas");
  const [hCamp,setHCamp]=useState("todas");
  const [hOp,setHOp]=useState("todos");
  const [ocFCamp,setOcFCamp]=useState("todas");
  const [ocFStatus,setOcFStatus]=useState("todos");
  const [ocSearch,setOcSearch]=useState("");
  const [selOCs,setSelOCs]=useState(new Set());
  const [newCamp,setNewCamp]=useState("");
  const [newEsp,setNewEsp]=useState("");
  const [newVar,setNewVar]=useState("");
  const [selAdmEsp,setSelAdmEsp]=useState(ESPECIES_DEF[0]);
  const [newPass,setNewPass]=useState("");
  const [newPass2,setNewPass2]=useState("");

  const flash=()=>{setSaveMsg("saving");setTimeout(()=>setSaveMsg("ok"),400);setTimeout(()=>setSaveMsg(""),2500);};
  const upd=(set,key)=>fn=>{set(p=>{const n=fn(p);lsSet(key,n);flash();return n;});};
  const updStock=upd(setStock,"ss:stock");
  const updHist=upd(setHistorial,"ss:historial");
  const updOrdenes=upd(setOrdenes,"ss:ordenes");
  const updCamps=upd(setCampañas,"ss:campañas");
  const updEsp=upd(setEspecies,"ss:especies");
  const updVars=upd(setVarMap,"ss:varMap");

  const nextId=()=>Math.max(0,...stock.map(i=>i.id))+1;
  const nextHid=()=>Math.max(0,...historial.map(h=>h.id),0)+1;
  const nextOCId=()=>Math.max(0,...ordenes.map(o=>o.id),0)+1;
  const nextOCNum=()=>Math.max(0,...ordenes.map(o=>parseInt(o.numero.replace("OC-",""))||0))+1;

  const handleSave=form=>{
    if(form.id)updStock(s=>s.map(i=>i.id===form.id?form:i));
    else updStock(s=>[{...form,id:nextId()},...s]);
    setModal(null);
  };
  const handleMove=({item,op,delta,nueva,motivo})=>{
    updStock(s=>s.map(i=>i.id===item.id?{...item,cantidad:nueva}:i));
    updHist(h=>[{id:nextHid(),fecha:nowStr(),campaña:item.campaña,especie:item.especie,variedad:item.variedad,tipo:item.tipo,tratada:item.tratada,lote:item.lote,op,delta,stockPrev:item.cantidad,stockPost:nueva,kgMovidos:delta*item.pesoUnit,motivo},...h]);
    setModal(null);
  };
  const handleDel=id=>{if(!window.confirm("¿Eliminar este registro?"))return;updStock(s=>s.filter(i=>i.id!==id));};

  const handleCreateOC=({lotes,destino,obs,remito,nPedido})=>{
    const item=modal.item;
    const num=nextOCNum();
    updOrdenes(os=>[...os,{
      id:nextOCId(),numero:fmtOCNum(num),fecha:nowStr(),
      campaña:item.campaña,especie:item.especie,variedad:item.variedad,
      tipo:item.tipo,tratada:item.tratada,pesoUnit:item.pesoUnit,
      pg:item.pg,pmil:item.pmil,lotes,destino,obs,remito,nPedido,
      estado:"pendiente",fechaDespachada:null,stockId:item.id,
    }]);
    setModal(null);
    setTab("ordenes");
  };
  const handleEditOC=({lotes,destino,obs,remito,nPedido})=>{
    updOrdenes(os=>os.map(o=>o.id===modal.oc.id?{...o,lotes,destino,obs,remito,nPedido}:o));
    setModal(null);
  };
  const handleDespacharOC=oc=>{
    const totalCant=oc.lotes.reduce((s,l)=>s+l.cantidad,0);
    if(!window.confirm(`¿Despachar ${oc.numero}? Se generará un egreso de ${fmt(totalCant)} unidades de ${oc.variedad}.`))return;
    
    // Verificar y procesar CADA lote individualmente
    let todoBien=true;
    const updatesStock={};
    
    // Primero verificar que hay stock suficiente para todos los lotes
    for(const lote of oc.lotes){
      const si=stock.find(i=>i.id===lote.stockId);
      if(!si){
        alert(`No se encontró el registro del lote ${lote.lote}`);
        todoBien=false;
        break;
      }
      if(si.cantidad<lote.cantidad){
        if(!window.confirm(`Stock de ${lote.lote} (${si.cantidad}) es menor a lo que intenta cargar (${lote.cantidad}). ¿Continuar?`)){
          todoBien=false;
          break;
        }
      }
      updatesStock[lote.stockId]=(updatesStock[lote.stockId]||0)+lote.cantidad;
    }
    
    if(!todoBien)return;
    
    // Actualizar stock de cada lote
    updStock(s=>s.map(item=>{
      if(updatesStock[item.id]){
        const delta=updatesStock[item.id];
        const nueva=Math.max(0,item.cantidad-delta);
        return {...item,cantidad:nueva};
      }
      return item;
    }));
    
    // Registrar historial para cada lote
    const ahora=nowStr();
    const histEntries=oc.lotes.map(lote=>{
      const si=stock.find(i=>i.id===lote.stockId);
      if(!si)return null;
      const delta=Math.min(lote.cantidad,si.cantidad);
      const stockPrev=si.cantidad;
      const stockPost=Math.max(0,si.cantidad-delta);
      return {
        id:nextHid(),
        fecha:ahora,
        campaña:oc.campaña,
        especie:oc.especie,
        variedad:oc.variedad,
        tipo:oc.tipo,
        tratada:oc.tratada,
        lote:lote.lote,
        op:"egreso",
        delta,
        stockPrev,
        stockPost,
        kgMovidos:delta*oc.pesoUnit,
        remito:oc.remito||"—",
        nPedido:oc.nPedido||"—",
        motivo:`${oc.numero} - ${lote.ubicacion}${oc.destino?" · "+oc.destino:""}`
      };
    }).filter(e=>e);
    
    updHist(h=>[...histEntries,...h]);
    
    // Marcar OC como despachada
    updOrdenes(os=>os.map(o=>o.id===oc.id?{...o,estado:"despachada",fechaDespachada:ahora}:o));
  };
  const handleDelOC=id=>{if(!window.confirm("¿Eliminar esta orden?"))return;updOrdenes(os=>os.filter(o=>o.id!==id));};

  const toggleSelOC=id=>setSelOCs(prev=>{const n=new Set(prev);n.has(id)?n.delete(id):n.add(id);return n;});
  const toggleAllOCs=arr=>{
    if(arr.every(o=>selOCs.has(o.id)))setSelOCs(new Set());
    else setSelOCs(new Set(arr.map(o=>o.id)));
  };

  const handleChangePass=()=>{
    if(!newPass||newPass.length<4)return alert("La clave debe tener al menos 4 caracteres.");
    if(newPass!==newPass2)return alert("Las claves no coinciden.");
    lsSet("ss:password",newPass);
    setNewPass("");setNewPass2("");
    alert("✓ Clave actualizada correctamente.");
  };
  const resetAll=()=>{
    if(!window.confirm("¿Borrar TODOS los datos y volver al estado inicial?"))return;
    updStock(()=>STOCK_INIT);updHist(()=>[]);updOrdenes(()=>[]);
    updCamps(()=>CAMPAÑAS_DEF);updEsp(()=>ESPECIES_DEF);updVars(()=>VARS_DEF);
  };

  /* Filtros tabla */
  const filtered=useMemo(()=>stock.filter(i=>{
    if(fCamp!=="todas"&&i.campaña!==fCamp)return false;
    if(fEsp!=="todas"&&i.especie!==fEsp)return false;
    if(fTipo!=="todos"&&i.tipo!==fTipo)return false;
    if(fTrat==="tratada"&&!i.tratada)return false;
    if(fTrat==="sintratar"&&i.tratada)return false;
    const hay=[i.variedad,i.especie,i.lote,i.campaña,i.obs].join(" ").toLowerCase();
    if(search&&!hay.includes(search.toLowerCase()))return false;
    return true;
  }),[stock,fCamp,fEsp,fTipo,fTrat,search]);

  /* Resumen agrupado */
  const resumen=useMemo(()=>{
    const rs=stock.filter(i=>(rCamp==="todas"||i.campaña===rCamp)&&(rEsp==="todas"||i.especie===rEsp));
    const map={};
    rs.forEach(i=>{
      if(!map[i.campaña])map[i.campaña]={};
      if(!map[i.campaña][i.especie])map[i.campaña][i.especie]={};
      const key=`${i.variedad}|||${i.tipo}|||${i.tratada}`;
      if(!map[i.campaña][i.especie][key])map[i.campaña][i.especie][key]={...i,_uds:0,_kgs:0};
      map[i.campaña][i.especie][key]._uds+=i.cantidad;
      map[i.campaña][i.especie][key]._kgs+=i.cantidad*i.pesoUnit;
    });
    return map;
  },[stock,rCamp,rEsp]);

  /* Historial filtrado */
  const filteredHist=useMemo(()=>historial.filter(h=>(hCamp==="todas"||h.campaña===hCamp)&&(hOp==="todos"||h.op===hOp)),[historial,hCamp,hOp]);

  /* Órdenes filtradas */
  const filteredOCs=useMemo(()=>ordenes.filter(o=>{
    if(ocFCamp!=="todas"&&o.campaña!==ocFCamp)return false;
    if(ocFStatus!=="todos"&&o.estado!==ocFStatus)return false;
    if(ocSearch){const hay=[o.numero,o.remito,o.nPedido,o.variedad,o.especie,...o.lotes.map(l=>l.lote),o.destino,o.obs].join(" ").toLowerCase();if(!hay.includes(ocSearch.toLowerCase()))return false;}
    return true;
  }),[ordenes,ocFCamp,ocFStatus,ocSearch]);

  /* KPIs */
  const totalBB=stock.filter(i=>i.tipo==="bigbag").reduce((s,i)=>s+i.cantidad,0);
  const totalBo=stock.filter(i=>i.tipo==="bolsa").reduce((s,i)=>s+i.cantidad,0);
  const totalKg=stock.reduce((s,i)=>s+i.cantidad*i.pesoUnit,0);
  const totalVars=new Set(stock.map(i=>i.especie+i.variedad)).size;
  const lowCount=stock.filter(i=>i.cantidad<=LOW).length;
  const ocPend=ordenes.filter(o=>o.estado==="pendiente").length;

  /* CSV */
  const exportCSV=()=>{
    const rows=[["Campaña","Especie","Variedad","Tipo","Tratada","Cantidad","Kg Totales","PG (%)","PMIL (g)","Lote","Fecha","Observaciones"]];
    filtered.forEach(i=>rows.push([i.campaña,i.especie,i.variedad,i.tipo==="bigbag"?"BigBag":"Bolsa",i.tratada?"Sí":"No",i.cantidad,i.cantidad*i.pesoUnit,i.pg||"",i.pmil||"",i.lote,i.fecha,i.obs||""]));
    downloadCSV(rows,`stock_semillas_${today()}.csv`);
  };
  const exportHistCSV=()=>{
    const rows=[["Fecha","Campaña","Especie","Variedad","Tipo","Lote","Remito","N° Pedido","Operación","Cantidad","Kg Movidos","Stock Anterior","Stock Nuevo","Motivo"]];
    filteredHist.forEach(h=>rows.push([h.fecha,h.campaña,h.especie,h.variedad,h.tipo==="bigbag"?"BigBag":"Bolsa",h.lote||"",h.remito||"",h.nPedido||"",h.op==="egreso"?"Egreso":"Ingreso",h.delta,h.kgMovidos,h.stockPrev,h.stockPost,h.motivo||""]));
    downloadCSV(rows,`historial_movimientos_${today()}.csv`);
  };
  const exportOCsCSV=()=>{
    const rows=[["N° OC","Remito","N° Pedido","Fecha","Campaña","Especie","Variedad","Tipo","Tratada","Cantidad","Kg","PG (%)","PMIL (g)","Lotes","Ubicaciones","Destino","Observaciones","Estado","Fecha Despacho"]];
    filteredOCs.forEach(o=>{
      const lotes=o.lotes.map(l=>l.lote).join("; ");
      const ubicaciones=o.lotes.map(l=>l.ubicacion).join("; ");
      const totalCant=o.lotes.reduce((s,l)=>s+l.cantidad,0);
      rows.push([o.numero,o.remito||"",o.nPedido||"",o.fecha,o.campaña,o.especie,o.variedad,o.tipo==="bigbag"?"BigBag":"Bolsa",o.tratada?"Sí":"No",totalCant,totalCant*o.pesoUnit,o.pg||"",o.pmil||"",lotes,ubicaciones,o.destino||"",o.obs||"",o.estado==="pendiente"?"Pendiente":"Despachada",o.fechaDespachada||""]);
    });
    downloadCSV(rows,`ordenes_carga_${today()}.csv`);
  };

  /* Admin */
  const addCampaña=()=>{const v=newCamp.trim();if(!v||campañas.includes(v))return;updCamps(c=>[...c,v]);setNewCamp("");};
  const delCampaña=c=>updCamps(p=>p.filter(x=>x!==c));
  const addEspecie=()=>{const v=newEsp.trim();if(!v||especies.includes(v))return;updEsp(e=>[...e,v]);updVars(m=>({...m,[v]:[]}));setNewEsp("");};
  const delEspecie=e=>{updEsp(p=>p.filter(x=>x!==e));updVars(m=>{const c={...m};delete c[e];return c;});};
  const addVariedad=()=>{const v=newVar.trim();if(!v)return;updVars(m=>({...m,[selAdmEsp]:[...(m[selAdmEsp]||[]).filter(x=>x!==v),v]}));setNewVar("");};
  const delVariedad=(esp,vr)=>updVars(m=>({...m,[esp]:(m[esp]||[]).filter(x=>x!==vr)}));

  if(!loggedIn)return <LoginScreen onLogin={()=>{sessionStorage.setItem("ss:session","1");setLoggedIn(true);}}/>;

  const selOCsList=filteredOCs.filter(o=>selOCs.has(o.id));
  const allSelInView=filteredOCs.length>0&&filteredOCs.every(o=>selOCs.has(o.id));

  return(
    <div className="app">

      {/* HEADER */}
      <div className="hdr no-print">
        <div className="hdr-left">
          <img src={LOGO_SRC} alt="La Clementina" className="hdr-logo"/>
          <div>
            <h1>Planta de Semillas · <span>Stock</span></h1>
            <p>Control de producción · BigBag & Bolsa · Por campaña y variedad</p>
          </div>
        </div>
        <div className="hdr-right">
          <div className={`save-ind${saveMsg==="saving"?" save-ing":saveMsg==="ok"?" save-ok":""}`}>
            {saveMsg==="saving"?"💾 Guardando...":saveMsg==="ok"?"✓ Guardado":""}
          </div>
          <div className="hdr-tabs">
            <button className={`tab${tab==="resumen"?" active":""}`} onClick={()=>setTab("resumen")}>📋 Resumen</button>
            <button className={`tab${tab==="tabla"?" active":""}`} onClick={()=>setTab("tabla")}>📦 Tabla</button>
            <button className={`tab${tab==="historial"?" active":""}`} onClick={()=>setTab("historial")}>
              🕘 Historial{historial.length>0?` (${historial.length})`:""}
            </button>
            <button className={`tab${tab==="ordenes"?" active":""}`} onClick={()=>setTab("ordenes")}>
              📋 Órd. de Carga{ocPend>0?` (${ocPend})`:""}
            </button>
            <button className={`tab${tab==="admin"?" active":""}`} onClick={()=>setTab("admin")}>⚙ Catálogos</button>
          </div>
        </div>
      </div>

      {/* KPIs */}
      <div className="kpi-strip no-print">
        <div className="kpi"><div className="kpi-val c-or">{fmt(totalBB)}</div><div className="kpi-lbl">BigBags</div></div>
        <div className="kpi"><div className="kpi-val c-bl">{fmt(totalBo)}</div><div className="kpi-lbl">Bolsas</div></div>
        <div className="kpi"><div className="kpi-val c-gr">{fmt(Math.round(totalKg/1000))} t</div><div className="kpi-lbl">Toneladas</div></div>
        <div className="kpi"><div className="kpi-val c-pu">{totalVars}</div><div className="kpi-lbl">Variedades</div></div>
        <div className="kpi"><div className="kpi-val" style={{color:lowCount>0?"var(--red)":"var(--muted)"}}>{lowCount}</div><div className="kpi-lbl">⚠ Stock bajo</div></div>
        <div className="kpi"><div className="kpi-val" style={{color:ocPend>0?"var(--purple)":"var(--muted)"}}>{ocPend}</div><div className="kpi-lbl">OC Pendientes</div></div>
      </div>

      {/* ── RESUMEN ── */}
      {tab==="resumen"&&(
        <div className="stock-view">
          <div className="sv-filters no-print">
            <select className="sel" value={rCamp} onChange={e=>setRCamp(e.target.value)}>
              <option value="todas">Todas las campañas</option>
              {campañas.map(c=><option key={c}>{c}</option>)}
            </select>
            <select className="sel" value={rEsp} onChange={e=>setREsp(e.target.value)}>
              <option value="todas">Todas las especies</option>
              {especies.map(e=><option key={e}>{e}</option>)}
            </select>
            <button className="btn btn-ol ph" onClick={()=>window.print()}>🖨 Imprimir / PDF</button>
          </div>
          {Object.keys(resumen).length===0&&<div className="no-data">Sin stock para mostrar.</div>}
          {Object.entries(resumen).sort().map(([camp,espMap])=>{
            const campKg=Object.values(espMap).flatMap(v=>Object.values(v)).reduce((s,d)=>s+d._kgs,0);
            return(
              <div className="camp-block" key={camp}>
                <div className="camp-title">
                  <span>📅 Campaña {camp}</span>
                  <span className="camp-sub">{fmt(Math.round(campKg/1000))} t totales</span>
                </div>
                {Object.entries(espMap).sort().map(([esp,varKeys])=>(
                  <div className="esp-block" key={esp}>
                    <div className="esp-title">🌱 {esp}</div>
                    <div className="sv-grid">
                      {Object.entries(varKeys).map(([key,d])=>{
                        const [variedad,tipo,tratadaStr]=key.split("|||");
                        const tratada=tratadaStr==="true";
                        const isLow=d._uds<=LOW;
                        return(
                          <div className="sv-card" key={key} style={{borderTopColor:isLow?"var(--red)":tipo==="bigbag"?"var(--accent)":"var(--blue)"}}>
                            <div className="sv-head">
                              <div className="sv-variedad">{variedad}</div>
                              <div style={{display:"flex",gap:3,flexWrap:"wrap",justifyContent:"flex-end"}}>
                                <span className={`badge ${tipo==="bigbag"?"bb":"bo"}`}>{tipo==="bigbag"?"🏗 BB":"🎒 Bolsa"}</span>
                                {isLow&&<span className="badge low">⚠ Bajo</span>}
                              </div>
                            </div>
                            <div className="sv-row"><span className="sv-label">Tratamiento</span>
                              <span className={`badge ${tratada?"tr-b":"st-b"}`}>{tratada?"✅ Tratada":"○ Sin tratar"}</span>
                            </div>
                            <div className="sv-row"><span className="sv-label">Unidades</span>
                              <span className="sv-val" style={{color:isLow?"var(--red)":"var(--accent)"}}>{fmt(d._uds)}</span>
                            </div>
                            <div className="sv-row"><span className="sv-label">Kilogramos</span>
                              <span className="sv-val c-gr">{fmt(d._kgs)} kg</span>
                            </div>
                            <div className="sv-row"><span className="sv-label">Toneladas</span>
                              <span className="sv-val" style={{color:"var(--muted)"}}>{(d._kgs/1000).toFixed(2)} t</span>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                ))}
              </div>
            );
          })}
        </div>
      )}

      {/* ── TABLA ── */}
      {tab==="tabla"&&<>
        <div className="toolbar no-print">
          <div className="search-wrap">
            <span className="search-icon">🔍</span>
            <input className="search-inp" placeholder="Buscar variedad, lote, especie…" value={search} onChange={e=>setSearch(e.target.value)}/>
          </div>
          <select className="sel" value={fCamp} onChange={e=>setFCamp(e.target.value)}>
            <option value="todas">Todas las campañas</option>
            {campañas.map(c=><option key={c}>{c}</option>)}
          </select>
          <select className="sel" value={fEsp} onChange={e=>setFEsp(e.target.value)}>
            <option value="todas">Todas las especies</option>
            {especies.map(e=><option key={e}>{e}</option>)}
          </select>
          <select className="sel" value={fTipo} onChange={e=>setFTipo(e.target.value)}>
            <option value="todos">BB + Bolsa</option>
            <option value="bigbag">BigBag</option>
            <option value="bolsa">Bolsa</option>
          </select>
          <select className="sel" value={fTrat} onChange={e=>setFTrat(e.target.value)}>
            <option value="todos">Tratada + S/T</option>
            <option value="tratada">Solo Tratada</option>
            <option value="sintratar">Sin tratar</option>
          </select>
          <button className="btn btn-ol ph" onClick={()=>window.print()}>🖨 Imprimir</button>
          <button className="btn btn-ol gnh" onClick={exportCSV}>⬇ Excel/CSV</button>
          <button className="btn btn-add" onClick={()=>setModal({mode:"new"})}>＋ Nuevo</button>
        </div>
        <div style={{display:"none"}} className="print-title">
          Stock de Semillas — Planta de Producción &nbsp;·&nbsp;
          <span style={{fontWeight:400,fontSize:".82rem"}}>Impreso el {printDate()}</span>
        </div>
        <div className="table-wrap">
          <table>
            <thead><tr>
              <th>Campaña</th><th>Especie</th><th>Variedad</th>
              <th>Envase</th><th>Tratamiento</th>
              <th>Cantidad</th><th>Kg totales</th>
              <th>PG %</th><th>PMIL g</th>
              <th>Lote</th><th>Fecha</th><th>Obs.</th>
              <th className="no-print">Acciones</th>
            </tr></thead>
            <tbody>
              {filtered.length===0
                ?<tr><td colSpan="13" style={{textAlign:"center",color:"var(--muted)",padding:36}}>Sin registros</td></tr>
                :filtered.map(item=>(
                <tr key={item.id} className={item.cantidad<=LOW?"low-row":""}>
                  <td><span className="cell-muted">{item.campaña}</span></td>
                  <td style={{fontWeight:500}}>{item.especie}</td>
                  <td style={{fontWeight:600}}>{item.variedad}{item.cantidad<=LOW&&<span className="badge low" style={{marginLeft:5,fontSize:".62rem"}}>⚠</span>}</td>
                  <td><span className={`badge ${item.tipo==="bigbag"?"bb":"bo"}`}>{item.tipo==="bigbag"?"BigBag":"Bolsa"}</span></td>
                  <td><span className={`badge ${item.tratada?"tr-b":"st-b"}`}>{item.tratada?"Tratada":"Sin tratar"}</span></td>
                  <td><span className="qty-big" style={{color:item.cantidad<=LOW?"var(--red)":item.tipo==="bigbag"?"var(--accent)":"var(--blue)"}}>{fmt(item.cantidad)}</span></td>
                  <td style={{color:"var(--green)",fontFamily:"Barlow Condensed",fontWeight:700}}>{fmt(item.cantidad*item.pesoUnit)} kg</td>
                  <td style={{fontFamily:"Barlow Condensed",fontWeight:700,color:"var(--blue)"}}>{item.pg!=null&&item.pg!==""?item.pg+"%":"—"}</td>
                  <td style={{fontFamily:"Barlow Condensed",fontWeight:700,color:"var(--purple)"}}>{item.pmil!=null&&item.pmil!==""?item.pmil+" g":"—"}</td>
                  <td><span className="cell-muted">{item.lote||"—"}</span></td>
                  <td><span className="cell-muted">{item.fecha}</span></td>
                  <td style={{fontSize:".73rem",color:"var(--muted)",maxWidth:110,overflow:"hidden",textOverflow:"ellipsis",whiteSpace:"nowrap"}}>{item.obs||"—"}</td>
                  <td className="no-print">
                    <button className="action-btn" onClick={()=>setModal({mode:"move",item})}>⇄ Mover</button>
                    <button className="action-btn" onClick={()=>setModal({mode:"edit",item})}>✏</button>
                    <button className="action-btn del" onClick={()=>handleDel(item.id)}>✕</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div style={{padding:"9px 16px",display:"flex",justifyContent:"space-between",alignItems:"center",flexWrap:"wrap",gap:8,color:"var(--muted)",fontSize:".76rem",background:"#fff",borderTop:"1px solid var(--border)"}}>
          <span>{filtered.length} registro{filtered.length!==1?"s":""}</span>
          <span style={{color:"var(--green)",fontFamily:"Barlow Condensed",fontWeight:700,fontSize:"1rem"}}>
            {fmt(filtered.reduce((s,i)=>s+i.cantidad*i.pesoUnit,0))} kg totales filtrados
          </span>
        </div>
      </>}

      {/* ── HISTORIAL ── */}
      {tab==="historial"&&(
        <div className="hist-view">
          <div className="hist-filters no-print">
            <select className="sel" value={hCamp} onChange={e=>setHCamp(e.target.value)}>
              <option value="todas">Todas las campañas</option>
              {campañas.map(c=><option key={c}>{c}</option>)}
            </select>
            <select className="sel" value={hOp} onChange={e=>setHOp(e.target.value)}>
              <option value="todos">Egresos + Ingresos</option>
              <option value="egreso">Solo Egresos</option>
              <option value="ingreso">Solo Ingresos</option>
            </select>
            <button className="btn btn-ol ph" onClick={()=>window.print()}>🖨 Imprimir</button>
            {historial.length>0&&<button className="btn btn-ol gnh" onClick={exportHistCSV}>⬇ Excel/CSV</button>}
          </div>
          <div style={{display:"none"}} className="print-title">
            Historial de Movimientos &nbsp;·&nbsp; <span style={{fontWeight:400,fontSize:".82rem"}}>Impreso el {printDate()}</span>
          </div>
          {filteredHist.length===0
            ?<div className="no-data">{historial.length===0?"Sin movimientos todavía. Usá ⇄ Mover en Tabla para registrar.":"Sin movimientos para los filtros seleccionados."}</div>
            :<>
              <div className="table-wrap">
                <table>
                  <thead><tr>
                    <th>Fecha y hora</th><th>Campaña</th><th>Especie</th><th>Variedad</th>
                    <th>Envase</th><th>Lote</th><th>🎫 Remito</th><th>📦 Pedido</th><th>Operación</th>
                    <th>Cantidad</th><th>Kg movidos</th>
                    <th>Stock ant.</th><th>Stock nuevo</th><th>Motivo / Destino</th>
                  </tr></thead>
                  <tbody>
                    {filteredHist.map(h=>(
                      <tr key={h.id}>
                        <td><span className="cell-muted">{h.fecha}</span></td>
                        <td><span className="cell-muted">{h.campaña}</span></td>
                        <td>{h.especie}</td>
                        <td style={{fontWeight:600}}>{h.variedad}</td>
                        <td><span className={`badge ${h.tipo==="bigbag"?"bb":"bo"}`}>{h.tipo==="bigbag"?"BB":"Bolsa"}</span></td>
                        <td><span className="cell-muted">{h.lote||"—"}</span></td>
                        <td style={{fontFamily:"Barlow Condensed",fontWeight:600,color:"var(--blue)"}}>{h.remito||"—"}</td>
                        <td style={{fontFamily:"Barlow Condensed",fontWeight:600,color:"var(--blue)"}}>{h.nPedido||"—"}</td>
                        <td><span className={`badge ${h.op==="egreso"?"egr":"ing"}`}>{h.op==="egreso"?"⬇ Egreso":"⬆ Ingreso"}</span></td>
                        <td><span className={h.op==="egreso"?"dneg":"dpos"}>{h.op==="egreso"?"-":"+"}{fmt(h.delta)}</span></td>
                        <td style={{fontFamily:"Barlow Condensed",fontWeight:700,color:h.op==="egreso"?"var(--red)":"var(--green)"}}>
                          {h.op==="egreso"?"-":"+"}{fmt(h.kgMovidos)} kg
                        </td>
                        <td><span className="cell-muted">{fmt(h.stockPrev)}</span></td>
                        <td><span style={{fontFamily:"Barlow Condensed",fontWeight:700,color:h.stockPost<=LOW?"var(--red)":"var(--text)"}}>{fmt(h.stockPost)}{h.stockPost<=LOW?" ⚠":""}</span></td>
                        <td style={{fontSize:".76rem",color:"var(--muted)",maxWidth:150}}>{h.motivo||"—"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div style={{padding:"9px 16px",display:"flex",gap:20,flexWrap:"wrap",color:"var(--muted)",fontSize:".76rem",background:"#fff",borderTop:"1px solid var(--border)"}}>
                <span>Egresos: <b style={{color:"var(--red)",fontFamily:"Barlow Condensed",fontSize:"1rem"}}>{fmt(filteredHist.filter(h=>h.op==="egreso").reduce((s,h)=>s+h.kgMovidos,0))} kg</b></span>
                <span>Ingresos: <b style={{color:"var(--green)",fontFamily:"Barlow Condensed",fontSize:"1rem"}}>{fmt(filteredHist.filter(h=>h.op==="ingreso").reduce((s,h)=>s+h.kgMovidos,0))} kg</b></span>
                <span>{filteredHist.length} movimiento{filteredHist.length!==1?"s":""}</span>
              </div>
            </>
          }
        </div>
      )}

      {/* ── ÓRDENES DE CARGA ── */}
      {tab==="ordenes"&&(
        <div className="oc-view">
          <div className="oc-filters">
            <select className="sel" value={ocFCamp} onChange={e=>setOcFCamp(e.target.value)}>
              <option value="todas">Todas las campañas</option>
              {campañas.map(c=><option key={c}>{c}</option>)}
            </select>
            <select className="sel" value={ocFStatus} onChange={e=>setOcFStatus(e.target.value)}>
              <option value="todos">Todas</option>
              <option value="pendiente">Pendientes</option>
              <option value="despachada">Despachadas</option>
            </select>
            <div className="search-wrap" style={{flex:"none",minWidth:160}}>
              <span className="search-icon">🔍</span>
              <input className="search-inp" placeholder="Buscar OC, variedad, destino…" value={ocSearch} onChange={e=>setOcSearch(e.target.value)}/>
            </div>
            {selOCsList.length>0&&(
              <button className="btn btn-ol oc" onClick={()=>printOCWindow(selOCsList)}>
                🖨 Imprimir seleccionadas ({selOCsList.length})
              </button>
            )}
            {filteredOCs.length>0&&<button className="btn btn-ol gnh" onClick={exportOCsCSV}>⬇ Excel/CSV</button>}
          </div>

          {filteredOCs.length===0
            ?<div className="no-data">{ordenes.length===0?"Sin órdenes todavía. Creá una desde Tabla → ⇄ Mover → Orden de Carga.":"Sin órdenes para los filtros seleccionados."}</div>
            :<>
              <div className="table-wrap">
                <table>
                  <thead><tr>
                    <th style={{width:32}}>
                      <input type="checkbox" checked={allSelInView} onChange={()=>toggleAllOCs(filteredOCs)} style={{cursor:"pointer"}}/>
                    </th>
                    <th>N° OC</th><th>Remito</th><th>📦 Pedido</th><th>Fecha</th><th>Campaña</th><th>Especie</th><th>Variedad</th>
                    <th>Envase</th><th>Tratamiento</th><th>Cant.</th><th>Kg</th>
                    <th>PG %</th><th>PMIL g</th><th>Lotes cargados</th><th>Destino / Campo</th><th>Observaciones</th>
                    <th>Estado</th><th>Fecha despacho</th><th className="no-print">Acciones</th>
                  </tr></thead>
                  <tbody>
                    {filteredOCs.map(o=>(
                      <tr key={o.id} style={{background:selOCs.has(o.id)?"#f0f7ff":""}}>
                        <td>
                          <input type="checkbox" checked={selOCs.has(o.id)} onChange={()=>toggleSelOC(o.id)} style={{cursor:"pointer"}}/>
                        </td>
                        <td style={{fontFamily:"Barlow Condensed",fontWeight:800,color:"var(--purple)"}}>{o.numero}</td>
                        <td style={{fontFamily:"Barlow Condensed",fontWeight:600,color:"var(--blue)"}}>{o.remito||"—"}</td>
                        <td style={{fontFamily:"Barlow Condensed",fontWeight:600,color:"var(--blue)"}}>{o.nPedido||"—"}</td>
                        <td><span className="cell-muted">{o.fecha}</span></td>
                        <td><span className="cell-muted">{o.campaña}</span></td>
                        <td>{o.especie}</td>
                        <td style={{fontWeight:600}}>{o.variedad}</td>
                        <td><span className={`badge ${o.tipo==="bigbag"?"bb":"bo"}`}>{o.tipo==="bigbag"?"BB":"Bolsa"}</span></td>
                        <td><span className={`badge ${o.tratada?"tr-b":"st-b"}`}>{o.tratada?"Tratada":"Sin tratar"}</span></td>
                        <td><span className="qty-big" style={{color:"var(--purple)"}}>{fmt(o.lotes.reduce((s,l)=>s+l.cantidad,0))}</span></td>
                        <td style={{fontFamily:"Barlow Condensed",fontWeight:700,color:"var(--green)"}}>{fmt(o.lotes.reduce((s,l)=>s+l.cantidad*o.pesoUnit,0))} kg</td>
                        <td style={{fontFamily:"Barlow Condensed",fontWeight:700,color:"var(--blue)"}}>{o.pg||"—"}{o.pg?"%":""}</td>
                        <td style={{fontFamily:"Barlow Condensed",fontWeight:700,color:"var(--purple)"}}>{o.pmil||"—"}{o.pmil?" g":""}</td>
                        <td><span className="cell-muted" style={{fontSize:".78rem"}}>{o.lotes.length} {o.lotes.length===1?"lote":"lotes"}: {o.lotes.map(l=>l.lote).join(", ")}</span></td>
                        <td style={{fontWeight:600,color:"var(--text)"}}>{o.destino||"—"}</td>
                        <td style={{fontSize:".73rem",color:"var(--muted)",maxWidth:120,overflow:"hidden",textOverflow:"ellipsis",whiteSpace:"nowrap"}}>{o.obs||"—"}</td>
                        <td><span className={`badge ${o.estado==="pendiente"?"pend":"desp"}`}>{o.estado==="pendiente"?"⏳ Pendiente":"✓ Despachada"}</span></td>
                        <td><span className="cell-muted" style={{fontSize:".73rem"}}>{o.fechaDespachada||"—"}</span></td>
                        <td className="no-print">
                          {o.estado==="pendiente"&&<button className="action-btn" onClick={()=>setModal({mode:"editOC",oc:o,item:o})}>✏</button>}
                          <button className="action-btn oc-btn" onClick={()=>printOCWindow([o])}>🖨</button>
                          {o.estado==="pendiente"&&<button className="action-btn dep" onClick={()=>handleDespacharOC(o)}>✓ Desp.</button>}
                          <button className="action-btn del" onClick={()=>handleDelOC(o.id)}>✕</button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div style={{padding:"9px 16px",display:"flex",gap:20,flexWrap:"wrap",color:"var(--muted)",fontSize:".76rem",background:"#fff",borderTop:"1px solid var(--border)"}}>
                <span>Pendientes: <b style={{color:"var(--purple)",fontFamily:"Barlow Condensed",fontSize:"1rem"}}>{filteredOCs.filter(o=>o.estado==="pendiente").length}</b></span>
                <span>Despachadas: <b style={{color:"var(--green)",fontFamily:"Barlow Condensed",fontSize:"1rem"}}>{filteredOCs.filter(o=>o.estado==="despachada").length}</b></span>
                <span>Kg pendientes: <b style={{color:"var(--purple)",fontFamily:"Barlow Condensed",fontSize:"1rem"}}>{fmt(filteredOCs.filter(o=>o.estado==="pendiente").reduce((s,o)=>s+o.lotes.reduce((sl,l)=>sl+l.cantidad*o.pesoUnit,0),0))} kg</b></span>
                {selOCsList.length>0&&<span style={{color:"var(--blue)"}}>✔ {selOCsList.length} seleccionada{selOCsList.length!==1?"s":""}</span>}
              </div>
            </>
          }
        </div>
      )}

      {/* ── ADMIN ── */}
      {tab==="admin"&&(
        <div className="admin">
          <h2>⚙ Gestión de Catálogos</h2>
          <div className="admin-grid">
            <div className="admin-card">
              <h3>Campañas</h3>
              <div className="tag-list">
                {campañas.map(c=><span className="tag" key={c}>{c}<button className="tag-del" onClick={()=>delCampaña(c)}>✕</button></span>)}
              </div>
              <div className="add-inline">
                <input placeholder="Ej. 2026/2027" value={newCamp} onChange={e=>setNewCamp(e.target.value)} onKeyDown={e=>e.key==="Enter"&&addCampaña()}/>
                <button onClick={addCampaña}>+ Agregar</button>
              </div>
            </div>
            <div className="admin-card">
              <h3>Especies</h3>
              <div className="tag-list">
                {especies.map(e=><span className="tag" key={e}>{e}<button className="tag-del" onClick={()=>delEspecie(e)}>✕</button></span>)}
              </div>
              <div className="add-inline">
                <input placeholder="Ej. Arveja" value={newEsp} onChange={e=>setNewEsp(e.target.value)} onKeyDown={e=>e.key==="Enter"&&addEspecie()}/>
                <button onClick={addEspecie}>+ Agregar</button>
              </div>
            </div>
            <div className="admin-card" style={{gridColumn:"1/-1"}}>
              <h3>Variedades por especie</h3>
              <div style={{display:"flex",gap:8,marginBottom:12,flexWrap:"wrap",alignItems:"center"}}>
                <select className="sel" value={selAdmEsp} onChange={e=>setSelAdmEsp(e.target.value)}>
                  {especies.map(e=><option key={e}>{e}</option>)}
                </select>
                <div className="add-inline" style={{flex:1,minWidth:200}}>
                  <input placeholder="Ej. NK 740" value={newVar} onChange={e=>setNewVar(e.target.value)} onKeyDown={e=>e.key==="Enter"&&addVariedad()}/>
                  <button onClick={addVariedad}>+ Agregar</button>
                </div>
              </div>
              <div className="tag-list">
                {(varMap[selAdmEsp]||[]).map(v=><span className="tag" key={v}>{v}<button className="tag-del" onClick={()=>delVariedad(selAdmEsp,v)}>✕</button></span>)}
                {(varMap[selAdmEsp]||[]).length===0&&<span style={{fontSize:".78rem",color:"var(--muted)"}}>Sin variedades cargadas</span>}
              </div>
            </div>
            <div className="admin-card">
              <h3>🔒 Cambiar clave de acceso</h3>
              <div className="move-row" style={{marginBottom:8}}>
                <label>Nueva clave (mín. 4 caracteres)</label>
                <input type="password" value={newPass} onChange={e=>setNewPass(e.target.value)} placeholder="Nueva clave" className="pass-row" style={{width:"100%",background:"var(--bg)",border:"1.5px solid var(--border)",borderRadius:8,padding:"6px 9px",fontFamily:"var(--fb)",fontSize:".83rem",outline:"none"}}/>
              </div>
              <div className="move-row" style={{marginBottom:10}}>
                <label>Confirmar nueva clave</label>
                <input type="password" value={newPass2} onChange={e=>setNewPass2(e.target.value)} placeholder="Repetir clave" style={{width:"100%",background:"var(--bg)",border:"1.5px solid var(--border)",borderRadius:8,padding:"6px 9px",fontFamily:"var(--fb)",fontSize:".83rem",outline:"none"}}/>
              </div>
              <button className="btn btn-ol gnh" onClick={handleChangePass}>✓ Guardar nueva clave</button>
            </div>
            <div className="admin-card" style={{borderColor:"#f5a5a5"}}>
              <div className="danger-zone" style={{margin:0,padding:0,border:"none"}}>
                <h3 style={{color:"var(--red)",marginBottom:8}}>⚠ Zona de peligro</h3>
                <p style={{fontSize:".8rem",color:"var(--muted)",marginBottom:10}}>Borra todo el stock, historial, órdenes y catálogos, volviendo al estado inicial de demostración.</p>
                <button className="btn btn-ol rh" onClick={resetAll}>🗑 Resetear todos los datos</button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* MODALES */}
      {modal?.mode==="new"&&<ModalForm campañas={campañas} especies={especies} varMap={varMap} onSave={handleSave} onClose={()=>setModal(null)}/>}
      {modal?.mode==="edit"&&<ModalForm item={modal.item} campañas={campañas} especies={especies} varMap={varMap} onSave={handleSave} onClose={()=>setModal(null)}/>}
      {modal?.mode==="move"&&<MoveModal stock={stock} item={modal.item} onSave={handleMove} onCreateOC={handleCreateOC} onClose={()=>setModal(null)}/>}
      {modal?.mode==="editOC"&&<OCModal stock={stock} item={modal.item} editOC={modal.oc} onSave={handleEditOC} onClose={()=>setModal(null)}/>}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App/>);
</script>
</body>
</html>
