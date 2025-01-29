import streamlit as st
import py3Dmol
import os

# Carpeta donde se guardarán las moléculas
SAVE_DIR = "molecules"
os.makedirs(SAVE_DIR, exist_ok=True)

def save_molecule(file):
    """Guarda el archivo en el directorio de moléculas."""
    file_path = os.path.join(SAVE_DIR, file.name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    return file_path

def load_molecule(file_path):
    """Carga el contenido del archivo."""
    with open(file_path, "r") as f:
        return f.read()

def display_molecule(mol_data, file_format):
    """Muestra la molécula en 3D."""
    view = py3Dmol.view(width=500, height=500)
    try:
        view.addModel(mol_data, file_format)
        view.setStyle({"stick": {}})
        view.zoomTo()
    except Exception as e:
        st.error(f"Error al cargar la molécula: {e}")
    return view

# Streamlit UI
st.title("Visualizador de Moléculas 3D")

# Cargar archivos
uploaded_file = st.file_uploader("Sube un archivo (.gjf o .xyz)", type=["gjf", "xyz"])

if uploaded_file:
    file_path = save_molecule(uploaded_file)
    file_format = "xyz" if uploaded_file.name.endswith(".xyz") else "mol"
    mol_data = load_molecule(file_path)
    st.text(f"Archivo cargado: {uploaded_file.name}")
    
    # Mostrar molécula
    view = display_molecule(mol_data, file_format)
    st.components.v1.html(view._repr_html_(), height=500)

# Lista de moléculas guardadas
st.sidebar.title("Moléculas guardadas")
saved_files = [f for f in os.listdir(SAVE_DIR) if f.endswith(".gjf") or f.endswith(".xyz")]
if saved_files:
    selected_file = st.sidebar.selectbox("Selecciona una molécula", saved_files)
    
    if selected_file:
        file_path = os.path.join(SAVE_DIR, selected_file)
        file_format = "xyz" if selected_file.endswith(".xyz") else "mol"
        mol_data = load_molecule(file_path)
        
        st.sidebar.text(f"Mostrando: {selected_file}")
        view = display_molecule(mol_data, file_format)
        st.sidebar.components.v1.html(view._repr_html_(), height=500)
else:
    st.sidebar.text("No hay moléculas guardadas aún.")

