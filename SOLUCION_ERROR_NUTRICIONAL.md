# 🔧 Solución: Error "Unknown column 'azucares' in 'field list'"

## ❌ Problema

El modelo Django `Nutricional` espera los campos:
- `azucares`
- `sodio`

Pero la tabla en la base de datos solo tiene:
- `calorias`
- `proteinas`
- `carbohidratos`
- `grasas`
- `fibra` (no se usa en el código)

---

## ✅ Solución

### Opción 1: Actualizar la tabla existente (RECOMENDADO)

**Ejecuta este script SQL en phpMyAdmin**:

1. Abre phpMyAdmin
2. Selecciona la base de datos `forneria`
3. Ve a la pestaña **SQL**
4. Copia y pega este código:

```sql
USE forneria;

-- Agregar campo azucares
ALTER TABLE `nutricional` 
ADD COLUMN `azucares` DECIMAL(10,2) DEFAULT NULL AFTER `carbohidratos`;

-- Agregar campo sodio
ALTER TABLE `nutricional` 
ADD COLUMN `sodio` DECIMAL(10,2) DEFAULT NULL AFTER `azucares`;

-- Opcional: Eliminar campo fibra (no se usa)
ALTER TABLE `nutricional` DROP COLUMN `fibra`;
```

5. Haz clic en **Continuar** o **Ejecutar**

---

### Opción 2: Usar el script SQL proporcionado

El archivo `sql_actualizar_tabla_nutricional.sql` contiene el mismo código.

---

## ✅ Verificación

Después de ejecutar el script, verifica que la tabla tenga la estructura correcta:

```sql
DESCRIBE nutricional;
```

**Estructura esperada**:
```
+---------------+--------------+------+-----+---------+----------------+
| Field         | Type         | Null | Key | Default | Extra          |
+---------------+--------------+------+-----+---------+----------------+
| id            | int          | NO   | PRI | NULL    | auto_increment |
| calorias      | decimal(10,2)| YES  |     | NULL    |                |
| proteinas     | decimal(10,2)| YES  |     | NULL    |                |
| grasas        | decimal(10,2)| YES  |     | NULL    |                |
| carbohidratos | decimal(10,2)| YES  |     | NULL    |                |
| azucares      | decimal(10,2)| YES  |     | NULL    |                |
| sodio         | decimal(10,2)| YES  |     | NULL    |                |
+---------------+--------------+------+-----+---------+----------------+
```

---

## 🎯 Después de la corrección

1. **Prueba agregar un producto nuevamente**:
   - Ve a `/productos/agregar/`
   - Completa el formulario
   - El error debería desaparecer

2. **Verifica que los datos se guarden correctamente**:
   - Revisa la tabla `nutricional` en phpMyAdmin
   - Deberías ver los valores de `azucares` y `sodio`

---

## 📝 Nota

El script `sql_completo_forneria.sql` ya fue actualizado para incluir estos campos. Si en el futuro recreas la base de datos desde cero, ya tendrá la estructura correcta.

---

**Estado**: ✅ **Script de corrección listo**  
**Próximo paso**: Ejecutar el script SQL en phpMyAdmin

