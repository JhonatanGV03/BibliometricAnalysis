from collections import Counter
import os
import json

# Obtener la ruta absoluta del directorio actual del script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construir rutas absolutas seguras
ruta_keywords = os.path.join(BASE_DIR, "..", "Data", "KeyWords", "keyWords.json")
ruta_tokens = os.path.join(BASE_DIR, "..", "Data", "tokens.txt")

# Cargar palabras clave desde el archivo JSON externo
with open(ruta_keywords, "r", encoding="utf-8") as f:
    palabras_clave = json.load(f)

# Leer los tokens guardados desde el archivo de texto
with open(ruta_tokens, "r", encoding="utf-8") as f:
    todos_los_tokens = f.read().splitlines()

# Contar ocurrencias de cada token
conteo_tokens = Counter(todos_los_tokens)

coincidencias = []

# Recorrer cada categoría y sus palabras
for categoria, lista_palabras in palabras_clave.items():
    for palabra in lista_palabras:
        cantidad = conteo_tokens.get(palabra, 0)
        coincidencias.append((palabra, cantidad, categoria))

# Mostrar todas las palabras, con o sin coincidencias
for palabra, cantidad, categoria in coincidencias:
    print(f"{palabra}: {cantidad} apariciones (Categoría: {categoria})")
