import streamlit as st

def mostrar():

    st.title("Acerca del Proyecto")
    st.write("Este proyecto es un análisis bibliométrico de artículos relacionados con la cadena de búsqueda 'Computationa Thinking'. " \
    "El objetivo es proporcionar una visión general de las tendencias y patrones en la investigación sobre este tema, " \
    "el análisis incluye gráficos de frecuencia, co-ocurrencia, dendogramas y nubes de palabras. " \
    "Se han utilizado técnicas de análisis de datos, simulitud de abstracts y visualización para extraer la información más relevante de los artículos analizados. " \
    "Los datos fueron obtenidos de las bases de datos academicas proporcionadas por el CRAI de la Universidad del Quindío, mas especificamente de las bases de datos: Science Direct, SAGE y IEEE")

    st.subheader("Autores")
    st.write("Julian Cruz")
    st.write("Yhonatan Gomez")
    st.write("María Paula Quintín")