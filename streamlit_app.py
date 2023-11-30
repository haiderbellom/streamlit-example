import streamlit as st
from pymongo import MongoClient
import json

# Conexión a la base de datos
def connect_to_mongodb():
    connection_str = "mongodb+srv://dcorread:BigMamma23@bigdata2023.hqgu6wf.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(connection_str)
    db = client["mlds3"]
    collection = db["pyfinal"]
    return collection

# Lógica para construir la consulta a MongoDB
def build_query():
    query = {}

    # Sección 1
    if incluir_palabras:
        query["Texto"] = {"$regex": incluir_palabras, "$options": "i"}

    if excluir_palabras:
        query["Texto"] = {"$not": {"$regex": excluir_palabras, "$options": "i"}}

    if codigo_providencia:
        query["Providencia"] = codigo_providencia

    # Sección 2
    anos_seleccionados = []
    if filtro_2020:
        anos_seleccionados.append(2020)
    if filtro_2021:
        anos_seleccionados.append(2021)
    if filtro_2022:
        anos_seleccionados.append(2022)
    if filtro_2023:
        anos_seleccionados.append(2023)

    if anos_seleccionados:
        query["AnoPublicacion"] = {"$in": anos_seleccionados}

    # Sección 3
    if tipo_providencia:
        query["Tipo"] = tipo_providencia

    return query



# Definición de la interfaz de usuario con Streamlit
def main():
    # Conexión a la base de datos
    collection = connect_to_mongodb()


# Definición de la interfaz de usuario con Streamlit
st.sidebar.title("Consulta de Providencias")

# Sección 1
st.sidebar.header("Búsqueda por palabras en el texto")
incluir_palabras = st.sidebar.text_input("Palabras o frases a incluir")
excluir_palabras = st.sidebar.text_input("Palabras o frases a excluir")
codigo_providencia = st.sidebar.text_input("Código de Providencia")

# Sección 2
st.sidebar.header("Filtros por rangos")

# Añadir título debajo de "Filtros por rangos"
st.sidebar.markdown("<span style='font-size:15px; color: #333;'>Seleccione uno o varios años:</span>", unsafe_allow_html=True)

# Dividir en dos columnas para los checkboxes
left_column, right_column = st.sidebar.columns(2)

# Checkboxes para los años
with left_column:
    filtro_2020 = st.checkbox("2020")

with right_column:
    filtro_2021 = st.checkbox("2021")

# Añadir el segundo par de checkboxes debajo del primer par
with left_column:
    filtro_2022 = st.checkbox("2022")

with right_column:
    filtro_2023 = st.checkbox("2023")

# Sección 3
st.sidebar.header("Filtros por Tipo de Providencia")
tipo_providencia = st.sidebar.selectbox("Tipo de Providencia", ["", "Constitucionalidad", "Auto", "Tutela"])



# Botón para realizar la consulta
if st.sidebar.button("Realizar Consulta"):
    # Lógica para construir la consulta a MongoDB
    query = {}

    # Obtener la colección MongoDB
    collection = connect_to_mongodb()

    # Sección 1
    if incluir_palabras:
        query["Texto"] = {"$regex": incluir_palabras, "$options": "i"}

    if excluir_palabras:
        query["Texto"] = {"$not": {"$regex": excluir_palabras, "$options": "i"}}

    if codigo_providencia:
        query["Providencia"] = codigo_providencia

    # Sección 2
    anos_seleccionados = []
    if filtro_2020:
        anos_seleccionados.append("2020")
    if filtro_2021:
        anos_seleccionados.append("2021")
    if filtro_2022:
        anos_seleccionados.append("2022")
    if filtro_2023:
        anos_seleccionados.append("2023")

    if anos_seleccionados:
        query["AnoPublicacion"] = {"$in": anos_seleccionados}

    # Sección 3
    if tipo_providencia:
        query["Tipo"] = tipo_providencia

    # Realizar la consulta a MongoDB
    resultados = list(collection.find(query))

    # Mostrar los resultados en Streamlit
    st.write(f"Total de resultados encontrados: {len(resultados)}")

    if resultados:
        st.write("Detalles de la consulta:")
        for resultado in resultados:
            st.markdown(f"**Providencia:** {resultado['Providencia']} - **Tipo:** {resultado['Tipo']}")
            
            with st.expander("Ver más detalles"):
                st.markdown(f"**Fecha de Publicación:** {resultado['FechaPublicacion']}")
                st.markdown(f"**Texto:** {resultado['Texto']}")
            
            st.markdown("---")  # Línea divisoria entre resultados
    else:
        st.write("No se encontraron resultados para los criterios de búsqueda.")


# Botón para limpiar todos los campos
if st.sidebar.button("Limpiar Campos"):
    incluir_palabras = ""
    excluir_palabras = ""
    codigo_providencia = ""
    filtro_2020 = False
    filtro_2021 = False
    filtro_2022 = False
    filtro_2023 = False
    tipo_providencia = None
    
    # Forzar la recarga de la página
    st.rerun()
