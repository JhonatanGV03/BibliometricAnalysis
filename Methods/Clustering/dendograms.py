import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram


def load_linkage_matrices():
    matrices = {
        "TF-IDF + Average": np.load('Data/Matrices/Z_tfidf_avg.npy'),
        "TF-IDF + Ward": np.load('Data/Matrices/Z_tfidf_ward.npy'),
        "BERT + Average": np.load('Data/Matrices/Z_bert_avg.npy'),
        "BERT + Ward": np.load('Data/Matrices/Z_bert_ward.npy')
    }
    return matrices


def plot_dendrogram(Z, title):
    plt.figure(figsize=(10, 6))
    dendrogram(Z)
    plt.title(f"Dendrogram - {title}")
    plt.xlabel("Abstracts")
    plt.ylabel("Distancia")
    plt.tight_layout()
    plt.savefig(f"Graphics/Dendograms/dendrogram_{title.replace(' + ', '_').lower()}.png")
    plt.close()


def graph_dendograms():
    matrices = load_linkage_matrices()
    for title, Z in matrices.items():
        plot_dendrogram(Z, title)

    print("Graficos de dendrogramas generados y guardados en la carpeta 'Graphics/Dendograms'.")
