# 🎓 Plan de Implementación - Proyecto Integrado (Presupuesto Limitado)

## 📋 Contexto
- **Proyecto**: Trabajo final de Proyecto Integrado
- **Presupuesto AWS**: ~$30 USD (cuenta estudiante)
- **Objetivo**: Presentación funcional del software
- **Prioridad**: Funcionalidad local + despliegue básico en AWS

---

## ✅ PRIORIDADES AJUSTADAS (Solo lo Esencial)

### 🔴 CRÍTICO - Debe Funcionar para Presentación

1. **Funcionalidad Local Completa**
   - ✅ Sistema de ventas funcionando
   - ✅ Gestión de productos e inventario
   - ✅ Sistema de proveedores y facturas
   - ✅ Dashboard con métricas
   - ✅ Alertas y notificaciones

2. **Correcciones de Lógica de Negocio Esenciales**
   - ✅ Movimientos de inventario en ventas (ya implementado)
   - ✅ Validación de stock antes de venta
   - ✅ Cálculo correcto de IVA

3. **Seguridad Básica (Sin Costos)**
   - Variables de entorno básicas (python-decouple es gratis)
   - Ocultar credenciales del código
   - DEBUG=False en producción

### 🟡 IMPORTANTE - Si Hay Tiempo

4. **Despliegue AWS Mínimo**
   - EC2 t2.micro (gratis 12 meses) o t3.micro (~$7/mes)
   - RDS MySQL db.t3.micro (gratis 12 meses) o ~$15/mes
   - O usar SQLite para presentación (gratis)

5. **Optimizaciones Básicas**
   - Índices esenciales en BD
   - Logging básico

### 🟢 OPCIONAL - Solo si Sobra Presupuesto

6. **Mejoras de Producción**
   - S3 para estáticos (muy barato, ~$0.023/GB)
   - CloudFront (solo si necesario)
   - Multi-tenancy (complejo, no necesario para presentación)

---

## 💰 ESTRATEGIA AWS CON PRESUPUESTO LIMITADO

### Opción 1: MÁXIMA ECONOMÍA (Recomendada para Presentación)

**Costo estimado: $0-5 USD/mes**

```
- EC2 t2.micro (Free Tier: 750 horas/mes gratis por 12 meses)
- RDS MySQL db.t3.micro (Free Tier: 750 horas/mes gratis por 12 meses)
- O mejor: SQLite en EC2 (completamente gratis)
- Elastic IP (gratis si asociado a instancia)
- Domain name opcional: ~$12/año (no necesario, usar IP pública)
```

**Ventajas**:
- ✅ Casi gratis con Free Tier
- ✅ Suficiente para demostración
- ✅ Fácil de configurar

**Desventajas**:
- ⚠️ Limitado en recursos
- ⚠️ Solo para presentación, no producción real

### Opción 2: PRESENTACIÓN LOCAL + DEMO EN AWS

**Costo estimado: $0-2 USD**

```
- Desarrollo y pruebas: 100% local (gratis)
- AWS solo para demo final: EC2 t2.micro (Free Tier)
- SQLite en lugar de RDS (gratis)
- Presentar desde localhost, mostrar AWS como "listo para producción"
```

**Ventajas**:
- ✅ Mínimo costo
- ✅ Control total en presentación
- ✅ No depende de conexión a AWS

---

## 🛠️ IMPLEMENTACIONES MÍNIMAS NECESARIAS

### 1. Variables de Entorno Básicas (GRATIS)

**Archivo `.env`** (no subir a Git):
```env
SECRET_KEY=tu-secret-key-local
DEBUG=True
DB_NAME=forneria
DB_USER=root
DB_PASSWORD=tu-password-local
```

**Modificar `settings.py`**:
```python
from decouple import config

SECRET_KEY = config('SECRET_KEY', default='fallback-key-solo-desarrollo')
DEBUG = config('DEBUG', default=True, cast=bool)
```

**Costo**: $0 (python-decouple es gratis)

### 2. Corrección de Movimientos en Ventas (YA HECHO)

✅ Ya implementado en `views_pos.py`

### 3. Validación de Stock (CRÍTICO)

Agregar validación antes de procesar venta.

### 4. Configuración para AWS Mínima

**Para EC2 + SQLite** (más económico):
- No necesita RDS
- SQLite funciona perfecto para demo
- Solo necesita EC2

---

## 📊 COMPARACIÓN DE COSTOS AWS

| Servicio | Free Tier | Post Free Tier | Recomendación |
|----------|-----------|----------------|---------------|
| EC2 t2.micro | ✅ 750h/mes (12 meses) | ~$7/mes | ✅ Usar |
| EC2 t3.micro | ❌ | ~$7.50/mes | Si necesitas más potencia |
| RDS db.t3.micro | ✅ 750h/mes (12 meses) | ~$15/mes | ⚠️ Solo si necesario |
| SQLite | ✅ Siempre gratis | ✅ Gratis | ✅ **RECOMENDADO para demo** |
| S3 | ✅ 5GB/mes (12 meses) | ~$0.023/GB | Opcional |
| CloudFront | ❌ | ~$0.085/GB | ❌ No necesario |

**Recomendación**: EC2 t2.micro (Free Tier) + SQLite = **$0/mes**

---

## 🎯 PLAN DE ACCIÓN SIMPLIFICADO

### Fase 1: Local (HOY - Sin Costos)
1. ✅ Verificar que todo funciona localmente
2. ✅ Corregir bugs críticos
3. ✅ Agregar validación de stock
4. ✅ Configurar variables de entorno básicas

### Fase 2: Preparación AWS (1-2 días antes de presentación)
1. Crear instancia EC2 t2.micro (Free Tier)
2. Instalar Python, MySQL/SQLite, Nginx
3. Configurar aplicación
4. Probar acceso

### Fase 3: Presentación
1. Mostrar funcionamiento local (principal)
2. Mostrar que está desplegado en AWS (opcional)
3. Demostrar funcionalidades principales

---

## 🔧 CONFIGURACIÓN MÍNIMA NECESARIA

### Para Desarrollo Local:
```python
# settings.py - Versión simplificada
DEBUG = True  # OK para desarrollo
SECRET_KEY = 'desarrollo-local'  # OK para desarrollo
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # ... configuración local
    }
}
```

### Para AWS (Producción):
```python
# settings.py - Detectar entorno
import os

if os.environ.get('AWS'):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # Configuración AWS
else:
    DEBUG = True
    SECRET_KEY = 'desarrollo'
    # Configuración local
```

---

## 📝 CHECKLIST PARA PRESENTACIÓN

### Funcionalidades que DEBEN funcionar:
- [ ] Login/Registro de usuarios
- [ ] Dashboard con métricas
- [ ] Gestión de productos (CRUD)
- [ ] Sistema POS (ventas)
- [ ] Gestión de inventario
- [ ] Alertas de vencimiento
- [ ] Gestión de merma
- [ ] Sistema de proveedores (nuevo)
- [ ] Facturas de proveedores (nuevo)
- [ ] Reportes básicos

### Para AWS (Opcional):
- [ ] Instancia EC2 creada
- [ ] Aplicación desplegada
- [ ] Accesible desde internet
- [ ] Funciona correctamente

---

## 💡 RECOMENDACIONES FINALES

1. **Enfócate en funcionalidad local primero**
   - Asegúrate que todo funciona perfecto localmente
   - AWS es solo "bonus" para la presentación

2. **Usa Free Tier de AWS**
   - EC2 t2.micro es gratis 12 meses
   - SQLite es gratis siempre
   - No necesitas RDS para demo

3. **Prepara demo local como respaldo**
   - Si AWS falla, puedes presentar desde local
   - Tienes control total

4. **Documenta lo que funciona**
   - Para la presentación, muestra funcionalidades
   - Menciona que está preparado para AWS

---

## ❓ PREGUNTAS PARA TI

1. **¿Tienes acceso a Free Tier de AWS?** (Primeros 12 meses)
2. **¿Cuánto tiempo tienes antes de la presentación?**
3. **¿Qué funcionalidades son MANDATORIAS para la presentación?**
4. **¿Prefieres SQLite (gratis) o MySQL en RDS (puede costar)?**

---

## 🚀 PRÓXIMOS PASOS INMEDIATOS

1. **Revisar Jira** (si me lo compartes) para entender requisitos exactos
2. **Priorizar funcionalidades** según lo que pide el proyecto
3. **Implementar solo lo crítico** para que funcione
4. **Preparar despliegue AWS mínimo** (solo si necesario)

**¿Quieres que revise tu Jira para entender mejor los requisitos del proyecto?**

