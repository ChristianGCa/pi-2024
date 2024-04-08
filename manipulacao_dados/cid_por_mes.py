import pandas as pd
import os
import glob
import matplotlib.pyplot as plt

# Localização dos arquivos .csv
CSV_PATCH = "/home/christian/Documentos/BIGDATA/ProjetoIntegrador-PSICOSSOCIAL/DADOS/CSV-teste"
COLUMNS = ['UFMUN', 'IDADEPAC', 'CIDPRI']

# ARQUIVOS AUXILIARES
CSV_FILE_MUNICIPIO = "/home/christian/Documentos/BIGDATA/ProjetoIntegrador-PSICOSSOCIAL/ARQUIVOS-TABULACAO/tb_municip.csv"
COLUMNS_MUNICIPIO = ['CO_MUNICIP', 'DS_NOME']

CSV_FILE_CID = "/home/christian/Documentos/BIGDATA/ProjetoIntegrador-PSICOSSOCIAL/ARQUIVOS-TABULACAO/S_CID.csv"
COLUMNS_CID = ['CD_COD', 'CD_DESCR']

# DADOS
CID_DOENCA = 'F710' # CID da doença a ser consultada (Coluna CIDPRI)
COD_MUNICIPIO = 431490 # Código do município (Coluna UFMUN)

def get_doenca_descricao(codigo_cid):
    return cid_df[cid_df['CD_COD'] == codigo_cid]['CD_DESCR'].iloc[0]

files = os.listdir(CSV_PATCH)
csv_files = [file for file in files if file.endswith('.csv')]

# Carregar os arquivos
dfs = []
for arquivo in csv_files:
    # Extrai o ano e o mês do nome do arquivo (PSRSaamm.csv)
    ano = int(arquivo[4:6])
    mes = int(arquivo[6:8])
    
    # Lê o arquivo CSV
    caminho_arq = os.path.join(CSV_PATCH, arquivo)
    df = pd.read_csv(caminho_arq)
    
    # Adiciona colunas de ano e mês ao DataFrame
    df['Ano'] = 2000 + ano
    df['Mes'] = mes
    
    dfs.append(df)

# Concatenar todos os dataframes em um só
df = pd.concat(dfs, ignore_index=True)

# Lendo os arquivos auxiliares
municip_df = pd.read_csv(CSV_FILE_MUNICIPIO, usecols=COLUMNS_MUNICIPIO, encoding='ISO-8859-1')
cid_df = pd.read_csv(CSV_FILE_CID, usecols=COLUMNS_CID, encoding='ISO-8859-1')

# Mesclar os três dataframes, sendo UFMUN=CO_MUNICIP e CIDPRI=CD_COD
merged_df = df.merge(municip_df, left_on='UFMUN', right_on='CO_MUNICIP').merge(cid_df, left_on='CIDPRI', right_on='CD_COD')

# Selecionar e renomear as colunas desejadas
merged_df = merged_df[['DS_NOME', 'IDADEPAC', 'CIDPRI', 'CD_DESCR', 'Ano', 'Mes']]
merged_df.columns = ['Municipio', 'Idade', 'CID', 'Doenca', 'Ano', 'Mês']

# Filtrar para o município e o CID especificado
filtered_df = merged_df[merged_df['CID'] == CID_DOENCA]

# Agrupar por mês e ano e somar as ocorrências
timeline = filtered_df.groupby(['Ano', 'Mês']).size()

# Plotar o gráfico
plt.figure(figsize=(10, 6))

# Cores para cada ano
cores = ['blue', 'green', 'red', 'orange', 'purple', 'yellow', 'black', 'gray', 'pink', 'brown', 'olive', 'cyan']  # Você pode adicionar mais cores conforme necessário

for i, (ano, data) in enumerate(timeline.groupby('Ano')):
    data.plot(marker='o', linestyle='-', color=cores[i], label=ano)

plt.title(f'Ocorrências de {get_doenca_descricao(CID_DOENCA)}')
plt.xlabel('Mês')
plt.ylabel('Ocorrências')
plt.xticks(range(0, 12), ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'])
plt.legend()
plt.tight_layout()
plt.show()

# Agrupar por ano e somar as ocorrências
timeline_por_ano = filtered_df.groupby('Ano').size()

# Plotar o gráfico
plt.figure(figsize=(10, 6))

# Cores para cada ano
cores = ['blue', 'green', 'red', 'orange', 'purple', 'yellow', 'black', 'gray', 'pink', 'brown', 'olive', 'cyan']

timeline_por_ano.plot(marker='o', linestyle='-', color='black')

plt.title(f'Ocorrências de {get_doenca_descricao(CID_DOENCA)} por Ano')
plt.xlabel('Ano')
plt.ylabel('Ocorrências')
plt.xticks(timeline_por_ano.index, timeline_por_ano.index)
plt.tight_layout()
plt.show()