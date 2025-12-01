# ================================================================
# =     IMPORTACIÓN DE TODAS LAS VISTAS DE LA APP VENTAS        =
# ================================================================
# 
# Este archivo centraliza todas las vistas para facilitar su importación.

# --- Vistas de Autenticación y Usuarios ---
from .views_autentication import home, login_view, register_view, dashboard_view
from .views_autentication import proximamente_view
from .views_autentication import logout_view
from .views_autentication import usuarios_list_view, usuario_editar_view, usuario_eliminar_view

# --- Vistas de Productos e Inventario ---
from .views_productos import agregar_producto_view, inventario_view, editar_producto_view, eliminar_producto_view

# --- Vistas del Sistema POS (Punto de Venta) ---
from .views_pos import pos_view, agregar_cliente_ajax, validar_producto_ajax, procesar_venta_ajax

# --- Vistas del Sistema de Alertas ---
from .views_alertas import (
    alertas_list_view,
    alerta_crear_view,
    alerta_editar_view,
    alerta_eliminar_view,
    alerta_cambiar_estado_ajax,
    generar_alertas_automaticas_view,
    generar_alerta_desde_producto
)

# --- Vistas de Movimientos de Inventario (NUEVO) ---
from .view_movimientos import movimientos_view

# --- Vistas de Gestión de Merma ---
from .view_merma import merma_list_view, mover_a_merma_ajax

# --- Vistas de Sistema de Reportes (NUEVO) ---
from .view_reportes import reportes_view

# --- Vistas de Acciones Masivas (NUEVO) ---
from .view_acciones_masivas import crear_alertas_masivo, mover_merma_masivo, eliminar_masivo