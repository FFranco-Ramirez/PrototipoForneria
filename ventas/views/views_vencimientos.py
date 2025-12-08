from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from ventas.models.productos import Productos


def productos_por_vencer_api(request):
    """API que retorna productos que vencen en los próximos 7 días"""
    hoy = timezone.localdate()
    limite = hoy + timedelta(days=7)
    qs = (Productos.objects
          .filter(eliminado__isnull=True, caducidad__range=(hoy, limite))
          .order_by('caducidad', 'nombre'))
    items = [{
        "id": p.id,
        "nombre": p.nombre, 
        "caducidad": p.caducidad.isoformat()
    } for p in qs]
    return JsonResponse({"count": len(items), "items": items})


def productos_por_vencer_14_dias_api(request):
    """API que retorna productos que vencen en los próximos 14 días"""
    hoy = timezone.localdate()
    limite = hoy + timedelta(days=14)
    qs = (Productos.objects
          .filter(eliminado__isnull=True, caducidad__range=(hoy, limite))
          .order_by('caducidad', 'nombre'))
    items = [{
        "id": p.id,
        "nombre": p.nombre, 
        "caducidad": p.caducidad.isoformat()
    } for p in qs]
    return JsonResponse({"count": len(items), "items": items})


def productos_por_vencer_30_dias_api(request):
    """API que retorna productos que vencen en los próximos 30 días"""
    hoy = timezone.localdate()
    limite = hoy + timedelta(days=30)
    qs = (Productos.objects
          .filter(eliminado__isnull=True, caducidad__range=(hoy, limite))
          .order_by('caducidad', 'nombre'))
    items = [{
        "id": p.id,
        "nombre": p.nombre, 
        "caducidad": p.caducidad.isoformat()
    } for p in qs]
    return JsonResponse({"count": len(items), "items": items})