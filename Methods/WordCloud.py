import re
from PIL import Image
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

# Obtener la ruta absoluta del directorio donde se encuentra el script actual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta a la carpeta de salida para nubes de palabras
carpeta_salida = os.path.join(BASE_DIR, "..", "Graphics", "WordCloud")
os.makedirs(carpeta_salida, exist_ok=True)

# Ruta donde están las tablas
carpeta_tablas = os.path.join(BASE_DIR, "..", "Tables")

# Ruta a la imagen de máscara
mask_image_path = os.path.join(BASE_DIR, "..", "Data", "Mask", "nube.png")


# Verificar si la imagen de la máscara existe
if not os.path.exists(mask_image_path):
    print(f"❌ La imagen de máscara no se encuentra en: {mask_image_path}")
    exit()

# Cargar imagen de máscara
mask = np.array(Image.open(mask_image_path))

# Inicializar un diccionario para las frecuencias totales de todas las palabras
datos_totales = {}

# Recorrer archivos de texto
for archivo in os.listdir(carpeta_tablas):
    if archivo.endswith(".txt"):
        ruta = os.path.join(carpeta_tablas, archivo)
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                texto = f.read()
        except Exception as e:
            print(f"❌ Error al leer el archivo {archivo}: {e}")
            continue

        # Extraer tuplas (palabra, frecuencia) ignorando encabezados y bordes
        matches = re.findall(r"│ ([^│]+?)\s+│\s+(\d+)\s+│", texto)

        # Sumar las frecuencias de las palabras para el conteo general
        for palabra, frecuencia in matches:
            palabra = palabra.strip()
            frecuencia = int(frecuencia)
            if palabra in datos_totales:
                datos_totales[palabra] += frecuencia
            else:
                datos_totales[palabra] = frecuencia

# Ordenar las palabras por frecuencia (de mayor a menor) y tomar solo las más frecuentes
# Por ejemplo, seleccionamos las 50 más frecuentes
palabras_destacadas = dict(sorted(datos_totales.items(), key=lambda item: item[1], reverse=True)[:50])

# Función para que las palabras sean blancas
def white_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "white"

# Crear la nube de palabras con las frecuencias de las palabras destacadas
wc = WordCloud(
    background_color='deepskyblue',  # Fondo azul
    mask=mask,  # Aplicar forma de nube
    contour_width=5,
    contour_color='white',
    max_words=50,  # Limitar a las 50 palabras más frecuentes
    color_func=white_color_func  # Aplicar el color blanco a las palabras
)
wc.generate_from_frequencies(palabras_destacadas)

# Guardar la imagen generada
ruta_salida = "../Graphics/WordCloud/general_wordcloud_destacadas.png"

# Convertir la imagen de la nube de palabras a un array de numpy
imagen_wc = wc.to_array()

# Usar matplotlib para mostrar la nube de palabras
plt.figure(figsize=(10, 8))
plt.imshow(imagen_wc, interpolation='bilinear')
plt.axis("off")

# Título de la nube de palabras
plt.text(0.05, 0.05, "Palabras Clave", color='blue', fontsize=20, ha='left', va='bottom', transform=plt.gca().transAxes)

# Guardar la imagen con el título
plt.savefig(ruta_salida, format="png", bbox_inches="tight", pad_inches=0.0)
plt.close()

print("✅ Nube de palabras destacadas generada en la carpeta 'WordCloud/'")
