// ================================================================
// =                                                              =
// =           JAVASCRIPT PARA MÉTRICAS DEL DASHBOARD            =
// =                                                              =
// ================================================================
//
// Este archivo maneja la carga y actualización de las métricas
// principales del dashboard en tiempo real.

/**
 * Formatea un número como moneda chilena (CLP)
 * @param {number} valor - El valor a formatear
 * @returns {string} - Valor formateado como "$1.234.567"
 */
function formatearMoneda(valor) {
    return '$' + Math.round(valor).toLocaleString('es-CL');
}

/**
 * Carga las ventas del día desde la API
 */
function cargarVentasDelDia() {
    fetch('/api/ventas-del-dia/')
        .then(response => response.json())
        .then(data => {
            // Actualizar el valor de ventas
            const ventasValue = document.querySelector('.dashboard-row .dashboard-col:nth-child(1) .metric-card-value');
            const ventasSubtitle = document.querySelector('.dashboard-row .dashboard-col:nth-child(1) .metric-card-subtitle');
            
            if (ventasValue && ventasSubtitle) {
                ventasValue.textContent = formatearMoneda(data.total_ventas);
                ventasSubtitle.textContent = `${data.num_transacciones} transacciones`;
            }
        })
        .catch(error => {
            console.error('Error al cargar ventas del día:', error);
        });
}

/**
 * Carga los productos con stock bajo desde la API
 */
function cargarStockBajo() {
    fetch('/api/stock-bajo/')
        .then(response => response.json())
        .then(data => {
            // Actualizar el valor de stock bajo
            const stockValue = document.querySelector('.dashboard-row .dashboard-col:nth-child(2) .metric-card-value');
            const stockSubtitle = document.querySelector('.dashboard-row .dashboard-col:nth-child(2) .metric-card-subtitle');
            
            if (stockValue && stockSubtitle) {
                stockValue.textContent = data.num_productos;
                stockSubtitle.textContent = 'Productos';
                
                // Cambiar color si hay productos con stock bajo
                if (data.num_productos > 0) {
                    stockValue.style.color = '#ff6b6b';
                }
            }
        })
        .catch(error => {
            console.error('Error al cargar stock bajo:', error);
        });
}

/**
 * Carga las alertas pendientes desde la API
 */
function cargarAlertasPendientes() {
    fetch('/api/alertas-pendientes/')
        .then(response => response.json())
        .then(data => {
            // Actualizar el valor de alertas
            const alertasValue = document.querySelector('.dashboard-row .dashboard-col:nth-child(3) .metric-card-value');
            const alertasSubtitle = document.querySelector('.dashboard-row .dashboard-col:nth-child(3) .metric-card-subtitle');
            
            if (alertasValue && alertasSubtitle) {
                alertasValue.textContent = data.num_alertas;
                
                // Mostrar desglose por tipo
                const rojas = data.por_tipo.roja;
                const amarillas = data.por_tipo.amarilla;
                const verdes = data.por_tipo.verde;
                
                alertasSubtitle.innerHTML = `
                    <span style="color: #ff6b6b;">${rojas} rojas</span> | 
                    <span style="color: #ffd93d;">${amarillas} amarillas</span> | 
                    <span style="color: #6bcf7f;">${verdes} verdes</span>
                `;
                
                // Cambiar color si hay alertas rojas
                if (rojas > 0) {
                    alertasValue.style.color = '#ff6b6b';
                }
            }
        })
        .catch(error => {
            console.error('Error al cargar alertas pendientes:', error);
        });
}

/**
 * Carga el producto más vendido del día desde la API
 */
function cargarTopProducto() {
    fetch('/api/top-producto/')
        .then(response => response.json())
        .then(data => {
            // Actualizar el valor del top producto
            const topValue = document.querySelector('.dashboard-row .dashboard-col:nth-child(4) .metric-card-value');
            const topSubtitle = document.querySelector('.dashboard-row .dashboard-col:nth-child(4) .metric-card-subtitle');
            
            if (topValue && topSubtitle) {
                topValue.textContent = data.nombre;
                topSubtitle.textContent = `${data.unidades} unidades`;
                
                // Cambiar estilo si es "Sin ventas"
                if (data.nombre === 'Sin ventas') {
                    topValue.style.color = '#888';
                    topValue.style.fontSize = '1.2rem';
                } else {
                    topValue.style.color = '#D4AF37';
                    topValue.style.fontSize = '1.5rem';
                }
            }
        })
        .catch(error => {
            console.error('Error al cargar top producto:', error);
        });
}

/**
 * Inicializa todas las métricas del dashboard
 */
function inicializarMetricas() {
    cargarVentasDelDia();
    cargarStockBajo();
    cargarAlertasPendientes();
    cargarTopProducto();
}

/**
 * Actualiza las métricas cada cierto tiempo
 * @param {number} intervalo - Intervalo en milisegundos (default: 30 segundos)
 */
function actualizarMetricasPeriodicamente(intervalo = 30000) {
    setInterval(() => {
        inicializarMetricas();
    }, intervalo);
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    inicializarMetricas();
    
    // Actualizar cada 30 segundos
    actualizarMetricasPeriodicamente(30000);
});
