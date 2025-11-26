from django.http import JsonResponse
from ventas.models.productos import Productos
from datetime import datetime, timedelta


def calcular_perdida_por_dias(dias):
    """
    Función auxiliar que calcula la pérdida potencial para un número específico de días.
    
    Args:
        dias (int): Número de días a calcular (7, 14, 30, etc.)
    
    Returns:
        float: Pérdida total calculada
    """
    # definimos la fecha actual
    hoy = datetime.now().date()

    # definimos la fecha de vencimiento según los días especificados
    fecha_vencimiento = hoy + timedelta(days=dias)

    # Obtenemos todos los productos que vencen en el período especificado
    productos_a_vencer = Productos.objects.filter(
        caducidad__gte=hoy,  # Caducan en o después de hoy
        caducidad__lte=fecha_vencimiento,  # Caducan antes de nuestra fecha límite
        eliminado__isnull=True  # Solo productos activos (no eliminados)
    )

    # Creamos una variable que sera la perdida
    perdida_total_calculada = 0

    # Recorremos cada producto
    for producto in productos_a_vencer:
        # Determinamos el stock real: usamos 'cantidad' si existe, sino 'stock_actual'
        stock_real = producto.cantidad if producto.cantidad > 0 else (producto.stock_actual or 0)

        # Solo calculamos pérdida si hay stock
        if stock_real > 0:
            # Calculamos el valor total de su stock
            valor_stock_del_producto = producto.precio * stock_real

            # Añadimos el valor al total acumulado
            perdida_total_calculada += valor_stock_del_producto

    return float(perdida_total_calculada)


def perdida_siete_dias(request):
    """
    Calcula la perdida total de productos que venceran
    en los proximos 7 dias siempre y cuando tengan stock
    """
    perdida_total = calcular_perdida_por_dias(7)
    
    data = {
        'perdida_total': perdida_total,
    }

    return JsonResponse(data)


def perdida_catorce_dias(request):
    """
    Calcula la perdida total de productos que venceran
    en los proximos 14 dias siempre y cuando tengan stock
    """
    perdida_total = calcular_perdida_por_dias(14)
    
    data = {
        'perdida_total': perdida_total,
    }

    return JsonResponse(data)


def perdida_treinta_dias(request):
    """
    Calcula la perdida total de productos que venceran
    en los proximos 30 dias siempre y cuando tengan stock
    """
    perdida_total = calcular_perdida_por_dias(30)
    
    data = {
        'perdida_total': perdida_total,
    }

    return JsonResponse(data)
