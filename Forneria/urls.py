# ================================================================
# =                                                              =
# =              URLS PRINCIPALES DEL PROYECTO FORNERIA          =
# =                                                              =
# ================================================================
#
# Este archivo define todas las rutas (URLs) del proyecto.
# Cada path() conecta una URL con una vista (función) que la maneja.
#
# Ejemplo:
# path('login/', login_view, name='login')
#       ↑ URL        ↑ Función    ↑ Nombre para usar en templates
#
# En los templates podemos usar: {% url 'login' %}
# En las vistas podemos usar: redirect('login')

from django.contrib import admin
from django.urls import path

# Importar todas las vistas necesarias
from ventas.views import (
    # Vistas de autenticación y navegación
    home, login_view, register_view, dashboard_view, logout_view,
    proximamente_view,
    
    # Vistas de productos e inventario
    agregar_producto_view, inventario_view, editar_producto_view, 
    eliminar_producto_view,
    
    # Vistas de gestión de usuarios (admin)
    usuarios_list_view, usuario_editar_view, usuario_eliminar_view,
    
    # Vistas del sistema POS (Punto de Venta)
    pos_view, agregar_cliente_ajax, validar_producto_ajax, procesar_venta_ajax,
    
    # Vistas del sistema de Alertas (NUEVO)
    alertas_list_view, alerta_crear_view, alerta_editar_view, alerta_eliminar_view,
    alerta_cambiar_estado_ajax, generar_alertas_automaticas_view, 
    generar_alerta_desde_producto,
)

# Vistas de APIs para el dashboard
from ventas.views.views_vencimientos import (
    productos_por_vencer_api,
    productos_por_vencer_14_dias_api,
    productos_por_vencer_30_dias_api
)
from ventas.views.view_dashboard import (
    perdida_siete_dias,
    perdida_catorce_dias,
    perdida_treinta_dias
)

# ================================================================
# =                     DEFINICIÓN DE RUTAS                      =
# ================================================================

urlpatterns = [
    # ============================================================
    # ADMINISTRACIÓN DE DJANGO
    # ============================================================
    # Panel de administración de Django (para superusuarios)
    path('admin/', admin.site.urls),
    
    # ============================================================
    # PÁGINAS PRINCIPALES Y AUTENTICACIÓN
    # ============================================================
    # Página de inicio (home) - Visible sin autenticar
    path('', home, name='home'),
    
    # Sistema de autenticación
    path('login/', login_view, name='login'),
    path('registro/', register_view, name='registro'),
    path('logout/', logout_view, name='logout'),
    
    # Dashboard principal (requiere autenticación)
    path('dashboard/', dashboard_view, name='dashboard'),
    
    # ============================================================
    # GESTIÓN DE PRODUCTOS E INVENTARIO
    # ============================================================
    # Agregar nuevo producto
    path('productos/agregar/', agregar_producto_view, name='agregar_producto'),
    
    # Ver inventario completo
    path('inventario/', inventario_view, name='inventario'),
    
    # Editar un producto existente
    path('inventario/editar/<int:producto_id>/', editar_producto_view, name='editar_producto'),
    
    # Eliminar un producto (borrado lógico)
    path('inventario/eliminar/<int:producto_id>/', eliminar_producto_view, name='eliminar_producto'),
    
    # ============================================================
    # SISTEMA DE PUNTO DE VENTA (POS) - NUEVO
    # ============================================================
    # Página principal del POS
    path('pos/', pos_view, name='pos'),
    
    # APIs del POS (llamadas AJAX desde JavaScript)
    path('api/agregar-cliente/', agregar_cliente_ajax, name='api_agregar_cliente'),
    path('api/validar-producto/<int:producto_id>/', validar_producto_ajax, name='api_validar_producto'),
    path('api/procesar-venta/', procesar_venta_ajax, name='api_procesar_venta'),
    
    # ============================================================
    # GESTIÓN DE USUARIOS (SOLO ADMINISTRADORES)
    # ============================================================
    # Listar todos los usuarios
    path('usuarios/', usuarios_list_view, name='usuarios_list'),
    
    # Editar un usuario
    path('usuarios/editar/<int:user_id>/', usuario_editar_view, name='usuario_editar'),
    
    # Eliminar un usuario
    path('usuarios/eliminar/<int:user_id>/', usuario_eliminar_view, name='usuario_eliminar'),
    
    # ============================================================
    # APIs PARA EL DASHBOARD
    # ============================================================
    # APIs de productos próximos a vencer
    path('api/proximos-vencimientos/', productos_por_vencer_api, name='api_proximos_vencimientos'),
    path('api/proximos-vencimientos-14/', productos_por_vencer_14_dias_api, name='api_proximos_vencimientos_14'),
    path('api/proximos-vencimientos-30/', productos_por_vencer_30_dias_api, name='api_proximos_vencimientos_30'),
    
    # APIs de pérdida potencial por vencimiento
    path('api/perdida-potencial/', perdida_siete_dias, name='api_perdida_potencial'),
    path('api/perdida-potencial-14/', perdida_catorce_dias, name='api_perdida_potencial_14'),
    path('api/perdida-potencial-30/', perdida_treinta_dias, name='api_perdida_potencial_30'),
    
    # ============================================================
    # SISTEMA DE ALERTAS (NUEVO)
    # ============================================================
    # Lista de alertas con filtros
    path('alertas/', alertas_list_view, name='alertas_list'),
    
    # Crear nueva alerta
    path('alertas/crear/', alerta_crear_view, name='alerta_crear'),
    
    # Editar una alerta existente
    path('alertas/editar/<int:alerta_id>/', alerta_editar_view, name='alerta_editar'),
    
    # Eliminar una alerta
    path('alertas/eliminar/<int:alerta_id>/', alerta_eliminar_view, name='alerta_eliminar'),
    
    # Crear alerta desde un producto específico (desde inventario)
    path('alertas/producto/<int:producto_id>/', generar_alerta_desde_producto, name='alerta_desde_producto'),
    
    # APIs para alertas (llamadas AJAX)
    path('api/alerta/<int:alerta_id>/cambiar-estado/', alerta_cambiar_estado_ajax, name='api_alerta_cambiar_estado'),
    path('api/generar-alertas-automaticas/', generar_alertas_automaticas_view, name='api_generar_alertas'),
    
    # ============================================================
    # PÁGINA "PRÓXIMAMENTE" (FUNCIONES EN DESARROLLO)
    # ============================================================
    # Página genérica para funcionalidades que aún no están listas
    path("proximamente/", proximamente_view, name="proximamente"),
    path("proximamente/<slug:feature>/", proximamente_view, name="proximamente_feature"),
]

# ================================================================
# NOTA: ¿Qué hace cada parte?
# ================================================================
#
# 1. path('url/', vista, name='nombre'):
#    - 'url/': Es lo que el usuario escribe en el navegador
#    - vista: La función Python que maneja esa URL
#    - name='nombre': Un identificador para usar en templates y redirects
#
# 2. <int:producto_id>: Es un parámetro dinámico
#    - Captura un número de la URL y lo pasa a la vista
#    - Ejemplo: /inventario/editar/5/ → producto_id = 5
#
# 3. <slug:feature>: Es un parámetro de texto
#    - Captura texto con guiones
#    - Ejemplo: /proximamente/reportes/ → feature = 'reportes'
