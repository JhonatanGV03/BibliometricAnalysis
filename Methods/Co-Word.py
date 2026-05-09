import os
import re
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import community  # from python-louvain

# Obtener la ruta absoluta del directorio donde se encuentra el script actual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Carpeta donde están las tablas
carpeta_tablas = os.path.join(BASE_DIR, "..", "Tables")

# Crear matriz de co-ocurrencia
cooccurrence_matrix = defaultdict(lambda: defaultdict(int))

# Verificar si la carpeta de tablas existe
if not os.path.exists(carpeta_tablas):
    print(f"Error: La carpeta de tablas no existe en la ruta {carpeta_tablas}")
else:
    print(f"Carpeta de tablas encontrada: {carpeta_tablas}")

# Recorrer archivos y construir co-ocurrencias
for archivo in os.listdir(carpeta_tablas):
    if archivo.endswith(".txt"):
        ruta = os.path.join(carpeta_tablas, archivo)
        with open(ruta, "r", encoding="utf-8") as f:
            texto = f.read()

        matches = re.findall(r"│ ([^│]+?)\s+│\s+(\d+)\s+│", texto)
        palabras_frecuencias = {palabra.strip(): int(frecuencia) for palabra, frecuencia in matches}
        palabras_clave = [palabra for palabra, frecuencia in palabras_frecuencias.items() if frecuencia > 1]

        for i, palabra1 in enumerate(palabras_clave):
            for palabra2 in palabras_clave[i+1:]:
                cooccurrence_matrix[palabra1][palabra2] += 1
                cooccurrence_matrix[palabra2][palabra1] += 1

# Crear DataFrame
cooccurrence_df = pd.DataFrame.from_dict(cooccurrence_matrix, orient='index').fillna(0).astype(int)

# Crear grafo
G = nx.Graph()

for palabra1 in cooccurrence_df.index:
    for palabra2 in cooccurrence_df.columns:
        weight = cooccurrence_df.loc[palabra1, palabra2]
        if weight > 0:
            G.add_edge(palabra1, palabra2, weight=weight)

# Calcular propiedades del grafo
degrees = dict(G.degree())
node_sizes = [300 + degrees[n]*100 for n in G.nodes()]
edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
max_weight = max(edge_weights) if edge_weights else 1
edge_widths = [1 + (w / max_weight) * 4 for w in edge_weights]

# Asignar colores a los nodos (por grado)
cmap = plt.colormaps.get_cmap('viridis')
norm = plt.Normalize(vmin=min(degrees.values()), vmax=max(degrees.values()))
node_colors = [cmap(norm(degrees[n])) for n in G.nodes()]

# Layout más disperso
pos = nx.spring_layout(G, k=1.2, seed=42)  # Más espacio entre nodos

# Detectar comunidades
partition = community.best_partition(G)

# Obtener colores distintos para cada comunidad
num_communities = len(set(partition.values()))
cmap = plt.colormaps.get_cmap('tab10')  # Colores discretos y claros
colors = [cmap(i % 10) for i in partition.values()]

# Tamaño de nodo proporcional al grado
degrees = dict(G.degree())
node_sizes = [degrees[node]*80 for node in G.nodes()]

# Crear carpeta para guardar el gráfico si no existe
carpeta_salida = os.path.join(BASE_DIR, "..", "Graphics", "Co-Word")
os.makedirs(carpeta_salida, exist_ok=True)

# Crear figura
fig, ax = plt.subplots(figsize=(14, 12))

# Dibujar nodos con colores por comunidad
nx.draw_networkx_nodes(G, pos, ax=ax,
                       node_size=node_sizes,
                       node_color=colors,
                       alpha=0.9)

# Dibujar aristas
nx.draw_networkx_edges(G, pos, ax=ax,
                       width=1, alpha=0.4, edge_color='gray')

# Dibujar etiquetas
nx.draw_networkx_labels(G, pos, ax=ax,
                        font_size=10, font_color='black')

# Título y presentación
ax.set_title("Visualización de Red de Co-ocurrencia de Palabras Clave", fontsize=16)
ax.axis("off")
plt.tight_layout()

# Guardar y mostrar
nombre_salida = os.path.join(carpeta_salida, "co_word_network.png")
plt.savefig(nombre_salida, format="png", bbox_inches="tight", dpi=300)
plt.close()
print(f"✅ Gráfico de Co-Word generado en la carpeta 'Co-Word/'")
