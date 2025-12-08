# 🛠️ Plan de Correcciones de Seguridad

## 📋 Resumen

**Estado Actual**: ⚠️ Requiere correcciones críticas antes de producción  
**Tiempo Estimado**: 1-2 horas  
**Prioridad**: 🔴 URGENTE

---

## ✅ PASOS PARA APLICAR CORRECCIONES

### Paso 1: Instalar python-decouple

```bash
pip install python-decouple
```

Agregar a `requerimientos.txt`:
```
python-decouple==3.8
```

---

### Paso 2: Crear archivo .env

En la raíz del proyecto, crear archivo `.env`:

```env
SECRET_KEY=tu-secret-key-generado-aleatoriamente
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,52.200.181.180
CSRF_TRUSTED_ORIGINS=https://52.200.181.180
DB_NAME=forneria
DB_USER=forneria_user
DB_PASSWORD=Ventana$123
DB_HOST=localhost
DB_PORT=3306
```

**⚠️ IMPORTANTE**: 
- Generar un nuevo SECRET_KEY para producción
- Cambiar la contraseña de BD si es necesario
- NO subir .env a git (ya está en .gitignore)

---

### Paso 3: Generar nuevo SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copiar el resultado al archivo `.env`

---

### Paso 4: Actualizar settings.py

**Opción A**: Reemplazar completamente con `settings_seguro.py`

**Opción B**: Integrar las mejoras manualmente:

1. Agregar al inicio:
```python
from decouple import config
```

2. Cambiar SECRET_KEY:
```python
SECRET_KEY = config('SECRET_KEY', default='django-insecure-...')
```

3. Cambiar DEBUG:
```python
DEBUG = config('DEBUG', default=False, cast=bool)
```

4. Cambiar DATABASES:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME', default='forneria'),
        'USER': config('DB_USER', default='forneria_user'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

5. Cambiar CSRF_TRUSTED_ORIGINS:
```python
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='http://localhost',
    cast=lambda v: [s.strip() for s in v.split(',')]
)
```

6. Agregar configuración de logging (ver `settings_seguro.py`)

---

### Paso 5: Crear directorio de logs

```bash
mkdir logs
```

Agregar a `.gitignore`:
```
logs/
*.log
```

---

### Paso 6: Probar en desarrollo

1. Crear `.env` con `DEBUG=True` para desarrollo
2. Probar que todo funciona
3. Verificar que los logs se crean correctamente

---

### Paso 7: Configurar para producción

1. Cambiar `DEBUG=False` en `.env`
2. Cambiar `CSRF_TRUSTED_ORIGINS` a HTTPS
3. Configurar HTTPS en el servidor
4. Verificar que los logs funcionan

---

## ✅ CHECKLIST DE VERIFICACIÓN

- [ ] Instalado python-decouple
- [ ] Creado archivo .env
- [ ] Generado nuevo SECRET_KEY
- [ ] Actualizado settings.py
- [ ] Creado directorio logs/
- [ ] Probado en desarrollo
- [ ] Configurado para producción
- [ ] Verificado que .env está en .gitignore

---

## 📝 NOTAS IMPORTANTES

1. **NUNCA** subir `.env` a git
2. **SIEMPRE** usar variables de entorno para secretos
3. **SIEMPRE** tener `DEBUG=False` en producción
4. **SIEMPRE** usar HTTPS en producción
5. **SIEMPRE** tener logging configurado

---

## 🚀 DESPUÉS DE APLICAR CORRECCIONES

1. Probar todas las funcionalidades
2. Verificar que los logs se generan
3. Verificar que no hay errores en producción
4. Documentar cambios

---

**Fecha**: Hoy  
**Estado**: Pendiente de aplicación

