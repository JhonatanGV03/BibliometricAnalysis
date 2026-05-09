import os
import pandas as pd
import numpy as np
import re
import torch
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

# Función para limpiar el texto respecto a la técnica BERT
def limpiar_texto_ligero(text):
    text = str(text).lower()
    text = re.sub(r"[^\w\s]", '', text)  # Solo remover puntuación básica
    return text.strip()

# Función para cargar y limpiar los abstracts
def load_and_clean():
    path = os.path.join('Data', 'Abstracts', 'abstracts_extraidos.csv')
    df = pd.read_csv(path)
    df['abstract'] = df['abstract'].apply(limpiar_texto_ligero)
    return df

# Función para vectorizar los abstracts usando BERT
def vectorize_bert(df):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(df['abstract'].tolist(), convert_to_tensor=True)
    return embeddings

# Función para calcular la similitud coseno entre los vectores BERT
def similarity(embeddings):
    return cos_sim(embeddings, embeddings)

# Función para exportar la matriz a un archivo .npy
def export_matrix(matrix, filename):
    path = os.path.join('Data', 'Matrices', filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    np.save(path, matrix.numpy())
    print(f'Matriz guardada en {path}')

# Función para exportar los embeddings a un archivo .npy
def export_embeddings(embeddings):
    path = os.path.join('Data', 'Matrices', 'bert_vector_matrix.npy')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    np.save(path, embeddings.cpu().numpy())
    print(f'Embeddings guardados en {path}')

# Función principal para ejecutar el proceso de BERT
def bert():
    df = load_and_clean()
    embeddings = vectorize_bert(df)
    cosine_matrix = similarity(embeddings)

    export_matrix(cosine_matrix, 'bert_cosine_sim_matrix.npy')
    export_embeddings(embeddings)

    # Ejemplos de la similitud
    top_results = torch.topk(cosine_matrix[0], k=6)
    print("Top 5 similares al abstract 0:")
    for score, idx in zip(top_results.values[1:], top_results.indices[1:]):
        print(f"Abstract {idx.item()} con similitud {score.item():.4f}")

if __name__ == "__main__":
    bert()
