# ================================================================
# =                                                              =
# =        VISTA: AJUSTES MANUALES DE STOCK                     =
# =                                                              =
# ================================================================
#
# Este archivo implementa ajustes manuales de stock según RF-I2 del Jira:
# "Ajustes de stock (entradas/mermas) y reflejo en kardex"
#
# REQUISITOS JIRA:
# - RF-I2: Ajustes de stock (entradas/mermas) y reflejo en kardex
#
# FUNCIONALIDADES:
# - Ajustar stock manualmente (entrada o salida)
# - Crear movimiento en kardex automáticamente
# - Registrar motivo del ajuste
# - Trazabilidad completa

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction
from django.conf import settings
from ventas.models import Productos, MovimientosInventario
from ventas.decorators import require_rol
import json
import logging


# ================================================================
# =        VISTA: PÁGINA DE AJUSTES DE STOCK                    =
# ================================================================

@login_required
@require_rol('Administrador', 'Contador')  # Solo admin y contador pueden ajustar
def ajustes_stock_view(request):
    """
    Vista para mostrar la página de ajustes manuales de stock.
    
    Cumple con RF-I2 del Jira:
    - Ajustes de stock (entradas/mermas)
    - Reflejo en kardex
    
    Args:
        request: HttpRequest
        
    Returns:
        HttpResponse: Página HTML con formulario de ajuste
    """
    
    # Obtener todos los productos activos
    productos = Productos.objects.filter(
        eliminado__isnull=True
    ).order_by('nombre')
    
    context = {
        'productos': productos,
    }
    
    return render(request, 'ajustes_stock.html', context)


# ================================================================
# =        VISTA API: PROCESAR AJUSTE DE STOCK                  =
# ================================================================

@login_required
@require_rol('Administrador', 'Contador')
@require_http_methods(["POST"])
def procesar_ajuste_stock_ajax(request):
    """
    Procesa un ajuste manual de stock.
    
    Args:
        request: HttpRequest con JSON:
        {
            "producto_id": 1,
            "tipo": "entrada" o "salida",
            "cantidad": 10,
            "motivo": "Ajuste por inventario físico"
        }
        
    Returns:
        JsonResponse: Resultado de la operación
    """
    
    try:
        # Obtener datos del JSON
        data = json.loads(request.body)
        producto_id = data.get('producto_id')
        tipo = data.get('tipo')  # 'entrada' o 'salida'
        cantidad = int(data.get('cantidad', 0))
        motivo = data.get('motivo', 'Ajuste manual')
        
        # Validaciones
        if not producto_id:
            return JsonResponse({
                'success': False,
                'mensaje': 'Debe seleccionar un producto'
            }, status=400)
        
        if cantidad <= 0:
            return JsonResponse({
                'success': False,
                'mensaje': 'La cantidad debe ser mayor a 0'
            }, status=400)
        
        if tipo not in ['entrada', 'salida']:
            return JsonResponse({
                'success': False,
                'mensaje': 'Tipo de ajuste inválido'
            }, status=400)
        
        # Obtener producto
        producto = get_object_or_404(Productos, pk=producto_id)
        
        # Procesar ajuste dentro de una transacción
        with transaction.atomic():
            # Actualizar stock según el tipo
            if tipo == 'entrada':
                producto.cantidad = (producto.cantidad or 0) + cantidad
                if producto.stock_actual is not None:
                    producto.stock_actual = (producto.stock_actual or 0) + cantidad
            else:  # salida
                stock_actual = producto.cantidad or 0
                if cantidad > stock_actual:
                    return JsonResponse({
                        'success': False,
                        'mensaje': f'Stock insuficiente. Disponible: {stock_actual}, Solicitado: {cantidad}'
                    }, status=400)
                
                producto.cantidad = stock_actual - cantidad
                if producto.stock_actual is not None:
                    producto.stock_actual = max(0, (producto.stock_actual or 0) - cantidad)
            
            producto.save(update_fields=['cantidad', 'stock_actual'])
            
            # Crear movimiento en kardex
            MovimientosInventario.objects.create(
                tipo_movimiento=tipo,
                cantidad=cantidad,
                productos=producto,
                origen='ajuste',
                referencia_id=None,
                tipo_referencia='ajuste_manual'
            )
        
        return JsonResponse({
            'success': True,
            'mensaje': f'Ajuste de stock procesado correctamente. Nuevo stock: {producto.cantidad}',
            'nuevo_stock': producto.cantidad
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'mensaje': 'Error al procesar los datos JSON'
        }, status=400)
        
    except Exception as e:
        logger = logging.getLogger('ventas')
        logger.error(f'Error al procesar ajuste de stock: {e}', exc_info=True)
        
        # En producción, no exponer detalles del error al usuario
        if settings.DEBUG:
            mensaje_error = f'Error al procesar el ajuste: {str(e)}'
        else:
            mensaje_error = 'Error al procesar el ajuste. Contacte al administrador.'
        
        return JsonResponse({
            'success': False,
            'mensaje': mensaje_error
        }, status=500)

