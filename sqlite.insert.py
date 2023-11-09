# Importar a biblioteca sqlite3 para trabalhar com SQLite
import sqlite3

# Conectar ao banco de dados 'items.db' ou criá-lo se não existir
conn = sqlite3.connect('items.db')

# Criar um cursor para executar comandos SQL no banco de dados
cursor = conn.cursor()

# Definir a instrução SQL de inserção de dados
sql = "INSERT INTO item (name, description, location) VALUES (?, ?, ?)"

# Executar a instrução SQL de inserção, fornecendo os valores a serem inseridos
cursor.execute(sql, ('Bagulho', 'Apenas um bagulho', 'Em uma caixa'))

# Confirmar (commit) as alterações no banco de dados
conn.commit()

# Fechar a conexão com o banco de dados após a inserção
conn.close()
