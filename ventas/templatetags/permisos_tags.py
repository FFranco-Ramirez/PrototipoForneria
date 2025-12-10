# ================================================================
# =                                                              =
# =        TEMPLATE TAGS PARA PERMISOS                           =
# =                                                              =
# ================================================================
#
# Este archivo proporciona template tags y filters para verificar
# permisos directamente en los templates de Django.

from django import template
from ventas.funciones.permisos import puede_acceder_seccion, tiene_permiso_escritura, obtener_secciones_permitidas

register = template.Library()

@register.filter(name='puede_acceder_seccion')
def puede_acceder_seccion_filter(user, seccion):
    """
    Template filter para verificar si un usuario puede acceder a una sección.
    
    Uso en template:
        {% load permisos_tags %}
        {% if request.user|puede_acceder_seccion:'pos' %}
            <a href="{% url 'pos' %}">Ventas</a>
        {% endif %}
    """
    return puede_acceder_seccion(user, seccion)

@register.simple_tag
def puede_acceder_seccion_tag(user, seccion):
    """
    Template tag para verificar si un usuario puede acceder a una sección.
    
    Uso en template:
        {% load permisos_tags %}
        {% puede_acceder_seccion_tag request.user 'pos' as puede_acceder %}
        {% if puede_acceder %}
            ...
        {% endif %}
    """
    return puede_acceder_seccion(user, seccion)

@register.filter(name='tiene_permiso_escritura')
def tiene_permiso_escritura_filter(user, seccion):
    """
    Template filter para verificar si un usuario tiene permisos de escritura.
    
    Uso en template:
        {% load permisos_tags %}
        {% if request.user|tiene_permiso_escritura:'inventario' %}
            <button>Editar</button>
        {% endif %}
    """
    return tiene_permiso_escritura(user, seccion)

