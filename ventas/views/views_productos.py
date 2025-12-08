from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from ventas.funciones.formularios_productos import ProductoForm, NutricionalForm
from ventas.models.productos import Productos, Nutricional
from django.utils import timezone  # NUEVO

def inventario_view(request):
    q = (request.GET.get('q') or '').strip()
    qs = Productos.objects.select_related('categorias').filter(eliminado__isnull=True)
    if q:
        qs = qs.filter(
            Q(nombre__icontains=q) |
            Q(marca__icontains=q) |
            Q(tipo__icontains=q) |
            Q(formato__icontains=q) |
            Q(categorias__nombre__icontains=q)
        )

    # Deduplicar: clave por (nombre, marca)
    productos = []
    seen = set()
    for p in qs.order_by('nombre', 'marca'):
        key = (p.nombre.strip().lower(), (p.marca or '').strip().lower())
        if key in seen:
            continue
        seen.add(key)
        productos.append(p)

    return render(request, 'inventario.html', {'productos': productos, 'q': q})

def editar_producto_view(request, producto_id):
    producto = get_object_or_404(Productos, pk=producto_id)
    nutri_inst = producto.nutricional or Nutricional()

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        nutricional_form = NutricionalForm(request.POST, instance=nutri_inst)
        if form.is_valid() and nutricional_form.is_valid():
            nutri = nutricional_form.save()  # crea/actualiza nutricional
            form.instance.nutricional = nutri
            form.save()  # mantiene lógica de formato y fallback de categoría
            messages.success(request, 'Producto actualizado exitosamente.')
            return render(request, 'editar_producto.html', {
                'form': form, 'nutricional_form': nutricional_form, 'producto': producto
            })
        messages.error(request, 'Corrige los campos marcados e inténtalo de nuevo.')
    else:
        form = ProductoForm(instance=producto)
        nutricional_form = NutricionalForm(instance=nutri_inst)

    return render(request, 'editar_producto.html', {
        'form': form, 'nutricional_form': nutricional_form, 'producto': producto
    })

def eliminar_producto_view(request, producto_id):
    producto = get_object_or_404(Productos, pk=producto_id)
    if request.method == 'POST':
        producto.eliminado = timezone.now()  # borrado lógico
        producto.save(update_fields=['eliminado'])
        messages.success(request, f'Producto "{producto.nombre}" eliminado correctamente.')
        return redirect('inventario')
    return render(request, 'confirmar_eliminar.html', {'producto': producto})

def agregar_producto_view(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Producto agregado exitosamente!')
            messages.info(request, 'Puedes completar la información nutricional y la categoría desde Inventario.')
            # Mantener en la misma página para seguir agregando
            form = ProductoForm()
            return render(request, 'agregar_producto.html', {'form': form})
        else:
            messages.error(request, 'Por favor corrige los campos marcados y vuelve a intentar.')
    else:
        form = ProductoForm()
    
    return render(request, 'agregar_producto.html', {'form': form})