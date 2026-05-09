import csv
import os
import re
from collections import Counter

from matplotlib import pyplot as plt

def agrupacion():

    rutaBD = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Data")

    basesFiltradas = os.path.join(rutaBD, "BasesFiltradas.bib")

    patronAutor = re.compile(r"author\s*=\s*\{([^}]+)\}", re.IGNORECASE)
    patronAnios = re.compile(r"year\s*=\s*\{([^}]+)\}", re.IGNORECASE)
    patronType = re.compile(r"@(\w+)\s*{", re.IGNORECASE)
    patronJournal = re.compile(r"journal\s*=\s*\{([^}]+)\}", re.IGNORECASE)
    patronPublisher = re.compile(r"publisher\s*=\s*\{([^}]+)\}", re.IGNORECASE)

    contadorAutor = Counter()
    contadorAnio = Counter()
    contadorType = Counter()
    contadorJournal = Counter()
    contadorPublisher = Counter()

    with open(basesFiltradas, "r", encoding="utf-8") as entrada:
        contenido = entrada.read()
        partes = re.split(r'\n(?=@)', contenido)

        for entrada in partes:
            entrada = entrada.strip()
            if not entrada:
                continue

            if not entrada.startswith("@"):
                entrada = "@" + entrada
            elif entrada.startswith("@@"):
                entrada = entrada[1:]

            autor = patronAutor.search(entrada)
            anio = patronAnios.search(entrada)
            type = patronType.search(entrada)
            journal = patronJournal.search(entrada)
            publisher = patronPublisher.search(entrada)

            autor = autor.group(1).strip().lower() if autor else "N/A"
            anio = anio.group(1).strip().lower() if anio else "N/A"
            type = type.group(1).strip().lower() if type else "N/A"
            journal = journal.group(1).strip().lower() if journal else "N/A"
            publisher = publisher.group(1).strip().lower() if publisher else "N/A"

            ' Count Authors '
            if autor != "N/A":
                autores = [a.strip() for a in autor.split(" and ")]
                contadorAutor.update(autores)

            ' Count Years '
            if anio != "N/A":
                contadorAnio[anio] += 1

            ' Count Types'
            tipoMatch = re.match(r"@(\w+)", entrada)
            if tipoMatch:
                tipo = tipoMatch.group(1).lower()
                contadorType[tipo] += 1

            ' Count Journals '
            if journal != "N/A":
                contadorJournal[journal] += 1

            ' Count Publishers '
            if publisher != "N/A":
                contadorPublisher[publisher] += 1

    ' Print the results '

    print("Autores más frecuentes:")
    for autor, count in contadorAutor.most_common(15):
        print(f"{autor}: {count}")

    print("\nAños más frecuentes:")
    for anio, count in contadorAnio.most_common(15):
        print(f"{anio}: {count}")

    print("\nTipos de artículos más frecuentes:")
    for tipo, count in contadorType.most_common():
        print(f"{tipo}: {count}")

    print("\nJournal más frecuentes:")
    for journal, count in contadorJournal.most_common(15):
        print(f"{journal}: {count}")

    print("\nPublisher más frecuentes:")
    for publisher, count in contadorPublisher.most_common(15):
        print(f"{publisher}: {count}")

    graficarCounter(contadorAutor, "Autors", cantidad = 15)
    graficarCounter(contadorAnio, "Years", cantidad = 15)
    graficarCounter(contadorType, "Types")
    graficarCounter(contadorJournal, "Journals", cantidad = 15)
    graficarCounter(contadorPublisher, "Publishers", cantidad = 15)


    ' Save the results to CSV/PNG files '

def graficarCounter(counter, titulo, cantidad = 15):

    rutaGraphics = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Graphics/Frecuency")
    rutaReports = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Reports")

    nombreArchivoCSV = os.path.join(rutaReports, f"Results {titulo}.csv")
    nombreArchivoPNG = os.path.join(rutaGraphics, f"Graphic {titulo}.png")

    ' CSV Files '
    with open(nombreArchivoCSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([titulo.capitalize(), "Frecuencia"])
        for item, count in counter.most_common(cantidad):
            writer.writerow([item, count])

    print(f"\n📂 Resultados guardados en: {nombreArchivoCSV}")

    ' Graphics '
    items = counter.most_common(cantidad)
    etiquetas = [x[0] for x in items]
    valores = [x[1] for x in items]

    plt.figure(figsize=(10, 6))
    plt.barh(etiquetas, valores, color='skyblue')
    plt.xlabel("Frequency")
    plt.title(f"Most Frequent {titulo.capitalize()}")
    plt.gca().invert_yaxis()
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(nombreArchivoPNG)
    print(f"📊 Gráfico guardado como: {nombreArchivoPNG}")