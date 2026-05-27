import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="La Clementina · Stock Semillas", layout="wide", initial_sidebar_state="collapsed")

# --- ESTADO (Replica tu useState de React) ---
if 'modal' not in st.session_state:
    st.session_state.modal = {"mode": None, "item": None, "oc": None}
if 'stock' not in st.session_state:
    st.session_state.stock = [] # Aquí cargarás tus datos

# --- FUNCIONES MANEJADORAS (Estructura original fiel) ---
# Copia aquí la lógica exacta de SEMILLERO (3).txt dentro de cada función
def handleSave(item_data):
    st.toast("Guardando lote...")
    # Tu lógica aquí
    st.session_state.modal = {"mode": None, "item": None, "oc": None}
    st.rerun()

def handleMove(item, cantidad, destino):
    st.toast("Procesando movimiento...")
    # Tu lógica aquí
    st.session_state.modal = {"mode": None, "item": None, "oc": None}
    st.rerun()

def handleCreateOC(item, oc_data):
    # Tu lógica de creación OC
    st.session_state.modal = {"mode": None, "item": None, "oc": None}
    st.rerun()

def handleEditOC(item, oc_data):
    # Tu lógica de edición OC
    st.session_state.modal = {"mode": None, "item": None, "oc": None}
    st.rerun()

def resetAll():
    st.session_state.stock = []
    st.rerun()

# --- COMPONENTES (Equivalentes a tus React Modals) ---

@st.dialog("Formulario de Lote")
def ModalForm(item=None):
    # Aquí mapeas: campañas, especies, varMap
    st.write("Configuración de Lote")
    if st.button("Guardar"):
        handleSave(item)

@st.dialog("Mover Stock")
def MoveModal(item):
    st.write(f"Gestionando stock de: {item.get('Variedad') if item else 'Lote'}")
    if st.button("Confirmar Movimiento"):
        handleMove(item, 0, "Destino")

@st.dialog("Editar Orden de Carga")
def OCModal(item, oc):
    st.write("Editando OC")
    if st.button("Guardar Cambios"):
        handleEditOC(item, oc)

# --- DISPATCHER PRINCIPAL (El motor que emula a React) ---
st.title("🌱 La Clementina · Stock Semillas")

# Simulando la tabla/interfaz (Coloca aquí tu tabla)
if st.button("Nuevo Lote"):
    st.session_state.modal = {"mode": "new", "item": None, "oc": None}

# Lógica de renderizado de modales (Igual a tu `{modal?.mode==="new" && ...}`)
m = st.session_state.modal
if m["mode"] == "new":
    ModalForm()
elif m["mode"] == "edit":
    ModalForm(item=m["item"])
elif m["mode"] == "move":
    MoveModal(item=m["item"])
elif m["mode"] == "editOC":
    OCModal(item=m["item"], oc=m["oc"])

# --- ZONA ADMINISTRATIVA ---
st.markdown("---")
with st.expander("⚙️ Administración"):
    if st.button("🗑 Resetear todos los datos"):
        resetAll()

st.markdown("""
    <div style="text-align: center; margin-top: 50px;">
        <p style="font-size: 0.8rem; color: #888;">Creado por Ignacio Diaz</p>
    </div>
""", unsafe_allow_html=True)
