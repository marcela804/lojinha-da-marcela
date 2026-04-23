import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash

# Hash exato
senha = '123456'
hash_senha = generate_password_hash(senha)
print(f"SENHA PLAIN: {senha}")
print(f"HASH GERADO: {hash_senha}")

# Conecta direto
try:
    con = mysql.connector.connect(host="localhost", user="root", password="", database="lojinha_da_marcela")
    cursor = con.cursor()
    
    # Cria tabela se não existir
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS login (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255),
        email VARCHAR(255) UNIQUE,
        senha TEXT
    )
    """)
    
    # Limpa e insere
    cursor.execute("DELETE FROM login WHERE email = 'admin@loja.com'")
    cursor.execute("INSERT INTO login (nome, email, senha) VALUES (%s, %s, %s)", 
                   ('Admin Loja', 'admin@loja.com', hash_senha))
    con.commit()
    
    # Verifica
    cursor.execute("SELECT id, nome, email FROM login WHERE email = 'admin@loja.com'")
    user = cursor.fetchone()
    print("✅ USUÁRIO CRIADO:", user)
    
except Error as e:
    print("❌ ERRO:", e)
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'con' in locals():
        con.close()

print("\n🎯 LOGIN:")
print("Email: admin@loja.com")
print("Senha: 123456")
print("\nPronto para localhost:5000/login!")
