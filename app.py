import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de página
st.set_page_config(page_title="La Clementina · Stock Semillas", layout="wide")

# Estilos CSS
st.markdown("""
    <style>
        .admin-card { border: 1px solid #dde1ea; padding: 20px; border-radius: 8px; background: #fff; }
        .danger-zone { border: 1px solid #f5a5a5; padding: 15px; border-radius: 8px; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# 2. Estado inicial (Simulación de base de datos)
if 'stock' not in st.session_state:
    st.session_state.stock = [] # Aquí cargarías tus datos desde Sheets
if 'modal' not in st.session_state:
    st.session_state.modal = None

# 3. Definición de Modales (Evitan el error de Null)
@st.dialog("Nuevo Lote")
def modal_new():
    st.write("Formulario para nuevo lote...")
    if st.button("Guardar"):
        st.rerun()

@st.dialog("Mover Stock")
def modal_move(item):
    # Aquí el 'item' nunca será null porque se pasa al llamar a la función
    st.write(f"Moviendo: {item.get('Variedad', 'Lote')}")
    if st.button("Confirmar Movimiento"):
        # Lógica de guardado
        st.rerun()

# 4. Lógica de UI
st.title("🌱 La Clementina · Stock Semillas")

# Ejemplo de tabla con botón que abre modal
data = [{"ID": 1, "Variedad": "Maíz Pro", "Stock": 100}, {"ID": 2, "Variedad": "Soja Plus", "Stock": 200}]
df = pd.DataFrame(data)

st.table(df)

# Botón para activar modal de movimiento
if st.button("Mover Lote 1"):
    st.session_state.selected_item = data[0]
    st.session_state.modal = "move"

# Disparador de modales (seguro)
if st.session_state.modal == "move":
    modal_move(st.session_state.selected_item)
    st.session_state.modal = None # Reset tras cerrar

# Footer requerido
st.markdown("---")
st.caption("Creado por Ignacio Diaz")
