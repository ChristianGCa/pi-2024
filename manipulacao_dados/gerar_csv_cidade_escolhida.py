import pandas as pd
import os

UFMUN = 431020
PASTA_DESTINO = '/home/christian/Documentos/BIGDATA/ProjetoIntegrador-PSICOSSOCIAL/DADOS/CSV-ijui'

csv_dir = '/home/christian/Documentos/BIGDATA/ProjetoIntegrador-PSICOSSOCIAL/DADOS/CSV'
files = os.listdir(csv_dir)
csv_files = [file for file in files if file.endswith('.csv')]

# Exportar arquivos CSV para pasta de destino
for file in csv_files:
    caminho_arq = os.path.join(csv_dir, file)
    df = pd.read_csv(caminho_arq, encoding='ISO-8859-1')
    df = df[(df['UFMUN'] == UFMUN)]
    df.to_csv(os.path.join(PASTA_DESTINO, file), index=False)
