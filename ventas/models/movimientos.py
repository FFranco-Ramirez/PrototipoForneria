# ================================================================
# =                                                              =
# =           MODELO PARA MOVIMIENTOS DE INVENTARIO             =
# =                                                              =
# ================================================================
#
# Este archivo define el modelo de MovimientosInventario que registra
# todos los cambios que ocurren en el inventario de la Fornería.
#
# PROPÓSITO:
# - Mantener un historial completo de entradas y salidas de productos
# - Permitir auditoría y seguimiento de cambios en el inventario
# - Facilitar reportes de movimientos por fecha y tipo
#
# TIPOS DE MOVIMIENTOS:
# - Entrada: Cuando se agregan productos nuevos al inventario
# - Salida: Cuando se venden productos o se reduce el stock
#
# RELACIÓN CON OTRAS TABLAS:
# - Se conecta con la tabla 'productos' mediante una ForeignKey
# - Cada movimiento está asociado a UN producto específico

from django.db import models
from .productos import Productos


# ================================================================
# =                    MODELO: MOVIMIENTOS                       =
# ================================================================

class MovimientosInventario(models.Model):
    """
    Modelo para registrar el historial de movimientos del inventario.
    
    Este modelo guarda cada cambio que ocurre en la cantidad de un producto,
    permitiendo rastrear cuándo y cómo se modificó el inventario.
    
    Ejemplo de uso:
    - Se agregan 50 panes → Movimiento tipo 'entrada', cantidad 50
    - Se venden 10 panes → Movimiento tipo 'salida', cantidad 10
    """
    
    # ============================================================
    # OPCIONES PARA EL TIPO DE MOVIMIENTO
    # ============================================================
    # Definimos las dos categorías de movimientos posibles
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),     # Se agregó stock (compra, producción)
        ('salida', 'Salida'),       # Se redujo stock (venta, merma)
    ]
    
    # ============================================================
    # CAMPOS DEL MODELO
    # ============================================================
    
    # --- Campo: Tipo de movimiento ---
    # Indica si es una entrada o salida de productos
    tipo_movimiento = models.CharField(
        max_length=20,              # Suficiente para 'entrada' o 'salida'
        choices=TIPO_CHOICES,       # Solo puede ser uno de los valores definidos arriba
        verbose_name='Tipo de movimiento'  # Nombre legible en el admin de Django
    )
    
    # --- Campo: Cantidad del movimiento ---
    # Cuántas unidades se movieron (siempre positivo)
    # Ejemplo: Si se vendieron 5 panes, cantidad = 5
    cantidad = models.IntegerField(
        verbose_name='Cantidad'
    )
    
    # --- Campo: Fecha del movimiento ---
    # Cuándo ocurrió este movimiento (se guarda automáticamente)
    fecha = models.DateTimeField(
        auto_now_add=True,          # Django lo llena automáticamente al crear el registro
        verbose_name='Fecha'
    )
    
    # ============================================================
    # CAMPOS DE TRAZABILIDAD (MEJORA)
    # ============================================================
    # Estos campos permiten rastrear el origen del movimiento
    
    origen = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text='Origen del movimiento: compra, venta, ajuste, merma, devolucion'
    )
    
    referencia_id = models.IntegerField(
        blank=True,
        null=True,
        help_text='ID de la tabla origen (factura_proveedor, ventas, etc.)'
    )
    
    tipo_referencia = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text='Tipo de referencia: factura_proveedor, venta, ajuste, merma, etc.'
    )
    
    # ============================================================
    # RELACIONES CON OTRAS TABLAS
    # ============================================================
    
    # --- Relación: Producto asociado ---
    # Cada movimiento pertenece a UN producto específico
    # ForeignKey = "Clave foránea" = conexión con la tabla de productos
    productos = models.ForeignKey(
        Productos,                  # Se conecta con el modelo Productos
        on_delete=models.CASCADE,   # Si se borra el producto, se borran sus movimientos
        related_name='movimientos', # Permite hacer producto.movimientos.all()
        verbose_name='Producto'
    )
    
    # ============================================================
    # MÉTODOS AUXILIARES
    # ============================================================
    
    def __str__(self):
        """
        Representación en texto del movimiento.
        Se usa en el admin de Django y al imprimir.
        
        Ejemplo: "entrada - Pan integral (50)"
        """
        return f"{self.tipo_movimiento} - {self.productos.nombre} ({self.cantidad})"
    
    # ============================================================
    # CONFIGURACIÓN DEL MODELO
    # ============================================================
    
    class Meta:
        managed = False                 # Django NO creará esta tabla (ya existe en MySQL)
        db_table = 'movimientos_inventario'  # Nombre de la tabla en la base de datos
        verbose_name = 'Movimiento de Inventario'  # Singular en el admin
        verbose_name_plural = 'Movimientos de Inventario'  # Plural en el admin
        ordering = ['-fecha']           # Ordenar por fecha (más recientes primero)
