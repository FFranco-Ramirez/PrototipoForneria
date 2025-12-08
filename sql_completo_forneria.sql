-- ============================================================
-- SCRIPT COMPLETO: BASE DE DATOS FORNERÍA
-- Sistema: Prototipo Fornería
-- Descripción: Script maestro para crear la base de datos completa
-- Fecha: Actualizado hoy
-- ============================================================
--
-- INSTRUCCIONES:
-- 1. Crear base de datos: CREATE DATABASE forneria;
-- 2. Usar base de datos: USE forneria;
-- 3. Ejecutar este script completo
--
-- ============================================================

-- ============================================================
-- CONFIGURACIÓN INICIAL
-- ============================================================

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================================
-- PARTE 1: TABLAS BASE DEL SISTEMA
-- ============================================================

-- Tabla: categorias
DROP TABLE IF EXISTS `categorias`;
CREATE TABLE IF NOT EXISTS `categorias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `descripcion` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- Tabla: nutricional
DROP TABLE IF EXISTS `nutricional`;
CREATE TABLE IF NOT EXISTS `nutricional` (
  `id` int NOT NULL AUTO_INCREMENT,
  `calorias` decimal(10,2) DEFAULT NULL,
  `proteinas` decimal(10,2) DEFAULT NULL,
  `grasas` decimal(10,2) DEFAULT NULL,
  `carbohidratos` decimal(10,2) DEFAULT NULL,
  `azucares` decimal(10,2) DEFAULT NULL,
  `sodio` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- Tabla: productos
DROP TABLE IF EXISTS `productos`;
CREATE TABLE IF NOT EXISTS `productos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(300) DEFAULT NULL,
  `marca` varchar(100) DEFAULT NULL,
  `precio` decimal(10,2) NOT NULL,
  `caducidad` date NOT NULL,
  `elaboracion` date DEFAULT NULL,
  `tipo` varchar(100) DEFAULT NULL,
  `stock_actual` int DEFAULT NULL,
  `stock_minimo` int DEFAULT NULL,
  `stock_maximo` int DEFAULT NULL,
  `presentacion` varchar(100) DEFAULT NULL,
  `formato` varchar(100) DEFAULT NULL,
  `creado` timestamp NULL DEFAULT NULL,
  `modificado` timestamp NULL DEFAULT NULL,
  `eliminado` timestamp NULL DEFAULT NULL,
  `categorias_id` int NOT NULL,
  `nutricional_id` int NOT NULL,
  `cantidad` int NOT NULL DEFAULT '0',
  `estado_merma` varchar(20) NOT NULL DEFAULT 'activo' COMMENT 'Estado del producto: activo, vencido, deteriorado, dañado',
  PRIMARY KEY (`id`),
  KEY `fk_productos_categorias1_idx` (`categorias_id`),
  KEY `fk_productos_nutricional1_idx` (`nutricional_id`),
  CONSTRAINT `fk_productos_categorias1` FOREIGN KEY (`categorias_id`) REFERENCES `categorias` (`id`),
  CONSTRAINT `fk_productos_nutricional1` FOREIGN KEY (`nutricional_id`) REFERENCES `nutricional` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- Tabla: alertas
DROP TABLE IF EXISTS `alertas`;
CREATE TABLE IF NOT EXISTS `alertas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo_alerta` enum('verde','amarilla','roja') NOT NULL,
  `mensaje` varchar(255) NOT NULL,
  `fecha_generada` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `estado` varchar(20) DEFAULT 'activa',
  `productos_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_alertas_productos1_idx` (`productos_id`),
  KEY `idx_tipo_alerta` (`tipo_alerta`),
  KEY `idx_estado` (`estado`),
  KEY `idx_fecha` (`fecha_generada`),
  CONSTRAINT `fk_alertas_productos1` FOREIGN KEY (`productos_id`) REFERENCES `productos` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- Tabla: clientes
DROP TABLE IF EXISTS `clientes`;
CREATE TABLE IF NOT EXISTS `clientes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rut` varchar(12) DEFAULT NULL,
  `nombre` varchar(150) NOT NULL,
  `correo` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- Tabla: ventas
DROP TABLE IF EXISTS `ventas`;
CREATE TABLE IF NOT EXISTS `ventas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha` timestamp NOT NULL,
  `total_sin_iva` decimal(10,2) NOT NULL,
  `total_iva` decimal(10,2) NOT NULL,
  `descuento` decimal(10,2) NOT NULL,
  `total_con_iva` decimal(10,2) NOT NULL,
  `canal_venta` enum('presencial','delivery') NOT NULL,
  `folio` varchar(20) DEFAULT NULL,
  `monto_pagado` decimal(10,2) DEFAULT NULL,
  `vuelto` decimal(10,2) DEFAULT NULL,
  `clientes_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_ventas_clientes1_idx` (`clientes_id`),
  CONSTRAINT `fk_ventas_clientes1` FOREIGN KEY (`clientes_id`) REFERENCES `clientes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- Tabla: detalle_venta
DROP TABLE IF EXISTS `detalle_venta`;
CREATE TABLE IF NOT EXISTS `detalle_venta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cantidad` int NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `descuento_pct` decimal(5,2) DEFAULT '0.00',
  `ventas_id` int NOT NULL,
  `productos_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_detalle_venta_ventas1_idx` (`ventas_id`),
  KEY `fk_detalle_venta_productos1_idx` (`productos_id`),
  CONSTRAINT `fk_detalle_venta_productos1` FOREIGN KEY (`productos_id`) REFERENCES `productos` (`id`),
  CONSTRAINT `fk_detalle_venta_ventas1` FOREIGN KEY (`ventas_id`) REFERENCES `ventas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- Tabla: movimientos_inventario (con campos de trazabilidad)
DROP TABLE IF EXISTS `movimientos_inventario`;
CREATE TABLE IF NOT EXISTS `movimientos_inventario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo_movimiento` enum('entrada','salida') NOT NULL,
  `cantidad` int NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `productos_id` int NOT NULL,
  `origen` varchar(50) DEFAULT NULL COMMENT 'origen: compra, venta, ajuste, merma, devolucion',
  `referencia_id` int DEFAULT NULL COMMENT 'ID de la tabla origen (factura_proveedor, ventas, etc.)',
  `tipo_referencia` varchar(50) DEFAULT NULL COMMENT 'tipo: factura_proveedor, venta, ajuste, merma, etc.',
  PRIMARY KEY (`id`),
  KEY `fk_movimientos_inventario_productos1_idx` (`productos_id`),
  KEY `idx_origen` (`origen`, `tipo_referencia`, `referencia_id`),
  CONSTRAINT `fk_movimientos_inventario_productos1` FOREIGN KEY (`productos_id`) REFERENCES `productos` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- ============================================================
-- PARTE 2: TABLAS DE PROVEEDORES Y FACTURAS
-- ============================================================

-- Tabla: proveedor
DROP TABLE IF EXISTS `proveedor`;
CREATE TABLE IF NOT EXISTS `proveedor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) NOT NULL COMMENT 'Razón social o nombre del proveedor',
  `rut` varchar(12) DEFAULT NULL COMMENT 'RUT del proveedor (formato: 12345678-9)',
  `contacto` varchar(100) DEFAULT NULL COMMENT 'Nombre de la persona de contacto',
  `telefono` varchar(20) DEFAULT NULL COMMENT 'Teléfono de contacto',
  `email` varchar(100) DEFAULT NULL COMMENT 'Correo electrónico',
  `direccion` varchar(200) DEFAULT NULL COMMENT 'Dirección del proveedor',
  `ciudad` varchar(100) DEFAULT NULL COMMENT 'Ciudad',
  `region` varchar(100) DEFAULT NULL COMMENT 'Región',
  `estado` enum('activo','inactivo') NOT NULL DEFAULT 'activo' COMMENT 'Estado del proveedor',
  `notas` text DEFAULT NULL COMMENT 'Notas adicionales sobre el proveedor',
  `creado` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creación del registro',
  `modificado` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Fecha de última modificación',
  `eliminado` timestamp NULL DEFAULT NULL COMMENT 'Fecha de eliminación lógica',
  PRIMARY KEY (`id`),
  UNIQUE KEY `rut_UNIQUE` (`rut`),
  KEY `idx_estado` (`estado`),
  KEY `idx_nombre` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci
COMMENT='Tabla de proveedores de la fornería';

-- Tabla: factura_proveedor
DROP TABLE IF EXISTS `factura_proveedor`;
CREATE TABLE IF NOT EXISTS `factura_proveedor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `numero_factura` varchar(50) NOT NULL COMMENT 'Número de factura del proveedor',
  `fecha_factura` date NOT NULL COMMENT 'Fecha de emisión de la factura',
  `fecha_vencimiento` date DEFAULT NULL COMMENT 'Fecha de vencimiento para pago',
  `fecha_recepcion` date DEFAULT NULL COMMENT 'Fecha en que se recibió la factura',
  `subtotal_sin_iva` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Subtotal sin IVA',
  `descuento` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Descuento global aplicado',
  `total_iva` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Total de IVA (19%)',
  `total_con_iva` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Total con IVA',
  `estado_pago` enum('pendiente','parcial','pagado','cancelado') NOT NULL DEFAULT 'pendiente' COMMENT 'Estado del pago',
  `estado_recepcion` enum('pendiente','recibida','cancelada') NOT NULL DEFAULT 'pendiente' COMMENT 'Estado de recepción de la factura',
  `observaciones` text DEFAULT NULL COMMENT 'Observaciones adicionales',
  `creado` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creación',
  `modificado` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Fecha de última modificación',
  `eliminado` timestamp NULL DEFAULT NULL COMMENT 'Fecha de eliminación lógica',
  `proveedor_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_factura_UNIQUE` (`numero_factura`),
  KEY `fk_factura_proveedor_proveedor1_idx` (`proveedor_id`),
  KEY `idx_estado_pago` (`estado_pago`),
  KEY `idx_estado_recepcion` (`estado_recepcion`),
  KEY `idx_fecha_factura` (`fecha_factura`),
  CONSTRAINT `fk_factura_proveedor_proveedor1` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedor` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci
COMMENT='Tabla de facturas de compra a proveedores';

-- Tabla: detalle_factura_proveedor
DROP TABLE IF EXISTS `detalle_factura_proveedor`;
CREATE TABLE IF NOT EXISTS `detalle_factura_proveedor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cantidad` int NOT NULL COMMENT 'Cantidad de productos',
  `precio_unitario` decimal(10,2) NOT NULL COMMENT 'Precio unitario del producto',
  `descuento_pct` decimal(5,2) DEFAULT '0.00' COMMENT 'Descuento porcentual aplicado',
  `subtotal` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Subtotal del detalle (cantidad * precio_unitario - descuento)',
  `factura_proveedor_id` int NOT NULL,
  `productos_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_detalle_factura_proveedor_factura_proveedor1_idx` (`factura_proveedor_id`),
  KEY `fk_detalle_factura_proveedor_productos1_idx` (`productos_id`),
  CONSTRAINT `fk_detalle_factura_proveedor_factura_proveedor1` FOREIGN KEY (`factura_proveedor_id`) REFERENCES `factura_proveedor` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_detalle_factura_proveedor_productos1` FOREIGN KEY (`productos_id`) REFERENCES `productos` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci
COMMENT='Detalle de productos en cada factura de proveedor';

-- Tabla: pago_proveedor
DROP TABLE IF EXISTS `pago_proveedor`;
CREATE TABLE IF NOT EXISTS `pago_proveedor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `monto` decimal(10,2) NOT NULL COMMENT 'Monto del pago',
  `fecha_pago` date NOT NULL COMMENT 'Fecha en que se realizó el pago',
  `metodo_pago` enum('efectivo','transferencia','cheque','tarjeta') DEFAULT 'efectivo' COMMENT 'Método de pago utilizado',
  `numero_comprobante` varchar(50) DEFAULT NULL COMMENT 'Número de comprobante o referencia del pago',
  `observaciones` text DEFAULT NULL COMMENT 'Observaciones sobre el pago',
  `creado` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creación del registro',
  `factura_proveedor_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_pago_proveedor_factura_proveedor1_idx` (`factura_proveedor_id`),
  CONSTRAINT `fk_pago_proveedor_factura_proveedor1` FOREIGN KEY (`factura_proveedor_id`) REFERENCES `factura_proveedor` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci
COMMENT='Registro de pagos realizados a proveedores';

-- ============================================================
-- PARTE 3: TABLAS DE USUARIOS Y ROLES
-- ============================================================

-- Tabla: direccion
DROP TABLE IF EXISTS `direccion`;
CREATE TABLE IF NOT EXISTS `direccion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `calle` varchar(100) NOT NULL,
  `numero` varchar(10) NOT NULL,
  `depto` varchar(10) DEFAULT NULL,
  `comuna` varchar(100) NOT NULL,
  `region` varchar(100) NOT NULL,
  `codigo_postal` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- Tabla: roles
DROP TABLE IF EXISTS `roles`;
CREATE TABLE IF NOT EXISTS `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- Tabla: usuarios
DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `run` varchar(10) NOT NULL,
  `fono` int DEFAULT NULL,
  `Direccion_id` int NOT NULL,
  `Roles_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `run_UNIQUE` (`run`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`),
  KEY `fk_Usuarios_Direccion1_idx` (`Direccion_id`),
  KEY `fk_Usuarios_Roles1_idx` (`Roles_id`),
  CONSTRAINT `fk_Usuarios_Direccion1` FOREIGN KEY (`Direccion_id`) REFERENCES `direccion` (`id`),
  CONSTRAINT `fk_Usuarios_Roles1` FOREIGN KEY (`Roles_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- ============================================================
-- PARTE 4: DATOS INICIALES
-- ============================================================

-- Insertar roles básicos
INSERT IGNORE INTO `roles` (`id`, `nombre`, `descripcion`) VALUES
(1, 'Vendedor', 'Puede realizar ventas y ver inventario'),
(2, 'Contador', 'Puede ver reportes, ventas e inventario'),
(3, 'Administrador', 'Acceso completo al sistema');

-- Insertar categorías de ejemplo (opcional)
INSERT IGNORE INTO `categorias` (`id`, `nombre`, `descripcion`) VALUES
(1, 'Panadería', 'Productos de panadería'),
(2, 'Pastelería', 'Productos de pastelería'),
(3, 'Bebidas', 'Bebidas varias');

-- Insertar información nutricional básica (opcional)
INSERT IGNORE INTO `nutricional` (`id`, `calorias`, `proteinas`, `carbohidratos`, `grasas`, `fibra`) VALUES
(1, 0, 0.00, 0.00, 0.00, 0.00);

-- Insertar cliente genérico (para ventas sin cliente específico)
INSERT IGNORE INTO `clientes` (`id`, `rut`, `nombre`, `correo`) VALUES
(1, NULL, 'Cliente Genérico', NULL);

-- ============================================================
-- FINALIZACIÓN
-- ============================================================

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- VERIFICACIÓN
-- ============================================================

-- Ver todas las tablas creadas
-- SHOW TABLES;

-- Verificar roles insertados
-- SELECT * FROM roles;

-- Verificar estructura de movimientos_inventario
-- DESCRIBE movimientos_inventario;

-- ============================================================
-- FIN DEL SCRIPT
-- ============================================================

