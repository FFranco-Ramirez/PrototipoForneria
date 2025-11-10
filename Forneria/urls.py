from django.contrib import admin
from django.urls import path
from ventas.views import home, login_view, register_view, dashboard_view, agregar_producto_view
from ventas.views import proximamente_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('registro/', register_view, name='registro'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('productos/agregar/', agregar_producto_view, name='agregar_producto'),
    path("proximamente/", proximamente_view, name="proximamente"),
    path("proximamente/<slug:feature>/", proximamente_view, name="proximamente_feature"),
]
