from django.contrib import admin
from django.urls import path
from ventas.views import home, login_view, register_view, dashboard_view, agregar_producto_view, inventario_view, editar_producto_view, eliminar_producto_view, logout_view
from ventas.views import proximamente_view
from ventas.views import usuarios_list_view, usuario_editar_view, usuario_eliminar_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('registro/', register_view, name='registro'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('productos/agregar/', agregar_producto_view, name='agregar_producto'),
    path('inventario/', inventario_view, name='inventario'),
    path('inventario/editar/<int:producto_id>/', editar_producto_view, name='editar_producto'),
    path('inventario/eliminar/<int:producto_id>/', eliminar_producto_view, name='eliminar_producto'),
    path("proximamente/", proximamente_view, name="proximamente"),
    path("proximamente/<slug:feature>/", proximamente_view, name="proximamente_feature"),
    path('usuarios/', usuarios_list_view, name='usuarios_list'),
    path('usuarios/editar/<int:user_id>/', usuario_editar_view, name='usuario_editar'),
    path('usuarios/eliminar/<int:user_id>/', usuario_eliminar_view, name='usuario_eliminar'),
]
