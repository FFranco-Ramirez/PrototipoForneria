# ================================================================
# =                                                              =
# =     VISTAS PARA DETALLES DE FACTURAS DE PROVEEDORES        =
# =                                                              =
# ================================================================
#
# Este archivo contiene las vistas para gestionar los detalles
# (productos) de las facturas de proveedores.

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from decimal import Decimal
from ventas.models.proveedores import FacturaProveedor, DetalleFacturaProveedor
from ventas.models.productos import Productos
from ventas.models.movimientos import MovimientosInventario
import logging

logger = logging.getLogger('ventas')


@login_required
@require_http_methods(["POST"])
def agregar_detalle_factura_ajax(request, factura_id):
    """
    API AJAX para agregar un producto a una factura de proveedor.
    
    Parámetros POST:
    - producto_id: ID del producto
    - cantidad: Cantidad a agregar
    - precio_unitario: Precio unitario del producto
    - descuento_pct: Porcentaje de descuento (opcional)
    """
    try:
        factura = get_object_or_404(FacturaProveedor, pk=factura_id, eliminado__isnull=True)
        
        producto_id = request.POST.get('producto_id')
        cantidad = int(request.POST.get('cantidad', 0))
        precio_unitario = Decimal(request.POST.get('precio_unitario', '0.00'))
        descuento_pct = Decimal(request.POST.get('descuento_pct', '0.00'))
        
        # Validaciones
        if not producto_id or cantidad <= 0 or precio_unitario <= 0:
            return JsonResponse({
                'success': False,
                'mensaje': 'Datos inválidos. Verifique cantidad y precio.'
            }, status=400)
        
        producto = get_object_or_404(Productos, pk=producto_id, eliminado__isnull=True)
        
        # Calcular subtotal
        subtotal = cantidad * precio_unitario
        if descuento_pct > 0:
            descuento = subtotal * (descuento_pct / 100)
            subtotal = subtotal - descuento
        
        # Crear el detalle
        with transaction.atomic():
            detalle = DetalleFacturaProveedor.objects.create(
                factura_proveedor=factura,
                productos=producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                descuento_pct=descuento_pct,
                subtotal=subtotal
            )
            
            # Actualizar totales de la factura
            factura.actualizar_totales()
        
        logger.info(f'Detalle agregado a factura {factura.id}: {producto.nombre} x {cantidad}')
        
        return JsonResponse({
            'success': True,
            'mensaje': f'Producto "{producto.nombre}" agregado exitosamente.',
            'detalle_id': detalle.id
        })
        
    except Exception as e:
        logger.error(f'Error al agregar detalle a factura: {str(e)}', exc_info=True)
        return JsonResponse({
            'success': False,
            'mensaje': f'Error al agregar producto: {str(e)}'
        }, status=500)


@login_required
@require_http_methods(["POST"])
def eliminar_detalle_factura_ajax(request, detalle_id):
    """
    API AJAX para eliminar un detalle de factura.
    """
    try:
        detalle = get_object_or_404(DetalleFacturaProveedor, pk=detalle_id)
        factura = detalle.factura_proveedor
        
        with transaction.atomic():
            # Eliminar el detalle (eliminación física, ya que no hay campo eliminado)
            factura = detalle.factura_proveedor
            detalle.delete()
            
            # Actualizar totales de la factura
            factura.actualizar_totales()
        
        logger.info(f'Detalle {detalle_id} eliminado de factura {factura.id}')
        
        return JsonResponse({
            'success': True,
            'mensaje': 'Producto eliminado de la factura exitosamente.'
        })
        
    except Exception as e:
        logger.error(f'Error al eliminar detalle: {str(e)}', exc_info=True)
        return JsonResponse({
            'success': False,
            'mensaje': f'Error al eliminar producto: {str(e)}'
        }, status=500)


@login_required
@require_http_methods(["POST"])
def recibir_factura_ajax(request, factura_id):
    """
    API AJAX para marcar una factura como recibida y actualizar el stock.
    
    Cuando se recibe una factura:
    1. Se marca como recibida
    2. Se actualiza el stock de todos los productos en los detalles
    3. Se crean movimientos de inventario
    """
    try:
        factura = get_object_or_404(
            FacturaProveedor.objects.select_related('proveedor'),
            pk=factura_id,
            eliminado__isnull=True
        )
        
        if factura.estado_recepcion == 'recibida':
            return JsonResponse({
                'success': False,
                'mensaje': 'Esta factura ya fue recibida anteriormente.'
            }, status=400)
        
        with transaction.atomic():
            # Marcar como recibida
            from datetime import date
            factura.estado_recepcion = 'recibida'
            factura.fecha_recepcion = date.today()
            factura.save()
            
            # Obtener todos los detalles
            detalles = DetalleFacturaProveedor.objects.filter(
                factura_proveedor=factura
            ).select_related('productos')
            
            productos_actualizados = []
            
            # Actualizar stock de cada producto
            for detalle in detalles:
                producto = detalle.productos
                
                # Actualizar cantidad
                producto.cantidad += detalle.cantidad
                producto.save()
                
                # Crear movimiento de inventario
                MovimientosInventario.objects.create(
                    tipo_movimiento='entrada',
                    cantidad=detalle.cantidad,
                    productos=producto,
                    origen='compra',
                    referencia_id=factura.id,
                    tipo_referencia='factura_proveedor'
                )
                
                productos_actualizados.append({
                    'nombre': producto.nombre,
                    'cantidad': detalle.cantidad,
                    'stock_actual': producto.cantidad
                })
            
            logger.info(f'Factura {factura.id} recibida. {len(productos_actualizados)} productos actualizados.')
        
        return JsonResponse({
            'success': True,
            'mensaje': f'Factura recibida exitosamente. {len(productos_actualizados)} productos actualizados.',
            'productos': productos_actualizados
        })
        
    except Exception as e:
        logger.error(f'Error al recibir factura: {str(e)}', exc_info=True)
        return JsonResponse({
            'success': False,
            'mensaje': f'Error al recibir factura: {str(e)}'
        }, status=500)

