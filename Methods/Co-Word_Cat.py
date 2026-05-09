import os
import re
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import community

# Obtener la ruta absoluta del directorio donde se encuentra el script actual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construir rutas absolutas desde ahí
carpeta_tablas = os.path.join(BASE_DIR, "..", "Tables")
carpeta_salida = os.path.join(BASE_DIR, "..", "Graphics", "Co-Word", "Cat")

# Crear la carpeta de salida si no existe
os.makedirs(carpeta_salida, exist_ok=True)

# Verificar existencia de la carpeta de tablas
if not os.path.exists(carpeta_tablas):
    print(f"Error: La carpeta de tablas no existe en la ruta {carpeta_tablas}")
else:
    print(f"Carpeta de tablas encontrada: {carpeta_tablas}")

# Recorrer archivos de la carpeta de tablas
for archivo in os.listdir(carpeta_tablas):
    if not archivo.endswith(".txt"):
        continue

    # Construir la ruta completa al archivo
    ruta = os.path.join(carpeta_tablas, archivo)

    # Leer el contenido del archivo
    with open(ruta, "r", encoding="utf-8") as f:
        texto = f.read()

    # Buscar las palabras y frecuencias con regex
    matches = re.findall(r"│ ([^│]+?)\s+│\s+(\d+)\s+│", texto)
    palabras_frecuencias = {palabra.strip(): int(frecuencia) for palabra, frecuencia in matches}

    # Filtrar las palabras clave que tienen más de 1 aparición
    palabras_clave = [palabra for palabra, frecuencia in palabras_frecuencias.items() if frecuencia > 1]

    # Construir la matriz de co-ocurrencias
    co_matrix = defaultdict(lambda: defaultdict(int))
    for i, palabra1 in enumerate(palabras_clave):
        for palabra2 in palabras_clave[i + 1:]:
            co_matrix[palabra1][palabra2] += 1
            co_matrix[palabra2][palabra1] += 1

    if not co_matrix:
        continue  # Saltar si no hay co-ocurrencias

    # Convertir la matriz de co-ocurrencias a un DataFrame
    df = pd.DataFrame.from_dict(co_matrix, orient='index').fillna(0).astype(int)

    # Crear el grafo de co-ocurrencias
    G = nx.Graph()
    for p1 in df.index:
        for p2 in df.columns:
            w = df.loc[p1, p2]
            if w > 0:
                G.add_edge(p1, p2, weight=w)

    if G.number_of_edges() == 0:
        continue

    # Tamaño proporcional al grado de los nodos
    degrees = dict(G.degree())
    node_sizes = [300 + degrees[n] * 80 for n in G.nodes()]

    # Pesos de los bordes (más gruesos para co-ocurrencias más frecuentes)
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
    max_weight = max(edge_weights) if edge_weights else 1
    edge_widths = [1 + (w / max_weight) * 4 for w in edge_weights]

    # Detección de comunidades
    partition = community.best_partition(G)
    num_communities = len(set(partition.values()))
    cmap = plt.colormaps.get_cmap('tab10')
    colors = [cmap(i % 10) for i in partition.values()]

    # Generar la disposición de los nodos
    pos = nx.spring_layout(G, k=1.2, seed=42)

    # Crear la figura y dibujar el grafo
    fig, ax = plt.subplots(figsize=(14, 12))
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=node_sizes, node_color=colors, alpha=0.9)
    nx.draw_networkx_edges(G, pos, ax=ax, width=edge_widths, alpha=0.4, edge_color='gray')
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_color='black')

    # Título del gráfico
    ax.set_title(f"Red de Co-ocurrencia: {archivo.replace('.txt', '')}", fontsize=15)

    # Desactivar los ejes
    ax.axis("off")
    plt.tight_layout()

    # Ruta de salida del gráfico
    nombre_salida = os.path.join(carpeta_salida, f"co_word_{archivo.replace('.txt', '')}.png")

    # Guardar el gráfico como imagen PNG
    plt.savefig(nombre_salida, format="png", dpi=300)
    plt.close()

    # Confirmación en consola
    print(f"✅ Gráfico generado para: {archivo}")
