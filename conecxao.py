# Importa a biblioteca para conectar no MySQL
import mysql.connector

# Função que cria e retorna a conexão com o banco
def conectar_db():
    conexao = mysql.connector.connect(
        host="localhost",         # Endereço do banco
        user="root",              # Usuário do MySQL
        password="",              # Senha do MySQL (no XAMPP geralmente é vazia)
        database="lojinha_da_marcela"  # Nome do seu banco de dados
    )

    # Retorna a conexão pronta para usar
    return conexao
