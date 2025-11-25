// ================================================================
// =                                                              =
// =         JAVASCRIPT PARA EL SISTEMA DE ALERTAS               =
// =                                                              =
// ================================================================
//
// Este archivo maneja toda la lógica de interacción del usuario
// con el sistema de alertas.
//
// FUNCIONALIDADES:
// - Cambiar estado de alertas (AJAX)
// - Generar alertas automáticas (AJAX)
// - Confirmar acciones importantes
// - Actualizar la interfaz dinámicamente

// ================================================================
// =         EVENTO: CUANDO LA PÁGINA CARGA COMPLETAMENTE         =
// ================================================================

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar todos los eventos
    inicializarEventosAlertas();
});


// ================================================================
// =        FUNCIÓN: INICIALIZAR TODOS LOS EVENTOS                =
// ================================================================
//
// Configura los eventos (clicks, envíos, etc.) de todos los
// elementos interactivos de la página de alertas.

function inicializarEventosAlertas() {
    
    // --- Evento: Cambiar estado de una alerta (links en dropdown) ---
    // Busca todos los elementos con clase "cambiar-estado"
    document.querySelectorAll('.cambiar-estado').forEach(link => {
        link.addEventListener('click', function(e) {
            // Prevenir que el link navegue (comportamiento por defecto)
            e.preventDefault();
            
            // Obtener datos del link
            const alertaId = this.dataset.alertaId;
            const nuevoEstado = this.dataset.estado;
            
            // Llamar a la función que cambia el estado
            cambiarEstadoAlerta(alertaId, nuevoEstado);
        });
    });
    
    // --- Evento: Generar alertas automáticas ---
    const btnGenerar = document.getElementById('btn-generar-alertas');
    if (btnGenerar) {
        btnGenerar.addEventListener('click', function() {
            // Confirmar antes de generar
            if (confirm('¿Deseas generar alertas automáticas para todos los productos?')) {
                generarAlertasAutomaticas();
            }
        });
    }
}


// ================================================================
// =     FUNCIÓN: CAMBIAR ESTADO DE UNA ALERTA (AJAX)            =
// ================================================================
//
// Envía una petición AJAX al servidor para cambiar el estado
// de una alerta sin recargar la página.
//
// @param {string|number} alertaId - ID de la alerta
// @param {string} nuevoEstado - Nuevo estado ('activa', 'resuelta', 'ignorada')

function cambiarEstadoAlerta(alertaId, nuevoEstado) {
    // Crear datos a enviar (FormData para envío tipo formulario)
    const formData = new FormData();
    formData.append('estado', nuevoEstado);
    
    // Obtener el token CSRF de Django (necesario para peticiones POST)
    const csrfToken = getCookie('csrftoken');
    
    // Construir la URL del endpoint
    const url = `/api/alerta/${alertaId}/cambiar-estado/`;
    
    // --- Enviar petición AJAX ---
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
    .then(response => response.json())  // Convertir respuesta a JSON
    .then(data => {
        // Verificar si fue exitoso
        if (data.success) {
            // Mostrar mensaje de éxito
            mostrarAlertaTemporal('success', data.mensaje);
            
            // Recargar la página para ver los cambios
            // (alternativa: actualizar solo la fila de la tabla con JavaScript)
            setTimeout(() => {
                location.reload();
            }, 1000);
        } else {
            // Mostrar mensaje de error
            mostrarAlertaTemporal('error', data.mensaje);
        }
    })
    .catch(error => {
        // Error de conexión o del servidor
        console.error('Error:', error);
        mostrarAlertaTemporal('error', 'Error de conexión. Intenta nuevamente.');
    });
}


// ================================================================
// =     FUNCIÓN: GENERAR ALERTAS AUTOMÁTICAMENTE (AJAX)          =
// ================================================================
//
// Llama al servidor para que genere alertas automáticas
// para todos los productos según sus fechas de vencimiento.

function generarAlertasAutomaticas() {
    // Obtener el token CSRF
    const csrfToken = getCookie('csrftoken');
    
    // URL del endpoint
    const url = '/api/generar-alertas-automaticas/';
    
    // Deshabilitar el botón mientras se procesa
    const btn = document.getElementById('btn-generar-alertas');
    const textoOriginal = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Generando...';
    
    // --- Enviar petición AJAX ---
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        // Rehabilitar el botón
        btn.disabled = false;
        btn.innerHTML = textoOriginal;
        
        if (data.success) {
            // Mostrar estadísticas
            const stats = data.estadisticas;
            const mensaje = `
                ✅ Alertas generadas exitosamente:
                • ${stats.roja} rojas
                • ${stats.amarilla} amarillas
                • ${stats.verde} verdes
                • Total: ${stats.total}
            `;
            
            mostrarAlertaTemporal('success', mensaje);
            
            // Recargar la página después de 2 segundos
            setTimeout(() => {
                location.reload();
            }, 2000);
        } else {
            mostrarAlertaTemporal('error', data.mensaje);
        }
    })
    .catch(error => {
        // Error
        console.error('Error:', error);
        mostrarAlertaTemporal('error', 'Error al generar alertas. Intenta nuevamente.');
        
        // Rehabilitar el botón
        btn.disabled = false;
        btn.innerHTML = textoOriginal;
    });
}


// ================================================================
// =               FUNCIONES AUXILIARES (HELPERS)                 =
// ================================================================

/**
 * Muestra una alerta temporal en la parte superior de la página.
 * 
 * @param {string} tipo - 'success', 'error', 'warning', 'info'
 * @param {string} mensaje - El mensaje a mostrar
 */
function mostrarAlertaTemporal(tipo, mensaje) {
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
             style="z-index: 9999; max-width: 400px; white-space: pre-line;">
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
 * Obtiene una cookie por su nombre.
 * Necesario para obtener el token CSRF de Django.
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
// =                 FUNCIÓN: RESALTAR ALERTAS URGENTES           =
// ================================================================
//
// Agrega clases CSS especiales a las filas de alertas rojas
// para que sean más visibles.

function resaltarAlertasUrgentes() {
    // Buscar todas las filas de alertas rojas
    const filasRojas = document.querySelectorAll('.alerta-row[data-tipo="roja"]');
    
    // Agregar una clase especial para animación
    filasRojas.forEach(fila => {
        fila.classList.add('alerta-urgente');
    });
}

// Ejecutar al cargar la página
document.addEventListener('DOMContentLoaded', resaltarAlertasUrgentes);


// ================================================================
// =                     FIN DEL ARCHIVO                          =
// ================================================================

console.log('✅ Sistema de Alertas cargado correctamente');

