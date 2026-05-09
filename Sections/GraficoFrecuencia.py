import streamlit as st
import os

def mostrar():

    st.title("Visualización de Imágenes")
    st.write("Las siguientes gráficas representan la frecuencia aparición cada una de las categorias de los artículos analizados.")
    st.write("De cada uno de las categorias analizadas se tomaron los primeros 15 con mayor frecuencia")

    carpetaGraficas = os.path.join("Graphics", "Frecuency")
    imagenes = [img for img in os.listdir(carpetaGraficas) if img.endswith(".png")]

    for imagen in imagenes:
        rutaImagen = os.path.join(carpetaGraficas, imagen)
        st.image(rutaImagen, caption=imagen, use_container_width=True)