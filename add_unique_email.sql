# SQL - Torna email único (evita duplicados)
USE lojinha_da_marcela;

ALTER TABLE login ADD UNIQUE KEY unique_email (email);

-- Testar tabela
DESCRIBE login;
SELECT * FROM login;
