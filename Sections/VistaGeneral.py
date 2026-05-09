import streamlit as st
import pandas as pd

def mostrar():

    df = loadData()
    st.title("Archivo Unificado")
    st.dataframe(df.head())

    st.write("Resumen estadístico")
    st.write(df.describe(include='all'))

def loadData():
    return pd.read_csv('Data/Abstracts/abstracts_extraidos.csv')