-- ============================================================
-- SCRIPT DE MEJORAS: MOVIMIENTOS DE INVENTARIO
-- Sistema: Prototipo Fornería
-- Descripción: Agregar campos para rastrear origen de movimientos
-- ============================================================

-- Agregar campos para rastrear el origen de los movimientos
-- Esto permite saber si un movimiento viene de una compra, venta, ajuste, etc.

ALTER TABLE `movimientos_inventario`
ADD COLUMN `origen` VARCHAR(50) NULL COMMENT 'origen: compra, venta, ajuste, merma, devolucion',
ADD COLUMN `referencia_id` INT NULL COMMENT 'ID de la tabla origen (factura_proveedor, ventas, etc.)',
ADD COLUMN `tipo_referencia` VARCHAR(50) NULL COMMENT 'tipo: factura_proveedor, venta, ajuste, merma, etc.',
ADD INDEX `idx_origen` (`origen`, `tipo_referencia`, `referencia_id`);

