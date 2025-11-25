# 🔔 SISTEMA DE ALERTAS - INSTRUCCIONES COMPLETAS

## 📋 RESUMEN

Se ha implementado un **sistema completo de alertas de vencimiento de productos** para la Forneria con las siguientes características:

- ✅ Lista de alertas con filtros (tipo, estado, producto, fecha)
- ✅ Crear, editar y eliminar alertas
- ✅ Cambiar estado (activa, resuelta, ignorada)
- ✅ Generación automática de alertas
- ✅ Botón en inventario para crear alertas por producto
- ✅ Tema dorado y negro consistente
- ✅ Navegación con sidebar del dashboard

---

## 🚀 PASO 1: ACTUALIZAR LA BASE DE DATOS

**Ejecuta este comando SQL en tu base de datos MySQL:**

```bash
mysql -u forneria_user -p forneria < actualizar_alertas.sql
```

O copia y pega el contenido de `actualizar_alertas.sql` en phpMyAdmin/MySQL Workbench.

**Esto creará la tabla `alertas` con:**
- Tipos de alerta (roja, amarilla, verde)
- Estados (activa, resuelta, ignorada)
- Relación con productos
- Índices para búsquedas rápidas

---

## 📂 ARCHIVOS CREADOS

### **Modelos** (`ventas/models/alertas.py`)
- Modelo `Alertas` con métodos auxiliares
- Método estático `generar_alertas_automaticas()`
- Métodos para calcular días hasta vencer

### **Formularios** (`ventas/funciones/formularios_alertas.py`)
- `AlertaForm`: Crear/editar alertas
- `AlertaFiltroForm`: Filtros de búsqueda
- `CambiarEstadoAlertasForm`: Cambio masivo de estados

### **Vistas** (`ventas/views/views_alertas.py`)
- `alertas_list_view`: Lista con filtros
- `alerta_crear_view`: Crear alerta
- `alerta_editar_view`: Editar alerta
- `alerta_eliminar_view`: Eliminar alerta
- `alerta_cambiar_estado_ajax`: API para cambiar estado
- `generar_alertas_automaticas_view`: API para generar alertas
- `generar_alerta_desde_producto`: Crear desde inventario

### **Templates**
- `templates/alertas_list.html`: Lista principal
- `templates/alerta_form.html`: Formulario crear/editar
- `templates/alerta_confirmar_eliminar.html`: Confirmación

### **CSS** (`static/css/pages/_alertas.css`)
- Tema dorado y negro
- Animaciones para alertas urgentes
- Estilos responsive

### **JavaScript** (`static/js/alertas.js`)
- Cambiar estado sin recargar (AJAX)
- Generar alertas automáticas
- Alertas temporales
- Funciones auxiliares

### **Comando Django** (`ventas/management/commands/generar_alertas.py`)
- Comando: `python manage.py generar_alertas`
- Genera alertas automáticamente
- Modo verbose para ver detalles

---

## 🎯 USO DEL SISTEMA

### **1. Acceder al Sistema de Alertas**

Desde el dashboard, haz clic en el botón:
```
🔔 Alertas
```

### **2. Ver Alertas**

La página principal muestra:
- 📊 **Cards de estadísticas**: Cantidad de alertas por tipo y estado
- 🎛️ **Filtros**: Buscar por tipo, estado, producto, fechas
- 📋 **Tabla**: Listado completo de alertas

**Tipos de alerta:**
- 🔴 **Roja**: 0-13 días hasta vencer (URGENTE)
- 🟡 **Amarilla**: 14-29 días hasta vencer (PRECAUCIÓN)
- 🟢 **Verde**: 30+ días hasta vencer (OK)

### **3. Crear Alerta Manual**

**Opción A: Desde el sistema de alertas**
1. Clic en "Nueva Alerta"
2. Seleccionar producto
3. Elegir tipo de alerta
4. Escribir mensaje
5. Guardar

**Opción B: Desde el inventario**
1. Ir a Inventario
2. En cada producto hay un botón 🔔
3. Se abre formulario pre-llenado
4. Ajustar si es necesario
5. Guardar

### **4. Editar Alerta**

1. En la lista de alertas, clic en ✏️ (Editar)
2. Modificar campos necesarios
3. Guardar cambios

### **5. Eliminar Alerta**

1. En la lista, clic en 🗑️ (Eliminar)
2. Confirmar eliminación
3. La alerta se eliminará permanentemente

### **6. Cambiar Estado de Alerta**

**Desde la tabla:**
1. Clic en el botón ⚙️ (dropdown de acciones)
2. Seleccionar nuevo estado:
   - **Activa**: Pendiente de acción
   - **Resuelta**: Se tomó acción sobre el producto
   - **Ignorada**: Se decidió no actuar

El cambio se aplica inmediatamente sin recargar la página.

### **7. Generar Alertas Automáticas**

**Opción A: Desde la interfaz web**
1. En la página de alertas, clic en "Generar Alertas Automáticas"
2. Confirmar
3. El sistema revisa todos los productos y crea/actualiza alertas

**Opción B: Comando de terminal**
```bash
python manage.py generar_alertas
```

**Con detalles verbose:**
```bash
python manage.py generar_alertas --verbose
```

### **8. Filtrar Alertas**

Usa los filtros en el panel superior:
- **Tipo**: Roja, amarilla o verde
- **Estado**: Activa, resuelta o ignorada
- **Producto**: Buscar por nombre
- **Fechas**: Rango de fechas de generación

---

## ⏰ AUTOMATIZACIÓN (OPCIONAL)

Para que las alertas se generen automáticamente cada día:

### **Windows (Task Scheduler)**

1. Abrir "Programador de tareas"
2. Crear tarea básica
3. Nombre: "Generar Alertas Forneria"
4. Activador: Diariamente a las 6:00 AM
5. Acción: Iniciar programa
6. Programa: `D:\tu\ruta\venv\Scripts\python.exe`
7. Argumentos: `manage.py generar_alertas`
8. Iniciar en: `D:\tu\ruta\Forneria`

### **Linux/Mac (Cron Job)**

1. Abrir crontab:
```bash
crontab -e
```

2. Agregar línea:
```bash
0 6 * * * cd /ruta/a/Forneria && /ruta/a/venv/bin/python manage.py generar_alertas
```

Esto ejecutará el comando todos los días a las 6:00 AM.

---

## 🎨 COLORES Y TEMA

El sistema usa el **tema dorado y negro** consistente:

- **Dorado (#D4AF37)**: Elementos principales, botones, bordes
- **Negro (#0e0e0e)**: Fondo principal
- **Gris oscuro (#141414)**: Fondo alternativo
- **Texto claro (#f2f2f2)**: Texto principal

**Alertas:**
- Roja: `#dc3545`
- Amarilla: `#ffc107`
- Verde: `#28a745`

---

## 📱 RESPONSIVE

El sistema funciona correctamente en:
- ✅ Desktop (1920px+)
- ✅ Laptop (1366px+)
- ✅ Tablet (768px+)
- ✅ Móvil (320px+)

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### **Error: Tabla 'alertas' no existe**
**Solución**: Ejecuta el archivo `actualizar_alertas.sql`

### **Error: No se ven las alertas**
**Solución**: Genera alertas con el botón o el comando:
```bash
python manage.py generar_alertas
```

### **Error: Los filtros no funcionan**
**Solución**: Verifica que el archivo `alertas.js` esté cargándose correctamente

### **Error: No se puede crear alerta desde inventario**
**Solución**: Verifica que las URLs estén correctamente configuradas en `urls.py`

---

## 📊 LÓGICA DE ALERTAS

**El sistema calcula días hasta vencer:**

```python
dias_hasta_vencer = (fecha_caducidad - fecha_actual).days

if dias_hasta_vencer < 0:
    tipo = 'roja'  # VENCIDO
elif dias_hasta_vencer <= 13:
    tipo = 'roja'  # URGENTE (0-13 días)
elif dias_hasta_vencer <= 29:
    tipo = 'amarilla'  # PRECAUCIÓN (14-29 días)
else:
    tipo = 'verde'  # OK (30+ días)
```

---

## 🎓 EJEMPLOS DE USO

### **Ejemplo 1: Producto vence en 5 días**
1. Sistema genera alerta ROJA
2. Mensaje: "Pan integral vence en 5 días - URGENTE"
3. Aparece en la lista con borde rojo y animación
4. Staff puede:
   - Hacer promoción para venderlo rápido
   - Donarlo
   - Descontarlo
   - Marcar alerta como "resuelta" después

### **Ejemplo 2: Producto vence en 20 días**
1. Sistema genera alerta AMARILLA
2. Mensaje: "Galletas avena vence en 20 días - PRECAUCIÓN"
3. Staff planifica promociones próximas
4. Revisa en unos días si sigue con stock

### **Ejemplo 3: Producto vence en 45 días**
1. Sistema genera alerta VERDE
2. Mensaje: "Brownie cacao vence en 45 días - OK"
3. Solo informativo, no requiere acción inmediata

---

## ✅ CHECKLIST DE VERIFICACIÓN

Antes de usar el sistema, verifica:

- [ ] Base de datos actualizada (`actualizar_alertas.sql` ejecutado)
- [ ] Todos los archivos copiados correctamente
- [ ] Servidor Django corriendo
- [ ] Puedes acceder a `http://127.0.0.1:8000/alertas/`
- [ ] Botón de Alertas visible en el dashboard
- [ ] Botón 🔔 visible en cada producto del inventario
- [ ] CSS cargándose correctamente (tema dorado/negro)
- [ ] JavaScript funcionando (cambiar estado sin recargar)

---

## 📞 SOPORTE

Si tienes problemas:
1. Revisa los logs de Django en la consola
2. Revisa la consola del navegador (F12) para errores JavaScript
3. Verifica que todos los archivos estén en su lugar
4. Asegúrate de que la tabla `alertas` exista en MySQL

---

## 🎉 ¡LISTO!

El sistema de alertas está completo y listo para usar. Todas las funcionalidades solicitadas están implementadas con comentarios detallados en cada archivo.

**¡Disfruta tu sistema de alertas!** 🔔✨

