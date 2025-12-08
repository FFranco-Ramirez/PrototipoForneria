# ================================================================
# =                                                              =
# =        COMANDO PARA VALIDAR PRODUCTOS VENCIDOS              =
# =                                                              =
# ================================================================
#
# Este comando de Django revisa todos los productos activos del inventario
# y mueve a estado de "merma" aquellos que ya cumplieron su fecha de vencimiento.
#
# PROPÓSITO:
# - Automatizar la detección de productos vencidos
# - Mantener el inventario actualizado sin intervención manual
# - Evitar que se vendan productos vencidos
#
# CÓMO USAR:
# - Ejecutar manualmente: python manage.py validar_vencimientos
# - Programar con cron job (Linux/Mac): 0 0 * * * python manage.py validar_vencimientos
# - Programar con Task Scheduler (Windows): Crear tarea que ejecute el comando diariamente
#
# QUÉ HACE:
# 1. Obtiene la fecha actual
# 2. Busca productos activos con fecha de caducidad anterior a hoy
# 3. Cambia su estado_merma de 'activo' a 'vencido'
# 4. Muestra un resumen de cuántos productos se movieron

from django.core.management.base import BaseCommand
from django.utils import timezone
from ventas.models import Productos


# ================================================================
# =                    CLASE DEL COMANDO                         =
# ================================================================

class Command(BaseCommand):
    """
    Comando personalizado de Django para validar productos vencidos.
    
    Hereda de BaseCommand que es la clase base para todos los
    comandos personalizados de Django.
    """
    
    # --- Descripción del comando ---
    # Se muestra cuando ejecutas: python manage.py help validar_vencimientos
    help = 'Valida productos vencidos y los mueve a estado de merma'
    
    def handle(self, *args, **options):
        """
        Función principal que ejecuta la validación.
        
        Esta función se llama automáticamente cuando ejecutas el comando.
        
        Args:
            *args: Argumentos posicionales (no usados en este comando)
            **options: Opciones del comando (no usadas en este comando)
        """
        
        # ============================================================
        # PASO 1: Obtener la fecha actual
        # ============================================================
        hoy = timezone.now().date()
        
        # Mostrar mensaje informativo en la consola
        self.stdout.write(
            self.style.NOTICE(
                f'🔍 Validando productos vencidos (Fecha: {hoy.strftime("%d/%m/%Y")})'
            )
        )
        
        # ============================================================
        # PASO 2: Buscar productos vencidos
        # ============================================================
        # Criterios de búsqueda:
        # - estado_merma='activo': Solo productos que están activos
        # - caducidad__lt=hoy: Fecha de caducidad menor que hoy (lt = less than)
        # - eliminado__isnull=True: Productos no eliminados
        productos_vencidos = Productos.objects.filter(
            estado_merma='activo',
            caducidad__lt=hoy,
            eliminado__isnull=True
        )
        
        # ============================================================
        # PASO 3: Mover productos a merma
        # ============================================================
        contador = 0  # Contador de productos movidos
        
        # Recorrer cada producto vencido
        for producto in productos_vencidos:
            # Cambiar el estado a 'vencido'
            producto.estado_merma = 'vencido'
            producto.save()
            
            # Incrementar el contador
            contador += 1
            
            # Mostrar mensaje de advertencia para cada producto
            self.stdout.write(
                self.style.WARNING(
                    f'⚠️  Producto movido a merma: {producto.nombre} '
                    f'(Venció: {producto.caducidad.strftime("%d/%m/%Y")})'
                )
            )
        
        # ============================================================
        # PASO 4: Mostrar resumen final
        # ============================================================
        if contador > 0:
            # Si se movieron productos, mostrar mensaje de éxito
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✓ Se movieron {contador} producto(s) a merma'
                )
            )
        else:
            # Si no hay productos vencidos, mostrar mensaje positivo
            self.stdout.write(
                self.style.SUCCESS(
                    '\n✓ No hay productos vencidos. ¡Inventario al día!'
                )
            )
