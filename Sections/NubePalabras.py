import streamlit as st
import os

def mostrar():
    st.title("Nubes de Palabras")
    
    # Carpeta donde se encuentran las imágenes
    carpetaGraficas = os.path.join("Graphics", "WordCloud", "Cat")
    
    # Obtener la lista de imágenes en la carpeta
    imagenes = [img for img in os.listdir(carpetaGraficas) if img.endswith(".png")]
    
    # Mostrar las imágenes en Streamlit
    for imagen in imagenes:
        rutaImagen = os.path.join(carpetaGraficas, imagen)
        st.image(rutaImagen, caption=imagen, use_container_width=True)