import os

import bibtexparser
import pandas as pd


# Metodo que extrae el ID, el título y el abstract de un archivo bibtex y lo guarda en un archivo CSV
def extract():
    bibtex_file_path = os.path.join('Data', 'BasesFiltradas.bib')

    with open(bibtex_file_path, encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    entries = bib_database.entries
    data = []
    for idx, entry in enumerate(entries):
        entry_id = entry.get('ID', f'entry_{idx}')
        title = entry.get('title', '').strip()
        abstract = entry.get('abstract', '').strip()
        if abstract:
            data.append({'id': entry_id, 'title': title, 'abstract': abstract})

    df = pd.DataFrame(data)
    output_path = os.path.join('Data', 'Abstracts', 'abstracts_extraidos.csv')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f'¡Datos extraídos y guardados exitosamente en: {output_path}!')


if __name__ == "__main__":
    extract()