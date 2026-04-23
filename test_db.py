# Importa o conector do MySQL
import mysql.connector

# Importa a classe de erro do mysql.connector
from mysql.connector import Error


try:
    # Tenta abrir uma conexão com o banco
    connection = mysql.connector.connect(
        host='localhost',                  # Servidor local
        user='root',                       # Usuário root do XAMPP
        password='',                       # Senha vazia
        database='lojinha_da_marcela'      # Nome do banco
    )

    # Verifica se conectou corretamente
    if connection.is_connected():
        # Pega a versão do servidor MySQL/MariaDB
        db_info = connection.get_server_info()

        # Mostra no terminal a versão encontrada
        print("Connected to MySQL Server version ", db_info)

        # Cria um cursor
        # Cursor é o objeto usado para executar comandos SQL
        cursor = connection.cursor()

        # Executa um SQL simples para descobrir qual banco está em uso
        cursor.execute("SELECT DATABASE();")

        # fetchone() pega apenas uma linha do resultado
        record = cursor.fetchone()

        # Mostra o nome do banco conectado
        print("You're connected to database: ", record)

except Error as e:
    # Se der erro, mostra no terminal
    print("Error while connecting to MySQL", e)

finally:
    # Verifica se a variável connection existe e se ainda está conectada
    if 'connection' in locals() and connection.is_connected():
        # Fecha o cursor
        cursor.close()

        # Fecha a conexão com o banco
        connection.close()

        # Mostra no terminal que a conexão foi encerrada
        print("MySQL connection closed")
