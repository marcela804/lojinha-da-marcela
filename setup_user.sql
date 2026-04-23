# SQL teste - Execute no phpMyAdmin

-- Usuário teste (senha plain '123456' → hash abaixo)
INSERT INTO login (nome, email, senha) VALUES 
('Teste', 'teste@teste.com', '$2b$12$9g8p8XJ5vL8y3k.4N5m6P7Q.r8s9t0u1v2w3x4y5z6A7B8C9D0E1F');

-- Verificar usuários
SELECT * FROM login;

-- Deletar teste
DELETE FROM login WHERE email = 'teste@teste.com';

# Login teste: email='teste@teste.com', senha='123456'
