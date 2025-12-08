from django.db import models
from django.core.validators import MinValueValidator

class Categorias(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'categorias'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

class Nutricional(models.Model):
    calorias = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    proteinas = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    grasas = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    carbohidratos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    azucares = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sodio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nutricional'
        verbose_name = 'Informacion Nutricional'
        verbose_name_plural = 'Informaciones Nutricionales'

class Productos(models.Model):
    """
    Modelo que representa un producto en el inventario de la Fornería.
    
    Este modelo maneja toda la información de productos, incluyendo:
    - Información básica (nombre, descripción, marca)
    - Precios y stock
    - Fechas de elaboración y caducidad
    - Estado de merma (para productos vencidos o deteriorados)
    """
    
    # ============================================================
    # OPCIONES DE ESTADO DE MERMA
    # ============================================================
    ESTADO_MERMA_CHOICES = [
        ('activo', 'Activo'),           # Producto en buen estado, disponible para venta
        ('vencido', 'Vencido'),         # Producto que superó su fecha de caducidad
        ('deteriorado', 'Deteriorado'), # Producto en mal estado físico
        ('dañado', 'Dañado'),           # Producto con daño en empaque o estructura
    ]
    
    # ============================================================
    # CAMPOS BÁSICOS DEL PRODUCTO
    # ============================================================
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300, blank=True, null=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    # ============================================================
    # FECHAS
    # ============================================================
    caducidad = models.DateField()
    elaboracion = models.DateField(blank=True, null=True)
    creado = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    modificado = models.DateTimeField(blank=True, null=True, auto_now=True)
    eliminado = models.DateTimeField(blank=True, null=True)
    
    # ============================================================
    # CLASIFICACIÓN Y FORMATO
    # ============================================================
    tipo = models.CharField(max_length=100, blank=True, null=True)
    formato = models.CharField(max_length=100, blank=True, null=True)
    presentacion = models.CharField(max_length=100, blank=True, null=True, help_text='Presentación del producto (Bolsa, Caja, Botella, etc.)')
    
    # ============================================================
    # STOCK Y CANTIDAD
    # ============================================================
    cantidad = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    stock_actual = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    stock_minimo = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    stock_maximo = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    
    # ============================================================
    # ESTADO DE MERMA (NUEVO)
    # ============================================================
    estado_merma = models.CharField(
        max_length=20,
        choices=ESTADO_MERMA_CHOICES,
        default='activo',
        help_text='Estado del producto: activo, vencido, deteriorado o dañado'
    )
    
    # ============================================================
    # RELACIONES
    # ============================================================
    categorias = models.ForeignKey(Categorias, on_delete=models.SET_NULL, null=True, blank=True)
    nutricional = models.ForeignKey(Nutricional, on_delete=models.SET_NULL, null=True, blank=True)
    
    # ============================================================
    # MÉTODOS AUXILIARES
    # ============================================================
    def __str__(self):
        return self.nombre
    
    def esta_vencido(self):
        """
        Verifica si el producto está vencido comparando con la fecha actual.
        
        Returns:
            bool: True si el producto está vencido, False en caso contrario
        """
        from datetime import date
        return self.caducidad < date.today()
    
    def dias_hasta_vencer(self):
        """
        Calcula cuántos días faltan para que el producto venza.
        
        Returns:
            int: Número de días (negativo si ya venció)
        """
        from datetime import date
        delta = self.caducidad - date.today()
        return delta.days
    
    def es_merma(self):
        """
        Verifica si el producto está en estado de merma.
        
        Returns:
            bool: True si el producto está en merma, False si está activo
        """
        return self.estado_merma != 'activo'
    
    def mover_a_merma(self, motivo='vencido'):
        """
        Mueve el producto a estado de merma.
        
        Args:
            motivo (str): Razón de la merma ('vencido', 'deteriorado', 'dañado')
        """
        if motivo in dict(self.ESTADO_MERMA_CHOICES):
            self.estado_merma = motivo
            self.save()
    
    def calcular_perdida(self):
        """
        Calcula la pérdida económica del producto (cantidad × precio).
        
        Returns:
            Decimal: Pérdida total del producto
        """
        return self.cantidad * self.precio
    
    # ============================================================
    # CONFIGURACIÓN DEL MODELO
    # ============================================================
    class Meta:
        managed = False
        db_table = 'productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'