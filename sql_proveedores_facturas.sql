-- ============================================================
-- SCRIPT DE CREACIÓN: TABLAS DE PROVEEDORES Y FACTURAS
-- Sistema: Prototipo Fornería
-- Descripción: Estructura completa para gestión de proveedores
--               y facturas de compra de productos
-- ============================================================

-- --------------------------------------------------------
-- Tabla: `proveedor`
-- Descripción: Almacena información de los proveedores
-- Cardinalidad con factura_proveedor: 1 a N (uno a muchos)
-- --------------------------------------------------------

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='Tabla de proveedores de la fornería';

-- --------------------------------------------------------
-- Tabla: `factura_proveedor`
-- Descripción: Almacena las facturas de compra a proveedores
-- Cardinalidad con proveedor: N a 1 (muchos a uno)
-- Cardinalidad con detalle_factura_proveedor: 1 a N (uno a muchos)
-- --------------------------------------------------------

DROP TABLE IF EXISTS `factura_proveedor`;
CREATE TABLE IF NOT EXISTS `factura_proveedor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `numero_factura` varchar(50) NOT NULL COMMENT 'Número de factura del proveedor',
  `fecha_factura` date NOT NULL COMMENT 'Fecha de emisión de la factura',
  `fecha_vencimiento` date DEFAULT NULL COMMENT 'Fecha de vencimiento para pago',
  `fecha_recepcion` date DEFAULT NULL COMMENT 'Fecha en que se recibió la factura',
  `estado_recepcion` enum('pendiente','recibida','parcial','cancelada') NOT NULL DEFAULT 'pendiente' COMMENT 'Estado de recepción física de la factura',
  `subtotal` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Subtotal sin IVA',
  `iva` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Monto de IVA',
  `descuento` decimal(10,2) DEFAULT '0.00' COMMENT 'Descuento aplicado',
  `total` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Total a pagar',
  `estado_pago` enum('pendiente','pagado','parcial','cancelado') NOT NULL DEFAULT 'pendiente' COMMENT 'Estado del pago',
  `fecha_pago` date DEFAULT NULL COMMENT 'Fecha en que se realizó el pago',
  `metodo_pago` varchar(50) DEFAULT NULL COMMENT 'Método de pago (transferencia, efectivo, cheque, etc.)',
  `observaciones` text DEFAULT NULL COMMENT 'Observaciones sobre la factura',
  `proveedor_id` int NOT NULL COMMENT 'Referencia al proveedor',
  `creado` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creación del registro',
  `modificado` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Fecha de última modificación',
  `eliminado` timestamp NULL DEFAULT NULL COMMENT 'Fecha de eliminación lógica',
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_factura_proveedor_UNIQUE` (`numero_factura`, `proveedor_id`),
  KEY `fk_factura_proveedor_proveedor1_idx` (`proveedor_id`),
  KEY `idx_fecha_factura` (`fecha_factura`),
  KEY `idx_estado_pago` (`estado_pago`),
  KEY `idx_estado_recepcion` (`estado_recepcion`),
  KEY `idx_fecha_vencimiento` (`fecha_vencimiento`),
  CONSTRAINT `fk_factura_proveedor_proveedor1`
    FOREIGN KEY (`proveedor_id`)
    REFERENCES `proveedor` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='Tabla de facturas de compra a proveedores';

-- --------------------------------------------------------
-- Tabla: `detalle_factura_proveedor`
-- Descripción: Tabla intermedia que relaciona facturas con productos
-- Cardinalidad con factura_proveedor: N a 1 (muchos a uno)
-- Cardinalidad con productos: N a 1 (muchos a uno)
-- Relación N:M entre factura_proveedor y productos
-- --------------------------------------------------------

DROP TABLE IF EXISTS `detalle_factura_proveedor`;
CREATE TABLE IF NOT EXISTS `detalle_factura_proveedor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cantidad` int NOT NULL COMMENT 'Cantidad de productos recibidos',
  `precio_unitario` decimal(10,2) NOT NULL COMMENT 'Precio unitario de compra',
  `descuento_pct` decimal(5,2) DEFAULT '0.00' COMMENT 'Porcentaje de descuento aplicado',
  `subtotal` decimal(10,2) NOT NULL COMMENT 'Subtotal del detalle (cantidad * precio_unitario * (1 - descuento_pct/100))',
  `fecha_vencimiento_producto` date DEFAULT NULL COMMENT 'Fecha de vencimiento del lote recibido',
  `lote` varchar(50) DEFAULT NULL COMMENT 'Número de lote del producto',
  `observaciones` varchar(300) DEFAULT NULL COMMENT 'Observaciones sobre este detalle',
  `factura_proveedor_id` int NOT NULL COMMENT 'Referencia a la factura',
  `productos_id` int NOT NULL COMMENT 'Referencia al producto',
  `creado` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creación del registro',
  `modificado` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Fecha de última modificación',
  PRIMARY KEY (`id`),
  KEY `fk_detalle_factura_proveedor_factura_proveedor1_idx` (`factura_proveedor_id`),
  KEY `fk_detalle_factura_proveedor_productos1_idx` (`productos_id`),
  KEY `idx_cantidad` (`cantidad`),
  CONSTRAINT `fk_detalle_factura_proveedor_factura_proveedor1`
    FOREIGN KEY (`factura_proveedor_id`)
    REFERENCES `factura_proveedor` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_detalle_factura_proveedor_productos1`
    FOREIGN KEY (`productos_id`)
    REFERENCES `productos` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='Detalle de productos en cada factura de proveedor';

-- ============================================================
-- DATOS DE EJEMPLO (OPCIONAL - COMENTAR SI NO SE DESEAN)
-- ============================================================

-- INSERT INTO `proveedor` (`nombre`, `rut`, `contacto`, `telefono`, `email`, `direccion`, `ciudad`, `region`, `estado`) VALUES
-- ('Distribuidora de Harinas S.A.', '76543210-8', 'Juan Pérez', '+56912345678', 'contacto@harinas.cl', 'Av. Principal 123', 'Santiago', 'Región Metropolitana', 'activo'),
-- ('Insumos Panadería Ltda.', '12345678-9', 'María González', '+56987654321', 'ventas@insumos.cl', 'Calle Secundaria 456', 'Valparaíso', 'Región de Valparaíso', 'activo'),
-- ('Proveedora de Ingredientes', '98765432-1', 'Carlos Rodríguez', '+56911223344', 'info@ingredientes.cl', 'Pasaje Industrial 789', 'Concepción', 'Región del Biobío', 'activo');

-- ============================================================
-- ÍNDICES ADICIONALES PARA OPTIMIZACIÓN
-- ============================================================

-- Índice compuesto para búsquedas frecuentes de facturas por proveedor y fecha
CREATE INDEX `idx_proveedor_fecha` ON `factura_proveedor` (`proveedor_id`, `fecha_factura`);

-- Índice para búsquedas de facturas pendientes de pago
CREATE INDEX `idx_pendientes_vencimiento` ON `factura_proveedor` (`estado_pago`, `fecha_vencimiento`);

-- ============================================================
-- TABLA: PAGOS PARCIALES
-- ============================================================
-- Esta tabla permite registrar pagos parciales a facturas
-- Un proveedor puede pagar una factura en múltiples cuotas

CREATE TABLE IF NOT EXISTS `pago_proveedor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `factura_proveedor_id` int NOT NULL,
  `monto` decimal(10,2) NOT NULL COMMENT 'Monto del pago',
  `fecha_pago` date NOT NULL COMMENT 'Fecha en que se realizó el pago',
  `metodo_pago` varchar(50) DEFAULT NULL COMMENT 'Método de pago utilizado',
  `comprobante` varchar(100) DEFAULT NULL COMMENT 'Número de comprobante o referencia',
  `observaciones` text DEFAULT NULL COMMENT 'Observaciones sobre el pago',
  `creado` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `modificado` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_pago_proveedor_factura_idx` (`factura_proveedor_id`),
  KEY `idx_fecha_pago` (`fecha_pago`),
  CONSTRAINT `fk_pago_proveedor_factura`
    FOREIGN KEY (`factura_proveedor_id`)
    REFERENCES `factura_proveedor` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='Pagos realizados a facturas de proveedores (permite pagos parciales)';

-- ============================================================
-- MEJORAS A LA TABLA MOVIMIENTOS_INVENTARIO
-- ============================================================
-- Agregar campos para rastrear el origen de los movimientos
-- Esto permite saber si un movimiento viene de una compra, venta, ajuste, etc.

-- NOTA: Esta modificación debe ejecutarse en la tabla existente
-- ALTER TABLE `movimientos_inventario`
-- ADD COLUMN `origen` VARCHAR(50) NULL COMMENT 'origen: compra, venta, ajuste, merma, devolucion',
-- ADD COLUMN `referencia_id` INT NULL COMMENT 'ID de la tabla origen (factura_proveedor, ventas, etc.)',
-- ADD COLUMN `tipo_referencia` VARCHAR(50) NULL COMMENT 'tipo: factura_proveedor, venta, ajuste, etc.',
-- ADD INDEX `idx_origen` (`origen`, `tipo_referencia`, `referencia_id`);

-- ============================================================
-- COMENTARIOS SOBRE CARDINALIDADES Y RELACIONES
-- ============================================================
-- 
-- PROVEEDOR (1) ────< FACTURA_PROVEEDOR (N)
--   - Un proveedor puede tener muchas facturas
--   - Una factura pertenece a un solo proveedor
--   - Relación: Uno a Muchos (1:N)
--   - Foreign Key: factura_proveedor.proveedor_id -> proveedor.id
--   - ON DELETE: RESTRICT (no se puede eliminar proveedor con facturas)
--   - ON UPDATE: CASCADE (si cambia el ID del proveedor, se actualiza en facturas)
--
-- FACTURA_PROVEEDOR (1) ────< DETALLE_FACTURA_PROVEEDOR (N)
--   - Una factura puede tener muchos detalles (productos)
--   - Un detalle pertenece a una sola factura
--   - Relación: Uno a Muchos (1:N)
--   - Foreign Key: detalle_factura_proveedor.factura_proveedor_id -> factura_proveedor.id
--   - ON DELETE: CASCADE (si se elimina la factura, se eliminan sus detalles)
--   - ON UPDATE: CASCADE
--
-- PRODUCTOS (1) ────< DETALLE_FACTURA_PROVEEDOR (N)
--   - Un producto puede aparecer en muchos detalles de factura
--   - Un detalle corresponde a un solo producto
--   - Relación: Uno a Muchos (1:N)
--   - Foreign Key: detalle_factura_proveedor.productos_id -> productos.id
--   - ON DELETE: RESTRICT (no se puede eliminar producto con detalles de factura)
--   - ON UPDATE: CASCADE
--
-- RELACIÓN N:M ENTRE FACTURA_PROVEEDOR Y PRODUCTOS
--   - Se implementa a través de la tabla intermedia detalle_factura_proveedor
--   - Una factura puede contener múltiples productos
--   - Un producto puede venir en múltiples facturas
--   - La tabla detalle_factura_proveedor almacena la cantidad y precio específico
--     de cada producto en cada factura
--
-- ============================================================
-- LÓGICA DE NEGOCIO RECOMENDADA
-- ============================================================
--
-- 1. REGISTRO DE PROVEEDOR:
--    - Se crea el proveedor con estado 'activo'
--    - El RUT debe ser único
--    - Se puede marcar como 'inactivo' sin eliminar (eliminación lógica)
--
-- 2. REGISTRO DE FACTURA:
--    - Al crear una factura, se debe calcular el total sumando los detalles
--    - El número de factura debe ser único por proveedor
--    - Estado inicial: 'pendiente'
--    - Al marcar como 'pagado', se debe registrar fecha_pago
--
-- 3. REGISTRO DE DETALLE DE FACTURA:
--    - Al agregar un detalle, se debe actualizar el stock del producto
--    - El subtotal se calcula: cantidad * precio_unitario * (1 - descuento_pct/100)
--    - Se debe actualizar el total de la factura sumando todos los detalles
--    - Si el producto tiene fecha_vencimiento en el detalle, actualizar el producto
--
-- 4. ACTUALIZACIÓN DE STOCK:
--    - Cuando se recibe una factura (fecha_recepcion), se debe:
--      a) Actualizar stock_actual del producto sumando la cantidad recibida
--      b) Actualizar cantidad del producto
--      c) Si hay fecha_vencimiento_producto, actualizar caducidad del producto
--
-- 5. CONTROL DE PAGOS:
--    - Facturas con fecha_vencimiento próxima deben generar alertas
--    - Reportes de facturas pendientes por proveedor
--    - Historial de pagos por proveedor
--
-- 6. ELIMINACIÓN LÓGICA:
--    - No se eliminan físicamente los registros
--    - Se marca con timestamp en campo 'eliminado'
--    - Las consultas deben filtrar WHERE eliminado IS NULL
--
-- ============================================================

