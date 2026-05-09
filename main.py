import os

from Automation.automatizacion import descargar_citas
from Automation.arreglar_ieee import procesar_archivos_ieee
from Methods.Clustering.dendograms import graph_dendograms
from Methods.unificarArchivos import unificar_filtrar_archivos
from Methods.agrupacion import agrupacion
import subprocess
from Methods.TextSimilarity import abstract_handler
from Methods.TextSimilarity.bert import bert
from Methods.TextSimilarity.tf_idf import tfidf
from Methods.Clustering.clustering import cluster

def main():

    #Req 1
    descargar_citas()  # ---> Descarga las citas de las bases de datos Sage, IEEE y ScienceDirect de manera automatizada
    procesar_archivos_ieee() # ---> Arregla las entradas IEEE en formato BibTeX (Saltos de linea)
    unificar_filtrar_archivos() # ---> Unifica y filtra las citas descargadas de las bases de datos

    #Req 2
    agrupacion()
    # Construye la ruta absoluta al ejecutable de Python en el entorno virtual
    venv_python = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")

    #Req 3
    subprocess.run(["python", "Methods/Token.py"])
    subprocess.run(["python", "Methods/Token.py"])
    subprocess.run(["python", "Methods/Coincidences.py"])
    subprocess.run(["python", "Methods/Tab.py"])
    subprocess.run(["python", "Methods/WordCloud.py"])
    subprocess.run(["python", "Methods/WordCloud_Cat.py"])
    subprocess.run(["python", "Methods/Co-Word.py"])
    subprocess.run(["python", "Methods/Co-Word_Cat.py"])

    #Req 5
    abstract_handler.extract()
    tfidf()
    bert()

    #Seguimiento 2
    cluster()
    graph_dendograms()


if __name__ == "__main__":
    main()
