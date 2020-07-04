import os 
import platform
import pandas as pd
import pyodbc 
import json


with open("config.json") as json_data_file:
    data = json.load(json_data_file)

driver = ''
csv_location = ''



if (platform.system() == 'Linux'):
    drivers = [item for item in pyodbc.drivers()]
    driver = drivers[-1]
    csv_location = '/csv/BreadBasket_DMS.csv'
else:
    driver = 'SQL Server'
    csv_location = '\\csv\BreadBasket_DMS.csv'

# Conecion con la base de datos

conn = pyodbc.connect(f"Driver={driver};Server={data['sqlserver']['server']};Database={data['sqlserver']['database']};UID={data['sqlserver']['user']};PWD={data['sqlserver']['password']}")


# Obtiene la ubicacion del directorio actual para cargar el data Frame
dir_path = os.path.dirname(os.path.realpath(__file__))
url = dir_path +  csv_location

data = pd.read_csv(url, delimiter =',', decimal='.', header=0, index_col=0)

#cursor 
cursor = conn.cursor()
iteration = 0
special_characters = 0

for row in data.iterrows():
    date = row[0]
    time = row[1][0]
    transactionId = row[1][1]
    product = row[1][2]

    if "'" in product:
        special_characters += 1
        product = product.replace("'", '"')

    cursor.execute(f"exec sp_insertTransaction '{date}', '{time}', {transactionId}, '{product}'")
    iteration += 1
    print(f'[{iteration}]-> One row inserted successfully!')

print(f'\n\n\tWere inserted {iteration} rows on Transactions.\n\tWere found {special_characters} special characters.')