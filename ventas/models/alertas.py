# ================================================================
# =                                                              =
# =                 MODELO PARA ALERTAS DE PRODUCTOS            =
# =                                                              =
# ================================================================
#
# Este archivo define el modelo de Alertas que se conecta con la
# tabla 'alertas' de MySQL.
#
# Las alertas son notificaciones automáticas que se generan cuando
# un producto está próximo a vencer, clasificadas por colores:
# - VERDE: 30+ días hasta vencer (informativo)
# - AMARILLA: 14-29 días hasta vencer (precaución)
# - ROJA: 0-13 días hasta vencer (urgente)

from django.db import models
from django.utils import timezone
from datetime import timedelta
from .productos import Productos


# ================================================================
# =                    MODELO: ALERTAS                           =
# ================================================================

class Alertas(models.Model):
    """
    Modelo para gestionar alertas de vencimiento de productos.
    
    Cada alerta está asociada a un producto específico y tiene un
    tipo (color) que indica la urgencia según los días hasta vencer.
    """
    
    # --- Opciones para el tipo de alerta ---
    # Definimos las tres categorías de alertas según urgencia
    TIPO_CHOICES = [
        ('verde', 'Verde (30+ días)'),      # Informativo
        ('amarilla', 'Amarilla (14-29 días)'),  # Precaución
        ('roja', 'Roja (0-13 días)'),       # Urgente
    ]
    
    # --- Opciones para el estado de la alerta ---
    # Permite hacer seguimiento de qué alertas se han atendido
    ESTADO_CHOICES = [
        ('activa', 'Activa'),           # Alerta recién creada o pendiente
        ('resuelta', 'Resuelta'),       # Se tomó acción sobre el producto
        ('ignorada', 'Ignorada'),       # Se decidió no actuar
    ]
    
    # --- Campo: Tipo de alerta ---
    # El color/categoría de la alerta según días hasta vencer
    tipo_alerta = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='verde',
        verbose_name='Tipo de alerta'
    )
    
    # --- Campo: Mensaje descriptivo ---
    # Texto que describe la alerta (ej: "Pan integral vence en 5 días")
    mensaje = models.CharField(
        max_length=255,
        verbose_name='Mensaje'
    )
    
    # --- Campo: Fecha de generación ---
    # Cuándo se creó la alerta (automático)
    fecha_generada = models.DateTimeField(
        auto_now_add=True,  # Se llena automáticamente al crear
        verbose_name='Fecha generada'
    )
    
    # --- Campo: Estado ---
    # Si la alerta está activa, resuelta o ignorada
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='activa',
        verbose_name='Estado'
    )
    
    # --- Relación: Producto asociado ---
    # Cada alerta pertenece a UN producto específico
    productos = models.ForeignKey(
        Productos,
        on_delete=models.CASCADE,  # Si se borra el producto, se borran sus alertas
        related_name='alertas',    # Para hacer producto.alertas.all()
        verbose_name='Producto'
    )
    
    # ============================================================
    # =                   MÉTODOS AUXILIARES                     =
    # ============================================================
    
    def __str__(self):
        """
        Representación en texto de la alerta.
        Se usa en el admin de Django y al imprimir.
        """
        return f"[{self.get_tipo_alerta_display()}] {self.mensaje}"
    
    def get_dias_hasta_vencer(self):
        """
        Calcula cuántos días faltan para que venza el producto.
        
        Returns:
            int: Número de días hasta la fecha de caducidad
        """
        hoy = timezone.now().date()
        dias = (self.productos.caducidad - hoy).days
        return dias
    
    def get_color_badge(self):
        """
        Retorna la clase CSS de Bootstrap según el tipo de alerta.
        Útil para mostrar badges de colores en el HTML.
        
        Returns:
            str: Clase CSS de Bootstrap (danger, warning, success)
        """
        colores = {
            'roja': 'danger',      # Bootstrap rojo
            'amarilla': 'warning', # Bootstrap amarillo
            'verde': 'success',    # Bootstrap verde
        }
        return colores.get(self.tipo_alerta, 'secondary')
    
    def get_icono(self):
        """
        Retorna un icono Bootstrap según el tipo de alerta.
        
        Returns:
            str: Clase de icono Bootstrap Icons
        """
        iconos = {
            'roja': 'bi-exclamation-triangle-fill',    # Triángulo con !
            'amarilla': 'bi-exclamation-circle-fill',  # Círculo con !
            'verde': 'bi-info-circle-fill',            # Círculo con i
        }
        return iconos.get(self.tipo_alerta, 'bi-bell-fill')
    
    def marcar_como_resuelta(self):
        """
        Marca la alerta como resuelta.
        Útil cuando se toma acción sobre el producto.
        """
        self.estado = 'resuelta'
        self.save(update_fields=['estado'])
    
    def marcar_como_ignorada(self):
        """
        Marca la alerta como ignorada.
        Útil cuando se decide no actuar sobre la alerta.
        """
        self.estado = 'ignorada'
        self.save(update_fields=['estado'])
    
    # ============================================================
    # =                MÉTODO ESTÁTICO: GENERAR ALERTAS          =
    # ============================================================
    
    @staticmethod
    def generar_alertas_automaticas():
        """
        Genera alertas automáticamente para todos los productos
        según sus fechas de caducidad Y niveles de stock.
        
        Este método debe ejecutarse diariamente (puede ser con un cron job
        o un comando de Django que se ejecute al iniciar el servidor).
        
        Lógica de VENCIMIENTO:
        - Roja: 0 a 13 días hasta vencer
        - Amarilla: 14 a 29 días hasta vencer
        - Verde: 30 o más días hasta vencer
        
        Lógica de STOCK BAJO:
        - Roja: cantidad <= stock_minimo (o <= 5 si no hay stock_minimo definido)
        - Se resuelve automáticamente cuando el stock vuelve a ser normal
        
        Returns:
            dict: Diccionario con estadísticas de alertas generadas
        """
        hoy = timezone.now().date()
        
        # Contadores para las estadísticas
        alertas_creadas = {
            'roja': 0,
            'amarilla': 0,
            'verde': 0,
            'stock_bajo': 0,
            'total': 0
        }
        
        # Obtener todos los productos activos (no eliminados)
        productos = Productos.objects.filter(
            eliminado__isnull=True,
            estado_merma='activo'  # Solo productos activos (no en merma)
        )
        
        for producto in productos:
            # ============================================================
            # PARTE 1: ALERTAS DE VENCIMIENTO
            # ============================================================
            # Solo generar alertas de vencimiento si el producto tiene stock
            if producto.cantidad > 0:
                # Calcular días hasta vencer
                dias_hasta_vencer = (producto.caducidad - hoy).days
                
                # Determinar el tipo de alerta según los días
                if dias_hasta_vencer < 0:
                    # Producto ya vencido (tratamos como roja urgente)
                    tipo = 'roja'
                    mensaje = f"{producto.nombre} YA VENCIÓ hace {abs(dias_hasta_vencer)} días"
                elif dias_hasta_vencer <= 13:
                    # Alerta ROJA: 0-13 días
                    tipo = 'roja'
                    mensaje = f"{producto.nombre} vence en {dias_hasta_vencer} días - URGENTE"
                elif dias_hasta_vencer <= 29:
                    # Alerta AMARILLA: 14-29 días
                    tipo = 'amarilla'
                    mensaje = f"{producto.nombre} vence en {dias_hasta_vencer} días - PRECAUCIÓN"
                else:
                    # Alerta VERDE: 30+ días (opcional, puedes omitir estas)
                    tipo = 'verde'
                    mensaje = f"{producto.nombre} vence en {dias_hasta_vencer} días - OK"
                
                # Verificar si ya existe una alerta activa de VENCIMIENTO para este producto
                alerta_vencimiento = Alertas.objects.filter(
                    productos=producto,
                    estado='activa',
                    mensaje__contains='vence'  # Distinguir alertas de vencimiento
                ).first()
                
                if alerta_vencimiento:
                    # Si existe, actualizar el tipo y mensaje si cambió
                    if alerta_vencimiento.tipo_alerta != tipo or alerta_vencimiento.mensaje != mensaje:
                        alerta_vencimiento.tipo_alerta = tipo
                        alerta_vencimiento.mensaje = mensaje
                        alerta_vencimiento.fecha_generada = timezone.now()
                        alerta_vencimiento.save()
                        alertas_creadas[tipo] += 1
                        alertas_creadas['total'] += 1
                else:
                    # Si no existe, crear nueva alerta de vencimiento
                    Alertas.objects.create(
                        tipo_alerta=tipo,
                        mensaje=mensaje,
                        productos=producto,
                        estado='activa'
                    )
                    alertas_creadas[tipo] += 1
                    alertas_creadas['total'] += 1
            
            # ============================================================
            # PARTE 2: ALERTAS DE STOCK BAJO
            # ============================================================
            # Determinar el stock mínimo (usar el definido o 5 por defecto)
            stock_minimo = producto.stock_minimo if producto.stock_minimo is not None else 5
            
            # Verificar si el stock está bajo
            if producto.cantidad <= stock_minimo:
                # Stock bajo - generar alerta ROJA
                tipo_stock = 'roja'
                mensaje_stock = f"{producto.nombre} - STOCK BAJO: {producto.cantidad} unidades (mínimo: {stock_minimo})"
                
                # Verificar si ya existe una alerta activa de STOCK para este producto
                alerta_stock = Alertas.objects.filter(
                    productos=producto,
                    estado='activa',
                    mensaje__contains='STOCK BAJO'  # Distinguir alertas de stock
                ).first()
                
                if alerta_stock:
                    # Si existe, actualizar el mensaje si cambió
                    if alerta_stock.mensaje != mensaje_stock:
                        alerta_stock.mensaje = mensaje_stock
                        alerta_stock.fecha_generada = timezone.now()
                        alerta_stock.save()
                        alertas_creadas['stock_bajo'] += 1
                        alertas_creadas['total'] += 1
                else:
                    # Si no existe, crear nueva alerta de stock
                    Alertas.objects.create(
                        tipo_alerta=tipo_stock,
                        mensaje=mensaje_stock,
                        productos=producto,
                        estado='activa'
                    )
                    alertas_creadas['stock_bajo'] += 1
                    alertas_creadas['total'] += 1
            else:
                # Stock normal - resolver alertas de stock activas
                alertas_stock_activas = Alertas.objects.filter(
                    productos=producto,
                    estado='activa',
                    mensaje__contains='STOCK BAJO'
                )
                for alerta in alertas_stock_activas:
                    alerta.marcar_como_resuelta()
        
        return alertas_creadas
    
    # ============================================================
    # =              CONFIGURACIÓN DEL MODELO                    =
    # ============================================================
    
    class Meta:
        managed = False              # Django NO creará esta tabla (ya existe)
        db_table = 'alertas'        # Nombre de la tabla en MySQL
        verbose_name = 'Alerta'     # Singular en el admin
        verbose_name_plural = 'Alertas'  # Plural en el admin
        ordering = ['-fecha_generada']  # Ordenar por fecha (más recientes primero)
        
        # Índices para mejorar el rendimiento
        indexes = [
            models.Index(fields=['tipo_alerta']),
            models.Index(fields=['estado']),
            models.Index(fields=['fecha_generada']),
        ]

