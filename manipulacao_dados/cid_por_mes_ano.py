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

# CID da doença a ser consultada (Coluna CIDPRI)
CID_DOENCA = 'F10'

# Código do município a ser consultado (Coluna UFMUN). Digite 0 para TODOS.
COD_MUNICIPIO = 431020

print('\nIniciando...\n')


files = os.listdir(CSV_PATCH)
csv_files = [file for file in files if file.endswith('.csv')]

municip_df = pd.read_csv(CSV_FILE_MUNICIPIO, usecols=COLUMNS_MUNICIPIO, encoding='ISO-8859-1')
cid_df = pd.read_csv(CSV_FILE_CID, usecols=COLUMNS_CID, encoding='ISO-8859-1')

dfs = []
for arquivo in csv_files:

    # Extrai o ano e o mês do nome do arquivo (PSRSaamm.csv)
    ano = int(arquivo[4:6])
    mes = int(arquivo[6:8])

    caminho_arq = os.path.join(CSV_PATCH, arquivo)
    df = pd.read_csv(caminho_arq, low_memory=False)
    df['Ano'] = 2000 + ano
    df['Mes'] = mes
    dfs.append(df)

df = pd.concat(dfs, ignore_index=True)

# Selecionar e renomear as colunas desejadas
df = df[['UFMUN', 'CIDPRI', 'Ano', 'Mes']]
df.columns = ['CodMunicipio', 'CID', 'Ano', 'Mês']

# Filtrar para o município e o CID especificado, se houver municipio
try:
    if COD_MUNICIPIO != 0:
        filtered_df = df[(df['CodMunicipio'] == COD_MUNICIPIO) & (df['CID'] == CID_DOENCA)]
        nome_municipio = municip_df[municip_df['CO_MUNICIP'] == COD_MUNICIPIO]['DS_NOME'].iloc[0]
    else:
        print('AVISO: Nenhum município selecionado. Mostrando as ocorrências do CID para todos os municípios.\n')
        filtered_df = df[df['CID'] == CID_DOENCA]
        nome_municipio = 'todos os municípios'

except IndexError as i:
    print("ERRO: Município especificado não foi encontrado.")
    exit()

except Exception as e:
    print("Erro inesperado. Erro: ", e)
    exit()

df_filtrado = []

df_grouped = filtered_df.groupby(['Ano', 'Mês']).size().reset_index(name='Ocorrências')

# Optional: If you want to fill missing months with 0 occurrences
# Generate a MultiIndex with all combinations of year and month
index = pd.MultiIndex.from_product([range(df_grouped['Ano'].min(), df_grouped['Ano'].max() + 1), range(1, 13)], names=['Ano', 'Mês'])
# Reindex with the MultiIndex and fill missing values with 0
df_grouped = df_grouped.set_index(['Ano', 'Mês']).reindex(index, fill_value=0).reset_index()

# Pivot the DataFrame to have each year's occurrences in separate columns
df_pivot = df_grouped.pivot(index='Mês', columns='Ano', values='Ocorrências')

# Plotting the graph with one line for each year
plt.figure(figsize=(12, 6))  # Set the figure size

# Plot each column (year) separately
for ano in df_pivot.columns:
    plt.plot(df_pivot.index, df_pivot[ano], marker='o', linestyle='-', label=f'Ano {ano}')

# Set the labels and title
plt.xlabel('Mês')
plt.ylabel('Número de Ocorrências')
plt.title(f'Ocorrências da doença CID {CID_DOENCA} em {nome_municipio}')

# Set x-axis labels to show months
plt.xticks(range(1, 13), [f'{mes:02d}' for mes in range(1, 13)])

# Show legend
plt.legend()

# Show grid
plt.grid(True)

# Show plot
plt.tight_layout()
plt.show()
