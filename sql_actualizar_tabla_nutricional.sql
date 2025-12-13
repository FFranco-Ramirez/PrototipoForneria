-- ============================================================
-- Script para actualizar la tabla nutricional
-- Agrega los campos faltantes: azucares y sodio
-- ============================================================

USE forneria;

-- Agregar campo azucares
ALTER TABLE `nutricional` 
ADD COLUMN `azucares` DECIMAL(10,2) DEFAULT NULL AFTER `carbohidratos`;

-- Agregar campo sodio
ALTER TABLE `nutricional` 
ADD COLUMN `sodio` DECIMAL(10,2) DEFAULT NULL AFTER `azucares`;

-- Eliminar campo fibra (no se usa en el código)
ALTER TABLE `nutricional` DROP COLUMN `fibra`;

-- Verificar la estructura actualizada
DESCRIBE `nutricional`;

