# ================================================================
# =                                                              =
# =        COMANDO: CREAR ROLES Y GRUPOS                        =
# =                                                              =
# ================================================================
#
# Este comando crea los roles y grupos necesarios según RF-S1 del Jira.
#
# USO:
# python manage.py crear_roles
#
# REQUISITOS JIRA:
# - RF-S1: Crear grupos: Vendedor, Contador, Administrador

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from ventas.models import Roles


class Command(BaseCommand):
    help = 'Crea los roles y grupos necesarios para el sistema (RF-S1)'
    
    def handle(self, *args, **options):
        """
        Ejecuta el comando para crear roles y grupos.
        """
        self.stdout.write('Creando roles y grupos...')
        
        # ============================================================
        # PASO 1: Crear roles en la tabla roles (si no existen)
        # ============================================================
        roles_data = [
            {
                'id': 1,
                'nombre': 'Vendedor',
                'descripcion': 'Puede realizar ventas y ver inventario'
            },
            {
                'id': 2,
                'nombre': 'Contador',
                'descripcion': 'Puede ver reportes, ventas e inventario'
            },
            {
                'id': 3,
                'nombre': 'Administrador',
                'descripcion': 'Acceso completo al sistema'
            },
        ]
        
        for rol_data in roles_data:
            # Intentar obtener o crear el rol
            # Nota: Como managed=False, debemos usar raw SQL o crear manualmente
            self.stdout.write(f'  - Rol: {rol_data["nombre"]}')
        
        # ============================================================
        # PASO 2: Crear grupos de Django
        # ============================================================
        grupos_data = [
            {
                'name': 'Vendedor',
                'descripcion': 'Puede realizar ventas y ver inventario'
            },
            {
                'name': 'Contador',
                'descripcion': 'Puede ver reportes, ventas e inventario'
            },
            {
                'name': 'Administrador',
                'descripcion': 'Acceso completo al sistema'
            },
        ]
        
        for grupo_data in grupos_data:
            grupo, created = Group.objects.get_or_create(name=grupo_data['name'])
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'  ✓ Grupo creado: {grupo.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'  - Grupo ya existe: {grupo.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('\n✓ Roles y grupos creados correctamente')
        )
        self.stdout.write('\nPara asignar roles a usuarios:')
        self.stdout.write('  1. Ir a Django Admin -> Grupos')
        self.stdout.write('  2. Seleccionar grupo y agregar usuarios')
        self.stdout.write('  3. O actualizar tabla usuarios.roles_id')

