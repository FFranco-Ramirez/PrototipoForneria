# ================================================================
# =                                                              =
# =        DECORADORES DE PERMISOS POR ROL                      =
# =                                                              =
# ================================================================
#
# Este archivo implementa decoradores para controlar acceso por rol
# según RF-S1 del Jira: "Autenticación (login) y autorización por rol"
#
# REQUISITOS JIRA:
# - RF-S1: Autorización por rol
#
# ROLES DEFINIDOS:
# - Vendedor: Puede realizar ventas y ver inventario
# - Contador: Puede ver reportes y ventas
# - Administrador: Acceso completo al sistema
#
# USO:
# @require_rol('Administrador')
# def vista_admin(request):
#     ...

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from ventas.models import Usuarios


# ================================================================
# =              DECORADOR: REQUERIR ROL                        =
# ================================================================

def require_rol(*roles_permitidos):
    """
    Decorador que verifica que el usuario tenga uno de los roles permitidos.
    
    Args:
        *roles_permitidos: Roles permitidos ('Vendedor', 'Contador', 'Administrador')
        
    Ejemplo:
        @require_rol('Administrador', 'Contador')
        def vista_reporte(request):
            # Solo administradores y contadores pueden acceder
            ...
    
    Returns:
        function: Función decorada que verifica el rol
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Verificar que el usuario esté autenticado
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
                return redirect('login')
            
            # Verificar si es superusuario (acceso total)
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Obtener el rol del usuario desde la tabla usuarios
            try:
                usuario_perfil = Usuarios.objects.get(user=request.user)
                rol_usuario = usuario_perfil.roles.nombre if usuario_perfil.roles else None
            except Usuarios.DoesNotExist:
                # Si no tiene perfil, verificar grupos de Django
                grupos = request.user.groups.all()
                if grupos.exists():
                    rol_usuario = grupos.first().name
                else:
                    rol_usuario = None
            
            # Si no tiene rol, denegar acceso
            if not rol_usuario:
                messages.error(request, 'No tienes permisos para acceder a esta página.')
                return redirect('dashboard')
            
            # Verificar si el rol está permitido
            if rol_usuario in roles_permitidos:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(
                    request, 
                    f'No tienes permisos para acceder a esta página. '
                    f'Se requiere uno de estos roles: {", ".join(roles_permitidos)}'
                )
                return redirect('dashboard')
        
        return _wrapped_view
    return decorator


# ================================================================
# =        FUNCIÓN AUXILIAR: OBTENER ROL DEL USUARIO             =
# ================================================================

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


# ================================================================
# =        FUNCIÓN AUXILIAR: VERIFICAR PERMISO                   =
# ================================================================

def tiene_permiso(user, rol_requerido):
    """
    Verifica si un usuario tiene un rol específico.
    
    Args:
        user: Usuario de Django
        rol_requerido: Rol requerido ('Vendedor', 'Contador', 'Administrador')
        
    Returns:
        bool: True si tiene el permiso, False en caso contrario
    """
    rol_usuario = obtener_rol_usuario(user)
    
    if not rol_usuario:
        return False
    
    # Administrador tiene acceso a todo
    if rol_usuario == 'Administrador':
        return True
    
    return rol_usuario == rol_requerido

