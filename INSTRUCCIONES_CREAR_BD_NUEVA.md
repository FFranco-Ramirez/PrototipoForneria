# 🗄️ Instrucciones para Crear Base de Datos Nueva

## 📋 Resumen

Esta guía es para cuando **NO tienes la base de datos aún** o quieres crear una nueva desde cero.

---

## 🚀 PASOS PARA CREAR LA BASE DE DATOS

### Paso 1: Crear la base de datos

#### Método A: phpMyAdmin (Recomendado) ⭐

1. Abre phpMyAdmin: `http://localhost/phpmyadmin`
2. Haz clic en **"Nueva"** (arriba, en el menú)
3. **Nombre de la base de datos**: `forneria`
4. **Intercalación**: Selecciona `utf8mb4_spanish_ci`
5. Haz clic en **"Crear"**
6. ✅ Listo, la base de datos está creada

#### Método B: Línea de comandos

```bash
mysql -u forneria_user -p
```

Luego ejecuta:
```sql
CREATE DATABASE forneria CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci;
```

---

### Paso 2: Ejecutar el script completo

**Script**: `sql_completo_forneria.sql`

Este script crea:
- ✅ Todas las tablas necesarias
- ✅ Relaciones (foreign keys)
- ✅ Índices para optimización
- ✅ Datos iniciales (roles, categorías, cliente genérico)

#### Método A: phpMyAdmin (Más fácil) ⭐

1. En phpMyAdmin, selecciona la base de datos `forneria` (recién creada)
2. Haz clic en la pestaña **"Importar"** (arriba)
3. Haz clic en **"Elegir archivo"**
4. Selecciona: `sql_completo_forneria.sql`
5. Haz clic en **"Continuar"** (abajo)
6. ✅ Espera a que termine (puede tardar unos segundos)
7. Deberías ver: **"La importación se ha finalizado correctamente"**

#### Método B: Línea de comandos

```bash
mysql -u forneria_user -p forneria < sql_completo_forneria.sql
```

Te pedirá la contraseña: `Ventana$123` (o la que tengas configurada)

---

### Paso 3: Verificar que todo se creó correctamente

#### En phpMyAdmin:
1. Selecciona la base de datos `forneria`
2. En el panel izquierdo deberías ver todas las tablas

#### En línea de comandos:
```sql
USE forneria;
SHOW TABLES;
```

**Deberías ver estas tablas** (al menos 15 tablas):
- `alertas`
- `categorias`
- `clientes`
- `detalle_factura_proveedor`
- `detalle_venta`
- `direccion`
- `factura_proveedor`
- `movimientos_inventario`
- `nutricional`
- `pago_proveedor`
- `productos`
- `proveedor`
- `roles`
- `usuarios`
- `ventas`

---

### Paso 4: Verificar datos iniciales

```sql
-- Verificar roles insertados
SELECT * FROM roles;
-- Deberías ver: Vendedor, Contador, Administrador

-- Verificar categorías
SELECT * FROM categorias;
-- Deberías ver: Panadería, Pastelería, Bebidas

-- Verificar cliente genérico
SELECT * FROM clientes;
-- Deberías ver: Cliente Genérico

-- Verificar estructura de movimientos_inventario
DESCRIBE movimientos_inventario;
-- Deberías ver las columnas: origen, referencia_id, tipo_referencia
```

---

### Paso 5: Verificar y crear superusuario de Django

#### Verificar si ya existe superusuario:

**Opción A: Desde la base de datos**
```sql
SELECT username, email, is_superuser 
FROM auth_user 
WHERE is_superuser = 1;
```

**Opción B: Intentar acceder al admin**
1. Inicia el servidor: `python manage.py runserver`
2. Abre: `http://127.0.0.1:8000/admin`
3. Si te pide login, ya existe (solo necesitas las credenciales)
4. Si no carga o da error, necesitas crear uno

#### Crear superusuario (si no existe):

```bash
python manage.py createsuperuser
```

Sigue las instrucciones:
- **Username**: (ej: admin)
- **Email**: (ej: admin@forneria.com)
- **Password**: (elige una contraseña segura)

**📖 Ver guía completa**: `VERIFICAR_CREAR_SUPERUSUARIO.md`

---

## ✅ CHECKLIST DE VERIFICACIÓN

Después de crear la base de datos:

- [ ] ✅ Base de datos `forneria` creada
- [ ] ✅ Intercalación: `utf8mb4_spanish_ci`
- [ ] ✅ Script SQL ejecutado sin errores
- [ ] ✅ Todas las tablas existen (15+ tablas)
- [ ] ✅ Roles insertados (3 roles)
- [ ] ✅ Categorías insertadas (3 categorías)
- [ ] ✅ Cliente genérico insertado
- [ ] ✅ Campos de trazabilidad en movimientos_inventario
- [ ] ✅ Tablas de proveedores creadas

---

## 🧪 PROBAR EL SISTEMA

Después de crear la base de datos:

1. **Iniciar servidor Django**:
   ```bash
   python manage.py runserver
   ```

2. **Abrir en navegador**:
   - `http://127.0.0.1:8000`

3. **Probar funcionalidades**:
   - Login (crear superusuario si es necesario)
   - Dashboard
   - Inventario
   - POS
   - Reportes

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Error: "Access denied"
**Solución**: Verifica usuario y contraseña:
- Usuario: `forneria_user`
- Contraseña: `Ventana$123` (o la de tu `.env`)

### Error: "Base de datos no existe"
**Solución**: Asegúrate de crear la base de datos primero (Paso 1)

### Error: "Table already exists"
**Solución**: Si la tabla ya existe, el script la borrará y la recreará. Está bien.

### Error: "Foreign key constraint fails"
**Solución**: El script está ordenado correctamente. Si hay error, verifica que ejecutaste el script completo.

### Django no conecta a la BD
**Solución**: Verifica las credenciales en `settings.py` o `.env`:
```python
DATABASES = {
    'default': {
        'NAME': 'forneria',
        'USER': 'forneria_user',
        'PASSWORD': 'Ventana$123',  # O la de tu .env
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

---

## 📝 RESUMEN RÁPIDO

```bash
# 1. Crear BD
mysql -u forneria_user -p -e "CREATE DATABASE forneria CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci;"

# 2. Ejecutar script completo
mysql -u forneria_user -p forneria < sql_completo_forneria.sql

# 3. Verificar
mysql -u forneria_user -p forneria -e "SHOW TABLES;"
```

---

## 📋 ESTRUCTURA CREADA

El script `sql_completo_forneria.sql` crea:

### Tablas Base:
- `categorias` - Categorías de productos
- `nutricional` - Información nutricional
- `productos` - Productos del inventario
- `alertas` - Alertas de stock y vencimiento
- `clientes` - Clientes del sistema
- `ventas` - Ventas realizadas
- `detalle_venta` - Detalle de productos en cada venta
- `movimientos_inventario` - Historial de movimientos (con trazabilidad)

### Tablas de Proveedores:
- `proveedor` - Proveedores
- `factura_proveedor` - Facturas de compra
- `detalle_factura_proveedor` - Detalle de productos en facturas
- `pago_proveedor` - Pagos realizados a proveedores

### Tablas de Usuarios:
- `direccion` - Direcciones
- `roles` - Roles del sistema
- `usuarios` - Perfiles de usuario

### Datos Iniciales:
- ✅ 3 roles: Vendedor, Contador, Administrador
- ✅ 3 categorías: Panadería, Pastelería, Bebidas
- ✅ 1 cliente genérico
- ✅ 1 registro nutricional básico

---

**Fecha**: Hoy  
**Script**: `sql_completo_forneria.sql`  
**Intercalación**: `utf8mb4_spanish_ci`  
**Estado**: ✅ **LISTO PARA USAR**

