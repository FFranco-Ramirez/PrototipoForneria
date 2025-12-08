# 🗄️ Instrucciones para Recrear la Base de Datos

## 📋 Resumen

Esta guía te explica cómo **borrar y recrear** la base de datos `forneria` desde cero con la estructura completa y actualizada.

**⚠️ NOTA**: Si **NO tienes la base de datos aún**, usa `INSTRUCCIONES_CREAR_BD_NUEVA.md` en su lugar (es más simple).

---

## ⚠️ IMPORTANTE: HACER BACKUP PRIMERO

**ANTES de borrar nada, haz un backup:**

### Opción 1: phpMyAdmin
1. Abre phpMyAdmin: `http://localhost/phpmyadmin`
2. Selecciona la base de datos `forneria`
3. Pestaña **"Exportar"**
4. Método: **"Personalizado"**
5. Clic en **"Continuar"**
6. Guarda el archivo (ej: `backup_forneria_20250101.sql`)

### Opción 2: Línea de comandos
```bash
mysqldump -u forneria_user -p forneria > backup_forneria_$(date +%Y%m%d).sql
```

---

## 🚀 PASOS PARA RECREAR LA BASE DE DATOS

### Paso 1: Borrar la base de datos actual

#### Método A: phpMyAdmin (Recomendado)
1. Abre phpMyAdmin: `http://localhost/phpmyadmin`
2. En el panel izquierdo, haz clic derecho en `forneria`
3. Selecciona **"Eliminar"** (o **"Drop"**)
4. Confirma la eliminación

#### Método B: Línea de comandos
```bash
mysql -u forneria_user -p
```
Luego ejecuta:
```sql
DROP DATABASE IF EXISTS forneria;
```

---

### Paso 2: Crear la base de datos nueva

#### Método A: phpMyAdmin
1. En phpMyAdmin, haz clic en **"Nueva"** (arriba)
2. Nombre de la base de datos: `forneria`
3. Intercalación: `utf8mb4_spanish_ci`
4. Clic en **"Crear"**

#### Método B: Línea de comandos
```sql
CREATE DATABASE forneria CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci;
```

---

### Paso 3: Ejecutar el script completo

**He creado un script maestro**: `sql_completo_forneria.sql`

Este script incluye:
- ✅ Todas las tablas base (productos, ventas, clientes, etc.)
- ✅ Tablas de proveedores y facturas
- ✅ Campos de trazabilidad en movimientos_inventario
- ✅ Tablas de usuarios y roles
- ✅ Datos iniciales (roles, categorías, cliente genérico)

#### Método A: phpMyAdmin (Más fácil) ⭐

1. Abre phpMyAdmin
2. Selecciona la base de datos `forneria` (recién creada)
3. Pestaña **"Importar"** (arriba)
4. Clic en **"Elegir archivo"**
5. Selecciona: `sql_completo_forneria.sql`
6. Clic en **"Continuar"** (abajo)
7. ✅ Espera a que termine (puede tardar unos segundos)
8. Deberías ver: **"La importación se ha finalizado correctamente"**

#### Método B: Línea de comandos

```bash
mysql -u forneria_user -p forneria < sql_completo_forneria.sql
```

---

### Paso 4: Verificar que todo se creó correctamente

#### En phpMyAdmin:
1. Selecciona `forneria`
2. Deberías ver todas las tablas en el panel izquierdo

#### En línea de comandos:
```sql
USE forneria;
SHOW TABLES;
```

**Deberías ver estas tablas**:
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
- (Y las tablas de Django: `auth_*`, `django_*`)

---

### Paso 5: Verificar datos iniciales

```sql
-- Verificar roles
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
-- Deberías ver: origen, referencia_id, tipo_referencia
```

---

### Paso 6: Crear usuario de Django (si es necesario)

Si necesitas crear un superusuario de Django:

```bash
python manage.py createsuperuser
```

Sigue las instrucciones:
- Username: (ej: admin)
- Email: (ej: admin@forneria.com)
- Password: (elige una contraseña segura)

---

## ✅ CHECKLIST DE VERIFICACIÓN

Después de recrear la base de datos, verifica:

- [ ] ✅ Base de datos `forneria` creada
- [ ] ✅ Todas las tablas existen (15+ tablas)
- [ ] ✅ Roles insertados (3 roles)
- [ ] ✅ Categorías insertadas (3 categorías)
- [ ] ✅ Cliente genérico insertado
- [ ] ✅ Campos de trazabilidad en movimientos_inventario
- [ ] ✅ Tablas de proveedores creadas
- [ ] ✅ Puedes iniciar sesión en Django
- [ ] ✅ El sistema funciona correctamente

---

## 🧪 PROBAR EL SISTEMA

Después de recrear la base de datos:

1. **Iniciar servidor Django**:
   ```bash
   python manage.py runserver
   ```

2. **Abrir en navegador**:
   - `http://127.0.0.1:8000`

3. **Probar funcionalidades**:
   - Login
   - Dashboard
   - Inventario
   - POS
   - Reportes

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Error: "Access denied"
**Solución**: Verifica usuario y contraseña en `settings.py` o `.env`

### Error: "Table already exists"
**Solución**: El script usa `DROP TABLE IF EXISTS`, así que está bien. Si persiste, borra la base de datos y créala de nuevo.

### Error: "Foreign key constraint fails"
**Solución**: Asegúrate de ejecutar el script completo en orden. El script ya está ordenado correctamente.

### Error: "Base de datos no existe"
**Solución**: Crea la base de datos primero (Paso 2)

### Django no conecta a la BD
**Solución**: Verifica las credenciales en `settings.py`:
```python
DATABASES = {
    'default': {
        'NAME': 'forneria',
        'USER': 'forneria_user',
        'PASSWORD': 'Ventana$123',  # O la de tu .env
        ...
    }
}
```

---

## 📝 NOTAS IMPORTANTES

1. **El script es seguro**: Usa `DROP TABLE IF EXISTS` e `INSERT IGNORE`
2. **No pierdes datos de Django**: Las tablas `auth_*` y `django_*` se recrean automáticamente
3. **Datos iniciales incluidos**: Roles, categorías y cliente genérico
4. **Estructura completa**: Incluye todas las mejoras y nuevas funcionalidades

---

## 🎯 RESUMEN RÁPIDO

```bash
# 1. Backup
mysqldump -u forneria_user -p forneria > backup.sql

# 2. Borrar BD
mysql -u forneria_user -p -e "DROP DATABASE IF EXISTS forneria;"

# 3. Crear BD
mysql -u forneria_user -p -e "CREATE DATABASE forneria CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci;"

# 4. Ejecutar script completo
mysql -u forneria_user -p forneria < sql_completo_forneria.sql

# 5. Verificar
mysql -u forneria_user -p forneria -e "SHOW TABLES;"
```

---

**Fecha**: Hoy  
**Script**: `sql_completo_forneria.sql`  
**Estado**: ✅ Listo para usar

