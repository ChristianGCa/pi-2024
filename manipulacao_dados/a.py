import pandas as pd
import os
import glob
import matplotlib.pyplot as plt

# Diretório dos arquivos CSV
CSV_PATCH = "/home/christian/Documentos/TESTE BIG DATA/CSV"
COLUMNS = ['UFMUN', 'IDADEPAC']

# ARQUIVOS AUXILIARES

# CSV municipios
CSV_PATCH_MUNICIPIO = "/home/christian/Documentos/TESTE BIG DATA/CSV_AUXILIAR/tb_municip.csv"
COLUMNS_MUNICIPIO = ['CO_MUNICIP', 'DS_NOME']

# Carregar os arquivos
municip_df = pd.read_csv(CSV_PATCH_MUNICIPIO, usecols=COLUMNS_MUNICIPIO)
csv_files = glob.glob(os.path.join(CSV_PATCH, '*.csv'))

# Concatenar os arquivos
dfs = [pd.read_csv(file, usecols=COLUMNS) for file in csv_files]
df = pd.concat(dfs, ignore_index=True)

# Mesclar os DataFrames
merged_df = pd.merge(df, municip_df, left_on='UFMUN', right_on='CO_MUNICIP', how='left')

# Selecionar e renomear as colunas desejadas
merged_df = merged_df[['DS_NOME', 'IDADEPAC']]
merged_df.columns = ['Nome do Município', 'Idade']

print(merged_df)