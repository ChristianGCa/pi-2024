import pandas as pd
import os

# Procurar e extrair os arquivos da pasta

directory_path = "/mnt/78DDB1555FC1C17E/Big-Data/BDSUS/SIASUS/PS-PSICOSSOCIAL/CSV"

csv_files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]

# Juntar os arquivos em um só

df = pd.DataFrame()

for csv_file in csv_files:
    file_path = os.path.join(directory_path, csv_file)
    data = pd.read_csv(file_path, sep=',', encoding='ISO-8859-1')
    data = 1
print()

# Salvar o arquivo consolidado

#result = pd.concat(frames, ignore_index=True)
#
#result.to_csv('output_data.csv', index=False)
#
#print("ETL finalizado")