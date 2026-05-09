import os
import re

'''
CÓDIGO GENERADO CON CHATGPT para arreglar las entradas IEEE en formato BibTeX (Saltos de linea)
'''

def arreglar_IEEE(entrada):
    entrada_corregida = re.sub(r'(@[A-Z]+{)', r'\n\1', entrada).strip()
    return entrada_corregida


def procesar_archivos_ieee():
    carpeta_datos = os.path.join(os.getcwd(), "Data/DownloadedCitations")  # Ruta absoluta a 'Datos'

    # Verificar si la carpeta 'Datos' existe
    if not os.path.exists(carpeta_datos):
        print(f"La carpeta '{carpeta_datos}' no existe.")
        return

    # Listar archivos que empiezan con 'IEEE'
    archivos = [f for f in os.listdir(carpeta_datos) if f.startswith("IEEE") and f.endswith(".bib")]

    if not archivos:
        print("No se encontraron archivos IEEE para procesar.")
        return

    for archivo in archivos:
        ruta_archivo = os.path.join(carpeta_datos, archivo)

        try:
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                contenido = f.read()

            contenido_corregido = arreglar_IEEE(contenido)

            with open(ruta_archivo, "w", encoding="utf-8") as f:
                f.write(contenido_corregido)

            print(f"Archivo corregido: {archivo}")

        except Exception as e:
            print(f"Error procesando {archivo}: {e}")