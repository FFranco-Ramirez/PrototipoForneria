# ================================================================
# =                                                              =
# =           APIS PARA MÉTRICAS DEL DASHBOARD                  =
# =                                                              =
# ================================================================
#
# Este archivo contiene las vistas API que proveen datos en tiempo real
# para las métricas principales del dashboard.

from django.http import JsonResponse
from django.db.models import Sum, Count, F
from datetime import datetime, date
from ventas.models.ventas import Ventas, DetalleVenta
from ventas.models.productos import Productos
from ventas.models.alertas import Alertas


def ventas_del_dia_api(request):
    """
    API que retorna las ventas del día actual.
    
    Returns:
        JSON con:
        - total_ventas: Monto total vendido hoy
        - num_transacciones: Número de ventas realizadas
    """
    hoy = date.today()
    
    # Obtener todas las ventas de hoy
    ventas_hoy = Ventas.objects.filter(
        fecha__date=hoy
    )
    
    # Calcular el total vendido
    total_ventas = ventas_hoy.aggregate(
        total=Sum('total_con_iva')
    )['total'] or 0
    
    # Contar número de transacciones
    num_transacciones = ventas_hoy.count()
    
    return JsonResponse({
        'total_ventas': float(total_ventas),
        'num_transacciones': num_transacciones
    })


def stock_bajo_api(request):
    """
    API que retorna productos con stock bajo.
    
    Un producto tiene stock bajo cuando:
    - cantidad <= stock_minimo (si stock_minimo está definido)
    - cantidad <= 5 (si stock_minimo no está definido)
    
    Returns:
        JSON con:
        - num_productos: Número de productos con stock bajo
        - productos: Lista de productos con stock bajo
    """
    # Obtener productos activos (no eliminados, no en merma)
    productos = Productos.objects.filter(
        eliminado__isnull=True,
        estado_merma='activo'
    )
    
    # Filtrar productos con stock bajo
    productos_stock_bajo = []
    for producto in productos:
        stock_minimo = producto.stock_minimo if producto.stock_minimo else 5
        if producto.cantidad <= stock_minimo:
            productos_stock_bajo.append({
                'id': producto.id,
                'nombre': producto.nombre,
                'cantidad': producto.cantidad,
                'stock_minimo': stock_minimo
            })
    
    return JsonResponse({
        'num_productos': len(productos_stock_bajo),
        'productos': productos_stock_bajo
    })


def alertas_pendientes_api(request):
    """
    API que retorna el número de alertas activas.
    
    Returns:
        JSON con:
        - num_alertas: Número total de alertas activas
        - por_tipo: Desglose por tipo (roja, amarilla, verde)
    """
    # Contar alertas activas
    alertas_activas = Alertas.objects.filter(estado='activa')
    
    # Contar por tipo
    alertas_rojas = alertas_activas.filter(tipo_alerta='roja').count()
    alertas_amarillas = alertas_activas.filter(tipo_alerta='amarilla').count()
    alertas_verdes = alertas_activas.filter(tipo_alerta='verde').count()
    
    total_alertas = alertas_activas.count()
    
    return JsonResponse({
        'num_alertas': total_alertas,
        'por_tipo': {
            'roja': alertas_rojas,
            'amarilla': alertas_amarillas,
            'verde': alertas_verdes
        }
    })


def top_producto_api(request):
    """
    API que retorna el producto más vendido del día.
    
    Returns:
        JSON con:
        - nombre: Nombre del producto más vendido
        - unidades: Cantidad de unidades vendidas
        - total_vendido: Monto total generado por ese producto
    """
    hoy = date.today()
    
    # Obtener detalles de ventas de hoy y agrupar por producto
    top_producto = DetalleVenta.objects.filter(
        ventas__fecha__date=hoy
    ).values(
        'productos__nombre'
    ).annotate(
        total_unidades=Sum('cantidad'),
        total_vendido=Sum(F('cantidad') * F('precio_unitario'))
    ).order_by('-total_unidades').first()
    
    if top_producto:
        return JsonResponse({
            'nombre': top_producto['productos__nombre'],
            'unidades': top_producto['total_unidades'],
            'total_vendido': float(top_producto['total_vendido'])
        })
    else:
        # Si no hay ventas hoy
        return JsonResponse({
            'nombre': 'Sin ventas',
            'unidades': 0,
            'total_vendido': 0
        })
