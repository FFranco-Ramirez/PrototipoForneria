-- ================================================================
-- SCRIPT SQL: MODIFICAR TABLA DE ALERTAS SIN PERDER DATOS
-- ================================================================
--
-- Este script actualiza la tabla 'alertas' SIN borrarla.
-- MANTIENE todos los datos existentes.
--
-- INSTRUCCIONES:
-- 1. Abre phpMyAdmin o tu cliente MySQL
-- 2. Selecciona la base de datos 'forneria'
-- 3. Ejecuta este script completo
--
-- O desde la terminal:
-- mysql -u forneria_user -p forneria < modificar_alertas_sin_borrar.sql

USE forneria;

-- ================================================================
-- VERIFICAR Y MODIFICAR COLUMNAS (si es necesario)
-- ================================================================

-- Modificar tipo_alerta si no es ENUM correcto
ALTER TABLE `alertas` 
MODIFY COLUMN `tipo_alerta` enum('verde','amarilla','roja') NOT NULL;

-- Asegurar que mensaje sea varchar(255)
ALTER TABLE `alertas` 
MODIFY COLUMN `mensaje` varchar(255) NOT NULL;

-- Asegurar que fecha_generada tenga valor por defecto
ALTER TABLE `alertas` 
MODIFY COLUMN `fecha_generada` timestamp NULL DEFAULT CURRENT_TIMESTAMP;

-- Asegurar que estado tenga valor por defecto
ALTER TABLE `alertas` 
MODIFY COLUMN `estado` varchar(20) DEFAULT 'activa';

-- ================================================================
-- AGREGAR ÍNDICES (si no existen)
-- ================================================================

-- Índice para producto (si no existe)
-- Nota: Si ya existe, MySQL mostrará un warning pero no fallará
ALTER TABLE `alertas` ADD INDEX IF NOT EXISTS `idx_productos` (`productos_id`);

-- Índice para tipo de alerta
ALTER TABLE `alertas` ADD INDEX IF NOT EXISTS `idx_tipo_alerta` (`tipo_alerta`);

-- Índice para estado
ALTER TABLE `alertas` ADD INDEX IF NOT EXISTS `idx_estado` (`estado`);

-- Índice para fecha
ALTER TABLE `alertas` ADD INDEX IF NOT EXISTS `idx_fecha` (`fecha_generada`);

-- ================================================================
-- VERIFICAR/AGREGAR CLAVE FORÁNEA
-- ================================================================

-- Primero eliminar la constraint antigua si existe (puede tener otro nombre)
-- Nota: Si no existe, mostrará un error pero continuará
SET FOREIGN_KEY_CHECKS = 0;

-- Agregar la nueva constraint
ALTER TABLE `alertas`
ADD CONSTRAINT `fk_alertas_productos1` 
FOREIGN KEY (`productos_id`) 
REFERENCES `productos` (`id`)
ON DELETE CASCADE
ON UPDATE CASCADE;

SET FOREIGN_KEY_CHECKS = 1;

-- ================================================================
-- AGREGAR COMENTARIO A LA TABLA
-- ================================================================

ALTER TABLE `alertas` 
COMMENT 'Tabla de alertas de vencimiento de productos';

-- ================================================================
-- MENSAJE DE CONFIRMACIÓN
-- ================================================================

SELECT '✅ Tabla de alertas actualizada correctamente (SIN perder datos)' AS Resultado;
SELECT COUNT(*) AS 'Alertas existentes' FROM alertas;

