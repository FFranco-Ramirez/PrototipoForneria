# 📦 ¿Para qué sirve el Sistema de Facturas de Proveedores?

## 🎯 Propósito Principal

El sistema de **Facturas de Proveedores** permite a la Fornería:
1. **Registrar las compras** que haces a tus proveedores (harina, azúcar, levadura, etc.)
2. **Controlar el inventario** automáticamente cuando recibes productos
3. **Gestionar los pagos** que debes hacer a tus proveedores
4. **Llevar un historial** de todas tus compras para contabilidad

---

## 🏪 Ejemplo Práctico: Escenario Real

Imagina que eres dueño de una panadería y necesitas comprar ingredientes:

### **Situación:**
- Necesitas comprar harina, azúcar y levadura
- Tu proveedor es "Distribuidora ABC"
- Te envían una factura por $50,000

### **¿Qué hace el sistema?**

#### 1️⃣ **Registrar la Factura**
```
Proveedor: Distribuidora ABC
Número de Factura: FAC-001-2025
Fecha: 07/12/2025
Productos:
  - Harina: 20 kg × $1,500 = $30,000
  - Azúcar: 10 kg × $1,200 = $12,000
  - Levadura: 5 kg × $1,600 = $8,000
Subtotal: $50,000
IVA (19%): $9,500
Total: $59,500
```

#### 2️⃣ **Recibir la Factura y Actualizar Stock**
Cuando recibes físicamente los productos:
- Haces clic en "Recibir Factura"
- El sistema **automáticamente**:
  - ✅ Aumenta el stock de harina en 20 kg
  - ✅ Aumenta el stock de azúcar en 10 kg
  - ✅ Aumenta el stock de levadura en 5 kg
  - ✅ Crea movimientos de inventario (para trazabilidad)

#### 3️⃣ **Registrar Pagos**
Cuando pagas al proveedor:
- Registras el pago: $30,000 (pago parcial)
- El sistema actualiza: "Pendiente: $29,500"
- Cuando pagas el resto, marca la factura como "Pagada"

---

## 🔄 Flujo Completo del Sistema

```
┌─────────────────┐
│   PROVEEDOR     │
│ Distribuidora   │
│      ABC        │
└────────┬────────┘
         │
         │ 1. Envía factura
         ▼
┌─────────────────┐
│  CREAR FACTURA  │
│  - Número       │
│  - Fecha        │
│  - Productos    │
│  - Totales      │
└────────┬────────┘
         │
         │ 2. Agregar productos
         ▼
┌─────────────────┐
│ DETALLES FACTURA│
│ - Harina: 20 kg │
│ - Azúcar: 10 kg │
│ - Levadura: 5kg │
└────────┬────────┘
         │
         │ 3. Recibir físicamente
         ▼
┌─────────────────┐
│ RECIBIR FACTURA │
│ ✅ Actualiza    │
│    stock        │
│ ✅ Crea         │
│    movimientos  │
└────────┬────────┘
         │
         │ 4. Pagar al proveedor
         ▼
┌─────────────────┐
│ REGISTRAR PAGO  │
│ - Monto         │
│ - Fecha         │
│ - Método        │
└─────────────────┘
```

---

## 📊 Componentes del Sistema

### 1. **Proveedores** (`proveedor`)
**¿Qué es?** La información de tus proveedores

**Ejemplo:**
```
Nombre: Distribuidora ABC
RUT: 76.123.456-7
Contacto: Juan Pérez
Teléfono: +56 9 1234 5678
Email: contacto@distribuidoraabc.cl
Estado: Activo
```

**¿Para qué sirve?**
- Tener todos los datos de contacto
- Saber a quién le compras
- Filtrar facturas por proveedor

---

### 2. **Facturas de Proveedor** (`factura_proveedor`)
**¿Qué es?** El documento de compra que recibes del proveedor

**Campos importantes:**
- `numero_factura`: "FAC-001-2025" (número único)
- `fecha_factura`: Cuándo se emitió
- `fecha_vencimiento`: Cuándo debes pagar
- `estado_pago`: pendiente / parcial / pagado
- `estado_recepcion`: pendiente / recibida

**Estados:**
- **Pendiente**: La factura está creada pero no has recibido los productos
- **Recibida**: Ya recibiste los productos físicamente (stock actualizado)
- **Pagada**: Ya pagaste al proveedor

---

### 3. **Detalles de Factura** (`detalle_factura_proveedor`)
**¿Qué es?** Los productos específicos que vienen en cada factura

**Ejemplo:**
```
Factura: FAC-001-2025
Detalles:
  - Producto: Harina
    Cantidad: 20 kg
    Precio unitario: $1,500
    Subtotal: $30,000
  
  - Producto: Azúcar
    Cantidad: 10 kg
    Precio unitario: $1,200
    Subtotal: $12,000
```

**¿Para qué sirve?**
- Saber exactamente qué productos compraste
- Calcular el total de la factura
- Actualizar el stock de cada producto

---

### 4. **Pagos a Proveedores** (`pago_proveedor`)
**¿Qué es?** El registro de cada pago que haces al proveedor

**Ejemplo:**
```
Factura: FAC-001-2025 (Total: $59,500)
Pagos realizados:
  - Pago 1: $30,000 (07/12/2025) - Transferencia
  - Pago 2: $29,500 (15/12/2025) - Efectivo
Estado: Pagado ✅
```

**¿Para qué sirve?**
- Llevar control de cuánto has pagado
- Saber cuánto debes aún
- Historial de pagos para contabilidad

---

## 🎯 Beneficios del Sistema

### ✅ **Control de Inventario Automático**
- Cuando recibes una factura, el stock se actualiza automáticamente
- No tienes que actualizar manualmente cada producto
- Trazabilidad completa (sabes de dónde vino cada producto)

### ✅ **Control de Pagos**
- Sabes exactamente cuánto debes a cada proveedor
- Puedes pagar parcialmente
- El sistema calcula automáticamente el saldo pendiente

### ✅ **Historial y Reportes**
- Tienes un registro de todas tus compras
- Puedes ver qué compraste a quién y cuándo
- Útil para contabilidad y auditorías

### ✅ **Integración con el Sistema**
- Las compras se reflejan en el inventario
- Los movimientos de inventario se crean automáticamente
- Todo está conectado y sincronizado

---

## 📝 Ejemplo Completo: Paso a Paso

### **Paso 1: Crear Proveedor**
```
Vas a: Proveedores → Crear
Llenas:
  - Nombre: "Distribuidora ABC"
  - RUT: "76.123.456-7"
  - Teléfono: "+56 9 1234 5678"
  - Email: "contacto@distribuidoraabc.cl"
Guardas ✅
```

### **Paso 2: Crear Factura**
```
Vas a: Facturas Proveedores → Crear
Seleccionas: Distribuidora ABC
Llenas:
  - Número: "FAC-001-2025"
  - Fecha: 07/12/2025
  - Fecha vencimiento: 15/12/2025
Guardas ✅
```

### **Paso 3: Agregar Productos a la Factura**
```
En la factura, haces clic en "Agregar Producto"
Agregas:
  - Harina: 20 kg × $1,500
  - Azúcar: 10 kg × $1,200
  - Levadura: 5 kg × $1,600
El sistema calcula automáticamente:
  - Subtotal: $50,000
  - IVA (19%): $9,500
  - Total: $59,500
```

### **Paso 4: Recibir la Factura (Actualizar Stock)**
```
Cuando recibes físicamente los productos:
Haces clic en "Recibir Factura y Actualizar Stock"
El sistema:
  ✅ Marca estado_recepcion = "recibida"
  ✅ Aumenta stock de Harina: +20 kg
  ✅ Aumenta stock de Azúcar: +10 kg
  ✅ Aumenta stock de Levadura: +5 kg
  ✅ Crea movimientos de inventario
```

### **Paso 5: Registrar Pago**
```
Vas a: Pagos Proveedores → Crear
Seleccionas: Factura FAC-001-2025
Llenas:
  - Monto: $30,000
  - Fecha: 07/12/2025
  - Método: Transferencia
  - Comprobante: "TRF-123456"
Guardas ✅

El sistema actualiza:
  - Estado pago: "parcial"
  - Saldo pendiente: $29,500
```

### **Paso 6: Completar Pago**
```
Registras otro pago:
  - Monto: $29,500
  - Fecha: 15/12/2025
  - Método: Efectivo

El sistema actualiza:
  - Estado pago: "pagado" ✅
  - Saldo pendiente: $0
```

---

## 🔍 Preguntas Frecuentes

### **¿Por qué necesito registrar facturas si ya tengo inventario?**
- Para tener un **historial completo** de compras
- Para **contabilidad** (saber cuánto gastaste)
- Para **controlar pagos** (saber cuánto debes)
- Para **trazabilidad** (saber de dónde vino cada producto)

### **¿Qué pasa si pago parcialmente?**
- El sistema registra el pago parcial
- Calcula automáticamente el saldo pendiente
- La factura queda en estado "parcial"
- Puedes seguir pagando hasta completar

### **¿Cuándo se actualiza el stock?**
- **Solo cuando haces clic en "Recibir Factura"**
- Esto permite que:
  - Crees la factura antes de recibir los productos
  - Actualices el stock cuando realmente los recibes
  - Tengas control sobre cuándo se actualiza el inventario

### **¿Puedo cancelar una factura?**
- Sí, puedes eliminar facturas que no hayas recibido
- Si ya la recibiste, debes revertir la recepción primero
- Si ya pagaste, no puedes eliminarla (para mantener historial)

---

## 🎓 Resumen Visual

```
┌─────────────────────────────────────────────────┐
│         SISTEMA DE FACTURAS PROVEEDORES        │
└─────────────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
   ┌────▼────┐            ┌────▼────┐
   │PROVEEDOR│            │ FACTURA  │
   │         │            │         │
   │ - Nombre│            │ - Número│
   │ - RUT   │            │ - Fecha │
   │ - Contacto           │ - Total │
   └─────────┘            └────┬────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
              ┌─────▼─────┐          ┌─────▼─────┐
              │ DETALLES  │          │   PAGOS   │
              │           │          │           │
              │ - Producto│          │ - Monto   │
              │ - Cantidad│          │ - Fecha   │
              │ - Precio  │          │ - Método  │
              └─────┬─────┘          └───────────┘
                    │
                    │ (Al recibir)
                    ▼
              ┌─────────────┐
              │   STOCK     │
              │ Actualizado │
              │ Automático  │
              └─────────────┘
```

---

## ✅ Conclusión

El sistema de **Facturas de Proveedores** es esencial para:
- ✅ **Controlar tus compras** de manera organizada
- ✅ **Actualizar inventario** automáticamente
- ✅ **Gestionar pagos** a proveedores
- ✅ **Mantener historial** para contabilidad
- ✅ **Trazabilidad completa** de productos

**En resumen:** Es como tener un "libro de compras" digital que se conecta automáticamente con tu inventario y te ayuda a controlar todo lo que compras y pagas a tus proveedores.

