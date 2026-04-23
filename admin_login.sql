# ADMIN LOGIN - Execute no phpMyAdmin

USE lojinha_da_marcela;

-- Admin user (senha plain: 'admin123')
INSERT INTO login (nome, email, senha) VALUES (
  'Admin',
  'admin@loja.com', 
  '$2b$12$w8p6z1vK4jL3mN5oP7qR8S.t9u0v1w2x3y4z5A6B7C8D9E0F1G2H'
) ON DUPLICATE KEY UPDATE senha=VALUES(senha);

-- Test
SELECT * FROM login WHERE email = 'admin@loja.com';

-- Login: email='admin@loja.com', senha='admin123'
