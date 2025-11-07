from django.shortcuts import render, redirect
from django.contrib import messages
from ventas.funciones.formularios_productos import ProductoForm

def agregar_producto_view(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Producto agregado exitosamente!')
            return redirect('dashboard') # O a donde quieras redirigir
    else:
        form = ProductoForm()
    
    return render(request, 'agregar_producto.html', {'form': form})