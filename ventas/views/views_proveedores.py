# ================================================================
# =                                                              =
# =           VISTAS PARA GESTIÓN DE PROVEEDORES                =
# =                                                              =
# ================================================================
#
# Este archivo contiene las vistas para gestionar proveedores y
# facturas de proveedores en el sistema.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.http import JsonResponse
from ventas.models.proveedores import Proveedor, FacturaProveedor, DetalleFacturaProveedor
from ventas.models.productos import Productos
from ventas.decorators import require_seccion
import logging

logger = logging.getLogger('ventas')


# ================================================================
# =                    VISTAS DE PROVEEDORES                     =
# ================================================================

@login_required
@require_seccion('proveedores')
def proveedores_list_view(request):
    """
    Vista para listar todos los proveedores.
    
    Permite:
    - Ver todos los proveedores activos
    - Buscar proveedores por nombre, RUT, contacto
    - Filtrar por estado
    """
    # Obtener parámetros de búsqueda
    q = request.GET.get('q', '').strip()
    estado_filter = request.GET.get('estado', '')
    
    # Obtener proveedores (solo no eliminados)
    proveedores = Proveedor.objects.filter(eliminado__isnull=True)
    
    # Aplicar filtros
    if q:
        proveedores = proveedores.filter(
            Q(nombre__icontains=q) |
            Q(rut__icontains=q) |
            Q(contacto__icontains=q) |
            Q(email__icontains=q)
        )
    
    if estado_filter:
        proveedores = proveedores.filter(estado=estado_filter)
    
    # Ordenar por nombre
    proveedores = proveedores.order_by('nombre')
    
    # Agregar información adicional (total facturas, facturas pendientes)
    for proveedor in proveedores:
        proveedor.total_facturas = proveedor.facturas.filter(eliminado__isnull=True).count()
        proveedor.facturas_pendientes = proveedor.facturas.filter(
            eliminado__isnull=True,
            estado_pago='pendiente'
        ).count()
        proveedor.total_pendiente = proveedor.obtener_total_pendiente()
    
    contexto = {
        'proveedores': proveedores,
        'q': q,
        'estado_filter': estado_filter,
    }
    
    return render(request, 'proveedores_list.html', contexto)


@login_required
@require_seccion('proveedores')
def proveedor_crear_view(request):
    """
    Vista para crear un nuevo proveedor.
    """
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombre = request.POST.get('nombre', '').strip()
            rut = request.POST.get('rut', '').strip() or None
            contacto = request.POST.get('contacto', '').strip() or None
            telefono = request.POST.get('telefono', '').strip() or None
            email = request.POST.get('email', '').strip() or None
            direccion = request.POST.get('direccion', '').strip() or None
            ciudad = request.POST.get('ciudad', '').strip() or None
            region = request.POST.get('region', '').strip() or None
            estado = request.POST.get('estado', 'activo')
            notas = request.POST.get('notas', '').strip() or None
            
            # Validaciones básicas
            if not nombre:
                messages.error(request, 'El nombre del proveedor es obligatorio.')
                return render(request, 'proveedor_form.html', {
                    'modo': 'crear',
                    'proveedor': None
                })
            
            # Verificar si el RUT ya existe
            if rut:
                if Proveedor.objects.filter(rut=rut, eliminado__isnull=True).exists():
                    messages.error(request, 'Ya existe un proveedor con ese RUT.')
                    return render(request, 'proveedor_form.html', {
                        'modo': 'crear',
                        'proveedor': None
                    })
            
            # Crear el proveedor
            proveedor = Proveedor.objects.create(
                nombre=nombre,
                rut=rut,
                contacto=contacto,
                telefono=telefono,
                email=email,
                direccion=direccion,
                ciudad=ciudad,
                region=region,
                estado=estado,
                notas=notas
            )
            
            messages.success(request, f'Proveedor "{proveedor.nombre}" creado exitosamente.')
            logger.info(f'Proveedor creado: {proveedor.id} - {proveedor.nombre}')
            return redirect('proveedores_list')
            
        except Exception as e:
            logger.error(f'Error al crear proveedor: {str(e)}', exc_info=True)
            messages.error(request, f'Error al crear el proveedor: {str(e)}')
            return render(request, 'proveedor_form.html', {
                'modo': 'crear',
                'proveedor': None
            })
    
    # GET: Mostrar formulario vacío
    return render(request, 'proveedor_form.html', {
        'modo': 'crear',
        'proveedor': None
    })


@login_required
@require_seccion('proveedores')
def proveedor_editar_view(request, proveedor_id):
    """
    Vista para editar un proveedor existente.
    """
    proveedor = get_object_or_404(Proveedor, pk=proveedor_id, eliminado__isnull=True)
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            proveedor.nombre = request.POST.get('nombre', '').strip()
            rut = request.POST.get('rut', '').strip() or None
            proveedor.contacto = request.POST.get('contacto', '').strip() or None
            proveedor.telefono = request.POST.get('telefono', '').strip() or None
            proveedor.email = request.POST.get('email', '').strip() or None
            proveedor.direccion = request.POST.get('direccion', '').strip() or None
            proveedor.ciudad = request.POST.get('ciudad', '').strip() or None
            proveedor.region = request.POST.get('region', '').strip() or None
            proveedor.estado = request.POST.get('estado', 'activo')
            proveedor.notas = request.POST.get('notas', '').strip() or None
            
            # Validaciones básicas
            if not proveedor.nombre:
                messages.error(request, 'El nombre del proveedor es obligatorio.')
                return render(request, 'proveedor_form.html', {
                    'modo': 'editar',
                    'proveedor': proveedor
                })
            
            # Verificar si el RUT ya existe (en otro proveedor)
            if rut and rut != proveedor.rut:
                if Proveedor.objects.filter(rut=rut, eliminado__isnull=True).exclude(pk=proveedor_id).exists():
                    messages.error(request, 'Ya existe otro proveedor con ese RUT.')
                    return render(request, 'proveedor_form.html', {
                        'modo': 'editar',
                        'proveedor': proveedor
                    })
            
            proveedor.rut = rut
            proveedor.save()
            
            messages.success(request, f'Proveedor "{proveedor.nombre}" actualizado exitosamente.')
            logger.info(f'Proveedor actualizado: {proveedor.id} - {proveedor.nombre}')
            return redirect('proveedores_list')
            
        except Exception as e:
            logger.error(f'Error al actualizar proveedor: {str(e)}', exc_info=True)
            messages.error(request, f'Error al actualizar el proveedor: {str(e)}')
            return render(request, 'proveedor_form.html', {
                'modo': 'editar',
                'proveedor': proveedor
            })
    
    # GET: Mostrar formulario con datos del proveedor
    return render(request, 'proveedor_form.html', {
        'modo': 'editar',
        'proveedor': proveedor
    })


@login_required
@require_seccion('proveedores')
def proveedor_eliminar_view(request, proveedor_id):
    """
    Vista para eliminar (borrado lógico) un proveedor.
    """
    proveedor = get_object_or_404(Proveedor, pk=proveedor_id, eliminado__isnull=True)
    
    if request.method == 'POST':
        try:
            from django.utils import timezone
            proveedor.eliminado = timezone.now()
            proveedor.save()
            
            messages.success(request, f'Proveedor "{proveedor.nombre}" eliminado exitosamente.')
            logger.info(f'Proveedor eliminado: {proveedor.id} - {proveedor.nombre}')
            return redirect('proveedores_list')
            
        except Exception as e:
            logger.error(f'Error al eliminar proveedor: {str(e)}', exc_info=True)
            messages.error(request, f'Error al eliminar el proveedor: {str(e)}')
            return redirect('proveedores_list')
    
    # GET: Mostrar confirmación
    # Verificar si tiene facturas
    tiene_facturas = proveedor.facturas.filter(eliminado__isnull=True).exists()
    
    return render(request, 'proveedor_eliminar.html', {
        'proveedor': proveedor,
        'tiene_facturas': tiene_facturas
    })

