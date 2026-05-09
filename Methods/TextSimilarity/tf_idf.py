import os
import pandas as pd
import numpy as np
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Función para limpiar el texto respecto a la tecnica TF-IDF
def limpiar_texto(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", '', text)
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return ' '.join(tokens)


# Funcion para cargar y limpiar los abstracts
def load_and_clean():
    path = os.path.join('Data', 'Abstracts', 'abstracts_extraidos.csv')
    df = pd.read_csv(path)
    df['abstract'] = df['abstract'].apply(limpiar_texto)
    return df

# Función para vectorizar los abstracts usando TF-IDF
def vectorize_tfidf(df):
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
    tfidf_matrix = vectorizer.fit_transform(df['abstract'])
    return tfidf_matrix

# Función para calcular la similitud coseno entre los vectores TF-IDF
def cosine_sim(matrix):
    return cosine_similarity(matrix)

# Función para exportar la matriz a un archivo .npy
def export_matrix(matrix, filename):
    path = os.path.join('Data', 'Matrices', filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    np.save(path, matrix)
    print(f'Matriz guardada en {path}')

# Función principal para ejecutar el proceso de TF-IDF
def tfidf():
    df = load_and_clean()
    tfidf_matrix = vectorize_tfidf(df)
    sim_matrix = cosine_sim(tfidf_matrix)

    export_matrix(tfidf_matrix.toarray(), 'tfidf_vector_matrix.npy')
    export_matrix(sim_matrix, 'tfidf_cosine_sim_matrix.npy')


    #Ejemeplo de la similitud
    sim_scores = list(enumerate(sim_matrix[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]
    print("Top 5 similares al abstract 0:")
    for idx, score in sim_scores:
        print(f"Abstract {idx} con similitud {score:.4f}")

if __name__ == "__main__":
    tfidf()
