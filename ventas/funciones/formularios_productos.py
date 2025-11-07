from django import forms
from ventas.models.productos import Productos, Categorias

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields = [
            'nombre', 'descripcion', 'marca', 'precio', 'caducidad', 
            'elaboracion', 'tipo', 'stock_actual', 'stock_minimo', 
            'stock_maximo', 'presentacion', 'formato', 'categorias'
        ]
        widgets = {
            'caducidad': forms.DateInput(attrs={'type': 'date'}),
            'elaboracion': forms.DateInput(attrs={'type': 'date'}),
        }