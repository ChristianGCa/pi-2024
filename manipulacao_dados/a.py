import pandas as pd
import os
import glob
import matplotlib.pyplot as plt

# Diretório dos arquivos CSV
CSV_PATCH = "/home/christian/Documentos/TESTE BIG DATA/CSV"
COLUMNS = ['UFMUN', 'IDADEPAC', 'CIDPRI']

# ARQUIVOS AUXILIARES
CSV_FILE_MUNICIPIO = "/home/christian/Documentos/TESTE BIG DATA/CSV_AUXILIAR/tb_municip.csv"
COLUMNS_MUNICIPIO = ['CO_MUNICIP', 'DS_NOME']

CSV_FILE_CID = "/home/christian/Documentos/TESTE BIG DATA/CSV_AUXILIAR/S_CID.csv"
COLUMNS_CID = ['CD_COD', 'CD_DESCR']

# Carregar os arquivos
csv_files = glob.glob(os.path.join(CSV_PATCH, '*.csv'))
dfs = [pd.read_csv(file, usecols=COLUMNS, encoding='ISO-8859-1') for file in csv_files]
df = pd.concat(dfs, ignore_index=True)

municip_df = pd.read_csv(CSV_FILE_MUNICIPIO, usecols=COLUMNS_MUNICIPIO, encoding='ISO-8859-1')
cid_df = pd.read_csv(CSV_FILE_CID, usecols=COLUMNS_CID, encoding='ISO-8859-1')

# Mesclar os três dataframes, sendo UFMUN=CO_MUNICIP e CIDPRI=CD_COD
merged_df = df.merge(municip_df, left_on='UFMUN', right_on='CO_MUNICIP').merge(cid_df, left_on='CIDPRI', right_on='CD_COD')

# Selecionar e renomear as colunas desejadas
merged_df = merged_df[['DS_NOME', 'IDADEPAC', 'CD_DESCR']]
merged_df.columns = ['Nome do Município', 'Idade', 'CID']

# Exibir o DataFrame com as primeiras 20 linhas
print(merged_df.head(20))