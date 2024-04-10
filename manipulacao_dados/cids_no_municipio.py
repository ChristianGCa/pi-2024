import pandas as pd
import os
import glob
import matplotlib.pyplot as plt


# Localização dos arquivos CSV PRINCIPAIS e as colunas desejadas
CSV_PATCH = "/home/christian/Documentos/BIGDATA/ProjetoIntegrador-PSICOSSOCIAL/DADOS/CSV"
COLUMNS = ['UFMUN', 'CIDPRI']

# Localização dos arquivos arquivos CSV AUXILIARES e as colunas desejadas
CSV_FILE_MUNICIPIO = "/home/christian/Documentos/BIGDATA/ProjetoIntegrador-PSICOSSOCIAL/ARQUIVOS-TABULACAO/tb_municip.csv"
COLUMNS_MUNICIPIO = ['CO_MUNICIP', 'DS_NOME']

CSV_FILE_CID = "/home/christian/Documentos/BIGDATA/ProjetoIntegrador-PSICOSSOCIAL/ARQUIVOS-TABULACAO/S_CID.csv"
COLUMNS_CID = ['CD_COD', 'CD_DESCR']

# Código do município a ser consultado (Coluna UFMUN)
COD_MUNICIPIO = 431020

# Carregar as colunas desejadas dos arquivos CSV principais
csv_files = glob.glob(os.path.join(CSV_PATCH, '*.csv'))
dfs = [pd.read_csv(file, usecols=COLUMNS, encoding='ISO-8859-1') for file in csv_files]
df = pd.concat(dfs, ignore_index=True)

# Carregar as colunas desejadas dos arquivos CSV auxiliares
municip_df = pd.read_csv(CSV_FILE_MUNICIPIO, usecols=COLUMNS_MUNICIPIO, encoding='ISO-8859-1')
cid_df = pd.read_csv(CSV_FILE_CID, usecols=COLUMNS_CID, encoding='ISO-8859-1')

# Mesclar os três dataframes, sendo UFMUN=CO_MUNICIP e CIDPRI=CD_COD
merged_df = df.merge(municip_df, left_on='UFMUN', right_on='CO_MUNICIP').merge(cid_df, left_on='CIDPRI', right_on='CD_COD')

# Selecionar e renomear as colunas desejadas
merged_df = merged_df[['UFMUN', 'DS_NOME', 'CIDPRI', 'CD_DESCR']]
merged_df.columns = ['CodMunicipio','Municipio', 'CID', 'Doenca']

# Filtrar o DataFrame para incluir a contagem de cada doença no município especificado
filtered_df = merged_df[merged_df['CodMunicipio'] == COD_MUNICIPIO]
df_contagem = filtered_df['Doenca'].value_counts().reset_index()
df_contagem.columns = ['Doenca', 'Count']

# Selecionar as doenças com mais ocorrências
top_doencas = df_contagem.nlargest(20, 'Count')
top_doencas = top_doencas.sort_values(by='Count', ascending=True)

# Ajustar o tamanho da figura e o layout para garantir que as doenças apareçam por completo
plt.figure(figsize=(15, 10))
bars = plt.barh(top_doencas['Doenca'], top_doencas['Count'])
plt.title(f'Top 10 Doenças em {filtered_df["Municipio"].iloc[0]} por número de ocorrências')
plt.xlabel('Número de ocorrências')

# Adicionar as anotações dos valores nas barras
for bar in bars:
    xval = bar.get_width()
    plt.text(xval + 50, bar.get_y() + bar.get_height()/2, int(xval), ha='left', va='center')

plt.tight_layout()  # Ajustar automaticamente o layout
plt.subplots_adjust(left=0.3)  # Ajustar a margem esquerda para garantir que as doenças fiquem visíveis

plt.show()