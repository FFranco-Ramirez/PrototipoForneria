# ================================================================
# =                                                              =
# =        MIDDLEWARE: VERIFICACIÓN DE ROLES                    =
# =                                                              =
# ================================================================
#
# Este archivo implementa middleware para verificación de roles
# según RF-S1 del Jira: "Autenticación (login) y autorización por rol"
#
# REQUISITOS JIRA:
# - RF-S1: Middleware para verificación de roles
#
# FUNCIONALIDADES:
# - Agrega el rol del usuario al request
# - Permite acceso condicional basado en roles
# - Redirige si no tiene permisos (opcional)

from django.utils.deprecation import MiddlewareMixin
from ventas.decorators import obtener_rol_usuario


class RolMiddleware(MiddlewareMixin):
    """
    Middleware que agrega el rol del usuario al objeto request.
    
    Después de este middleware, puedes acceder a request.user_rol
    en cualquier vista.
    
    Uso en vistas:
        def mi_vista(request):
            if request.user_rol == 'Administrador':
                # Hacer algo solo para administradores
                ...
    """
    
    def process_request(self, request):
        """
        Procesa la petición y agrega el rol del usuario.
        
        Args:
            request: HttpRequest
            
        Returns:
            None (modifica request en lugar)
        """
        # Agregar rol al request
        request.user_rol = obtener_rol_usuario(request.user) if request.user.is_authenticated else None
        
        # Agregar flag de si es administrador
        request.es_administrador = (
            request.user.is_authenticated and 
            (request.user.is_superuser or request.user_rol == 'Administrador')
        )
        
        return None

