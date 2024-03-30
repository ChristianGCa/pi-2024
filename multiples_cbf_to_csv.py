import csv
from dbfread import DBF
import glob
import os

# Função que converte .dbf em .csv
def convert_all_dbf_to_csv(folder_path):
    dbf_files = glob.glob(os.path.join(folder_path, '*.dbf'))
    csv_paths = []
    for dbf_file in dbf_files:
        csv_path = dbf_file[:-4] + ".csv"
        dbf = DBF(dbf_file, encoding='ISO-8859-1')
        with open(csv_path, 'w', newline='') as arq:
            writer = csv.writer(arq)
            writer.writerow(dbf.field_names)
            for record in dbf:
                writer.writerow(list(record.values()))
        csv_paths.append(csv_path)
    return csv_paths

# Chamando a função e passando o caminho da pasta contendo os arquivos .dbf
csv_files = convert_all_dbf_to_csv('/home/christian/Documentos/q')