// ================================================================
// =                                                              =
// =     JAVASCRIPT PARA EL SISTEMA POS (PUNTO DE VENTA)         =
// =                                                              =
// ================================================================
//
// Este archivo maneja toda la lógica del carrito de compras:
// - Agregar productos al carrito
// - Quitar productos del carrito
// - Actualizar cantidades
// - Calcular totales (subtotal, IVA, total)
// - Validar stock antes de agregar
// - Procesar la venta completa
// - Agregar nuevos clientes
//
// NOTA: Este código usa JavaScript moderno (ES6+) con const, let, arrow functions, etc.

// ================================================================
// =                 VARIABLES GLOBALES                           =
// ================================================================

// --- Carrito de compras ---
// Es un array (lista) que contiene los productos agregados al carrito
// Cada producto es un objeto con: {producto_id, nombre, precio, cantidad, stock}
let carrito = [];

// --- Constante: Tasa de IVA en Chile ---
// En Chile el IVA es del 19% (0.19 en decimal)
const IVA_RATE = 0.19;


// ================================================================
// =              EVENTO: CUANDO LA PÁGINA CARGA                  =
// ================================================================
// 
// DOMContentLoaded es un evento que se dispara cuando el navegador
// termina de cargar todo el HTML. Aquí inicializamos todo.

document.addEventListener('DOMContentLoaded', function() {
    // Llama la función que configura todos los eventos
    inicializarEventos();
    
    // Actualizar totales al cargar (inicialmente todo en $0)
    actualizarTotales();
});


// ================================================================
// =          FUNCIÓN: INICIALIZAR TODOS LOS EVENTOS              =
// ================================================================
//
// Esta función busca todos los elementos HTML y les asigna
// funciones que se ejecutarán cuando el usuario haga clic,
// escriba algo, etc.

function inicializarEventos() {
    
    // --- Evento: Agregar producto al carrito ---
    // Busca TODOS los botones con clase "agregar-al-carrito"
    // y les asigna la función agregarProductoAlCarrito cuando se hace clic
    document.querySelectorAll('.agregar-al-carrito').forEach(boton => {
        boton.addEventListener('click', agregarProductoAlCarrito);
    });
    
    // --- Evento: Buscar productos ---
    // Cuando el usuario escribe en el buscador, filtra los productos
    const inputBuscar = document.getElementById('buscar-producto');
    if (inputBuscar) {
        inputBuscar.addEventListener('input', filtrarProductos);
    }
    
    // --- Evento: Limpiar carrito ---
    const btnLimpiar = document.getElementById('btn-limpiar-carrito');
    if (btnLimpiar) {
        btnLimpiar.addEventListener('click', limpiarCarrito);
    }
    
    // --- Evento: Procesar venta ---
    const btnProcesar = document.getElementById('btn-procesar-venta');
    if (btnProcesar) {
        btnProcesar.addEventListener('click', abrirModalFinalizarVenta);
    }
    
    // --- Evento: Guardar nuevo cliente ---
    const btnGuardarCliente = document.getElementById('btn-guardar-cliente');
    if (btnGuardarCliente) {
        btnGuardarCliente.addEventListener('click', guardarNuevoCliente);
    }
    
    // --- Evento: Confirmar venta ---
    const btnConfirmarVenta = document.getElementById('btn-confirmar-venta');
    if (btnConfirmarVenta) {
        btnConfirmarVenta.addEventListener('click', confirmarVenta);
    }
    
    // --- Evento: Calcular vuelto en tiempo real ---
    const inputMontoPagado = document.getElementById('monto-pagado');
    if (inputMontoPagado) {
        inputMontoPagado.addEventListener('input', calcularVuelto);
    }
    
    // --- Evento: Recalcular totales cuando cambia el descuento ---
    const inputDescuento = document.getElementById('descuento-global');
    if (inputDescuento) {
        inputDescuento.addEventListener('input', actualizarTotales);
    }
}


// ================================================================
// =       FUNCIÓN: AGREGAR PRODUCTO AL CARRITO                   =
// ================================================================
//
// Esta función se ejecuta cuando el usuario hace clic en el botón
// "Agregar" de un producto.
//
// PASOS:
// 1. Obtener información del producto desde el botón (usando data-attributes)
// 2. Validar que el producto tenga stock (llamada AJAX al servidor)
// 3. Si ya está en el carrito, aumentar la cantidad
// 4. Si no está, agregarlo al carrito
// 5. Actualizar la visualización del carrito
// 6. Recalcular totales

function agregarProductoAlCarrito(evento) {
    // "evento.currentTarget" es el botón que se clickeó
    const boton = evento.currentTarget;
    
    // Obtenemos el ID del producto desde el atributo "data-producto-id"
    const productoId = boton.dataset.productoId;
    
    // Buscamos la tarjeta completa del producto (el div padre)
    const card = document.querySelector(`.producto-card[data-producto-id="${productoId}"]`);
    
    // Extraemos toda la información del producto desde los data-attributes
    const producto = {
        producto_id: parseInt(productoId),
        nombre: card.dataset.productoNombre,
        precio: parseFloat(card.dataset.productoPrecio),
        stock: parseInt(card.dataset.productoStock),
        cantidad: 1,  // Por defecto agregamos 1 unidad
        descuento: 0  // Sin descuento por defecto
    };
    
    // --- Validación 1: Verificar que haya stock ---
    if (producto.stock <= 0) {
        mostrarAlerta('error', 'Este producto no tiene stock disponible');
        return;  // Salir de la función, no agregar al carrito
    }
    
    // --- Verificar si el producto ya está en el carrito ---
    const indiceExistente = carrito.findIndex(item => item.producto_id === producto.producto_id);
    
    if (indiceExistente >= 0) {
        // El producto YA está en el carrito
        
        // Verificamos si podemos aumentar la cantidad
        const cantidadActual = carrito[indiceExistente].cantidad;
        
        if (cantidadActual >= producto.stock) {
            // No hay más stock disponible
            mostrarAlerta('warning', `Solo hay ${producto.stock} unidades disponibles`);
            return;
        }
        
        // Aumentamos la cantidad en 1
        carrito[indiceExistente].cantidad += 1;
        
    } else {
        // El producto NO está en el carrito, lo agregamos
        carrito.push(producto);
    }
    
    // Actualizar la visualización del carrito en la pantalla
    renderizarCarrito();
    
    // Recalcular los totales
    actualizarTotales();
    
    // Mostrar mensaje de éxito
    mostrarAlerta('success', `${producto.nombre} agregado al carrito`);
}


// ================================================================
// =         FUNCIÓN: RENDERIZAR (MOSTRAR) EL CARRITO             =
// ================================================================
//
// Esta función actualiza la visualización del carrito en el HTML.
// Toma el array "carrito" y lo convierte en elementos HTML visibles.

function renderizarCarrito() {
    // Obtener el contenedor donde se mostrarán los items
    const contenedor = document.getElementById('carrito-items');
    
    // Obtener el mensaje de "carrito vacío"
    const mensajeVacio = document.getElementById('carrito-vacio');
    
    // Obtener el contador de items en el header del carrito
    const contadorItems = document.getElementById('items-count');
    
    // --- Caso 1: Si el carrito está vacío ---
    if (carrito.length === 0) {
        // Mostrar mensaje de "carrito vacío"
        mensajeVacio.classList.remove('d-none');
        
        // Limpiar el contenedor
        contenedor.innerHTML = '';
        
        // Actualizar contador a 0
        contadorItems.textContent = '0';
        
        // Deshabilitar el botón de procesar venta
        document.getElementById('btn-procesar-venta').disabled = true;
        
        return;  // Salir de la función
    }
    
    // --- Caso 2: Hay productos en el carrito ---
    
    // Ocultar el mensaje de "carrito vacío"
    mensajeVacio.classList.add('d-none');
    
    // Limpiar el contenedor antes de agregar los nuevos items
    contenedor.innerHTML = '';
    
    // Contador de items totales (sumando las cantidades)
    let totalItems = 0;
    
    // --- Recorrer cada producto del carrito ---
    carrito.forEach((item, indice) => {
        // Sumar la cantidad de este item al total
        totalItems += item.cantidad;
        
        // Calcular el subtotal de este item (precio × cantidad)
        const subtotalItem = item.precio * item.cantidad;
        
        // Crear el HTML para este item del carrito
        const itemHTML = `
            <div class="card mb-2" data-item-index="${indice}">
                <div class="card-body p-2">
                    <!-- Nombre del producto -->
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <strong class="text-truncate" style="max-width: 200px;">
                            ${item.nombre}
                        </strong>
                        <!-- Botón para quitar del carrito -->
                        <button class="btn btn-sm btn-danger btn-quitar-item" 
                                data-index="${indice}"
                                title="Quitar del carrito">
                            <i class="bi bi-x-lg"></i>
                        </button>
                    </div>
                    
                    <!-- Controles de cantidad y precio -->
                    <div class="d-flex justify-content-between align-items-center">
                        <div class="input-group input-group-sm" style="width: 120px;">
                            <!-- Botón para disminuir cantidad -->
                            <button class="btn btn-outline-secondary btn-disminuir" 
                                    data-index="${indice}"
                                    type="button">
                                <i class="bi bi-dash"></i>
                            </button>
                            
                            <!-- Input de cantidad -->
                            <input type="number" 
                                   class="form-control text-center input-cantidad" 
                                   data-index="${indice}"
                                   value="${item.cantidad}" 
                                   min="1" 
                                   max="${item.stock}">
                            
                            <!-- Botón para aumentar cantidad -->
                            <button class="btn btn-outline-secondary btn-aumentar" 
                                    data-index="${indice}"
                                    type="button">
                                <i class="bi bi-plus"></i>
                            </button>
                        </div>
                        
                        <!-- Precio × cantidad -->
                        <div class="text-end">
                            <small class="text-muted">$${item.precio.toFixed(2)} c/u</small>
                            <div class="fw-bold text-primary">
                                $${subtotalItem.toFixed(2)}
                            </div>
                        </div>
                    </div>
                    
                    <!-- Indicador de stock disponible -->
                    <div class="mt-1">
                        <small class="text-muted">
                            <i class="bi bi-box"></i> Stock: ${item.stock}
                        </small>
                    </div>
                </div>
            </div>
        `;
        
        // Agregar este item al contenedor
        contenedor.innerHTML += itemHTML;
    });
    
    // Actualizar el contador de items
    contadorItems.textContent = totalItems;
    
    // Habilitar el botón de procesar venta
    document.getElementById('btn-procesar-venta').disabled = false;
    
    // --- Asignar eventos a los nuevos botones creados ---
    asignarEventosCarrito();
}


// ================================================================
// =       FUNCIÓN: ASIGNAR EVENTOS A BOTONES DEL CARRITO         =
// ================================================================
//
// Después de renderizar el carrito, necesitamos asignar eventos
// a todos los botones nuevos (quitar, aumentar, disminuir)

function asignarEventosCarrito() {
    
    // --- Botones para quitar items ---
    document.querySelectorAll('.btn-quitar-item').forEach(boton => {
        boton.addEventListener('click', function() {
            const indice = parseInt(this.dataset.index);
            quitarDelCarrito(indice);
        });
    });
    
    // --- Botones para disminuir cantidad ---
    document.querySelectorAll('.btn-disminuir').forEach(boton => {
        boton.addEventListener('click', function() {
            const indice = parseInt(this.dataset.index);
            cambiarCantidad(indice, -1);  // -1 significa disminuir
        });
    });
    
    // --- Botones para aumentar cantidad ---
    document.querySelectorAll('.btn-aumentar').forEach(boton => {
        boton.addEventListener('click', function() {
            const indice = parseInt(this.dataset.index);
            cambiarCantidad(indice, 1);  // +1 significa aumentar
        });
    });
    
    // --- Inputs de cantidad (cuando el usuario escribe directamente) ---
    document.querySelectorAll('.input-cantidad').forEach(input => {
        input.addEventListener('change', function() {
            const indice = parseInt(this.dataset.index);
            const nuevaCantidad = parseInt(this.value);
            establecerCantidad(indice, nuevaCantidad);
        });
    });
}


// ================================================================
// =         FUNCIÓN: CAMBIAR CANTIDAD DE UN ITEM                 =
// ================================================================
//
// Aumenta o disminuye la cantidad de un producto en el carrito
//
// @param {number} indice - Posición del producto en el array carrito
// @param {number} cambio - Cantidad a sumar (+1) o restar (-1)

function cambiarCantidad(indice, cambio) {
    // Obtener el item del carrito
    const item = carrito[indice];
    
    // Calcular la nueva cantidad
    const nuevaCantidad = item.cantidad + cambio;
    
    // Validar que la cantidad esté en el rango válido
    if (nuevaCantidad < 1) {
        // Si intentan poner menos de 1, mejor quitar del carrito
        quitarDelCarrito(indice);
        return;
    }
    
    if (nuevaCantidad > item.stock) {
        // No hay suficiente stock
        mostrarAlerta('warning', `Solo hay ${item.stock} unidades disponibles`);
        return;
    }
    
    // Actualizar la cantidad
    item.cantidad = nuevaCantidad;
    
    // Re-renderizar el carrito
    renderizarCarrito();
    
    // Recalcular totales
    actualizarTotales();
}


// ================================================================
// =      FUNCIÓN: ESTABLECER CANTIDAD EXACTA DE UN ITEM          =
// ================================================================
//
// Cuando el usuario escribe directamente en el input de cantidad
//
// @param {number} indice - Posición del producto en el array carrito
// @param {number} cantidad - Nueva cantidad deseada

function establecerCantidad(indice, cantidad) {
    // Obtener el item del carrito
    const item = carrito[indice];
    
    // Validar que la cantidad sea un número válido
    if (isNaN(cantidad) || cantidad < 1) {
        // Restaurar la cantidad anterior
        renderizarCarrito();
        mostrarAlerta('error', 'La cantidad debe ser al menos 1');
        return;
    }
    
    if (cantidad > item.stock) {
        // Restaurar la cantidad anterior
        renderizarCarrito();
        mostrarAlerta('warning', `Solo hay ${item.stock} unidades disponibles`);
        return;
    }
    
    // Actualizar la cantidad
    item.cantidad = cantidad;
    
    // Recalcular totales
    actualizarTotales();
}


// ================================================================
// =           FUNCIÓN: QUITAR PRODUCTO DEL CARRITO               =
// ================================================================
//
// Elimina un producto del carrito
//
// @param {number} indice - Posición del producto en el array carrito

function quitarDelCarrito(indice) {
    // Obtener el nombre del producto antes de quitarlo
    const nombreProducto = carrito[indice].nombre;
    
    // Quitar el elemento del array usando splice()
    // splice(indice, 1) significa: "desde 'indice', quita 1 elemento"
    carrito.splice(indice, 1);
    
    // Re-renderizar el carrito
    renderizarCarrito();
    
    // Recalcular totales
    actualizarTotales();
    
    // Mostrar mensaje
    mostrarAlerta('info', `${nombreProducto} quitado del carrito`);
}


// ================================================================
// =              FUNCIÓN: LIMPIAR TODO EL CARRITO                =
// ================================================================
//
// Vacía completamente el carrito (elimina todos los productos)

function limpiarCarrito() {
    // Confirmar con el usuario
    if (carrito.length === 0) {
        mostrarAlerta('info', 'El carrito ya está vacío');
        return;
    }
    
    // Pedir confirmación
    if (!confirm('¿Estás seguro de que deseas limpiar el carrito?')) {
        return;  // El usuario canceló
    }
    
    // Vaciar el array del carrito
    carrito = [];
    
    // Re-renderizar el carrito
    renderizarCarrito();
    
    // Recalcular totales
    actualizarTotales();
    
    // Mostrar mensaje
    mostrarAlerta('success', 'Carrito limpiado correctamente');
}


// ================================================================
// =            FUNCIÓN: ACTUALIZAR TOTALES                       =
// ================================================================
//
// Calcula y muestra el subtotal, IVA y total del carrito

function actualizarTotales() {
    // --- Paso 1: Calcular el subtotal (suma de todos los items) ---
    let subtotal = 0;
    
    carrito.forEach(item => {
        subtotal += item.precio * item.cantidad;
    });
    
    // --- Paso 2: Obtener el descuento global (si hay) ---
    const inputDescuento = document.getElementById('descuento-global');
    const descuentoGlobal = inputDescuento ? parseFloat(inputDescuento.value) || 0 : 0;
    
    // Aplicar descuento al subtotal
    subtotal = subtotal - descuentoGlobal;
    
    // Asegurar que el subtotal no sea negativo
    if (subtotal < 0) subtotal = 0;
    
    // --- Paso 3: Calcular el IVA (19% del subtotal) ---
    const iva = subtotal * IVA_RATE;
    
    // --- Paso 4: Calcular el total (subtotal + IVA) ---
    const total = subtotal + iva;
    
    // --- Paso 5: Actualizar los elementos HTML ---
    document.getElementById('subtotal').textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById('iva').textContent = `$${iva.toFixed(2)}`;
    document.getElementById('total').textContent = `$${total.toFixed(2)}`;
    
    // También actualizar el total en el modal de finalizar venta
    const modalTotal = document.getElementById('modal-total');
    if (modalTotal) {
        modalTotal.textContent = `$${total.toFixed(2)}`;
    }
}


// ================================================================
// =           FUNCIÓN: FILTRAR PRODUCTOS (BÚSQUEDA)              =
// ================================================================
//
// Filtra los productos mostrados según lo que el usuario escribe

function filtrarProductos(evento) {
    // Obtener el texto que el usuario escribió (en minúsculas)
    const textoBusqueda = evento.target.value.toLowerCase().trim();
    
    // Obtener todos los items de productos
    const items = document.querySelectorAll('.producto-item');
    
    // Recorrer cada producto
    items.forEach(item => {
        // Obtener los datos del producto
        const nombre = item.dataset.nombre || '';
        const marca = item.dataset.marca || '';
        const tipo = item.dataset.tipo || '';
        
        // Verificar si el texto de búsqueda está en nombre, marca o tipo
        const coincide = nombre.includes(textoBusqueda) || 
                        marca.includes(textoBusqueda) || 
                        tipo.includes(textoBusqueda);
        
        // Mostrar u ocultar el producto según si coincide
        if (coincide) {
            item.style.display = '';  // Mostrar
        } else {
            item.style.display = 'none';  // Ocultar
        }
    });
}


// ================================================================
// =       FUNCIÓN: ABRIR MODAL PARA FINALIZAR VENTA              =
// ================================================================
//
// Abre el modal para capturar el monto pagado y confirmar la venta

function abrirModalFinalizarVenta() {
    // Validar que haya un cliente seleccionado
    const selectCliente = document.getElementById('select-cliente');
    if (!selectCliente.value) {
        mostrarAlerta('error', 'Debes seleccionar un cliente antes de procesar la venta');
        return;
    }
    
    // Validar que el carrito no esté vacío
    if (carrito.length === 0) {
        mostrarAlerta('error', 'El carrito está vacío');
        return;
    }
    
    // Limpiar el input de monto pagado
    document.getElementById('monto-pagado').value = '';
    document.getElementById('vuelto-calculado').textContent = '$0.00';
    
    // Ocultar errores anteriores
    document.getElementById('errores-venta').classList.add('d-none');
    
    // Abrir el modal usando Bootstrap
    const modal = new bootstrap.Modal(document.getElementById('modalFinalizarVenta'));
    modal.show();
}


// ================================================================
// =             FUNCIÓN: CALCULAR VUELTO                         =
// ================================================================
//
// Calcula el vuelto en tiempo real mientras el usuario escribe

function calcularVuelto() {
    // Obtener el monto pagado
    const montoPagado = parseFloat(document.getElementById('monto-pagado').value) || 0;
    
    // Obtener el total de la venta
    const totalTexto = document.getElementById('total').textContent.replace('$', '');
    const total = parseFloat(totalTexto);
    
    // Calcular el vuelto
    const vuelto = montoPagado - total;
    
    // Mostrar el vuelto
    const elementoVuelto = document.getElementById('vuelto-calculado');
    elementoVuelto.textContent = `$${vuelto.toFixed(2)}`;
    
    // Cambiar el color según si es positivo o negativo
    if (vuelto < 0) {
        elementoVuelto.classList.remove('text-success');
        elementoVuelto.classList.add('text-danger');
    } else {
        elementoVuelto.classList.remove('text-danger');
        elementoVuelto.classList.add('text-success');
    }
}


// ================================================================
// =          FUNCIÓN: CONFIRMAR Y PROCESAR VENTA                 =
// ================================================================
//
// Envía la venta al servidor para procesarla y guardarla

async function confirmarVenta() {
    // --- Paso 1: Obtener todos los datos necesarios ---
    
    const clienteId = document.getElementById('select-cliente').value;
    const canalVenta = document.querySelector('input[name="canal_venta"]:checked').value;
    const montoPagado = parseFloat(document.getElementById('monto-pagado').value) || 0;
    const descuentoGlobal = parseFloat(document.getElementById('descuento-global').value) || 0;
    
    // --- Paso 2: Validaciones ---
    
    if (!clienteId) {
        mostrarError('errores-venta', 'Debes seleccionar un cliente');
        return;
    }
    
    if (carrito.length === 0) {
        mostrarError('errores-venta', 'El carrito está vacío');
        return;
    }
    
    // Obtener el total
    const totalTexto = document.getElementById('total').textContent.replace('$', '');
    const total = parseFloat(totalTexto);
    
    if (montoPagado < total) {
        mostrarError('errores-venta', `Monto insuficiente. Falta: $${(total - montoPagado).toFixed(2)}`);
        return;
    }
    
    // --- Paso 3: Preparar los datos para enviar ---
    
    const datosVenta = {
        cliente_id: parseInt(clienteId),
        canal_venta: canalVenta,
        carrito: carrito,
        monto_pagado: montoPagado,
        descuento: descuentoGlobal
    };
    
    // --- Paso 4: Deshabilitar el botón para evitar doble clic ---
    const btnConfirmar = document.getElementById('btn-confirmar-venta');
    btnConfirmar.disabled = true;
    btnConfirmar.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Procesando...';
    
    try {
        // --- Paso 5: Enviar la venta al servidor (AJAX) ---
        
        const response = await fetch('/api/procesar-venta/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  // Token de seguridad de Django
            },
            body: JSON.stringify(datosVenta)
        });
        
        const resultado = await response.json();
        
        // --- Paso 6: Manejar la respuesta ---
        
        if (resultado.success) {
            // ¡Venta exitosa!
            
            // Cerrar el modal
            bootstrap.Modal.getInstance(document.getElementById('modalFinalizarVenta')).hide();
            
            // Mostrar mensaje de éxito
            mostrarAlerta('success', `¡Venta procesada! Folio: ${resultado.venta.folio}`);
            
            // Limpiar el carrito
            carrito = [];
            renderizarCarrito();
            actualizarTotales();
            
            // Limpiar selección de cliente
            document.getElementById('select-cliente').value = '';
            
            // Opcionalmente, mostrar un resumen de la venta
            mostrarResumenVenta(resultado.venta);
            
        } else {
            // Hubo un error
            mostrarError('errores-venta', resultado.mensaje);
        }
        
    } catch (error) {
        // Error de conexión o del servidor
        console.error('Error al procesar la venta:', error);
        mostrarError('errores-venta', 'Error de conexión. Intenta nuevamente.');
        
    } finally {
        // Rehabilitar el botón
        btnConfirmar.disabled = false;
        btnConfirmar.innerHTML = '<i class="bi bi-check-circle"></i> Confirmar Venta';
    }
}


// ================================================================
// =          FUNCIÓN: GUARDAR NUEVO CLIENTE (AJAX)               =
// ================================================================
//
// Envía los datos del nuevo cliente al servidor

async function guardarNuevoCliente() {
    // --- Paso 1: Obtener los datos del formulario ---
    
    const nombre = document.getElementById('cliente-nombre').value.trim();
    const rut = document.getElementById('cliente-rut').value.trim();
    const correo = document.getElementById('cliente-correo').value.trim();
    
    // --- Paso 2: Validación básica ---
    
    if (!nombre) {
        mostrarError('errores-cliente', 'El nombre es obligatorio');
        return;
    }
    
    // --- Paso 3: Preparar los datos ---
    
    const datosCliente = {
        nombre: nombre,
        rut: rut,
        correo: correo
    };
    
    // --- Paso 4: Deshabilitar el botón ---
    const btnGuardar = document.getElementById('btn-guardar-cliente');
    btnGuardar.disabled = true;
    btnGuardar.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Guardando...';
    
    try {
        // --- Paso 5: Enviar al servidor ---
        
        const response = await fetch('/api/agregar-cliente/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(datosCliente)
        });
        
        const resultado = await response.json();
        
        // --- Paso 6: Manejar la respuesta ---
        
        if (resultado.success) {
            // ¡Cliente guardado!
            
            // Cerrar el modal
            bootstrap.Modal.getInstance(document.getElementById('modalNuevoCliente')).hide();
            
            // Limpiar el formulario
            document.getElementById('form-nuevo-cliente').reset();
            
            // Agregar el cliente al selector
            const selectCliente = document.getElementById('select-cliente');
            const option = document.createElement('option');
            option.value = resultado.cliente.id;
            option.textContent = `${resultado.cliente.nombre}${resultado.cliente.rut ? ' (' + resultado.cliente.rut + ')' : ''}`;
            selectCliente.appendChild(option);
            
            // Seleccionar automáticamente el nuevo cliente
            selectCliente.value = resultado.cliente.id;
            
            // Mostrar mensaje de éxito
            mostrarAlerta('success', resultado.mensaje);
            
        } else {
            // Mostrar errores
            let mensajeError = resultado.mensaje;
            if (resultado.errores) {
                mensajeError += '<ul>';
                for (let campo in resultado.errores) {
                    mensajeError += `<li>${resultado.errores[campo].join(' ')}</li>`;
                }
                mensajeError += '</ul>';
            }
            mostrarError('errores-cliente', mensajeError);
        }
        
    } catch (error) {
        console.error('Error al guardar cliente:', error);
        mostrarError('errores-cliente', 'Error de conexión. Intenta nuevamente.');
        
    } finally {
        // Rehabilitar el botón
        btnGuardar.disabled = false;
        btnGuardar.innerHTML = '<i class="bi bi-save"></i> Guardar Cliente';
    }
}


// ================================================================
// =              FUNCIONES AUXILIARES (HELPERS)                  =
// ================================================================

/**
 * Muestra una alerta temporal en la parte superior
 * 
 * @param {string} tipo - 'success', 'error', 'warning', 'info'
 * @param {string} mensaje - El mensaje a mostrar
 */
function mostrarAlerta(tipo, mensaje) {
    // Mapear tipos a clases de Bootstrap
    const claseBootstrap = {
        'success': 'success',
        'error': 'danger',
        'warning': 'warning',
        'info': 'info'
    };
    
    // Crear el HTML de la alerta
    const alertaHTML = `
        <div class="alert alert-${claseBootstrap[tipo]} alert-dismissible fade show position-fixed top-0 end-0 m-3" 
             role="alert" 
             style="z-index: 9999; max-width: 400px;">
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    // Agregar la alerta al body
    document.body.insertAdjacentHTML('beforeend', alertaHTML);
    
    // Eliminar la alerta automáticamente después de 5 segundos
    setTimeout(() => {
        const alertas = document.querySelectorAll('.alert');
        if (alertas.length > 0) {
            alertas[alertas.length - 1].remove();
        }
    }, 5000);
}

/**
 * Muestra un mensaje de error en un contenedor específico
 * 
 * @param {string} elementoId - ID del elemento donde mostrar el error
 * @param {string} mensaje - El mensaje de error
 */
function mostrarError(elementoId, mensaje) {
    const elemento = document.getElementById(elementoId);
    if (elemento) {
        elemento.innerHTML = mensaje;
        elemento.classList.remove('d-none');
    }
}

/**
 * Muestra un resumen de la venta procesada
 * 
 * @param {object} venta - Datos de la venta
 */
function mostrarResumenVenta(venta) {
    alert(`
🎉 ¡VENTA EXITOSA! 🎉

Folio: ${venta.folio}
Fecha: ${venta.fecha}
Total: $${venta.total.toFixed(2)}
Vuelto: $${venta.vuelto.toFixed(2)}

¡Gracias por su compra!
    `);
}

/**
 * Obtiene una cookie por su nombre (necesario para el CSRF token de Django)
 * 
 * @param {string} name - Nombre de la cookie
 * @returns {string} - Valor de la cookie
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// ================================================================
// =                     FIN DEL ARCHIVO                          =
// ================================================================

console.log('✅ Sistema POS cargado correctamente');

