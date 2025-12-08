# ================================================================
# =                                                              =
# =          VISTA: REPORTE TOP PRODUCTOS VENDIDOS              =
# =                                                              =
# ================================================================
#
# Este archivo implementa el reporte de top productos según RF-V5 del Jira:
# "Reporte Top productos (cantidad / neto)"
#
# REQUISITOS JIRA:
# - RF-V5: Reporte Top productos (cantidad / neto)
#
# FUNCIONALIDADES:
# - Ranking por cantidad vendida
# - Ranking por monto neto vendido
# - Filtro por rango de fechas
# - Visualización con gráficos (opcional)
# - Exportación a CSV (opcional)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Count, Q
from django.http import HttpResponse
from datetime import datetime
from decimal import Decimal
import csv

from ventas.models import Productos, DetalleVenta, Ventas


# ================================================================
# =              VISTA: TOP PRODUCTOS                           =
# ================================================================

@login_required
def top_productos_view(request):
    """
    Vista para mostrar ranking de productos más vendidos.
    
    Cumple con RF-V5 del Jira:
    - Ranking por cantidad vendida
    - Ranking por monto neto vendido
    - Filtro por rango de fechas
    
    Args:
        request: HttpRequest con parámetros de filtro
        
    Returns:
        HttpResponse: Página HTML con el ranking
    """
    
    # ============================================================
    # PASO 1: Inicializar variables
    # ============================================================
    reporte_generado = False
    ranking_cantidad = []
    ranking_neto = []
    tipo_ranking = 'cantidad'  # Por defecto mostrar por cantidad
    
    fecha_desde = None
    fecha_hasta = None
    
    # ============================================================
    # PASO 2: Procesar filtros del formulario
    # ============================================================
    if request.method == 'GET' and 'generar' in request.GET:
        reporte_generado = True
        
        # Obtener tipo de ranking
        tipo_ranking = request.GET.get('tipo_ranking', 'cantidad')
        
        # Obtener fechas
        fecha_desde_str = request.GET.get('fecha_desde')
        fecha_hasta_str = request.GET.get('fecha_hasta')
        
        try:
            if fecha_desde_str:
                fecha_desde = datetime.strptime(fecha_desde_str, '%Y-%m-%d').date()
            if fecha_hasta_str:
                fecha_hasta = datetime.strptime(fecha_hasta_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            # Si hay error, usar último mes
            hoy = timezone.now().date()
            fecha_desde = hoy.replace(day=1)
            fecha_hasta = hoy
        
        # ============================================================
        # PASO 3: Obtener ventas en el rango de fechas
        # ============================================================
        ventas_query = Ventas.objects.all()
        
        if fecha_desde:
            ventas_query = ventas_query.filter(fecha__date__gte=fecha_desde)
        if fecha_hasta:
            ventas_query = ventas_query.filter(fecha__date__lte=fecha_hasta)
        
        ventas_ids = ventas_query.values_list('id', flat=True)
        
        # ============================================================
        # PASO 4: Calcular ranking por cantidad
        # ============================================================
        ranking_cantidad_query = DetalleVenta.objects.filter(
            ventas_id__in=ventas_ids
        ).values(
            'productos_id',
            'productos__nombre',
            'productos__precio'
        ).annotate(
            total_cantidad=Sum('cantidad'),
            total_neto=Sum('precio_unitario') * Sum('cantidad')
        ).order_by('-total_cantidad')[:20]  # Top 20
        
        ranking_cantidad = []
        for item in ranking_cantidad_query:
            # Calcular total neto correctamente
            detalles = DetalleVenta.objects.filter(
                ventas_id__in=ventas_ids,
                productos_id=item['productos_id']
            )
            total_neto = sum(
                detalle.cantidad * detalle.precio_unitario 
                for detalle in detalles
            )
            
            ranking_cantidad.append({
                'producto_id': item['productos_id'],
                'nombre': item['productos__nombre'],
                'cantidad_vendida': item['total_cantidad'],
                'total_neto': total_neto,
                'precio_promedio': total_neto / item['total_cantidad'] if item['total_cantidad'] > 0 else Decimal('0.00'),
            })
        
        # ============================================================
        # PASO 5: Calcular ranking por monto neto
        # ============================================================
        ranking_neto_query = DetalleVenta.objects.filter(
            ventas_id__in=ventas_ids
        ).values(
            'productos_id',
            'productos__nombre'
        ).annotate(
            total_cantidad=Sum('cantidad')
        ).order_by()[:20]
        
        ranking_neto = []
        for item in ranking_neto_query:
            # Calcular total neto sumando todos los detalles
            detalles = DetalleVenta.objects.filter(
                ventas_id__in=ventas_ids,
                productos_id=item['productos_id']
            )
            
            total_neto = sum(
                detalle.cantidad * detalle.precio_unitario 
                for detalle in detalles
            )
            
            ranking_neto.append({
                'producto_id': item['productos_id'],
                'nombre': item['productos__nombre'],
                'cantidad_vendida': item['total_cantidad'],
                'total_neto': total_neto,
                'precio_promedio': total_neto / item['total_cantidad'] if item['total_cantidad'] > 0 else Decimal('0.00'),
            })
        
        # Ordenar por total_neto descendente
        ranking_neto.sort(key=lambda x: x['total_neto'], reverse=True)
        ranking_neto = ranking_neto[:20]  # Top 20
    
    # ============================================================
    # PASO 6: Preparar contexto
    # ============================================================
    context = {
        'reporte_generado': reporte_generado,
        'ranking_cantidad': ranking_cantidad,
        'ranking_neto': ranking_neto,
        'tipo_ranking': tipo_ranking,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
    }
    
    # ============================================================
    # PASO 7: Renderizar template
    # ============================================================
    return render(request, 'top_productos.html', context)


# ================================================================
# =        VISTA: EXPORTAR TOP PRODUCTOS A CSV                  =
# ================================================================

@login_required
def exportar_top_productos_csv(request, tipo='cantidad'):
    """
    Exporta el ranking de productos a formato CSV.
    
    Args:
        request: HttpRequest con parámetros de filtro
        tipo: 'cantidad' o 'neto'
        
    Returns:
        HttpResponse: Archivo CSV descargable
    """
    
    # Aplicar mismos filtros que el reporte
    fecha_desde_str = request.GET.get('fecha_desde')
    fecha_hasta_str = request.GET.get('fecha_hasta')
    
    ventas_query = Ventas.objects.all()
    
    if fecha_desde_str:
        try:
            fecha_desde = datetime.strptime(fecha_desde_str, '%Y-%m-%d').date()
            ventas_query = ventas_query.filter(fecha__date__gte=fecha_desde)
        except ValueError:
            pass
    
    if fecha_hasta_str:
        try:
            fecha_hasta = datetime.strptime(fecha_hasta_str, '%Y-%m-%d').date()
            ventas_query = ventas_query.filter(fecha__date__lte=fecha_hasta)
        except ValueError:
            pass
    
    ventas_ids = ventas_query.values_list('id', flat=True)
    
    # Obtener ranking según tipo
    if tipo == 'cantidad':
        ranking = DetalleVenta.objects.filter(
            ventas_id__in=ventas_ids
        ).values(
            'productos_id',
            'productos__nombre'
        ).annotate(
            total_cantidad=Sum('cantidad')
        ).order_by('-total_cantidad')[:20]
    else:
        # Por neto - necesitamos calcular manualmente
        productos_data = {}
        detalles = DetalleVenta.objects.filter(ventas_id__in=ventas_ids)
        
        for detalle in detalles:
            producto_id = detalle.productos_id
            if producto_id not in productos_data:
                productos_data[producto_id] = {
                    'nombre': detalle.productos.nombre,
                    'cantidad': 0,
                    'neto': Decimal('0.00'),
                }
            productos_data[producto_id]['cantidad'] += detalle.cantidad
            productos_data[producto_id]['neto'] += detalle.cantidad * detalle.precio_unitario
        
        ranking = sorted(
            productos_data.items(),
            key=lambda x: x[1]['neto'],
            reverse=True
        )[:20]
    
    # Crear respuesta CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="top_productos_{tipo}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Producto', 'Cantidad Vendida', 'Total Neto', 'Precio Promedio'])
    
    # Escribir datos
    for item in ranking:
        if tipo == 'cantidad':
            detalles = DetalleVenta.objects.filter(
                ventas_id__in=ventas_ids,
                productos_id=item['productos_id']
            )
            total_neto = sum(d.cantidad * d.precio_unitario for d in detalles)
            precio_promedio = total_neto / item['total_cantidad'] if item['total_cantidad'] > 0 else 0
            
            writer.writerow([
                item['productos__nombre'],
                item['total_cantidad'],
                float(total_neto),
                float(precio_promedio),
            ])
        else:
            producto_id, data = item
            precio_promedio = data['neto'] / data['cantidad'] if data['cantidad'] > 0 else 0
            writer.writerow([
                data['nombre'],
                data['cantidad'],
                float(data['neto']),
                float(precio_promedio),
            ])
    
    return response

