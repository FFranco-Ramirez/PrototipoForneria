# ================================================================
# =                                                              =
# =        SISTEMA DE PERMISOS POR ROLES                        =
# =                                                              =
# ================================================================
#
# Este archivo centraliza la lógica de permisos basada en roles.
# Define qué secciones puede acceder cada rol y qué permisos tiene.

from ventas.models.usuarios import Usuarios
from django.contrib.auth.models import Group

# Mapeo de roles a secciones permitidas
# Basado en la matriz de permisos 4.2 del documento de requisitos
PERMISOS_POR_ROL = {
    'Administrador': [
        # Acceso completo a todas las secciones
        'dashboard', 'pos', 'inventario', 'movimientos', 'merma', 'alertas',
        'reportes', 'proveedores', 'facturas_proveedores', 'pagos_proveedores',
        'produccion', 'usuarios', 'ajustes_stock', 'historial_boletas',
    ],
    'Contador': [
        # Según matriz: Dashboard, Consultar ventas, Consultar stock, 
        # Reporte de ventas, Reporte de inventario, Top productos, Exportar datos,
        # Consultar cliente, Historial de compras
        'dashboard', 
        'inventario',  # Consultar stock (solo lectura)
        'reportes',  # Reporte de ventas, Reporte de inventario, Top productos, Exportar datos
        'historial_boletas',  # Consultar ventas, Historial de compras
        # NOTA: No tiene acceso a movimientos (kardex), merma, alertas según matriz
    ],
    'Vendedor': [
        # Según matriz: Dashboard, Venta presencial/delivery, Aplicar descuentos,
        # Calcular totales, Emitir comprobante, Registrar pago, Consultar ventas,
        # Consultar stock, Gestionar alertas, Registrar cliente, Consultar cliente,
        # Historial de compras, Descuentos fidelidad
        'dashboard',
        'pos',  # Venta presencial/delivery, aplicar descuentos, calcular totales, 
                # emitir comprobante, registrar pago, registrar cliente
        'inventario',  # Consultar stock (solo lectura)
        'alertas',  # Gestionar alertas (según matriz tiene acceso completo)
        'historial_boletas',  # Consultar ventas, Consultar cliente, Historial de compras
        # NOTA: No tiene acceso a movimientos, merma, reportes según matriz
    ],
}

# Secciones que requieren permisos especiales (solo lectura para algunos roles)
SECCIONES_SOLO_LECTURA = {
    'Contador': [
        'inventario',  # Solo consultar stock, no gestionar productos
    ],
    'Vendedor': [
        'inventario',  # Solo consultar stock, no gestionar productos
        # NOTA: alertas NO es solo lectura para Vendedor según matriz (puede gestionar)
    ],
}

def obtener_rol_usuario(user):
    """
    Obtiene el rol del usuario desde la base de datos.
    
    Args:
        user: Usuario de Django (User)
        
    Returns:
        str: Nombre del rol o None si no tiene
    """
    if not user.is_authenticated:
        return None
    
    # Si es superusuario, retornar 'Administrador'
    if user.is_superuser:
        return 'Administrador'
    
    # Intentar obtener desde tabla usuarios
    try:
        usuario_perfil = Usuarios.objects.get(user=user)
        if usuario_perfil.roles:
            return usuario_perfil.roles.nombre
    except Usuarios.DoesNotExist:
        pass
    
    # Intentar obtener desde grupos de Django
    grupos = user.groups.all()
    if grupos.exists():
        return grupos.first().name
    
    return None

def puede_acceder_seccion(user, seccion):
    """
    Verifica si un usuario puede acceder a una sección específica.
    
    Args:
        user: Usuario de Django
        seccion: Nombre de la sección (ej: 'pos', 'inventario', 'reportes')
        
    Returns:
        bool: True si puede acceder, False en caso contrario
    """
    rol = obtener_rol_usuario(user)
    
    if not rol:
        return False
    
    # Administrador tiene acceso a todo
    if rol == 'Administrador':
        return True
    
    # Verificar si el rol tiene acceso a la sección
    secciones_permitidas = PERMISOS_POR_ROL.get(rol, [])
    return seccion in secciones_permitidas

def tiene_permiso_escritura(user, seccion):
    """
    Verifica si un usuario tiene permisos de escritura en una sección.
    Algunos roles solo tienen acceso de lectura.
    
    Args:
        user: Usuario de Django
        seccion: Nombre de la sección
        
    Returns:
        bool: True si tiene permisos de escritura, False si solo lectura o sin acceso
    """
    rol = obtener_rol_usuario(user)
    
    if not rol:
        return False
    
    # Administrador tiene permisos de escritura en todo
    if rol == 'Administrador':
        return True
    
    # Verificar si puede acceder a la sección
    if not puede_acceder_seccion(user, seccion):
        return False
    
    # Verificar si la sección es solo lectura para este rol
    secciones_solo_lectura = SECCIONES_SOLO_LECTURA.get(rol, [])
    return seccion not in secciones_solo_lectura

def obtener_secciones_permitidas(user):
    """
    Obtiene la lista de secciones a las que el usuario puede acceder.
    
    Args:
        user: Usuario de Django
        
    Returns:
        list: Lista de nombres de secciones permitidas
    """
    rol = obtener_rol_usuario(user)
    
    if not rol:
        return []
    
    if rol == 'Administrador':
        # Retornar todas las secciones
        todas_las_secciones = set()
        for secciones in PERMISOS_POR_ROL.values():
            todas_las_secciones.update(secciones)
        return list(todas_las_secciones)
    
    return PERMISOS_POR_ROL.get(rol, [])

