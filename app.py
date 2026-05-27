import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="La Clementina · Stock Semillas", layout="wide")

# --- ESTADO INICIAL (Igual que en tu React) ---
if 'modal' not in st.session_state:
    st.session_state.modal = {"mode": None, "item": None, "oc": None}
if 'stock' not in st.session_state:
    st.session_state.stock = [] # Aquí cargarás tu data de Sheets

# --- FUNCIONES DE LÓGICA (Tus funciones originales) ---
def handleSave(data):
    # Inserta aquí tu lógica original de guardado
    st.write(f"Guardando: {data}")
    st.session_state.modal = {"mode": None, "item": None}

def handleMove(item, cantidad, destino):
    # Inserta aquí tu lógica de movimiento
    st.write(f"Moviendo {cantidad} unidades a {destino}")
    st.session_state.modal = {"mode": None, "item": None}

def handleCreateOC(item, oc_data):
    # Inserta aquí tu lógica de creación de OC
    st.session_state.modal = {"mode": None, "item": None}

def handleEditOC(item, oc_data):
    # Inserta aquí tu lógica de edición de OC
    st.session_state.modal = {"mode": None, "item": None}

def resetAll():
    # Tu función original de reset
    st.session_state.stock = []
    st.rerun()

# --- MODALES (Estructura fiel a tu React) ---

@st.dialog("Formulario de Lote")
def ModalForm(item=None):
    # Aquí mapeas: campañas={campañas}, especies={especies}, varMap={varMap}
    st.write("Configuración de Lote")
    # ... inputs ...
    if st.button("Guardar"):
        handleSave({"item": item})
        st.rerun()

@st.dialog("Mover Stock")
def MoveModal(item):
    st.write(f"Mover: {item.get('Variedad')}")
    # ... inputs ...
    if st.button("Confirmar Movimiento"):
        handleMove(item, 0, "Destino")
        st.rerun()

@st.dialog("Editar Orden de Carga")
def OCModal(item, oc):
    st.write("Editando OC")
    # ... inputs ...
    if st.button("Guardar Cambios"):
        handleEditOC(item, oc)
        st.rerun()

# --- INTERFAZ PRINCIPAL ---
st.title("🌱 La Clementina · Stock Semillas")

# Aquí iría tu renderizado de tabla
if st.button("Nuevo Lote"):
    st.session_state.modal = {"mode": "new", "item": None}

# --- LÓGICA DE APERTURA DE MODALES (Mantiene tu estructura original) ---
m = st.session_state.modal

if m["mode"] == "new":
    ModalForm()
elif m["mode"] == "edit":
    ModalForm(item=m["item"])
elif m["mode"] == "move":
    MoveModal(item=m["item"])
elif m["mode"] == "editOC":
    OCModal(item=m["item"], oc=m["oc"])

# Zona de peligro (tal cual tu HTML)
with st.expander("⚙️ Administración"):
    if st.button("🗑 Resetear todos los datos"):
        resetAll()
