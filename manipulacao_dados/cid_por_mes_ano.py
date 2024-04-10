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
CID_DOENCA = 'G20'

# Código do município a ser consultado (Coluna UFMUN). Digite 0 para TODOS.
COD_MUNICIPIO = 431020

print('\nIniciando...\n')

try:
    files = os.listdir(CSV_PATCH)
    csv_files = [file for file in files if file.endswith('.csv')]

    municip_df = pd.read_csv(CSV_FILE_MUNICIPIO, usecols=COLUMNS_MUNICIPIO, encoding='ISO-8859-1')
    cid_df = pd.read_csv(CSV_FILE_CID, usecols=COLUMNS_CID, encoding='ISO-8859-1')

except FileNotFoundError as e:
    print("Nenhum arquivo encontrado. Erro: ", e)
    exit()

except IndexError as i:
    print("CID especificado não encontrado. Erro: ",i)
    exit()

except Exception as e:
    print("Erro inesperado. Erro: ", e)
    exit()

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

try:
    nome_doenca = cid_df[cid_df['CD_COD'] == CID_DOENCA]['CD_DESCR'].iloc[0]

    # ///////////////////////////////  |
    # // CID por ANOS em MUNICIPIO //  |
    # ///////////////////////////////  V

    timeline_por_ano = filtered_df.groupby('Ano').size()
    plt.figure(figsize=(10, 6))
    timeline_por_ano.plot(marker='o', linestyle='-', color='black')
    plt.title(f'Ocorrências de {nome_doenca} por Ano em {nome_municipio}')
    plt.xlabel('Ano')
    plt.ylabel('Ocorrências')
    plt.xticks(timeline_por_ano.index, timeline_por_ano.index)
    plt.tight_layout()
    plt.show()

    # ///////////////////////////////////////  |
    # // CID por MESES e ANOS em MUNICIPIO //  |
    # ///////////////////////////////////////  V

    timeline = filtered_df.groupby(['Ano', 'Mês']).size()
    plt.figure(figsize=(10, 6))
    cores = ['blue', 'green', 'red', 'orange', 'purple', 'yellow', 'black', 'gray', 'pink', 'brown', 'olive', 'cyan']

    # Mostrando o gráfico com números em cada ponto
    for i, (ano, data) in enumerate(timeline.groupby('Ano')):
        data.plot(marker='o', linestyle='-', color=cores[i], label=ano)

    plt.title(f'Ocorrências de {nome_doenca} por Mês em {nome_municipio}')
    plt.xlabel('Mês')
    plt.ylabel('Ocorrências')
    plt.xticks(range(0, 12), ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'])
    plt.legend()
    plt.tight_layout()
    plt.show()

except IndexError as i:
    print("Nenhum registro de CID encontrado. Erro: ",i)

except Exception as e:
    print("Erro inesperado. Erro: ", e)