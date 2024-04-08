import pandas as pd
import os
import glob
import matplotlib.pyplot as plt

# Localização dos arquivos .csv
CSV_PATCH = "/home/christian/Documentos/BIGDATA/ProjetoIntegrador-PSICOSSOCIAL/DADOS/CSV"
COLUMNS = ['UFMUN', 'IDADEPAC', 'CIDPRI']

# ARQUIVOS AUXILIARES
CSV_FILE_MUNICIPIO = "/home/christian/Documentos/BIGDATA/ProjetoIntegrador-PSICOSSOCIAL/ARQUIVOS-TABULACAO/municip.csv"
COLUMNS_MUNICIPIO = ['CO_MUNICIP', 'DS_NOME']

CSV_FILE_CID = "/home/christian/Documentos/BIGDATA/ProjetoIntegrador-PSICOSSOCIAL/ARQUIVOS-TABULACAO/S_CID.csv"
COLUMNS_CID = ['CD_COD', 'CD_DESCR']

# CID da doença a ser consultada (Coluna CIDPRI)
CID_DOENCA = 'F710'

# Código do município (UFMUN)
COD_MUNICIPIO = 431490

# Lista todos os arquivos na pasta
arquivos = os.listdir(CSV_PATCH)

# Filtra apenas os arquivos CSV
csv_files = [arquivo for arquivo in arquivos if arquivo.endswith('.csv')]

# Carregar os arquivos
dfs = []
for arquivo in csv_files:
# Extrai o ano e o mês do nome do arquivo
    ano = int(arquivo[4:6])
    mes = int(arquivo[6:8])
    
    # Lê o arquivo CSV
    caminho_arquivo = os.path.join(CSV_PATCH, arquivo)
    df = pd.read_csv(caminho_arquivo)
    
    # Adiciona colunas de ano e mês ao DataFrame
    df['Ano'] = 2000 + ano  # Supondo que os anos sejam representados de 00 a 99
    df['Mês'] = mes
    
    dfs.append(df)

# Concatenar todos os dataframes em um só
df = pd.concat(dfs, ignore_index=True)

# Filtrar para o município e o CID especificado
filtered_df = df[df['CIDPRI'] == CID_DOENCA]


# Agrupar por mês e ano e somar as ocorrências
timeline = filtered_df.groupby(['Ano', 'Mês']).size()

# Plotar o gráfico
plt.figure(figsize=(10, 6))

# Cores para cada ano
cores = ['blue', 'green', 'red', 'orange', 'purple', 'yellow', 'black', 'gray', 'pink', 'brown', 'olive', 'cyan']  # Você pode adicionar mais cores conforme necessário

for i, (ano, data) in enumerate(timeline.groupby('Ano')):
    data.plot(marker='o', linestyle='-', color=cores[i], label=ano)

plt.title(f'Ocorrências de {CID_DOENCA}')
plt.xlabel('Mês')
plt.ylabel('Ocorrências')
plt.xticks(range(0, 12), ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'])
plt.legend()
plt.tight_layout()
plt.show()