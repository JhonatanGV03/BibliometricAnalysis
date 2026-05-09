import streamlit as st
import pandas as pd
import bibtexparser
import os

def mostrar():
    st.title("Datos Analizados")
    st.write("En la siguiente sección se muestra el corpus utilizado para la realización de este proyecto. " \
    "Estos datos fueron obtenidos de las bases de datos académicas brindas por el CRAI de la Universidad del Quindío. " \
    "Este corpus fue debidamente filtrado con el fin de eliminar las entradas duplicadas que pudieran presentarse en las diferentes bases de datos, de estas, únicamente se obtuvieron dos entradas duplicadas de un estimado de 1300 entradas. " )

    rutaArchivo = os.path.join("Data", "BasesFiltradas.bib")

    try:
        with open(rutaArchivo, "r", encoding="utf-8") as file:
            contenido = file.read()

        st.subheader("Contenido del Archivo")
        st.text_area("Datos", contenido, height=300)

        bibData = bibtexparser.loads(contenido)
        entradas = bibData.entries

        if entradas:
            df = pd.DataFrame(entradas)

            for col in ['author', 'title', 'journal', 'year']:
                if col not in df.columns:
                    df[col] = ""

            st.subheader("Filtro de Datos")

            autores = sorted({autor.strip() for lista in df['author'].dropna() for autor in lista.split(" and")})
            autorSeleccionado = st.multiselect("Autor", autores)

            years = sorted(df['year'].dropna().unique())
            yearSelected = st.multiselect("Año", years)

            palabrasClave = st.text_input("Buscar palabras en el título")

            journals = sorted(df['journal'].dropna().unique())
            journalSelected = st.multiselect("Journals", journals)

            publishers = sorted(df['publisher'].dropna().unique())
            publisherSelected = st.multiselect("Publisher", publishers)

            types = sorted(df['ENTRYTYPE'].dropna().unique())
            typeSelected = st.multiselect("Tipo de entrada", types)

            dfFiltrado = df.copy()

            if autorSeleccionado:
                dfFiltrado = dfFiltrado[dfFiltrado['author'].apply(
                    lambda x: any(a.strip() in str(x) for a in autorSeleccionado))]
                
            if yearSelected:
                dfFiltrado = dfFiltrado[dfFiltrado['year'].isin(yearSelected)]

            if palabrasClave:
                dfFiltrado = dfFiltrado[dfFiltrado['title'].str.contains(palabrasClave, case=False, na=False)]

            if journalSelected:
                dfFiltrado = dfFiltrado[dfFiltrado['journal'].isin(journalSelected)]

            if publisherSelected:
                dfFiltrado = dfFiltrado[dfFiltrado['publisher'].isin(publisherSelected)]

            if typeSelected:
                dfFiltrado = dfFiltrado[dfFiltrado['ENTRYTYPE'].isin(typeSelected)]

            st.subheader("Datos Filtrados")
            st.dataframe(dfFiltrado.reset_index(drop=True), use_container_width=True)

            st.markdown(f"Total de entradas encontradas: {len(dfFiltrado)}")
        else:
            st.warning("No se encontraron entradas en el archivo.")

    except FileNotFoundError:
        st.error("El archivo no se encontró. Asegúrate de que la ruta sea correcta.")