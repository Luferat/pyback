# Importar a biblioteca sqlite3 para trabalhar com SQLite
import sqlite3

# Importar biblioteca para trabalhar com o formato JSON
import json

# Conectar ao banco de dados
conn = sqlite3.connect('items.db')

# Definir a fábrica de linhas como dicionário
conn.row_factory = sqlite3.Row

# Criar um cursor
cursor = conn.cursor()

# Consultar dados
cursor.execute('SELECT * FROM item')
dados = cursor.fetchall()

# Criar uma lista para armazenar os registros
registros = []

# Converter cada objeto Row em um dicionário e adicionar à lista
for registro in dados:
    registros.append(dict(registro))

# Serializar os dados em formato JSON como uma string
json_string = json.dumps(registros)

# Exibir os dados JSON usando print()
print(json_string)

# Fechar a conexão com o banco de dados
conn.close()
