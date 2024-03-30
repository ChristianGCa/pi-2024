import csv
from dbfread import DBF

# Função que converte .dbf em .csv
def dbf_to_csv(path):

    # Configurand o nome do arquivo .csv
    csv_path = path[:-4] + ".csv"

    # Criando um objeto DBF com o caminho especificado
    dbf = DBF(path, encoding='ISO-8859-1')
    # Criando um arquivo .csv e preenchendo 
    with open(csv_path, 'w', newline = '') as arq:
        writer = csv.writer(arq)
        # Escrevendo o nome das colunas
        writer.writerow(dbf.field_names)
        # Escrevendo as linhas
        for record in dbf:
            writer.writerow(list(record.values()))
    return csv_path

# Chamando a função e passando o caminho de um arquivo .dbf
dbf_to_csv('PSRS1512.dbf')