# 📋 Documentación: Sistema de Proveedores y Facturas

## 📊 Diagrama de Relaciones y Cardinalidades

```
┌─────────────┐
│  PROVEEDOR  │
│             │
│ - id (PK)   │
│ - nombre    │
│ - rut       │
│ - contacto  │
│ - telefono  │
│ - email     │
│ - direccion │
│ - estado    │
└──────┬──────┘
       │
       │ 1
       │
       │ N (Uno a Muchos)
       │
       ▼
┌──────────────────────┐
│ FACTURA_PROVEEDOR    │
│                      │
│ - id (PK)            │
│ - numero_factura     │
│ - fecha_factura      │
│ - fecha_vencimiento  │
│ - subtotal           │
│ - iva                │
│ - total              │
│ - estado_pago        │
│ - proveedor_id (FK)  │
└──────┬───────────────┘
       │
       │ 1
       │
       │ N (Uno a Muchos)
       │
       ▼
┌──────────────────────────────┐
│ DETALLE_FACTURA_PROVEEDOR    │
│                              │
│ - id (PK)                    │
│ - cantidad                   │
│ - precio_unitario            │
│ - descuento_pct              │
│ - subtotal                   │
│ - fecha_vencimiento_producto │
│ - lote                       │
│ - factura_proveedor_id (FK)  │
│ - productos_id (FK)          │
└──────────────┬───────────────┘
               │
               │ N
               │
               │ 1 (Muchos a Uno)
               │
               ▼
       ┌─────────────┐
       │  PRODUCTOS  │
       │             │
       │ - id (PK)   │
       │ - nombre    │
       │ - precio    │
       │ - cantidad  │
       │ - stock_... │
       └─────────────┘
```

## 🔗 Cardinalidades Detalladas

### 1. Proveedor ↔ FacturaProveedor
- **Tipo**: Uno a Muchos (1:N)
- **Descripción**: 
  - Un proveedor puede tener muchas facturas
  - Una factura pertenece a un solo proveedor
- **Foreign Key**: `factura_proveedor.proveedor_id` → `proveedor.id`
- **Restricciones**:
  - `ON DELETE RESTRICT`: No se puede eliminar un proveedor que tenga facturas asociadas
  - `ON UPDATE CASCADE`: Si cambia el ID del proveedor, se actualiza en todas sus facturas

### 2. FacturaProveedor ↔ DetalleFacturaProveedor
- **Tipo**: Uno a Muchos (1:N)
- **Descripción**:
  - Una factura puede tener muchos detalles (productos)
  - Un detalle pertenece a una sola factura
- **Foreign Key**: `detalle_factura_proveedor.factura_proveedor_id` → `factura_proveedor.id`
- **Restricciones**:
  - `ON DELETE CASCADE`: Si se elimina la factura, se eliminan automáticamente todos sus detalles
  - `ON UPDATE CASCADE`: Si cambia el ID de la factura, se actualiza en todos sus detalles

### 3. Productos ↔ DetalleFacturaProveedor
- **Tipo**: Uno a Muchos (1:N)
- **Descripción**:
  - Un producto puede aparecer en muchos detalles de factura
  - Un detalle corresponde a un solo producto
- **Foreign Key**: `detalle_factura_proveedor.productos_id` → `productos.id`
- **Restricciones**:
  - `ON DELETE RESTRICT`: No se puede eliminar un producto que tenga detalles de factura asociados
  - `ON UPDATE CASCADE`: Si cambia el ID del producto, se actualiza en todos sus detalles

### 4. FacturaProveedor ↔ Productos (Relación N:M)
- **Tipo**: Muchos a Muchos (N:M)
- **Implementación**: A través de la tabla intermedia `detalle_factura_proveedor`
- **Descripción**:
  - Una factura puede contener múltiples productos
  - Un producto puede venir en múltiples facturas
  - La tabla intermedia almacena información específica de cada relación:
    - Cantidad recibida
    - Precio unitario de compra
    - Descuento aplicado
    - Fecha de vencimiento del lote
    - Número de lote

## 📝 Lógica de Negocio

### 1. Registro de Proveedor

**Flujo**:
1. Se crea un nuevo proveedor con estado `'activo'`
2. El RUT debe ser único en el sistema
3. Se pueden registrar datos de contacto opcionales
4. El proveedor puede marcarse como `'inactivo'` sin eliminarlo físicamente (eliminación lógica)

**Validaciones**:
- RUT único (si se proporciona)
- Nombre obligatorio
- Email válido (si se proporciona)

**Ejemplo**:
```python
proveedor = Proveedor.objects.create(
    nombre="Distribuidora de Harinas S.A.",
    rut="76543210-8",
    contacto="Juan Pérez",
    telefono="+56912345678",
    email="contacto@harinas.cl",
    estado="activo"
)
```

### 2. Registro de Factura

**Flujo**:
1. Se crea una factura asociada a un proveedor
2. El número de factura debe ser único por proveedor (mismo número puede existir en diferentes proveedores)
3. Estado inicial: `'pendiente'`
4. Se registran fechas importantes:
   - `fecha_factura`: Fecha de emisión
   - `fecha_vencimiento`: Fecha límite de pago
   - `fecha_recepcion`: Fecha en que se recibió físicamente
5. Los totales se calculan automáticamente desde los detalles

**Validaciones**:
- Número de factura + proveedor debe ser único
- Fecha de factura obligatoria
- Totales no negativos

**Ejemplo**:
```python
factura = FacturaProveedor.objects.create(
    numero_factura="FAC-2025-001",
    fecha_factura="2025-01-15",
    fecha_vencimiento="2025-02-15",
    fecha_recepcion="2025-01-16",
    proveedor=proveedor,
    estado_pago="pendiente"
)
```

### 3. Registro de Detalle de Factura

**Flujo**:
1. Se agregan productos a la factura creando detalles
2. Cada detalle incluye:
   - Producto específico
   - Cantidad recibida
   - Precio unitario de compra
   - Descuento (opcional)
   - Información del lote (opcional)
3. El subtotal se calcula automáticamente: `cantidad × precio_unitario × (1 - descuento_pct/100)`
4. Al guardar un detalle, se actualiza el total de la factura
5. **IMPORTANTE**: Al confirmar la recepción de la factura, se debe actualizar el stock de productos

**Validaciones**:
- Cantidad mínima: 1
- Precio unitario no negativo
- Descuento entre 0 y 100%

**Ejemplo**:
```python
detalle = DetalleFacturaProveedor.objects.create(
    factura_proveedor=factura,
    productos=producto_harina,
    cantidad=50,
    precio_unitario=1500.00,
    descuento_pct=5.00,
    fecha_vencimiento_producto="2025-12-31",
    lote="LOTE-2025-001"
)
detalle.actualizar_subtotal()  # Calcula y guarda el subtotal
factura.actualizar_totales()   # Actualiza totales de la factura
```

### 4. Actualización de Stock

**Flujo cuando se recibe una factura**:
1. Se marca `fecha_recepcion` en la factura
2. Para cada detalle de la factura:
   - Se suma la `cantidad` al `stock_actual` del producto
   - Se suma la `cantidad` a la `cantidad` del producto
   - Si hay `fecha_vencimiento_producto` en el detalle, se actualiza `caducidad` del producto
3. Se puede usar el método `actualizar_stock_producto()` del detalle

**Ejemplo**:
```python
# Confirmar recepción de factura
factura.fecha_recepcion = date.today()
factura.save()

# Actualizar stock de cada producto
for detalle in factura.detalles.all():
    detalle.actualizar_stock_producto()
```

### 5. Control de Pagos

**Estados de Pago**:
- `'pendiente'`: Factura sin pagar
- `'pagado'`: Factura completamente pagada
- `'parcial'`: Factura pagada parcialmente
- `'cancelado'`: Factura cancelada/anulada

**Flujo de Pago**:
1. Al marcar como pagado, se registra:
   - `estado_pago = 'pagado'`
   - `fecha_pago`: Fecha del pago
   - `metodo_pago`: Método utilizado (transferencia, efectivo, cheque, etc.)
2. Se puede usar el método `marcar_como_pagada()`

**Alertas Recomendadas**:
- Facturas próximas a vencer (7 días antes)
- Facturas vencidas sin pagar
- Reportes de facturas pendientes por proveedor

**Ejemplo**:
```python
factura.marcar_como_pagada(
    fecha_pago=date.today(),
    metodo_pago="Transferencia bancaria"
)
```

### 6. Eliminación Lógica

**Principio**: No se eliminan físicamente los registros, se marcan con timestamp.

**Implementación**:
- Campo `eliminado`: `NULL` = activo, `timestamp` = eliminado
- Todas las consultas deben filtrar: `WHERE eliminado IS NULL`
- Permite mantener historial completo

**Ejemplo**:
```python
# Eliminar lógicamente
proveedor.eliminado = timezone.now()
proveedor.save()

# Consultar solo activos
proveedores_activos = Proveedor.objects.filter(eliminado__isnull=True)
```

## 🔍 Consultas Útiles

### Obtener facturas pendientes de un proveedor
```python
proveedor = Proveedor.objects.get(id=1)
facturas_pendientes = proveedor.obtener_facturas_pendientes()
```

### Obtener total pendiente de un proveedor
```python
total_pendiente = proveedor.obtener_total_pendiente()
```

### Obtener facturas vencidas
```python
from datetime import date
facturas_vencidas = FacturaProveedor.objects.filter(
    fecha_vencimiento__lt=date.today(),
    estado_pago='pendiente',
    eliminado__isnull=True
)
```

### Obtener productos recibidos en una factura
```python
factura = FacturaProveedor.objects.get(id=1)
productos = [detalle.productos for detalle in factura.detalles.all()]
```

### Obtener todas las facturas donde aparece un producto
```python
producto = Productos.objects.get(id=1)
facturas = FacturaProveedor.objects.filter(
    detalles__productos=producto,
    eliminado__isnull=True
).distinct()
```

### Registrar un pago parcial
```python
from ventas.models import PagoProveedor

pago = PagoProveedor.objects.create(
    factura_proveedor=factura,
    monto=50000.00,
    fecha_pago=date.today(),
    metodo_pago="Transferencia bancaria",
    comprobante="TRF-123456"
)
# El estado de la factura se actualiza automáticamente
```

### Cancelar recepción de factura (revertir stock)
```python
factura.cancelar_recepcion()
# Esto revierte el stock y crea movimientos de salida
```

### Calcular saldo pendiente de una factura
```python
saldo = factura.calcular_saldo_pendiente()
total_pagado = factura.calcular_total_pagado()
```

## 📈 Reportes Recomendados

1. **Facturas Pendientes por Proveedor**
   - Lista de facturas sin pagar agrupadas por proveedor
   - Total pendiente por proveedor

2. **Facturas Próximas a Vencer**
   - Facturas que vencen en los próximos 7 días
   - Alertas automáticas

3. **Historial de Compras por Producto**
   - Todas las facturas donde se compró un producto específico
   - Precio histórico de compra

4. **Proveedores Activos**
   - Lista de proveedores con estado activo
   - Total de facturas y monto total por proveedor

5. **Análisis de Compras**
   - Total comprado por mes
   - Proveedores más utilizados
   - Productos más comprados

## ⚠️ Consideraciones Importantes

1. **Integridad Referencial**: 
   - No se pueden eliminar proveedores con facturas
   - No se pueden eliminar productos con detalles de factura
   - Las facturas se pueden eliminar (CASCADE elimina detalles)
   - No se pueden eliminar facturas con pagos registrados

2. **Cálculo de Totales**:
   - Siempre calcular desde los detalles
   - Actualizar totales después de modificar detalles
   - **IVA en Chile: 19%** - Se calcula sobre el subtotal ANTES de descuentos
   - Fórmula: `subtotal_sin_descuento → IVA = subtotal * 0.19 → total = (subtotal + IVA) - descuento`

3. **Actualización de Stock**:
   - Solo actualizar stock cuando `estado_recepcion = 'recibida'`
   - Se crean movimientos de inventario automáticamente
   - Considerar fechas de vencimiento del lote
   - Registrar número de lote para trazabilidad
   - Se puede revertir con `cancelar_recepcion()`

4. **Validaciones de Fechas**:
   - `fecha_vencimiento` debe ser posterior a `fecha_factura`
   - `fecha_recepcion` debe ser posterior o igual a `fecha_factura`
   - Validaciones automáticas en el modelo

5. **Pagos Parciales**:
   - Se pueden registrar múltiples pagos a una factura
   - El estado de pago se actualiza automáticamente
   - Validación: no se puede pagar más del saldo pendiente

6. **Unicidad**:
   - RUT de proveedor único
   - Número de factura único por proveedor (no globalmente)

7. **Auditoría**:
   - Campos `creado` y `modificado` se actualizan automáticamente
   - Usar eliminación lógica para mantener historial
   - Movimientos de inventario con trazabilidad completa

## 🚀 Próximos Pasos Recomendados

1. Crear vistas y formularios para gestión de proveedores
2. Implementar sistema de alertas para facturas vencidas
3. Crear reportes de compras y pagos
4. Implementar sistema de órdenes de compra (opcional)
5. Agregar sistema de evaluación de proveedores (opcional)

