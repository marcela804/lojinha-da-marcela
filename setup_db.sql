-- CLEAN ROLES - Run in phpMyAdmin
USE lojinha_da_marcela;

UPDATE login SET tipo = 'vendedor' WHERE tipo IN ('usuario', 'financeiro') OR tipo IS NULL OR tipo = '';

ALTER TABLE login MODIFY tipo ENUM('admin', 'vendedor') NOT NULL DEFAULT 'vendedor';

SELECT email, tipo FROM login;
