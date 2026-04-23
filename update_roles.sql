# UPDATE roles - Run in phpMyAdmin
USE lojinha_da_marcela;

ALTER TABLE login MODIFY tipo ENUM('admin','vendedor','financeiro') DEFAULT 'financeiro';

UPDATE login SET tipo = 'financeiro' WHERE tipo = 'usuario' OR tipo IS NULL;

SELECT email, tipo FROM login;
