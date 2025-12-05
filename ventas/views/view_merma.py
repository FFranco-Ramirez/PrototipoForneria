# ================================================================
# =                                                              =
# =              VISTA PARA PRODUCTOS EN MERMA                   =
# =                                                              =
# ================================================================
#
# Este archivo contiene las vistas para gestionar productos en merma.
# La merma incluye productos vencidos, deteriorados o dañados.
#
# PROPÓSITO:
# - Mostrar listado de productos en merma
# - Permitir mover productos desde inventario activo a merma
# - Facilitar la gestión de productos que no se pueden vender
#
# VISTAS INCLUIDAS:
# 1. merma_list_view: Muestra el listado de productos en merma
# 2. mover_a_merma_ajax: API para mover productos a merma (llamada desde JavaScript)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ventas.models import Productos
import json


# ================================================================
# =              VISTA: LISTADO DE MERMA                         =
# ================================================================

@login_required
def merma_list_view(request):
    """
    Muestra el listado de productos en estado de merma.
    
    Filtra y muestra todos los productos que NO están en estado 'activo',
    es decir, productos vencidos, deteriorados o dañados.
    
    Filtros disponibles:
    - Tipo de merma: vencido, deteriorado, dañado
    
    Args:
        request: Objeto HttpRequest con la información de la petición
        
    Returns:
        HttpResponse: Página HTML con el listado de productos en merma
    """
    
    # ============================================================
    # PASO 1: Obtener productos en merma
    # ============================================================
    # Criterios de búsqueda:
    # - eliminado__isnull=True: Productos no eliminados
    # - exclude(estado_merma='activo'): Excluir productos activos
    productos_merma = Productos.objects.filter(
        eliminado__isnull=True
    ).exclude(estado_merma='activo')
    
    # ============================================================
    # PASO 2: Mostrar todos los productos en merma (sin filtro)
    # ============================================================
    # Ya no filtramos por tipo, mostramos todo por defecto
    
    # ============================================================
    # PASO 3: Calcular estadísticas de merma
    # ============================================================
    # Calcular pérdida total y total de unidades
    perdida_total = 0
    total_unidades = 0
    
    for producto in productos_merma:
        # Calcular pérdida por producto (cantidad × precio)
        perdida_producto = producto.cantidad * producto.precio
        perdida_total += perdida_producto
        total_unidades += producto.cantidad
    
    # ============================================================
    # PASO 4: Preparar el contexto para el template
    # ============================================================
    context = {
        'productos': productos_merma,    # Lista de productos en merma
        'perdida_total': perdida_total,  # Pérdida económica total
        'total_unidades': total_unidades, # Total de unidades en merma
    }
    
    # ============================================================
    # PASO 5: Renderizar el template
    # ============================================================
    return render(request, 'merma_list.html', context)


# ================================================================
# =              API: MOVER PRODUCTOS A MERMA                    =
# ================================================================

@login_required
def mover_a_merma_ajax(request):
    """
    API para mover productos seleccionados a estado de merma.
    
    Esta función se llama desde JavaScript (AJAX) cuando el usuario
    selecciona productos en el inventario y hace clic en "Mover a Merma".
    
    Recibe:
    - producto_ids: Lista de IDs de productos a mover
    - motivo: Razón de la merma ('vencido', 'deteriorado', 'dañado')
    
    Retorna:
    - JSON con el resultado de la operación
    
    Args:
        request: Objeto HttpRequest con los datos en formato JSON
        
    Returns:
        JsonResponse: Respuesta en formato JSON con el resultado
    """
    
    # ============================================================
    # PASO 1: Validar que sea una petición POST
    # ============================================================
    # Solo aceptamos peticiones POST (no GET)
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': 'Método no permitido. Usa POST.'
        })
    
    try:
        # ============================================================
        # PASO 2: Obtener los datos enviados desde JavaScript
        # ============================================================
        # Los datos vienen en formato JSON en el body de la petición
        data = json.loads(request.body)
        
        # Extraer la lista de IDs de productos
        producto_ids = data.get('producto_ids', [])
        
        # Extraer el motivo de la merma (por defecto: 'deteriorado')
        motivo = data.get('motivo', 'deteriorado')
        
        # ============================================================
        # PASO 3: Validar que el motivo sea válido
        # ============================================================
        # Solo aceptamos estos tres motivos
        motivos_validos = ['vencido', 'deteriorado', 'dañado']
        
        if motivo not in motivos_validos:
            return JsonResponse({
                'success': False,
                'error': f'Motivo inválido. Usa: {", ".join(motivos_validos)}'
            })
        
        # ============================================================
        # PASO 4: Validar que se seleccionaron productos
        # ============================================================
        if not producto_ids or len(producto_ids) == 0:
            return JsonResponse({
                'success': False,
                'error': 'No se seleccionaron productos'
            })
        
        # ============================================================
        # PASO 5: Mover productos a merma
        # ============================================================
        # Buscar los productos por sus IDs
        productos = Productos.objects.filter(id__in=producto_ids)
        
        # Actualizar el estado_merma de todos los productos seleccionados
        # update() es más eficiente que un bucle for porque hace una sola consulta SQL
        contador = productos.update(estado_merma=motivo)
        
        # ============================================================
        # PASO 6: Retornar respuesta exitosa
        # ============================================================
        return JsonResponse({
            'success': True,
            'mensaje': f'Se movieron {contador} producto(s) a merma ({motivo})'
        })
        
    except json.JSONDecodeError:
        # Si hay error al decodificar el JSON
        return JsonResponse({
            'success': False,
            'error': 'Error al procesar los datos. Formato JSON inválido.'
        })
    
    except Exception as e:
        # Cualquier otro error inesperado
        return JsonResponse({
            'success': False,
            'error': f'Error inesperado: {str(e)}'
        })
