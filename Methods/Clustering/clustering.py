import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.preprocessing import normalize


def load_data():
    tfidf_vectors = np.load('Data/Matrices/tfidf_vector_matrix.npy')
    bert_vectors = np.load('Data/Matrices/bert_vector_matrix.npy')
    return tfidf_vectors, bert_vectors


def apply_clustering(vectors, method, n_clusters=5):
    Z = linkage(vectors, method=method)
    labels = fcluster(Z, t=n_clusters, criterion='maxclust')
    score = silhouette_score(vectors, labels)
    return Z, labels, score


def cluster():
    print("hasta aca funciona")
    tfidf_vectors, bert_vectors = load_data()

    print("Clustering usando TF-IDF")
    Z_tfidf_avg, _, score_avg_tfidf = apply_clustering(tfidf_vectors, method='average')
    Z_tfidf_ward, _, score_ward_tfidf = apply_clustering(tfidf_vectors, method='ward')

    print(f"Silhouette Score (TF-IDF, average): {score_avg_tfidf:.4f}")
    print(f"Silhouette Score (TF-IDF, ward): {score_ward_tfidf:.4f}")

    print("\nClustering usando BERT")
    Z_bert_avg, _, score_avg_bert = apply_clustering(bert_vectors, method='average')
    Z_bert_ward, _, score_ward_bert = apply_clustering(bert_vectors, method='ward')

    print(f"Silhouette Score (BERT, average): {score_avg_bert:.4f}")
    print(f"Silhouette Score (BERT, ward): {score_ward_bert:.4f}")

    # Exportar los linkage matrices para usar en dendrogramas
    np.save('Data/Matrices/Z_tfidf_avg.npy', Z_tfidf_avg)
    np.save('Data/Matrices/Z_tfidf_ward.npy', Z_tfidf_ward)
    np.save('Data/Matrices/Z_bert_avg.npy', Z_bert_avg)
    np.save('Data/Matrices/Z_bert_ward.npy', Z_bert_ward)
