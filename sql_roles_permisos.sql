-- ============================================================
-- SCRIPT: INICIALIZACIÓN DE ROLES Y PERMISOS
-- Sistema: Prototipo Fornería
-- Descripción: Crear roles según RF-S1 del Jira
-- ============================================================

-- ============================================================
-- INSERTAR ROLES EN LA TABLA roles
-- ============================================================

-- Insertar roles si no existen
INSERT IGNORE INTO `roles` (`id`, `nombre`, `descripcion`) VALUES
(1, 'Vendedor', 'Puede realizar ventas y ver inventario'),
(2, 'Contador', 'Puede ver reportes, ventas e inventario'),
(3, 'Administrador', 'Acceso completo al sistema');

-- ============================================================
-- CREAR GRUPOS EN DJANGO (Opcional - se puede hacer desde admin)
-- ============================================================
-- Los grupos de Django se pueden crear desde el admin o con un script Python
-- Este SQL solo crea los roles en la tabla 'roles' que ya existe

-- ============================================================
-- NOTAS
-- ============================================================
-- 
-- Los roles se relacionan con usuarios a través de:
-- 1. Tabla 'usuarios' -> campo 'roles_id' -> tabla 'roles'
-- 2. O usando grupos de Django (auth_group)
--
-- Para asignar un rol a un usuario:
-- UPDATE usuarios SET Roles_id = 1 WHERE user_id = [ID_USUARIO];
--
-- O desde Django admin:
-- - Ir a Usuarios -> Seleccionar usuario -> Asignar rol

