from db import get_db
from werkzeug.security import generate_password_hash
from mysql.connector import Error

# CRIA USUÁRIO TESTE
nome = 'Admin Loja'
email = 'admin@loja.com'
senha = '123456'

senha_hash = generate_password_hash(senha)

db = get_db()
if db:
    cursor = db.cursor()
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS login (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), email VARCHAR(255) UNIQUE, senha VARCHAR(255))")
        cursor.execute("INSERT IGNORE INTO login (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha_hash))
        db.commit()
        print(f"✅ USUÁRIO CRIADO!")
        print(f"📧 Email: {email}")
        print(f"🔑 Senha: {senha}")
        print("🎯 Vá para localhost:5000/login")
        cursor.execute("SELECT * FROM login")
        print("Tabela:", cursor.fetchall())
    except Error as e:
        print(f"Erro: {e}")
    finally:
        cursor.close()
        db.close()
else:
    print("❌ Erro conexão DB. Rode XAMPP MySQL.")
