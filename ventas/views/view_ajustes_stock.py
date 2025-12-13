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
        from decimal import Decimal
        
        data = json.loads(request.body)
        producto_id = data.get('producto_id')
        tipo = data.get('tipo')  # 'entrada' o 'salida'
        cantidad = Decimal(str(data.get('cantidad', 0)))  # Permitir decimales
        motivo = data.get('motivo', 'Ajuste manual')
        
        # Validaciones
        if not producto_id:
            return JsonResponse({
                'success': False,
                'mensaje': 'Debe seleccionar un producto'
            }, status=400)
        
        if cantidad <= Decimal('0'):
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
            if tipo == 'entrada':
                # Para ENTRADAS: crear un lote nuevo para mantener trazabilidad
                from ventas.models import Lote
                from django.utils import timezone
                from datetime import timedelta, date
                from decimal import Decimal
                
                # Obtener fecha de caducidad del ajuste (si se proporcionó) o usar fecha por defecto
                fecha_caducidad_ajuste = data.get('fecha_caducidad')
                if fecha_caducidad_ajuste:
                    from datetime import datetime
                    try:
                        fecha_caducidad_obj = datetime.strptime(fecha_caducidad_ajuste, '%Y-%m-%d').date()
                    except ValueError:
                        fecha_caducidad_obj = date.today() + timedelta(days=30)  # Default: 30 días
                else:
                    # Si no se especifica, usar fecha del producto o fecha actual + 30 días
                    fecha_caducidad_obj = producto.caducidad if producto.caducidad else (date.today() + timedelta(days=30))
                
                # Generar número de lote automático
                numero_lote = f"AJUSTE-{producto.id}-{timezone.now().strftime('%Y%m%d%H%M%S')}"
                
                # Crear lote para el ajuste
                lote_ajuste = Lote.objects.create(
                    productos=producto,
                    numero_lote=numero_lote,
                    cantidad=Decimal(str(cantidad)),
                    cantidad_inicial=Decimal(str(cantidad)),
                    fecha_elaboracion=date.today(),
                    fecha_caducidad=fecha_caducidad_obj,
                    fecha_recepcion=timezone.now(),
                    origen='ajuste_manual',
                    estado='activo'
                )
                
                # Actualizar cantidad del producto desde lotes (manejar Decimal)
                cantidad_producto = Decimal(str(producto.cantidad)) if producto.cantidad else Decimal('0')
                producto.cantidad = cantidad_producto + cantidad
                if producto.stock_actual is not None:
                    stock_actual_decimal = Decimal(str(producto.stock_actual)) if producto.stock_actual else Decimal('0')
                    producto.stock_actual = stock_actual_decimal + cantidad
                
                # Actualizar fecha de caducidad del producto con la del lote más antiguo
                lote_mas_antiguo = Lote.objects.filter(
                    productos=producto,
                    estado='activo',
                    cantidad__gt=0
                ).order_by('fecha_caducidad', 'fecha_recepcion').first()
                
                if lote_mas_antiguo and lote_mas_antiguo.fecha_caducidad:
                    producto.caducidad = lote_mas_antiguo.fecha_caducidad
                
                producto.save(update_fields=['cantidad', 'stock_actual', 'caducidad'])
                
                # Crear movimiento en kardex
                MovimientosInventario.objects.create(
                    tipo_movimiento='entrada',
                    cantidad=cantidad,
                    productos=producto,
                    origen='ajuste_manual',
                    referencia_id=lote_ajuste.id,
                    tipo_referencia='lote'
                )
            else:  # salida
                # Para SALIDAS: reducir lotes usando FIFO (igual que en ventas)
                from ventas.models import Lote
                from decimal import Decimal
                
                cantidad_restante = Decimal(str(cantidad))
                
                # Obtener lotes activos ordenados por fecha de caducidad (más antiguos primero)
                lotes_activos = Lote.objects.filter(
                    productos=producto,
                    estado='activo',
                    cantidad__gt=0
                ).order_by('fecha_caducidad', 'fecha_recepcion')
                
                stock_disponible = sum(Decimal(str(l.cantidad)) for l in lotes_activos)
                if stock_disponible < cantidad_restante:
                    return JsonResponse({
                        'success': False,
                        'mensaje': f'Stock insuficiente. Disponible: {stock_disponible}, Solicitado: {cantidad}'
                    }, status=400)
                
                for lote in lotes_activos:
                    if cantidad_restante <= Decimal('0'):
                        break
                    
                    cantidad_lote = Decimal(str(lote.cantidad))
                    cantidad_a_tomar = min(cantidad_restante, cantidad_lote)
                    
                    nueva_cantidad_lote = cantidad_lote - cantidad_a_tomar
                    lote.cantidad = nueva_cantidad_lote
                    
                    if nueva_cantidad_lote <= Decimal('0'):
                        lote.estado = 'agotado'
                        lote.cantidad = Decimal('0')
                    
                    lote.save(update_fields=['cantidad', 'estado'])
                    cantidad_restante = cantidad_restante - cantidad_a_tomar
                
                # Actualizar cantidad del producto desde lotes (manejar Decimal)
                cantidad_producto = Decimal(str(producto.cantidad)) if producto.cantidad else Decimal('0')
                producto.cantidad = max(Decimal('0'), cantidad_producto - cantidad)
                if producto.stock_actual is not None:
                    stock_actual_decimal = Decimal(str(producto.stock_actual)) if producto.stock_actual else Decimal('0')
                    producto.stock_actual = max(Decimal('0'), stock_actual_decimal - cantidad)
                
                # Actualizar fecha de caducidad del producto con la del lote más antiguo activo
                lote_mas_antiguo = Lote.objects.filter(
                    productos=producto,
                    estado='activo',
                    cantidad__gt=0
                ).order_by('fecha_caducidad', 'fecha_recepcion').first()
                
                if lote_mas_antiguo and lote_mas_antiguo.fecha_caducidad:
                    producto.caducidad = lote_mas_antiguo.fecha_caducidad
                elif not lote_mas_antiguo:
                    producto.caducidad = None
                
                producto.save(update_fields=['cantidad', 'stock_actual', 'caducidad'])
                
                # Crear movimiento en kardex
                MovimientosInventario.objects.create(
                    tipo_movimiento='salida',
                    cantidad=cantidad,
                    productos=producto,
                    origen='ajuste_manual',
                    referencia_id=None,
                    tipo_referencia='ajuste_manual'
                )
        
        # Obtener nombre de unidad legible para el mensaje
        nombres_unidades = {
            'unidad': 'unidad(es)',
            'kg': 'kilogramo(s)',
            'g': 'gramo(s)',
            'l': 'litro(s)',
            'ml': 'mililitro(s)'
        }
        unidad = producto.unidad_stock or 'unidad'
        nombre_unidad = nombres_unidades.get(unidad, unidad)
        
        return JsonResponse({
            'success': True,
            'mensaje': f'Ajuste de stock procesado correctamente. Nuevo stock: {producto.cantidad} {nombre_unidad}',
            'nuevo_stock': str(producto.cantidad)
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

