# Manual de Mantenimiento - Sistema de Gestión Fornería

## Índice

1. [Introducción](#introducción)
2. [Plan de Mantenimiento Preventivo](#plan-de-mantenimiento-preventivo)
3. [Mantenimiento Diario](#mantenimiento-diario)
4. [Mantenimiento Semanal](#mantenimiento-semanal)
5. [Mantenimiento Mensual](#mantenimiento-mensual)
6. [Mantenimiento Trimestral](#mantenimiento-trimestral)
7. [Mantenimiento Anual](#mantenimiento-anual)
8. [Monitoreo Continuo](#monitoreo-continuo)
9. [Actualizaciones y Parches](#actualizaciones-y-parches)
10. [Backups y Recuperación](#backups-y-recuperación)
11. [Seguridad](#seguridad)
12. [Optimización de Performance](#optimización-de-performance)
13. [Resolución de Problemas Comunes](#resolución-de-problemas-comunes)
14. [Registro de Mantenimiento](#registro-de-mantenimiento)

---

## Introducción

Este manual describe el plan de mantenimiento preventivo del Sistema de Gestión Fornería, desarrollado con 
Django 5.2.7 y MySQL. 
El mantenimiento preventivo es esencial para garantizar la estabilidad, seguridad y rendimiento del sistema 
a lo largo de su ciclo de vida.

**Objetivo:** Evitar fallos inesperados, mantener el sistema actualizado y optimizado, y garantizar 
la continuidad del servicio.

**Responsable:** Administrador del Sistema / Equipo de Soporte Técnico

**Tecnologías del Sistema:**
- Framework: Django 5.2.7
- Base de Datos: MySQL (nombre: `forneria`, usuario: `forneria_user`)
- Lenguaje: Python 3.11.x
- Servidor WSGI: Apache (producción) 
- Gestión de Variables: python-decouple
- Frontend: Bootstrap 5, Crispy Forms

---

## Plan de Mantenimiento Preventivo

### Periodicidad y Frecuencia

El mantenimiento se divide en diferentes niveles según la frecuencia:

| Frecuencia | Tipo de Mantenimiento | Duración Estimada |
|------------|----------------------|-------------------|
| **Diario** | Verificaciones básicas | 5-10 minutos |
| **Semanal** | Revisión de logs y alertas | 15-30 minutos |
| **Mensual** | Actualizaciones y optimización | 1-2 horas |
| **Trimestral** | Revisión completa del sistema | 3-4 horas |
| **Anual** | Auditoría completa y planificación | 1 día |

---

## Mantenimiento Diario

### Checklist Diario (5-10 minutos)

#### 1. Verificar Estado de Servicios

**[ACCIÓN]**

```bash
# Verificar que MySQL esté corriendo
sudo systemctl status mysql

# Verificar que el servidor Django/WSGI esté corriendo
# Si usa Apache:
sudo systemctl status apache2

# Si usa supervisor:
sudo supervisorctl status

# Verificar que los servicios estén habilitados para iniciar automáticamente
sudo systemctl is-enabled mysql
sudo systemctl is-enabled apache2  # Si aplica
```

**[RESULTADO ESPERADO]**

- Todos los servicios deben estar "active (running)"
- Todos los servicios deben estar "enabled"

**[ACCIÓN SI HAY PROBLEMAS]**

- Si un servicio está detenido, iniciarlo: `sudo systemctl start [servicio]`
- Si un servicio no está habilitado, habilitarlo: `sudo systemctl enable [servicio]`
- Revisar logs para identificar la causa

#### 2. Verificar Acceso al Sistema

**[ACCIÓN]**

1. Abrir navegador
2. Acceder a la URL del sistema (configurada en `ALLOWED_HOSTS` y `SITE_URL`)
3. Verificar que la página de login carga correctamente
4. Intentar iniciar sesión con usuario de prueba

**[RESULTADO ESPERADO]**

- La página carga en menos de 3 segundos
- El login funciona correctamente

**[ACCIÓN SI HAY PROBLEMAS]**

- Revisar logs de Django: `tail -f logs/django.log`
- Verificar conectividad de red
- Verificar que el servidor tenga recursos disponibles
- Verificar variables de entorno en archivo `.env`

#### 3. Verificar Espacio en Disco

**[ACCIÓN]**

```bash
# Verificar espacio en disco
df -h

# Verificar espacio en directorio de backups
du -sh /var/backups/forneria/* 2>/dev/null || echo "Directorio de backups no existe"

# Verificar tamaño de logs
du -sh logs/

# Verificar tamaño de archivos estáticos
du -sh staticfiles/
```

**[RESULTADO ESPERADO]**

- Al menos 20% de espacio libre en disco
- Los backups no ocupan más del 50% del espacio disponible
- Los logs no ocupan más de 1GB

**[ACCIÓN SI HAY PROBLEMAS]**

- Si el espacio es bajo (< 20%), limpiar backups antiguos
- Si los logs son muy grandes, rotarlos o limpiarlos
- Revisar archivos estáticos duplicados

#### 4. Verificar Backups Automáticos

**[ACCIÓN]**

```bash
# Verificar que el último backup se haya ejecutado
ls -lh /var/backups/forneria/ | tail -5 2>/dev/null || echo "No hay backups en /var/backups/forneria"

# Verificar la fecha del último backup
stat /var/backups/forneria/db_*.sql 2>/dev/null | grep Modify | tail -1 || echo "No se encontraron backups"

# Verificar cron jobs configurados
sudo crontab -l | grep -i backup
```

**[RESULTADO ESPERADO]**

- Debe existir un backup del día anterior (o del mismo día si es temprano)
- El tamaño del backup debe ser razonable (no 0 bytes)

**[ACCIÓN SI HAY PROBLEMAS]**

- Verificar el cron job: `sudo crontab -l`
- Ejecutar manualmente el backup (ver sección de Backups)
- Revisar logs del cron: `grep CRON /var/log/syslog | tail -20`

#### 5. Verificar Comandos de Management Personalizados

**[ACCIÓN]**

```bash
# Navegar al directorio del proyecto
cd /ruta/al/proyecto/PrototipoForneria

# Activar entorno virtual si existe
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Verificar que los comandos estén disponibles
python manage.py help generar_alertas
python manage.py help verificar_vencimientos
python manage.py help validar_vencimientos
```

**[RESULTADO ESPERADO]**

- Los comandos deben estar disponibles y mostrar ayuda

**[ACCIÓN SI HAY PROBLEMAS]**

- Verificar que el entorno virtual esté activado
- Verificar que las dependencias estén instaladas: `pip install -r requerimientos.txt`
- Revisar estructura de directorios `ventas/management/commands/`

---

## Mantenimiento Semanal

### Checklist Semanal (15-30 minutos)

#### 1. Revisar Logs de Errores

**[ACCIÓN]**

```bash
# Revisar errores de Django
tail -100 logs/django.log | grep -i error

# Revisar errores de MySQL
sudo tail -100 /var/log/mysql/error.log | grep -i error

# Revisar errores del sistema operativo relacionados con el proyecto
sudo journalctl -u apache2 -n 100 --no-pager | grep -i error  # Si usa Apache
```

**[RESULTADO ESPERADO]**

- No deben haber errores críticos
- Los errores menores deben ser esporádicos y no repetitivos

**[ACCIÓN SI HAY PROBLEMAS]**

- Documentar errores encontrados
- Investigar la causa de errores repetitivos
- Aplicar correcciones si es necesario

#### 2. Revisar Alertas del Sistema

**[ACCIÓN]**

1. Acceder al sistema como administrador
2. Ir al Dashboard (`/dashboard/`)
3. Revisar la sección de "Alertas Pendientes"
4. Verificar alertas de:
   - Stock bajo
   - Productos próximos a vencer
   - Facturas por vencer

5. Ejecutar comando para generar alertas automáticas:
```bash
cd /ruta/al/proyecto
source venv/bin/activate
python manage.py generar_alertas --verbose
```

**[RESULTADO ESPERADO]**

- Las alertas deben ser relevantes y actualizadas
- No deben haber alertas obsoletas o incorrectas
- El comando debe ejecutarse sin errores

**[ACCIÓN SI HAY PROBLEMAS]**

- Revisar la lógica de generación de alertas en `ventas/models/alertas.py`
- Verificar que los datos en la base de datos sean correctos
- Limpiar alertas obsoletas si es necesario

#### 3. Verificar Performance del Sistema

**[ACCIÓN]**

```bash
# Verificar uso de CPU
top -bn1 | head -20

# Verificar uso de memoria
free -h

# Verificar uso de disco
df -h

# Verificar procesos de Python/Django
ps aux | grep python | grep manage.py

# Verificar conexiones a MySQL
mysqladmin -u forneria_user -p processlist
```

**[RESULTADO ESPERADO]**

- CPU: < 70% de uso promedio
- Memoria: < 80% de uso
- Disco: < 80% de uso
- Procesos Python: Cantidad razonable (depende del servidor WSGI)

**[ACCIÓN SI HAY PROBLEMAS]**

- Si el CPU está alto, identificar procesos que consumen recursos
- Si la memoria está alta, considerar aumentar RAM o optimizar
- Si hay muchas conexiones MySQL, revisar configuración de pool de conexiones

#### 4. Revisar Accesos y Seguridad

**[ACCIÓN]**

```bash
# Revisar intentos de acceso fallidos
sudo grep "Failed password" /var/log/auth.log | tail -20

# Revisar accesos SSH
sudo grep "Accepted password" /var/log/auth.log | tail -10

# Verificar archivo .env existe y tiene permisos correctos
ls -la .env
```

**[RESULTADO ESPERADO]**

- No deben haber intentos de acceso sospechosos
- El archivo `.env` debe tener permisos 600 (solo lectura/escritura para el propietario)

**[ACCIÓN SI HAY PROBLEMAS]**

- Si hay intentos sospechosos, bloquear IPs: `sudo fail2ban-client set sshd banip [IP]`
- Asegurar permisos del `.env`: `chmod 600 .env`

#### 5. Verificar Integridad de Base de Datos

**[ACCIÓN]**

```bash
# Conectarse a MySQL
mysql -u forneria_user -p forneria

# Verificar tablas principales
SHOW TABLES;

# Verificar tamaño de tablas principales
SELECT 
    table_name AS 'Tabla',
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Tamaño (MB)'
FROM information_schema.TABLES
WHERE table_schema = 'forneria'
ORDER BY (data_length + index_length) DESC
LIMIT 10;

# Verificar índices en tablas críticas
SHOW INDEX FROM ventas;
SHOW INDEX FROM productos;
SHOW INDEX FROM movimientos_inventario;
SHOW INDEX FROM lotes;
SHOW INDEX FROM historial_boletas;
SHOW INDEX FROM historial_merma;
```

**[RESULTADO ESPERADO]**

- Todas las tablas deben existir
- Las tablas no deben tener tamaños anormalmente grandes
- Los índices deben estar presentes en tablas críticas

**[ACCIÓN SI HAY PROBLEMAS]**

- Si faltan índices, crearlos según sea necesario
- Si las tablas son muy grandes, considerar limpieza de datos antiguos
- Ejecutar `OPTIMIZE TABLE` en tablas grandes si es necesario

#### 6. Ejecutar Verificación de Vencimientos

**[ACCIÓN]**

```bash
cd /ruta/al/proyecto
source venv/bin/activate

# Ejecutar verificación de vencimientos (modo dry-run primero)
python manage.py verificar_vencimientos --dry-run

# Si todo está bien, ejecutar sin dry-run
python manage.py verificar_vencimientos
```

**[RESULTADO ESPERADO]**

- El comando debe ejecutarse sin errores
- Debe mostrar productos vencidos encontrados (si los hay)

**[ACCIÓN SI HAY PROBLEMAS]**

- Revisar la lógica en `ventas/management/commands/verificar_vencimientos.py`
- Verificar que las fechas de caducidad estén correctas en la base de datos

---

## Mantenimiento Mensual

### Checklist Mensual (1-2 horas)

#### 1. Actualizar Sistema Operativo

**[ACCIÓN]**

```bash
# Actualizar lista de paquetes
sudo apt update

# Verificar actualizaciones disponibles
sudo apt list --upgradable

# Aplicar actualizaciones de seguridad (recomendado)
sudo apt upgrade -y

# Reiniciar si es necesario (solo si hay actualizaciones del kernel)
sudo reboot
```

**[RESULTADO ESPERADO]**

- El sistema debe estar actualizado con los últimos parches de seguridad
- No deben haber vulnerabilidades conocidas críticas

**[ACCIÓN SI HAY PROBLEMAS]**

- Si hay conflictos, resolverlos antes de actualizar
- Hacer backup antes de actualizaciones importantes
- Probar en ambiente de desarrollo primero si es posible

#### 2. Actualizar Dependencias de Python

**[ACCIÓN]**

```bash
cd /ruta/al/proyecto/PrototipoForneria
source venv/bin/activate

# Verificar dependencias desactualizadas
pip list --outdated

# Actualizar dependencias (con cuidado)
pip install --upgrade pip
pip install -r requerimientos.txt --upgrade

# Verificar que no hay conflictos
pip check

# Verificar que Django sigue funcionando
python manage.py check
```

**[RESULTADO ESPERADO]**

- Las dependencias deben estar actualizadas
- No deben haber conflictos entre paquetes
- El comando `python manage.py check` no debe mostrar errores críticos

**[ACCIÓN SI HAY PROBLEMAS]**

- Si hay conflictos, revisar el archivo `requerimientos.txt`
- Probar en ambiente de desarrollo primero
- Hacer backup antes de actualizar
- Considerar actualizar dependencias una por una si hay problemas

#### 3. Optimizar Base de Datos

**[ACCIÓN]**

```bash
# Conectarse a MySQL
mysql -u forneria_user -p forneria

# Optimizar tablas principales
OPTIMIZE TABLE ventas;
OPTIMIZE TABLE productos;
OPTIMIZE TABLE movimientos_inventario;
OPTIMIZE TABLE lotes;
OPTIMIZE TABLE historial_boletas;
OPTIMIZE TABLE historial_merma;
OPTIMIZE TABLE detalle_venta;
OPTIMIZE TABLE alertas;
OPTIMIZE TABLE factura_proveedor;
OPTIMIZE TABLE detalle_factura_proveedor;
OPTIMIZE TABLE pago_proveedor;

# Analizar tablas para actualizar estadísticas
ANALYZE TABLE ventas;
ANALYZE TABLE productos;
ANALYZE TABLE movimientos_inventario;
ANALYZE TABLE lotes;
```

**[RESULTADO ESPERADO]**

- Las tablas deben estar optimizadas
- Las consultas deben ejecutarse más rápido

**[ACCIÓN SI HAY PROBLEMAS]**

- Si la optimización tarda mucho, hacerla en horarios de bajo tráfico
- Considerar hacerla tabla por tabla si hay muchas tablas
- Verificar que no haya bloqueos de tablas durante la optimización

#### 4. Limpiar Logs Antiguos

**[ACCIÓN]**

```bash
# Limpiar logs de Django antiguos (mantener últimos 30 días)
find logs/ -name "*.log" -mtime +30 -delete

# Limpiar logs de MySQL antiguos (mantener últimos 30 días)
sudo find /var/log/mysql -name "*.log" -mtime +30 -delete

# Limpiar backups antiguos (mantener últimos 30 días)
find /var/backups/forneria -name "*.sql" -mtime +30 -delete
find /var/backups/forneria -name "*.tar.gz" -mtime +30 -delete

# Limpiar archivos de sesión antiguos de Django (si existen)
find /tmp -name "django_*" -mtime +7 -delete 2>/dev/null
```

**[RESULTADO ESPERADO]**

- Los logs antiguos deben estar eliminados
- El espacio en disco debe liberarse

**[ACCIÓN SI HAY PROBLEMAS]**

- Verificar que no se eliminen logs necesarios
- Asegurar que los backups estén funcionando antes de eliminar
- Considerar rotación de logs en lugar de eliminación

#### 5. Revisar y Limpiar Datos Antiguos

**[ACCIÓN]**

1. Acceder al sistema como administrador
2. Revisar datos antiguos que puedan limpiarse:
   - Historial de boletas muy antiguo (más de 2 años)
   - Movimientos de inventario muy antiguos (más de 2 años)
   - Alertas resueltas antiguas (más de 6 meses)
   - Historial de merma muy antiguo (más de 2 años)
3. Exportar datos importantes antes de eliminar
4. Eliminar solo si es seguro y necesario

**Script SQL de ejemplo para limpiar alertas antiguas:**

```sql
-- Eliminar alertas resueltas de más de 6 meses
DELETE FROM alertas 
WHERE estado = 'resuelta' 
AND fecha_creacion < DATE_SUB(NOW(), INTERVAL 6 MONTH);
```

**[RESULTADO ESPERADO]**

- Los datos antiguos deben estar archivados o eliminados
- El sistema debe funcionar más rápido

**[ACCIÓN SI HAY PROBLEMAS]**

- Hacer backup completo antes de eliminar datos
- Consultar con el cliente antes de eliminar datos históricos importantes
- Probar en ambiente de desarrollo primero

#### 6. Revisar Variables de Entorno

**[ACCIÓN]**

```bash
# Verificar que el archivo .env existe
ls -la .env

# Verificar que tiene las variables necesarias (sin mostrar valores)
grep -E "^[A-Z_]+=" .env | cut -d= -f1 | sort

# Variables críticas que deben existir:
# - SECRET_KEY
# - DEBUG
# - ALLOWED_HOSTS
# - DB_NAME
# - DB_USER
# - DB_PASSWORD
# - DB_HOST
# - DB_PORT
```

**[RESULTADO ESPERADO]**

- El archivo `.env` debe existir
- Debe tener todas las variables necesarias
- Los permisos deben ser 600 (solo lectura/escritura para propietario)

**[ACCIÓN SI HAY PROBLEMAS]**

- Si falta el archivo `.env`, crearlo basándose en `settings.py`
- Asegurar permisos: `chmod 600 .env`
- Verificar que `DEBUG=False` en producción

---

## Mantenimiento Trimestral

### Checklist Trimestral (3-4 horas)

#### 1. Auditoría de Seguridad

**[ACCIÓN]**

1. Revisar usuarios del sistema:
   - Verificar que no haya usuarios no autorizados
   - Verificar que los usuarios tengan los permisos correctos
   - Eliminar usuarios inactivos o no necesarios

2. Revisar configuración de seguridad:
   - Verificar configuración de Django (`DEBUG=False`, `ALLOWED_HOSTS`)
   - Verificar permisos de archivos y directorios
   - Verificar que el archivo `.env` tenga permisos correctos
   - Revisar `settings.py` para configuraciones de seguridad

3. Revisar logs de seguridad:
   - Buscar intentos de acceso no autorizados
   - Buscar patrones sospechosos
   - Verificar que no haya vulnerabilidades explotadas

4. Verificar roles y permisos:
```bash
cd /ruta/al/proyecto
source venv/bin/activate
python manage.py shell

# En el shell de Django:
from ventas.models import Roles, Usuarios
from django.contrib.auth.models import User

# Listar todos los usuarios
for user in User.objects.all():
    print(f"{user.username} - {user.email} - Activo: {user.is_active}")

# Listar roles
for rol in Roles.objects.all():
    print(f"{rol.nombre} - {rol.descripcion}")
```

**[RESULTADO ESPERADO]**

- No deben haber usuarios no autorizados
- La configuración debe ser segura
- No deben haber intentos de acceso sospechosos

#### 2. Revisión Completa de Performance

**[ACCIÓN]**

1. Analizar consultas lentas:

```sql
-- Habilitar log de consultas lentas (temporalmente)
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;

-- Después de un tiempo, revisar el log
-- /var/log/mysql/slow-query.log
```

2. Analizar uso de recursos:
   - CPU, memoria, disco, red
   - Identificar cuellos de botella

3. Optimizar según sea necesario:
   - Agregar índices si faltan
   - Optimizar consultas lentas
   - Ajustar configuración de MySQL

4. Revisar consultas frecuentes en el código:
   - Buscar consultas N+1
   - Optimizar uso de `select_related` y `prefetch_related`

**[RESULTADO ESPERADO]**

- El sistema debe tener buen rendimiento
- Las consultas deben ejecutarse rápidamente

#### 3. Revisión de Código y Actualizaciones

**[ACCIÓN]**

1. Revisar actualizaciones de Django:
   - Verificar si hay nuevas versiones
   - Revisar changelog y breaking changes
   - Planificar actualización si es necesario

2. Revisar código del proyecto:
   - Verificar que no haya código obsoleto
   - Verificar que las dependencias estén actualizadas
   - Revisar que no haya vulnerabilidades conocidas

3. Ejecutar análisis de seguridad:
```bash
# Instalar bandit para análisis de seguridad (opcional)
pip install bandit

# Ejecutar análisis
bandit -r ventas/ Forneria/
```

**[RESULTADO ESPERADO]**

- El código debe estar actualizado
- No deben haber vulnerabilidades conocidas

#### 4. Prueba de Recuperación de Backup

**[ACCIÓN]**

1. Seleccionar un backup reciente
2. Crear una base de datos de prueba
3. Restaurar el backup en la base de datos de prueba
4. Verificar que los datos se restauraron correctamente
5. Probar funcionalidades básicas

**[RESULTADO ESPERADO]**

- El backup debe restaurarse correctamente
- Los datos deben estar completos y correctos

#### 5. Revisión de Documentación

**[ACCIÓN]**

1. Revisar que la documentación esté actualizada:
   - Manual de Usuario
   - Manual de Instalación
   - Manual de Mantenimiento (este documento)
   - README.md

2. Actualizar documentación si hay cambios:
   - Nuevas funcionalidades
   - Cambios en procesos
   - Nuevos requisitos

**[RESULTADO ESPERADO]**

- La documentación debe estar actualizada
- Debe reflejar el estado actual del sistema

#### 6. Revisar Comandos de Management Personalizados

**[ACCIÓN]**

```bash
cd /ruta/al/proyecto
source venv/bin/activate

# Probar todos los comandos personalizados
python manage.py generar_alertas --verbose
python manage.py verificar_vencimientos --dry-run
python manage.py validar_vencimientos --help
python manage.py crear_roles --help
```

**[RESULTADO ESPERADO]**

- Todos los comandos deben funcionar correctamente
- Deben mostrar información útil

---

## Mantenimiento Anual

### Checklist Anual (1 día)

#### 1. Auditoría Completa del Sistema

**[ACCIÓN]**

1. Revisar todos los aspectos del sistema:
   - Seguridad
   - Performance
   - Funcionalidades
   - Integración con otros sistemas

2. Generar reporte completo:
   - Estado actual del sistema
   - Problemas encontrados
   - Recomendaciones de mejora
   - Plan de acción para el próximo año

**[RESULTADO ESPERADO]**

- Reporte completo y detallado
- Plan de acción claro

#### 2. Planificación para el Próximo Año

**[ACCIÓN]**

1. Revisar objetivos del negocio
2. Identificar necesidades de mejora
3. Planificar actualizaciones y mejoras
4. Estimar recursos necesarios

**[RESULTADO ESPERADO]**

- Plan claro para el próximo año
- Presupuesto estimado

#### 3. Revisión de Infraestructura

**[ACCIÓN]**

1. Evaluar si el servidor actual es suficiente:
   - CPU, RAM, disco
   - Ancho de banda
   - Capacidad de crecimiento

2. Evaluar opciones de mejora:
   - Actualizar hardware
   - Migrar a servidor más potente
   - Optimizar configuración actual

**[RESULTADO ESPERADO]**

- Evaluación completa de infraestructura
- Recomendaciones claras

#### 4. Actualización Mayor de Django (si aplica)

**[ACCIÓN]**

Si hay una nueva versión mayor de Django disponible:

1. Revisar breaking changes
2. Probar actualización en ambiente de desarrollo
3. Actualizar dependencias relacionadas
4. Probar todas las funcionalidades
5. Planificar migración a producción

**[RESULTADO ESPERADO]**

- Sistema actualizado a la última versión estable
- Todas las funcionalidades funcionando correctamente

---

## Monitoreo Continuo

### Herramientas de Monitoreo Recomendadas

#### 1. Monitoreo de Servicios

**[CONFIGURACIÓN]**

```bash
# Instalar monit (opcional)
sudo apt install monit -y

# Configurar monit para monitorear MySQL y el servidor WSGI
sudo nano /etc/monit/monitrc
```

#### 2. Alertas Automáticas

**[CONFIGURACIÓN]**

- Configurar alertas por email para:
  - Servicios caídos
  - Espacio en disco bajo
  - Errores críticos
  - Intentos de acceso sospechosos

#### 3. Dashboard de Monitoreo

**[RECOMENDACIÓN]**

- Considerar usar herramientas como:
  - Grafana (si se implementa)
  - Monit
  - Uptime Robot (monitoreo externo)

#### 4. Monitoreo de Comandos Automáticos

**[CONFIGURACIÓN]**

Configurar cron jobs para comandos automáticos:

```bash
# Editar crontab
sudo crontab -e

# Ejemplo de configuración:
# Generar alertas diariamente a las 6:00 AM
0 6 * * * cd /ruta/al/proyecto && /ruta/al/venv/bin/python manage.py generar_alertas >> /var/log/forneria/alertas.log 2>&1

# Verificar vencimientos diariamente a las 00:00
0 0 * * * cd /ruta/al/proyecto && /ruta/al/venv/bin/python manage.py verificar_vencimientos >> /var/log/forneria/vencimientos.log 2>&1
```

---

## Actualizaciones y Parches

### Proceso de Actualización

#### 1. Antes de Actualizar

**[CHECKLIST]**

- [ ] Hacer backup completo del sistema
- [ ] Probar actualización en ambiente de desarrollo
- [ ] Notificar a usuarios sobre mantenimiento programado
- [ ] Planificar ventana de mantenimiento

#### 2. Durante la Actualización

**[PASOS]**

1. Poner el sistema en modo mantenimiento (si es posible)
2. Hacer backup final
3. Aplicar actualizaciones
4. Ejecutar migraciones de base de datos si es necesario:
```bash
cd /ruta/al/proyecto
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```
5. Probar funcionalidades críticas
6. Restaurar servicio

#### 3. Después de Actualizar

**[VERIFICACIÓN]**

- [ ] Verificar que todos los servicios funcionan
- [ ] Probar funcionalidades principales
- [ ] Monitorear logs por errores
- [ ] Notificar a usuarios que el servicio está restaurado

---

## Backups y Recuperación

### Estrategia de Backups

#### 1. Frecuencia de Backups

- **Base de Datos:** Diario (automático a las 2:00 AM)
- **Archivos Estáticos:** Diario (automático a las 2:00 AM)
- **Configuración:** Semanal (manual)
- **Archivo .env:** Semanal (manual, con cuidado)

#### 2. Script de Backup de Base de Datos

**[CREAR SCRIPT]**

Crear script `/usr/local/bin/backup-forneria.sh`:

```bash
#!/bin/bash

# Configuración
DB_NAME="forneria"
DB_USER="forneria_user"
DB_PASSWORD="[PASSWORD]"  # Usar variable de entorno en producción
BACKUP_DIR="/var/backups/forneria"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Crear directorio si no existe
mkdir -p $BACKUP_DIR

# Backup de base de datos
mysqldump -u $DB_USER -p$DB_PASSWORD $DB_NAME > $BACKUP_DIR/db_$DATE.sql

# Comprimir backup
gzip $BACKUP_DIR/db_$DATE.sql

# Backup de archivos estáticos
tar -czf $BACKUP_DIR/staticfiles_$DATE.tar.gz /ruta/al/proyecto/staticfiles/

# Eliminar backups antiguos
find $BACKUP_DIR -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete

echo "Backup completado: $DATE"
```

**[PERMISOS]**

```bash
sudo chmod +x /usr/local/bin/backup-forneria.sh
```

**[CRON JOB]**

```bash
# Editar crontab
sudo crontab -e

# Agregar línea:
0 2 * * * /usr/local/bin/backup-forneria.sh >> /var/log/forneria/backup.log 2>&1
```

#### 3. Retención de Backups

- **Backups Diarios:** 7 días
- **Backups Semanales:** 4 semanas
- **Backups Mensuales:** 12 meses

#### 4. Prueba de Recuperación

- **Frecuencia:** Trimestral
- **Proceso:** Restaurar backup en ambiente de prueba y verificar

#### 5. Restaurar Backup

**[PROCESO]**

```bash
# Descomprimir backup
gunzip /var/backups/forneria/db_YYYYMMDD_HHMMSS.sql.gz

# Restaurar base de datos
mysql -u forneria_user -p forneria < /var/backups/forneria/db_YYYYMMDD_HHMMSS.sql

# Restaurar archivos estáticos
tar -xzf /var/backups/forneria/staticfiles_YYYYMMDD_HHMMSS.tar.gz -C /
```

---

## Seguridad

### Checklist de Seguridad

#### Mensual

- [ ] Revisar intentos de acceso fallidos
- [ ] Revisar actualizaciones de seguridad del SO
- [ ] Verificar permisos del archivo `.env`

#### Trimestral

- [ ] Auditoría de usuarios y permisos
- [ ] Revisión de configuración de seguridad
- [ ] Revisión de logs de seguridad
- [ ] Verificar que `DEBUG=False` en producción

#### Anual

- [ ] Auditoría completa de seguridad
- [ ] Revisión de políticas de seguridad
- [ ] Plan de respuesta a incidentes

### Configuración de Seguridad en Django

**[VERIFICAR]**

1. `DEBUG=False` en producción
2. `ALLOWED_HOSTS` configurado correctamente
3. `SECRET_KEY` en variable de entorno
4. `SESSION_COOKIE_SECURE=False` (no se usa HTTPS/SSL)
5. `CSRF_COOKIE_SECURE=False` (no se usa HTTPS/SSL)
6. `SECURE_SSL_REDIRECT=False` (no se usa HTTPS/SSL)

---

## Optimización de Performance

### Áreas a Monitorear

1. **Base de Datos:**
   - Consultas lentas
   - Índices faltantes
   - Tamaño de tablas

2. **Servidor WSGI (Apache):**
   - Procesos y threads de Apache/mod_wsgi
   - Uso de memoria
   - Tiempo de respuesta

3. **Aplicación Django:**
   - Caché
   - Consultas N+1
   - Archivos estáticos
   - Uso de `select_related` y `prefetch_related`

### Optimizaciones Recomendadas

1. **Habilitar Caché:**
   - Configurar Redis o Memcached
   - Usar caché de sesiones
   - Caché de consultas frecuentes

2. **Optimizar Consultas:**
   - Usar `select_related` para relaciones ForeignKey
   - Usar `prefetch_related` para relaciones ManyToMany
   - Evitar consultas N+1

3. **Archivos Estáticos:**
   - Usar `collectstatic` para producción
   - Servir archivos estáticos con Nginx
   - Habilitar compresión gzip

---

## Resolución de Problemas Comunes

### Problema: Servidor Django No Responde

**[SÍNTOMAS]**

- Error 500 al acceder al sistema
- Timeout en las peticiones

**[SOLUCIÓN]**

```bash
# Verificar estado del servidor WSGI
sudo systemctl status apache2  # Si usa Apache
sudo supervisorctl status  # Si usa Supervisor

# Ver logs de Django
tail -50 logs/django.log

# Verificar configuración
cd /ruta/al/proyecto
source venv/bin/activate
python manage.py check

# Reiniciar servicio
sudo systemctl restart apache2  # Si usa Apache
```

### Problema: Base de Datos No Responde

**[SÍNTOMAS]**

- Error de conexión a base de datos
- Timeout en consultas

**[SOLUCIÓN]**

```bash
# Verificar estado
sudo systemctl status mysql

# Ver logs de MySQL
sudo tail -50 /var/log/mysql/error.log

# Verificar conexión
mysql -u forneria_user -p forneria

# Reiniciar servicio
sudo systemctl restart mysql

# Verificar variables de entorno
cat .env | grep DB_
```

### Problema: Espacio en Disco Bajo

**[SÍNTOMAS]**

- Sistema lento
- Errores al escribir archivos

**[SOLUCIÓN]**

```bash
# Identificar qué ocupa espacio
sudo du -h --max-depth=1 / | sort -hr | head -10

# Limpiar logs antiguos
find logs/ -name "*.log" -mtime +30 -delete

# Limpiar backups antiguos
find /var/backups/forneria -name "*.sql.gz" -mtime +30 -delete

# Limpiar archivos estáticos compilados antiguos
rm -rf staticfiles/
python manage.py collectstatic --noinput
```

### Problema: Sistema Muy Lento

**[SÍNTOMAS]**

- Páginas tardan mucho en cargar
- Timeouts frecuentes

**[SOLUCIÓN]**

1. Verificar uso de recursos: `top`, `free -h`, `df -h`
2. Revisar consultas lentas en MySQL
3. Optimizar base de datos: `OPTIMIZE TABLE`
4. Revisar logs de errores
5. Verificar que no haya consultas N+1 en el código
6. Considerar aumentar recursos del servidor

### Problema: Error de Migraciones

**[SÍNTOMAS]**

- Error al ejecutar `python manage.py migrate`
- Tablas faltantes o inconsistentes

**[SOLUCIÓN]**

```bash
# Verificar estado de migraciones
python manage.py showmigrations

# Aplicar migraciones faltantes
python manage.py migrate

# Si hay conflictos, hacer backup primero
# Luego resolver conflictos manualmente
```

### Problema: Archivos Estáticos No Se Cargan

**[SÍNTOMAS]**

- CSS/JS no se cargan
- Imágenes no se muestran

**[SOLUCIÓN]**

```bash
# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Verificar que STATIC_ROOT esté configurado correctamente
# Verificar permisos del directorio staticfiles
chmod -R 755 staticfiles/
```

---

## Registro de Mantenimiento

### Formato de Registro

Mantener un registro de todas las actividades de mantenimiento:

| Fecha | Tipo | Descripción | Realizado por | Resultado | Notas |
|-------|------|-------------|---------------|------------|-------|
| YYYY-MM-DD | Diario | Verificación de servicios | [Nombre] | OK / Problemas | [Notas] |
| YYYY-MM-DD | Semanal | Revisión de logs | [Nombre] | OK / Problemas | [Notas] |
| YYYY-MM-DD | Mensual | Actualización de sistema | [Nombre] | OK / Problemas | [Notas] |

### Ejemplo de Registro

```
Fecha: 2025-12-10
Tipo: Semanal
Descripción: Revisión de logs y alertas
Realizado por: Admin Sistema
Resultado: OK
Notas: 
- Encontrados 3 errores menores en logs de Django (no críticos)
- Alertas funcionando correctamente
- Performance dentro de parámetros normales
- Comando generar_alertas ejecutado exitosamente
```

---

## Contacto y Soporte

Para consultas sobre mantenimiento o problemas técnicos:

- **Email de Soporte:** [COMPLETAR]
- **Teléfono:** [COMPLETAR]
- **Horario de Atención:** [COMPLETAR]

---

## Anexos

### A. Scripts de Mantenimiento

#### Script de Verificación Rápida

```bash
#!/bin/bash
# Verificación rápida del sistema

echo "=== Verificación de Servicios ==="
systemctl status mysql --no-pager | head -3
systemctl status apache2 --no-pager | head -3 2>/dev/null || echo "Apache no configurado"

echo -e "\n=== Espacio en Disco ==="
df -h | grep -E '^/dev/'

echo -e "\n=== Uso de Memoria ==="
free -h

echo -e "\n=== Último Backup ==="
ls -lh /var/backups/forneria/ | tail -3 2>/dev/null || echo "No hay backups"

echo -e "\n=== Logs Recientes ==="
tail -5 logs/django.log 2>/dev/null || echo "No hay logs de Django"

echo -e "\n=== Verificación de Django ==="
cd /ruta/al/proyecto
source venv/bin/activate
python manage.py check --deploy
```

#### Script de Limpieza de Logs

```bash
#!/bin/bash
# Limpiar logs antiguos

# Logs de Django (mantener 30 días)
find logs/ -name "*.log" -mtime +30 -delete

# Logs de MySQL (mantener 30 días)
sudo find /var/log/mysql -name "*.log" -mtime +30 -delete

# Backups antiguos (mantener 30 días)
find /var/backups/forneria -name "*.sql.gz" -mtime +30 -delete
find /var/backups/forneria -name "*.tar.gz" -mtime +30 -delete

echo "Limpieza completada"
```

### B. Comandos Útiles

```bash
# Ver logs en tiempo real
tail -f logs/django.log

# Reiniciar servicios
sudo systemctl restart mysql
sudo systemctl restart apache2  # Si aplica

# Ver procesos de Python
ps aux | grep python

# Ver uso de recursos
htop  # Si está instalado
top

# Ver conexiones a MySQL
mysqladmin -u forneria_user -p processlist

# Ejecutar comandos de Django
cd /ruta/al/proyecto
source venv/bin/activate
python manage.py [comando]

# Verificar configuración de Django
python manage.py check
python manage.py check --deploy

# Ver migraciones pendientes
python manage.py showmigrations

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Crear superusuario
python manage.py createsuperuser
```

### C. Estructura del Proyecto

```
PrototipoForneria/
├── Forneria/              # Configuración del proyecto Django
│   ├── settings.py        # Configuración principal
│   ├── urls.py            # URLs principales
│   ├── wsgi.py            # Configuración WSGI
│   └── asgi.py            # Configuración ASGI
├── ventas/                # App principal de ventas
│   ├── models/            # Modelos de base de datos
│   ├── views/             # Vistas del sistema
│   ├── management/        # Comandos personalizados
│   │   └── commands/
│   │       ├── generar_alertas.py
│   │       ├── verificar_vencimientos.py
│   │       └── validar_vencimientos.py
│   └── funciones/         # Funciones auxiliares
├── rrhh/                  # App de recursos humanos
├── templates/             # Plantillas HTML
├── static/                # Archivos estáticos fuente
├── staticfiles/           # Archivos estáticos compilados
├── logs/                  # Logs de Django
├── manage.py              # Script de gestión Django
├── requerimientos.txt     # Dependencias Python
└── .env                   # Variables de entorno (no versionar)
```

### D. Tablas Principales de la Base de Datos

- `productos` - Productos del inventario
- `ventas` - Ventas realizadas
- `detalle_venta` - Detalles de cada venta
- `lotes` - Lotes de productos
- `movimientos_inventario` - Movimientos de inventario
- `historial_boletas` - Historial de boletas emitidas
- `historial_merma` - Historial de productos en merma
- `alertas` - Alertas del sistema
- `proveedor` - Proveedores
- `factura_proveedor` - Facturas de proveedores
- `detalle_factura_proveedor` - Detalles de facturas
- `pago_proveedor` - Pagos a proveedores
- `usuarios` - Usuarios del sistema
- `roles` - Roles de usuarios
- `clientes` - Clientes
- `categorias` - Categorías de productos

---

**Última actualización:** Diciembre 2025  
**Versión del Manual:** 2.0  
**Próxima revisión:** Marzo 2026  
**Proyecto:** PrototipoForneria - Django 5.2.7

