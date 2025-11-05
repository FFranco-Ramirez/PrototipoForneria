from django.contrib import admin
from django.urls import path

# importamos vista desde el template/
from ventas import views as ventas_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ventas_views.home, name='home'),
    path('login/', ventas_views.login_view, name='login'),
    path('registro/', ventas_views.register_view, name='registro'),
    path('dashboard/', ventas_views.dashboard_view, name='dashboard'),
]
