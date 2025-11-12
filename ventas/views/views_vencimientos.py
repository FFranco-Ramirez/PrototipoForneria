from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from ventas.models.productos import Productos

def productos_por_vencer_api(request):
    hoy = timezone.localdate()
    limite = hoy + timedelta(days=7)
    qs = (Productos.objects
          .filter(eliminado__isnull=True, caducidad__range=(hoy, limite))
          .order_by('caducidad', 'nombre'))
    items = [{"nombre": p.nombre, "caducidad": p.caducidad.isoformat()} for p in qs]
    return JsonResponse({"count": len(items), "items": items})

def perdida_potencial_7d_api(request):
    hoy = timezone.localdate()
    limite = hoy + timedelta(days=7)
    qs = (
        Productos.objects
        .filter(
            eliminado__isnull=True,
            caducidad__range=(hoy, limite),
            precio__gt=0,
        )
        .annotate(stock=Coalesce(F('stock_actual'), F('cantidad'), Value(0)))
        .filter(stock__gt=0)
    )
    total = qs.aggregate(
        perdida=Coalesce(Sum(F('precio') * F('stock')), Value(0))
    )['perdida']
    return JsonResponse({"perdida_potencial": float(total)})