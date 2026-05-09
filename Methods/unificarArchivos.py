import os
import glob
import re

def unificar_filtrar_archivos():
    rutaArchivos = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Data/DownloadedCitations")
    rutaSuperior = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Data")

    if not os.path.exists(rutaArchivos):
        print(f"Error: La carpeta {rutaArchivos} no existe.")
        exit()

    basesUnificadas = os.path.join(rutaSuperior, "BasesUnificadas.bib")
    basesFiltradas = os.path.join(rutaSuperior, "BasesFiltradas.bib")
    basesRepetidas = os.path.join(rutaSuperior, "BasesRepetidas.bib")

    # Unificar archivos .bib

    archivos = glob.glob(os.path.join(rutaArchivos, "*.bib"))

    if not archivos:
        print("No se encontraron archivos .bib en la carpeta especificada.")
        exit()

    with open(basesUnificadas, "w", encoding="utf-8") as salida:
        for archivo in archivos:
            with open(archivo, "r", encoding="utf-8") as entrada:
                salida.write(entrada.read() + "\n")

    print(f"Bases de datos unificadas en:  {basesUnificadas}")

    # Filtro de entradas repetidas

    entradasUnicas = {}
    entradasRepetidas = {}

    patronTitulo = re.compile(r"title\s*=\s*\{([^}]+)\}", re.IGNORECASE)
    patronISBN = re.compile(r"isbn\s*=\s*\{([^}]+)\}", re.IGNORECASE)
    patronDOI = re.compile(r"doi\s*=\s*\{([^}]+)\}", re.IGNORECASE)
    patronVolumen = re.compile(r"volume\s*=\s*\{([^}]+)\}", re.IGNORECASE)
    patronAutor = re.compile(r"author\s*=\s*\{([^}]+)\}", re.IGNORECASE)
    patronAnio = re.compile(r"year\s*=\s*\{([^}]+)\}", re.IGNORECASE)

    with open(basesUnificadas, "r", encoding="utf-8") as entrada:
        contenido = entrada.read()
        partes = re.split(r'\n(?=@)', contenido)

        for entrada in partes:
            entrada = entrada.strip()
            if not entrada:
                continue

            '''
            If generado con ChatGPT para el manejo de los @ en las entradas
            '''
            if not entrada.startswith("@"):
                entrada = "@" + entrada
            elif entrada.startswith("@@"):
                entrada = entrada[1:]

            titulo = patronTitulo.search(entrada)
            isbn = patronISBN.search(entrada)
            doi = patronDOI.search(entrada)
            volumen = patronVolumen.search(entrada)
            autor = patronAutor.search(entrada)
            anio = patronAnio.search(entrada)

            titulo = titulo.group(1).strip().lower() if titulo else "N/A"
            isbn = isbn.group(1).strip().lower() if isbn else "N/A"
            doi = doi.group(1).strip().lower() if doi else "N/A"
            volumen = volumen.group(1).strip().lower() if volumen else "N/A"
            autor = autor.group(1).strip().lower() if autor else "N/A"
            anio = anio.group(1).strip().lower() if anio else "N/A"

            identificador = isbn if isbn != "N/A" else doi if doi != "N/A" else "Sin ISBN/DOI"

            claveUnica = f"{titulo} | {identificador} | {volumen} | {autor} | {anio}"

            if claveUnica in entradasUnicas:
                entradasRepetidas[claveUnica] = entrada
            else:
                entradasUnicas[claveUnica] = entrada

    with open(basesFiltradas, "w", encoding="utf-8") as salidaFiltrada:
        for entrada in entradasUnicas.values():
            salidaFiltrada.write(entrada + "\n\n")

    with open(basesRepetidas, "w", encoding="utf-8") as salidaRepetidas:
        for entrada in entradasRepetidas.values():
            salidaRepetidas.write(entrada + "\n\n")

    print(f"Archivo filtrado en: {basesFiltradas} ({len(entradasUnicas)} entradasUnicas).")
    print(f"Archivo de entradas repetidas en: {basesRepetidas} ({len(entradasRepetidas)} entradasRepetidas).")
