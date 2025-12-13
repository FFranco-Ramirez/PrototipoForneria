# ✅ Checklist - 4 Días para Video Demo

## 📅 DÍA 1 (HOY) - Correcciones Críticas

### Validación de Stock
- [x] Agregada validación antes de procesar venta
- [x] Agregada validación dentro de transacción (doble seguridad)
- [ ] **PROBAR**: Intentar vender más de lo disponible

### Movimientos de Inventario
- [x] Agregada creación de movimiento al vender
- [ ] **PROBAR**: Hacer una venta y verificar que aparece en "Movimientos"

### Pruebas Funcionales
- [ ] Probar login
- [ ] Probar dashboard
- [ ] Probar agregar producto
- [ ] Probar editar producto
- [ ] Probar POS (agregar al carrito)
- [ ] Probar procesar venta
- [ ] Probar validación de stock (intentar vender más)
- [ ] Probar crear proveedor
- [ ] Probar registrar factura de compra
- [ ] Probar que actualiza stock al recibir factura
- [ ] Probar alertas
- [ ] Probar merma

### Bugs Encontrados
- [ ] Bug 1: ________________
- [ ] Bug 2: ________________
- [ ] Bug 3: ________________

---

## 📅 DÍA 2 - Preparación para Video

### Datos de Prueba
- [ ] Crear 10-15 productos variados
  - [ ] Panes (diferentes tipos)
  - [ ] Pasteles
  - [ ] Snacks
  - [ ] Con diferentes precios
  - [ ] Con diferentes cantidades de stock
  
- [ ] Crear 2-3 proveedores
  - [ ] Con datos completos
  - [ ] Con facturas de ejemplo
  
- [ ] Crear 3-5 ventas de ejemplo
  - [ ] Diferentes montos
  - [ ] Diferentes productos
  
- [ ] Generar algunas alertas
  - [ ] Productos próximos a vencer
  - [ ] Stock bajo

### Script del Video
- [ ] Escribir guión/narrador (opcional)
- [ ] Practicar flujo de demostración
- [ ] Asegurar que todo funciona sin errores

---

## 📅 DÍA 3 - Grabación

### Antes de Grabar
- [ ] Cerrar aplicaciones innecesarias
- [ ] Limpiar escritorio
- [ ] Verificar que el micrófono funciona
- [ ] Verificar resolución de pantalla (1920x1080 recomendado)

### Durante la Grabación
- [ ] Introducción (30 seg)
- [ ] Login (30 seg)
- [ ] Dashboard (1 min)
- [ ] Gestión de productos (1.5 min)
- [ ] Sistema POS - Venta completa (2 min) ⭐
- [ ] Sistema de proveedores (1 min)
- [ ] Alertas y merma (1 min)
- [ ] Cierre (30 seg)

### Después de Grabar
- [ ] Revisar video completo
- [ ] Verificar que se ve bien
- [ ] Verificar que se escucha bien
- [ ] Editar si es necesario (cortar pausas, errores)

---

## 📅 DÍA 4 - AWS (Opcional) + Finalización

### AWS - Si hay tiempo
- [ ] Crear instancia EC2 t2.micro
- [ ] Configurar seguridad (Security Groups)
- [ ] Instalar dependencias
- [ ] Desplegar aplicación
- [ ] Probar acceso desde internet
- [ ] Tomar screenshot de AWS Console

### Revisión Final
- [ ] Revisar video final
- [ ] Preparar presentación
- [ ] Preparar respuestas a preguntas posibles
- [ ] Verificar que todo funciona

---

## 🎬 ESTRUCTURA DEL VIDEO (Guía)

### 1. Introducción (30 segundos)
```
"Hola, hoy les presento el sistema de gestión para Fornería.
Este software permite gestionar inventario, ventas, proveedores
y más. Empecemos."
```

### 2. Login (30 segundos)
```
"Primero, accedemos al sistema con usuario y contraseña.
[Mostrar login]
Una vez dentro, vemos el dashboard principal."
```

### 3. Dashboard (1 minuto)
```
"El dashboard muestra métricas importantes:
- Ventas del día
- Stock bajo
- Alertas pendientes
- Productos más vendidos
[Mostrar cada métrica]
```

### 4. Gestión de Productos (1.5 minutos)
```
"Ahora veamos la gestión de productos.
[Ir a inventario]
Aquí podemos ver todos los productos.
[Mostrar lista]
Podemos agregar un nuevo producto.
[Agregar producto]
También podemos editar productos existentes.
[Editar producto]
Y ver el stock actual de cada uno."
```

### 5. Sistema POS - VENTA (2 minutos) ⭐ MÁS IMPORTANTE
```
"La funcionalidad más importante es el punto de venta.
[Ir a POS]
Aquí podemos procesar ventas rápidamente.
[Agregar productos al carrito]
El sistema calcula automáticamente:
- Subtotal
- IVA (19%)
- Total
[Mostrar cálculos]
Si intentamos vender más de lo disponible,
el sistema nos avisa.
[Intentar vender más - mostrar error]
Al procesar la venta,
el stock se actualiza automáticamente.
[Procesar venta]
Y se crea un registro de movimiento de inventario.
[Mostrar movimientos]"
```

### 6. Sistema de Proveedores (1 minuto)
```
"El sistema también gestiona proveedores.
[Ir a proveedores - si existe la vista]
Podemos crear proveedores,
registrar facturas de compra,
y al recibir una factura,
el stock se actualiza automáticamente.
[Mostrar proceso]"
```

### 7. Alertas y Merma (1 minuto)
```
"El sistema genera alertas automáticas
para productos próximos a vencer.
[Mostrar alertas]
También podemos gestionar productos en merma.
[Mover a merma]"
```

### 8. Cierre (30 segundos)
```
"Este sistema está preparado para desplegarse en AWS
y puede escalar según las necesidades del negocio.
Gracias por su atención."
```

---

## 🐛 PROBLEMAS COMUNES Y SOLUCIONES

### Si el video se ve lento:
- Cierra otras aplicaciones
- Usa resolución 1280x720 en lugar de 1920x1080
- Graba en partes y edita después

### Si hay errores durante la grabación:
- No te detengas, sigue adelante
- Puedes editar después
- O grabar de nuevo solo esa parte

### Si algo no funciona:
- Tiene 4 días, hay tiempo de corregir
- Enfócate en lo que SÍ funciona
- Menciona que es un prototipo

---

## 📝 NOTAS IMPORTANTES

1. **El POS es lo más impresionante** - Dedícale más tiempo
2. **Muestra que el stock se actualiza** - Es importante
3. **Menciona las funcionalidades nuevas** - Proveedores, facturas
4. **Si algo falla, sigue adelante** - No te detengas mucho
5. **Practica antes de grabar** - Conoce el flujo

---

## ✅ ESTADO ACTUAL

### ✅ Completado:
- [x] Validación de stock en ventas
- [x] Creación de movimientos de inventario en ventas
- [x] Plan de 4 días

### 🔄 En Progreso:
- [ ] Pruebas funcionales

### ⏳ Pendiente:
- [ ] Preparación de datos
- [ ] Grabación del video
- [ ] AWS (opcional)

---

## 🚀 SIGUIENTE PASO INMEDIATO

**AHORA MISMO:**
1. Probar que la validación de stock funciona
2. Probar que se crean movimientos de inventario
3. Probar todas las funcionalidades
4. Anotar cualquier bug crítico

**Luego:**
- Compartir Jira (si puedes)
- Corregir bugs encontrados
- Preparar datos de prueba

