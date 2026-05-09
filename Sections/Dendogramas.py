import streamlit as st
import os

def mostrar():
    st.title("Dendogramas")
    st.write("Esta sección muestra los dendogramas generados mediante el análisis de abstracts y palabras clave de los artículos analizados.")
    st.write("Los dendogramas son representaciones gráficas que muestran la relación jerárquica entre diferentes elementos, en este caso, los artículos analizados.")
    
    # Carpeta donde se encuentran las imágenes
    carpetaGraficas = os.path.join("Graphics", "Dendograms")
    
    # Obtener la lista de imágenes en la carpeta
    imagenes = [img for img in os.listdir(carpetaGraficas) if img.endswith(".png")]
    
    # Mostrar las imágenes en Streamlit
    for imagen in imagenes:
        rutaImagen = os.path.join(carpetaGraficas, imagen)
        st.image(rutaImagen, caption=imagen, use_container_width=True)