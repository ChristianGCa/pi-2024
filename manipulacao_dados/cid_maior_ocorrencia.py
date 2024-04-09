import pandas as pd
import os
import glob
import matplotlib.pyplot as plt

# Diretório dos arquivos CSV
CSV_PATCH = "/home/christian/Documentos/BIGDATA/ProjetoIntegrador-PSICOSSOCIAL/DADOS/CSV"
COLUMNS = ['UFMUN', 'IDADEPAC', 'CIDPRI']

# ARQUIVOS AUXILIARES
CSV_FILE_MUNICIPIO = "/home/christian/Documentos/BIGDATA/ProjetoIntegrador-PSICOSSOCIAL/ARQUIVOS-TABULACAO/tb_municip.csv"
COLUMNS_MUNICIPIO = ['CO_MUNICIP', 'DS_NOME']

CSV_FILE_CID = "/home/christian/Documentos/BIGDATA/ProjetoIntegrador-PSICOSSOCIAL/ARQUIVOS-TABULACAO/S_CID.csv"
COLUMNS_CID = ['CD_COD', 'CD_DESCR']

# CID da doença a ser consultada
CID_DOENCA = 'F10'

try:
    # Carregar os arquivos
    csv_files = glob.glob(os.path.join(CSV_PATCH, '*.csv'))
    dfs = [pd.read_csv(file, usecols=COLUMNS, encoding='ISO-8859-1') for file in csv_files]
    df = pd.concat(dfs, ignore_index=True)

    municip_df = pd.read_csv(CSV_FILE_MUNICIPIO, usecols=COLUMNS_MUNICIPIO, encoding='ISO-8859-1')
    cid_df = pd.read_csv(CSV_FILE_CID, usecols=COLUMNS_CID, encoding='ISO-8859-1')

    # Mesclar os três dataframes, sendo UFMUN=CO_MUNICIP e CIDPRI=CD_COD
    merged_df = df.merge(municip_df, left_on='UFMUN', right_on='CO_MUNICIP').merge(cid_df, left_on='CIDPRI', right_on='CD_COD')

    # Selecionar e renomear as colunas desejadas
    merged_df = merged_df[['DS_NOME', 'IDADEPAC', 'CIDPRI', 'CD_DESCR']]
    merged_df.columns = ['Municipio', 'Idade', 'CID', 'Doenca']

    # Filtrar o DataFrame para incluir apenas os casos da doença especificada
    casos_cid = merged_df[merged_df['CID'] == CID_DOENCA]

    # Contar o número de casos de doença por município
    casos_por_municipio = casos_cid['Municipio'].value_counts()

    # Função para mapear códigos CID para descrições de doenças
    def get_doenca_descricao(codigo_cid):
        return cid_df[cid_df['CD_COD'] == codigo_cid]['CD_DESCR'].iloc[0]

    # Plotar o gráfico de barras
    plt.figure(figsize=(15, 8), tight_layout=True)
    casos_por_municipio.plot(kind='barh')
    plt.title('Casos de: '+get_doenca_descricao(CID_DOENCA))
    plt.xlabel('Município')
    plt.ylabel('Número de Casos')
    plt.xticks(rotation=90)
    plt.show()

except IndexError as i:
    print("Nenhum registro encontrado. Erro: ",i)
