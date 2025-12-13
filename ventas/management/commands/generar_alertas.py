# ================================================================
# =                                                              =
# =       COMANDO: GENERAR ALERTAS AUTOMÁTICAMENTE              =
# =                                                              =
# ================================================================
#
# Este comando personalizado de Django genera alertas automáticas
# para todos los productos según sus fechas de vencimiento.
#
# USO:
#   python manage.py generar_alertas
#
# Este comando se puede ejecutar:
# - Manualmente cuando lo necesites
# - Automáticamente con un cron job (cada día a las 6 AM, por ejemplo)
# - Al iniciar el servidor (agregando al archivo wsgi.py o apps.py)

from django.core.management.base import BaseCommand
from django.utils import timezone
from ventas.models import Alertas


class Command(BaseCommand):
    """
    Comando para generar alertas automáticas de vencimiento y stock bajo.
    
    Este comando revisa todos los productos activos y genera alertas:
    
    VENCIMIENTO:
    - Roja: 0-13 días (URGENTE)
    - Amarilla: 14-29 días (PRECAUCIÓN)
    - Verde: 30+ días (OK)
    
    STOCK BAJO:
    - Roja: cantidad <= stock_minimo (o <= 5 si no está definido)
    """
    
    # Descripción que aparece cuando ejecutas: python manage.py help generar_alertas
    help = 'Genera alertas automáticas para productos próximos a vencer'
    
    def add_arguments(self, parser):
        """
        Agregar argumentos opcionales al comando.
        
        Ejemplo de uso:
        python manage.py generar_alertas --verbose
        """
        # Argumento opcional para modo verbose (más detalles)
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Muestra información detallada sobre cada alerta generada',
        )
    
    def handle(self, *args, **options):
        """
        Método principal que se ejecuta cuando se llama al comando.
        
        Args:
            options: Diccionario con los argumentos del comando
        """
        # Obtener el modo verbose
        verbose = options.get('verbose', False)
        
        # Mensaje inicial
        self.stdout.write(
            self.style.SUCCESS('🔔 Iniciando generación de alertas...')
        )
        
        try:
            # Llamar al método estático del modelo Alertas
            resultado = Alertas.generar_alertas_automaticas()
            
            # Mostrar resumen de resultados
            self.stdout.write(
                self.style.SUCCESS(f'\n✅ Alertas generadas exitosamente:\n')
            )
            self.stdout.write(f'   🔴 Rojas (0-13 días): {resultado.get("roja", 0)}')
            self.stdout.write(f'   🟡 Amarillas (14-29 días): {resultado.get("amarilla", 0)}')
            self.stdout.write(f'   🟢 Verdes (30+ días): {resultado.get("verde", 0)}')
            self.stdout.write(f'   📦 Stock Bajo: {resultado.get("stock_bajo", 0)}')
            self.stdout.write(
                self.style.SUCCESS(f'   📊 Total: {resultado["total"]}\n')
            )
            
            # Mostrar fecha y hora de ejecución
            ahora = timezone.now().strftime('%d/%m/%Y %H:%M:%S')
            self.stdout.write(f'   🕒 Fecha: {ahora}\n')
            
            # Si está en modo verbose, mostrar alertas activas
            if verbose:
                self.stdout.write('📋 Alertas activas:\n')
                alertas_activas = Alertas.objects.filter(estado='activa').order_by('tipo_alerta')
                
                for alerta in alertas_activas:
                    color = {
                        'roja': self.style.ERROR,
                        'amarilla': self.style.WARNING,
                        'verde': self.style.SUCCESS,
                    }
                    estilo = color.get(alerta.tipo_alerta, self.style.SUCCESS)
                    
                    self.stdout.write(
                        estilo(f'   - [{alerta.tipo_alerta.upper()}] {alerta.mensaje}')
                    )
            
        except Exception as e:
            # Si hay un error, mostrarlo en rojo
            self.stdout.write(
                self.style.ERROR(f'❌ Error al generar alertas: {str(e)}')
            )
            return
        
        self.stdout.write(
            self.style.SUCCESS('\n✨ Proceso completado exitosamente\n')
        )

