-- CLEAN ROLES - Run in phpMyAdmin
USE lojinha_da_marcela;

UPDATE login SET tipo = 'vendedor' WHERE tipo NOT IN ('admin', 'vendedor');
DELETE FROM login WHERE tipo IS NULL OR tipo = '';

ALTER TABLE login MODIFY tipo ENUM('admin', 'vendedor', 'fornecedor') NOT NULL DEFAULT 'vendedor';

SELECT email, tipo FROM login;
