// ================================================================
// =                                                              =
// =        JAVASCRIPT PARA FILTROS Y BÚSQUEDA DE MERMA          =
// =                                                              =
// ================================================================
//
// Este archivo maneja la búsqueda en tiempo real y el ordenamiento
// de productos en la página de merma.

document.addEventListener('DOMContentLoaded', function() {
    // ============================================================
    // ELEMENTOS DEL DOM
    // ============================================================
    const searchInput = document.getElementById('searchInput');
    const clearSearchBtn = document.getElementById('clearSearch');
    const sortableHeaders = document.querySelectorAll('.sortable-header');
    const tableBody = document.getElementById('mermaTableBody');
    
    if (!searchInput || !tableBody) return;
    
    // Guardar el orden original de las filas
    let originalRows = Array.from(tableBody.querySelectorAll('.merma-row'));
    
    // Estado actual de ordenamiento
    let currentSort = {
        column: null,
        direction: null // 'asc' o 'desc'
    };
    
    // ============================================================
    // FUNCIÓN: BÚSQUEDA EN TIEMPO REAL
    // ============================================================
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase().trim();
        const rows = tableBody.querySelectorAll('.merma-row');
        let visibleCount = 0;
        
        // Mostrar/ocultar botón de limpiar
        clearSearchBtn.style.display = searchTerm ? 'block' : 'none';
        
        // Filtrar filas
        rows.forEach(row => {
            const productName = row.getAttribute('data-nombre');
            
            if (productName.includes(searchTerm)) {
                row.style.display = '';
                visibleCount++;
                
                // Efecto de highlight en el texto encontrado
                row.style.animation = 'fadeIn 0.3s ease';
            } else {
                row.style.display = 'none';
            }
        });
        
        // Mostrar mensaje si no hay resultados
        mostrarMensajeNoResultados(visibleCount, searchTerm);
    });
    
    // ============================================================
    // FUNCIÓN: LIMPIAR BÚSQUEDA
    // ============================================================
    clearSearchBtn.addEventListener('click', function() {
        searchInput.value = '';
        searchInput.dispatchEvent(new Event('input'));
        searchInput.focus();
    });
    
    // ============================================================
    // FUNCIÓN: ORDENAMIENTO POR ENCABEZADOS
    // ============================================================
    sortableHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const sortColumn = this.getAttribute('data-sort');
            
            // Determinar dirección de ordenamiento
            if (currentSort.column === sortColumn) {
                // Si es la misma columna, alternar dirección
                if (currentSort.direction === 'asc') {
                    currentSort.direction = 'desc';
                } else if (currentSort.direction === 'desc') {
                    // Si ya está descendente, volver al orden original
                    currentSort.column = null;
                    currentSort.direction = null;
                } else {
                    currentSort.direction = 'asc';
                }
            } else {
                // Nueva columna, empezar con ascendente
                currentSort.column = sortColumn;
                currentSort.direction = 'asc';
            }
            
            // Actualizar clases visuales
            actualizarEstadoHeaders();
            
            // Aplicar ordenamiento
            if (currentSort.column && currentSort.direction) {
                ordenarTabla(currentSort.column, currentSort.direction);
            } else {
                // Restaurar orden original
                restaurarOrdenOriginal();
            }
        });
    });
    
    // ============================================================
    // FUNCIÓN: ACTUALIZAR ESTADO VISUAL DE HEADERS
    // ============================================================
    function actualizarEstadoHeaders() {
        sortableHeaders.forEach(header => {
            const column = header.getAttribute('data-sort');
            
            // Remover clases de ordenamiento
            header.classList.remove('sort-asc', 'sort-desc');
            
            // Agregar clase si es la columna activa
            if (column === currentSort.column) {
                if (currentSort.direction === 'asc') {
                    header.classList.add('sort-asc');
                } else if (currentSort.direction === 'desc') {
                    header.classList.add('sort-desc');
                }
            }
        });
    }
    
    // ============================================================
    // FUNCIÓN: ORDENAR TABLA
    // ============================================================
    function ordenarTabla(column, direction) {
        const rows = Array.from(tableBody.querySelectorAll('.merma-row'));
        
        let sortedRows = rows.sort((a, b) => {
            let valueA, valueB;
            
            if (column === 'perdida') {
                valueA = parseFloat(a.getAttribute('data-perdida'));
                valueB = parseFloat(b.getAttribute('data-perdida'));
            } else if (column === 'cantidad') {
                valueA = parseInt(a.getAttribute('data-cantidad'));
                valueB = parseInt(b.getAttribute('data-cantidad'));
            } else if (column === 'precio') {
                valueA = parseFloat(a.getAttribute('data-precio'));
                valueB = parseFloat(b.getAttribute('data-precio'));
            } else if (column === 'fecha') {
                // Convertir fechas a timestamps para comparar
                valueA = new Date(a.getAttribute('data-fecha')).getTime();
                valueB = new Date(b.getAttribute('data-fecha')).getTime();
            }
            
            // Ordenar según dirección
            if (direction === 'asc') {
                return valueA - valueB;
            } else {
                return valueB - valueA;
            }
        });
        
        // Limpiar tabla
        tableBody.innerHTML = '';
        
        // Agregar filas ordenadas con animación
        sortedRows.forEach((row, index) => {
            row.style.animation = 'slideIn 0.3s ease';
            row.style.animationDelay = `${index * 0.02}s`;
            tableBody.appendChild(row);
        });
    }
    
    // ============================================================
    // FUNCIÓN: RESTAURAR ORDEN ORIGINAL
    // ============================================================
    function restaurarOrdenOriginal() {
        // Limpiar tabla
        tableBody.innerHTML = '';
        
        // Agregar filas en orden original
        originalRows.forEach((row, index) => {
            row.style.animation = 'slideIn 0.3s ease';
            row.style.animationDelay = `${index * 0.02}s`;
            tableBody.appendChild(row);
        });
    }
    
    // ============================================================
    // FUNCIÓN: MOSTRAR MENSAJE DE NO RESULTADOS
    // ============================================================
    function mostrarMensajeNoResultados(count, searchTerm) {
        // Remover mensaje anterior si existe
        const mensajeAnterior = tableBody.querySelector('.no-results-row');
        if (mensajeAnterior) {
            mensajeAnterior.remove();
        }
        
        // Si no hay resultados, mostrar mensaje
        if (count === 0 && searchTerm) {
            const noResultsRow = document.createElement('tr');
            noResultsRow.className = 'no-results-row';
            noResultsRow.innerHTML = `
                <td colspan="6" class="merma-vacio">
                    <i class="bi bi-search"></i>
                    <p><strong>No se encontraron resultados</strong></p>
                    <p>No hay productos que coincidan con "${searchTerm}"</p>
                    <small>Intenta con otro término de búsqueda</small>
                </td>
            `;
            tableBody.appendChild(noResultsRow);
        }
    }
});

// ============================================================
// ANIMACIONES CSS
// ============================================================
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
`;
document.head.appendChild(style);
