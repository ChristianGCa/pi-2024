import pandas as pd
import matplotlib.pyplot as plt
import os

UFMUN = 431020
CID = 'F10'

csv_dir = '/home/christian/Documentos/BIGDATA/ProjetoIntegrador-PSICOSSOCIAL/DADOS/CSV'
files = os.listdir(csv_dir)
csv_files = [file for file in files if file.endswith('.csv')]

dfs = []
for file in csv_files:
    ano = int(file[4:6])
    mes = int(file[6:8])
    caminho_arq = os.path.join(csv_dir, file)
    df = pd.read_csv(caminho_arq, usecols=['UFMUN', 'CIDPRI'], encoding='ISO-8859-1')
    df['Ano'] = 2000 + ano
    df['Mes'] = mes
    dfs.append(df)

df = pd.concat(dfs, ignore_index=True)

df = df[(df['UFMUN'] == UFMUN) & (df['CIDPRI'] == CID)]
df = df.groupby(['Ano', 'Mes']).size().reset_index(name='Ocorrencias')

cidade = pd.read_csv('/home/christian/Documentos/BIGDATA/ProjetoIntegrador-PSICOSSOCIAL/ARQUIVOS-TABULACAO/tb_municip.csv', usecols=['CO_MUNICIP', 'DS_NOME'])
cidade_desc = cidade[cidade['CO_MUNICIP'] == UFMUN]['DS_NOME'].iloc[0]
cid = pd.read_csv('/home/christian/Documentos/BIGDATA/ProjetoIntegrador-PSICOSSOCIAL/ARQUIVOS-TABULACAO/S_CID.csv', usecols=['CD_COD', 'CD_DESCR'])
cid_desc = cid[cid['CD_COD'] == CID]['CD_DESCR'].iloc[0]
df = df.pivot(index='Ano', columns='Mes', values='Ocorrencias').fillna(0).astype(int)

plt.figure(figsize=(10, 6))

for year in df.index:
    year_data = df.loc[year]
    full_year_data = year_data.reindex(range(1, 13), fill_value=0)
    plt.plot(full_year_data.index, full_year_data.values, label=str(year))

plt.title(f'CAPS: Ocorrências de CID {cid_desc} em {cidade_desc}')
plt.xlabel('Mês')
plt.ylabel('Número de Ocorrências')
plt.xticks(range(1, 13))
plt.legend(title='Ano')
plt.grid(True)
plt.tight_layout()
plt.show()
