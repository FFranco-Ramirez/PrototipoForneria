# ================================================================
# =                                                              =
# =        COMANDO DJANGO: VERIFICAR VENCIMIENTOS               =
# =                                                              =
# ================================================================
#
# Este comando verifica diariamente qué productos han vencido
# y los mueve automáticamente a estado de merma.
#
# CÓMO EJECUTAR:
# python manage.py verificar_vencimientos
#
# PARA AUTOMATIZAR (Windows):
# 1. Crear archivo .bat:
#    cd C:\ruta\a\tu\proyecto
#    python manage.py verificar_vencimientos
#
# 2. Programar tarea en Windows:
#    - Abrir "Programador de tareas"
#    - Crear tarea básica
#    - Ejecutar diariamente a las 00:00
#    - Acción: Iniciar programa
#    - Programa: ruta\al\archivo.bat

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from ventas.models.productos import Productos


class Command(BaseCommand):
    """
    Comando para verificar productos vencidos y moverlos a merma.
    
    Este comando se ejecuta diariamente para:
    1. Buscar productos cuya fecha de caducidad ya pasó
    2. Cambiar su estado_merma de 'activo' a 'vencido'
    3. Generar un reporte de los productos procesados
    """
    
    help = 'Verifica productos vencidos y los mueve a estado de merma'
    
    def add_arguments(self, parser):
        """
        Argumentos opcionales del comando.
        
        --dry-run: Simula la ejecución sin hacer cambios reales
        """
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simula la ejecución sin hacer cambios en la base de datos',
        )
    
    def handle(self, *args, **options):
        """
        Lógica principal del comando.
        """
        # Obtener la fecha actual
        hoy = date.today()
        
        # Indicar si es simulación
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('🔍 MODO SIMULACIÓN - No se harán cambios reales')
            )
        
        # Línea separadora
        self.stdout.write('=' * 60)
        self.stdout.write(f'📅 Verificando vencimientos para: {hoy.strftime("%d/%m/%Y")}')
        self.stdout.write('=' * 60)
        
        # Buscar productos vencidos que aún están activos
        productos_vencidos = Productos.objects.filter(
            caducidad__lt=hoy,          # Fecha de caducidad menor a hoy
            estado_merma='activo',       # Solo productos activos
            eliminado__isnull=True       # No eliminados
        )
        
        # Contar productos encontrados
        total_vencidos = productos_vencidos.count()
        
        if total_vencidos == 0:
            self.stdout.write(
                self.style.SUCCESS('✅ No hay productos vencidos. Todo está en orden.')
            )
            return
        
        # Mostrar productos encontrados
        self.stdout.write(
            self.style.WARNING(f'\n⚠️  Se encontraron {total_vencidos} productos vencidos:\n')
        )
        
        # Procesar cada producto
        productos_procesados = 0
        valor_total_merma = 0
        
        for producto in productos_vencidos:
            # Calcular días vencidos
            dias_vencido = (hoy - producto.caducidad).days
            
            # Calcular valor de la merma
            stock = producto.cantidad if producto.cantidad > 0 else (producto.stock_actual or 0)
            valor_merma = float(producto.precio) * stock
            valor_total_merma += valor_merma
            
            # Mostrar información del producto
            self.stdout.write(
                f'  📦 {producto.nombre}'
            )
            self.stdout.write(
                f'     Vencido hace: {dias_vencido} días'
            )
            self.stdout.write(
                f'     Stock: {stock} unidades'
            )
            self.stdout.write(
                f'     Valor perdido: ${valor_merma:,.0f}'
            )
            self.stdout.write('')  # Línea en blanco
            
            # Si no es simulación, hacer el cambio
            if not dry_run:
                producto.estado_merma = 'vencido'
                producto.save()
                productos_procesados += 1
        
        # Resumen final
        self.stdout.write('=' * 60)
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'🔍 SIMULACIÓN: {total_vencidos} productos serían movidos a merma'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ {productos_procesados} productos movidos a merma exitosamente'
                )
            )
        
        self.stdout.write(
            self.style.ERROR(
                f'💰 Valor total de merma: ${valor_total_merma:,.0f}'
            )
        )
        self.stdout.write('=' * 60)
        
        # Mensaje final
        if not dry_run:
            self.stdout.write(
                self.style.SUCCESS('\n✨ Proceso completado exitosamente\n')
            )
