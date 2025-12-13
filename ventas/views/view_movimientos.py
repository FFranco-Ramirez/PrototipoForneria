# ================================================================
# =                                                              =
# =           VISTA PARA HISTORIAL DE MOVIMIENTOS               =
# =                                                              =
# ================================================================
#
# Este archivo contiene la vista que muestra el historial completo
# de movimientos del inventario de la Fornería.
#
# PROPÓSITO:
# - Mostrar todos los movimientos de entrada y salida de productos
# - Permitir filtrar por tipo de movimiento (entrada/salida)
# - Facilitar la auditoría y seguimiento del inventario
#
# ACCESO:
# - URL: /movimientos/
# - Requiere autenticación (login)
# - Disponible para todos los usuarios autenticados

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ventas.models import MovimientosInventario


# ================================================================
# =                    VISTA: MOVIMIENTOS                        =
# ================================================================

@login_required
def movimientos_view(request):
    """
    Muestra el listado de todos los movimientos de inventario.
    
    Esta vista permite ver el historial completo de cambios en el inventario,
    con la opción de filtrar por tipo de movimiento.
    
    Filtros disponibles:
    - Tipo de movimiento: entrada o salida
    - (Futuro: Rango de fechas, producto específico)
    
    Args:
        request: Objeto HttpRequest con la información de la petición
        
    Returns:
        HttpResponse: Página HTML con el listado de movimientos
    """
    
    # ============================================================
    # PASO 1: Obtener todos los movimientos
    # ============================================================
    # select_related('productos'): Optimización para evitar consultas múltiples
    # Carga el producto relacionado en la misma consulta SQL
    movimientos = MovimientosInventario.objects.select_related('productos').all()
    
    # ============================================================
    # PASO 2: Aplicar filtros si existen
    # ============================================================
    # Obtener el parámetro 'tipo' de la URL (ej: ?tipo=entrada)
    tipo_filtro = request.GET.get('tipo', '')
    
    # Si se seleccionó un tipo, filtrar los movimientos
    if tipo_filtro:
        movimientos = movimientos.filter(tipo_movimiento=tipo_filtro)
    
    # ============================================================
    # PASO 3: Preparar el contexto para el template
    # ============================================================
    # El contexto es un diccionario con las variables que usaremos en el HTML
    context = {
        'movimientos': movimientos,      # Lista de movimientos a mostrar
        'tipo_filtro': tipo_filtro,      # Tipo seleccionado (para mantener el filtro activo)
    }
    
    # ============================================================
    # PASO 4: Renderizar el template
    # ============================================================
    # render() combina el template HTML con el contexto y devuelve la página
    return render(request, 'movimientos.html', context)
