# 🎬 Plan de Acción - 4 Días para Video Demo

## 📋 Situación Actual
- ✅ **Tiempo**: 4 días
- ✅ **Objetivo**: Video demostración del software
- ✅ **Base de datos**: MySQL en WAMP (local)
- ✅ **AWS**: Free Tier disponible
- ✅ **Presentación**: Video, no demo en vivo

---

## 🎯 FUNCIONALIDADES MANDATORIAS (Lo Obvio del Negocio)

### 1. Sistema de Ventas (POS) ⭐ CRÍTICO
- [x] Interfaz de punto de venta
- [x] Agregar productos al carrito
- [x] Calcular totales con IVA
- [x] Procesar venta
- [ ] **FALTA**: Validar stock antes de vender
- [ ] **FALTA**: Crear movimiento de inventario al vender

### 2. Gestión de Productos ⭐ CRÍTICO
- [x] Agregar productos
- [x] Editar productos
- [x] Ver inventario
- [x] Eliminar (lógico)
- [x] Stock actual

### 3. Sistema de Inventario ⭐ CRÍTICO
- [x] Ver productos
- [x] Stock actual
- [x] Alertas de vencimiento
- [x] Movimientos de inventario
- [x] Gestión de merma

### 4. Dashboard ⭐ IMPORTANTE
- [x] Métricas principales
- [x] Ventas del día
- [x] Stock bajo
- [x] Alertas pendientes

### 5. Sistema de Proveedores ⭐ NUEVO (Ya implementado)
- [x] Gestión de proveedores
- [x] Facturas de compra
- [x] Detalles de factura
- [x] Actualización de stock al recibir

### 6. Reportes ⭐ OPCIONAL
- [x] Reportes básicos
- [ ] Mejorar si hay tiempo

---

## 🔧 CORRECCIONES CRÍTICAS (Hacer HOY)

### 1. Validar Stock Antes de Vender
**Archivo**: `ventas/views/views_pos.py`
**Tiempo**: 15 minutos

### 2. Crear Movimiento de Inventario al Vender
**Archivo**: `ventas/views/views_pos.py`  
**Tiempo**: 10 minutos
**Estado**: Ya está implementado, solo verificar

### 3. Verificar que Todo Funciona Localmente
**Tiempo**: 1 hora
- Probar cada funcionalidad
- Anotar bugs críticos
- Corregir solo lo que impida funcionar

---

## 📹 PLAN PARA EL VIDEO DEMO

### Estructura del Video (5-7 minutos)

1. **Introducción (30 seg)**
   - Mostrar landing page
   - Login al sistema

2. **Dashboard (1 min)**
   - Mostrar métricas
   - Explicar qué muestra

3. **Gestión de Productos (1.5 min)**
   - Agregar producto nuevo
   - Editar producto existente
   - Ver inventario

4. **Sistema de Ventas (2 min)** ⭐ MÁS IMPORTANTE
   - Abrir POS
   - Agregar productos al carrito
   - Calcular total
   - Procesar venta
   - Mostrar que se actualiza stock

5. **Sistema de Proveedores (1 min)**
   - Crear proveedor
   - Registrar factura de compra
   - Mostrar que actualiza stock

6. **Alertas y Merma (1 min)**
   - Mostrar alertas de vencimiento
   - Mover producto a merma

7. **Cierre (30 seg)**
   - Mostrar que está desplegado en AWS (opcional)
   - Resumen de funcionalidades

---

## 🗓️ CRONOGRAMA 4 DÍAS

### DÍA 1 (HOY) - Correcciones Críticas
**Tiempo**: 2-3 horas

- [ ] Validar stock antes de vender
- [ ] Verificar movimientos de inventario en ventas
- [ ] Probar TODAS las funcionalidades
- [ ] Anotar bugs críticos
- [ ] Corregir solo lo que impida funcionar

**Resultado**: Software funcionando 100% localmente

### DÍA 2 - Preparación para Video
**Tiempo**: 2-3 horas

- [ ] Preparar datos de prueba (productos, proveedores)
- [ ] Crear script/narrador para video
- [ ] Practicar flujo de demostración
- [ ] Asegurar que todo se ve bien en pantalla

**Resultado**: Listo para grabar

### DÍA 3 - Grabación del Video
**Tiempo**: 2-4 horas

- [ ] Grabar video completo
- [ ] Editar si es necesario
- [ ] Verificar calidad

**Resultado**: Video demo listo

### DÍA 4 - AWS (Opcional) + Revisión Final
**Tiempo**: 2-3 horas

- [ ] Desplegar en AWS (si hay tiempo)
- [ ] O simplemente mencionar que está preparado
- [ ] Revisar video final
- [ ] Preparar presentación

**Resultado**: Todo listo para presentar

---

## 🐛 BUGS CRÍTICOS A CORREGIR HOY

### 1. Validación de Stock en Ventas

**Problema**: Se puede vender más de lo que hay en stock

**Solución**: Agregar validación antes de procesar venta

**Código a agregar en `ventas/views/views_pos.py`**:

```python
# Antes del transaction.atomic(), agregar:
# Validar stock de todos los productos
for item in carrito:
    producto_id = item.get('producto_id')
    cantidad = int(item.get('cantidad', 0))
    
    try:
        producto = Productos.objects.get(pk=producto_id, eliminado__isnull=True)
        stock_disponible = producto.cantidad if producto.cantidad else 0
        
        if stock_disponible < cantidad:
            return JsonResponse({
                'success': False,
                'mensaje': f'Stock insuficiente para {producto.nombre}. Disponible: {stock_disponible}, Solicitado: {cantidad}'
            }, status=400)
    except Productos.DoesNotExist:
        return JsonResponse({
            'success': False,
            'mensaje': f'Producto no encontrado'
        }, status=404)
```

### 2. Verificar Movimientos de Inventario

**Estado**: Ya debería estar implementado, solo verificar que funciona

**Verificar**: Después de una venta, debe aparecer en "Movimientos de Inventario"

---

## 📊 SOBRE JIRA

Puedes compartir Jira de varias formas:

1. **Screenshots** (Más fácil)
   - Captura de pantalla de las tareas/requisitos
   - Sube las imágenes

2. **Exportar de Jira**
   - Jira → Exportar → CSV o Excel
   - Comparte el archivo

3. **Copiar y pegar**
   - Copia el texto de las tareas principales
   - Pégalo aquí

4. **Describir**
   - Dime qué funcionalidades pide el proyecto
   - Lista de requisitos principales

**Cualquiera de estas opciones funciona. Lo más fácil son screenshots.**

---

## ✅ CHECKLIST FINAL (Antes de Grabar Video)

### Funcionalidades que DEBEN funcionar:
- [ ] Login funciona
- [ ] Dashboard muestra datos
- [ ] Se pueden agregar productos
- [ ] Se pueden editar productos
- [ ] Se puede ver inventario
- [ ] POS funciona (agregar al carrito)
- [ ] Se puede procesar una venta
- [ ] Stock se actualiza al vender
- [ ] Se pueden crear proveedores
- [ ] Se pueden registrar facturas de compra
- [ ] Stock se actualiza al recibir factura
- [ ] Alertas funcionan
- [ ] Merma funciona

### Datos de Prueba Preparados:
- [ ] Al menos 10 productos diferentes
- [ ] Al menos 2 proveedores
- [ ] Al menos 1 factura de compra
- [ ] Al menos 1 venta realizada
- [ ] Al menos 1 alerta generada

---

## 🚀 ACCIÓN INMEDIATA (HOY)

1. **Corregir validación de stock** (15 min)
2. **Probar todas las funcionalidades** (1 hora)
3. **Anotar bugs críticos** (30 min)
4. **Corregir solo lo crítico** (1 hora)

**Total**: ~3 horas de trabajo hoy

---

## 💡 CONSEJOS PARA EL VIDEO

1. **Prepara datos de prueba realistas**
   - Productos con nombres claros
   - Precios coherentes
   - Stock variado

2. **Practica el flujo antes de grabar**
   - Sabe qué vas a hacer en cada paso
   - Evita pausas largas

3. **Muestra lo más importante primero**
   - POS es lo más impresionante
   - Dashboard muestra que funciona

4. **Si algo falla, sigue adelante**
   - No te detengas mucho en errores
   - Muestra que el sistema funciona en general

5. **Menciona las funcionalidades nuevas**
   - Sistema de proveedores
   - Facturas de compra
   - Trazabilidad completa

---

## ❓ ¿QUÉ NECESITAS AHORA?

1. **¿Quieres que corrija la validación de stock ahora?** (15 minutos)
2. **¿Puedes compartir Jira?** (screenshots, export, o descripción)
3. **¿Hay alguna funcionalidad específica que deba priorizar?**

**Empecemos con lo crítico y luego ajustamos según Jira.**

