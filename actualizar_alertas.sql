-- ================================================================
-- SCRIPT SQL: ACTUALIZAR TABLA DE ALERTAS
-- ================================================================
--
-- Este script actualiza la tabla 'alertas' en la base de datos forneria
-- para que funcione correctamente con el sistema de alertas de Django.
--
-- INSTRUCCIONES:
-- 1. Abre MySQL Workbench, phpMyAdmin o tu cliente MySQL
-- 2. Selecciona la base de datos 'forneria'
-- 3. Ejecuta este script completo
--
-- O desde la terminal:
-- mysql -u forneria_user -p forneria < actualizar_alertas.sql

USE forneria;

-- Eliminar la tabla anterior si existe (CUIDADO: Esto borra los datos)
DROP TABLE IF EXISTS `alertas`;

-- Crear la tabla de alertas mejorada
CREATE TABLE `alertas` (
  `id` int NOT NULL AUTO_INCREMENT,
  
  -- Tipo de alerta según días hasta vencimiento
  -- verde: 30+ días, amarilla: 14-29 días, roja: 0-13 días
  `tipo_alerta` enum('verde','amarilla','roja') NOT NULL,
  
  -- Mensaje descriptivo de la alerta
  `mensaje` varchar(255) NOT NULL,
  
  -- Fecha cuando se generó la alerta (automático)
  `fecha_generada` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  
  -- Estado de la alerta: activa, resuelta, ignorada
  `estado` varchar(20) DEFAULT 'activa',
  
  -- Relación con el producto que generó la alerta
  `productos_id` int NOT NULL,
  
  -- Llave primaria
  PRIMARY KEY (`id`),
  
  -- Índice para buscar por producto rápidamente
  KEY `idx_productos` (`productos_id`),
  
  -- Índice para filtrar por tipo de alerta
  KEY `idx_tipo_alerta` (`tipo_alerta`),
  
  -- Índice para filtrar por estado
  KEY `idx_estado` (`estado`),
  
  -- Índice para ordenar por fecha
  KEY `idx_fecha` (`fecha_generada`),
  
  -- Clave foránea: conecta con la tabla productos
  CONSTRAINT `fk_alertas_productos1` 
    FOREIGN KEY (`productos_id`) 
    REFERENCES `productos` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Comentario descriptivo para la tabla
ALTER TABLE `alertas` 
  COMMENT 'Tabla de alertas de vencimiento de productos';

-- Mensaje de confirmación
SELECT 'Tabla de alertas actualizada correctamente' AS Resultado;

