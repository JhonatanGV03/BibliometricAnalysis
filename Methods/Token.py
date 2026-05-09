import re
import os
import string

# Ruta base del archivo actual (por ejemplo, Token.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construir rutas absolutas desde ahí
archivo_bib = os.path.join(BASE_DIR, "..", "Data", "BasesUnificadas.bib")
archivo_frases = os.path.join(BASE_DIR, "..", "Data", "KeyWords", "compoundWords.txt")

# Leer el contenido del archivo .bib
with open(archivo_bib, "r", encoding="utf-8") as archivo:
    contenido = archivo.read()

# Extraer abstracts usando regex
abstracts = re.findall(r'abstract\s*=\s*[{"](.+?)[}"]', contenido, re.IGNORECASE | re.DOTALL)

# Leer frases clave y convertir a minúsculas
with open(archivo_frases, "r", encoding="utf-8") as f:
    frases = [line.strip().lower() for line in f if line.strip()]

todos_los_tokens = []

for abstract in abstracts:
    abstract = abstract.lower()  # Convertir abstract a minúsculas

    # Reemplazar frases compuestas
    for frase in frases:
        palabras = frase.split()
        patron = r'\b' + r'[\s\.,;:"\'()\[\]{}!?]*'.join(map(re.escape, palabras)) + r'\b'

        if re.search(patron, abstract, flags=re.IGNORECASE):
            print(f"[✔] Reemplazando '{frase}' → '{frase.replace(' ', '_')}' en abstract.")

        abstract = re.sub(patron, frase.replace(" ", "_"), abstract, flags=re.IGNORECASE)

    # Eliminar puntuación (excepto guiones bajos y medios)
    abstract_limpio = abstract.translate(str.maketrans('', '', string.punctuation.replace("_", "").replace("-", "")))

    # Tokenizar y agregar al conjunto global
    tokens = abstract_limpio.split()
    todos_los_tokens.extend(tokens)

# Guardar tokens en un archivo
tokens_file_path = os.path.join(BASE_DIR, "..", "Data", "tokens.txt")
with open(tokens_file_path, "w", encoding="utf-8") as f:
    f.write("\n".join(todos_los_tokens))

# Verificación de la frase 'mobile_application'
with open(tokens_file_path, "r", encoding="utf-8") as f:
    tokens = f.read().splitlines()
