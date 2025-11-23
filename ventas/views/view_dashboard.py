from django.http import JsonResponse
from ventas.models.productos import Productos
from datetime import datetime, timedelta

def perdida_siete_dias(request):
    """
    Calcula la perdida total de productos que venceran
    en los proximos 7 dias siempre y cuando tengan stock
    """

    # definimos la fecha actual
    hoy = datetime.now().date()

    # definimos la fecha de vencimiento de 7 dias
    fecha_vencimiento = hoy + timedelta(days=7)

    # lo siguiente es parecido a hacer la consulta de SQL
    # SELECT id, nombre, precio, stock_actual, caducidad, ... (todos los campos)
    # FROM ventas_productos
    # WHERE caducidad >= 'fecha_de_hoy' 
    #   AND caducidad <= 'fecha_de_vencimiento' 
    #   AND stock_actual > 0;
    # La respuesta a esta seudo consulta de SQL se guarda dentro de productos_a_vencer
    productos_a_vencer = Productos.objects.filter(
        caducidad__gte=hoy, # Caducan en o después de hoy (caducidad__gte=hoy)
        caducidad__lte=fecha_vencimiento, # Caducan antes de nuestra fecha límite de 7 días
        stock_actual__gt=0 # Tienen al menos 1 unidad en stock
    )

    # Creamos una variable que sera la perdida, de momento le ponemos 0 por que debe tener unvalor
    perdida_total_calculada = 0

    # Ahora, recorremos uno por uno cada producto que encontramos en el paso anterior.
    for producto in productos_a_vencer:
        # Para cada producto, calculamos el valor total de su stock.
        valor_stock_del_producto = producto.precio * producto.stock_actual
        
        # Añadimos el valor de este producto a nuestro total acumulado.
        perdida_total_calculada += valor_stock_del_producto

    # Paso 4: Preparar los datos para la respuesta JSON
    data = {
        'perdida_total': float(perdida_total_calculada),
    }

    return JsonResponse(data)
