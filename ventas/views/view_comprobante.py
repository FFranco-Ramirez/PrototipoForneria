# ================================================================
# =                                                              =
# =        VISTA: GENERACIÓN DE COMPROBANTE PDF                 =
# =                                                              =
# ================================================================
#
# Este archivo implementa la generación de comprobante PDF según RF-V3 del Jira:
# "Registrar pago y vuelto; emitir comprobante"
#
# REQUISITOS JIRA:
# - RF-V3: Emitir comprobante
#
# FUNCIONALIDADES:
# - Generar comprobante en formato PDF
# - Incluir datos fiscales requeridos
# - Diseño profesional
# - Opción de impresión directa

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from ventas.models import Ventas, DetalleVenta
from decimal import Decimal

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


# ================================================================
# =        VISTA: COMPROBANTE PDF                               =
# ================================================================

@login_required
def comprobante_pdf_view(request, venta_id):
    """
    Genera un comprobante de venta en formato PDF.
    
    Cumple con RF-V3 del Jira:
    - Emitir comprobante de venta
    
    Args:
        request: HttpRequest
        venta_id: ID de la venta
        
    Returns:
        HttpResponse: Archivo PDF descargable
    """
    
    # Obtener la venta
    venta = get_object_or_404(Ventas, pk=venta_id)
    
    # Si reportlab no está disponible, retornar HTML simple
    if not REPORTLAB_AVAILABLE:
        return comprobante_html_view(request, venta_id)
    
    # ============================================================
    # PASO 1: Crear respuesta HTTP para PDF
    # ============================================================
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="comprobante_{venta.folio or venta.id}.pdf"'
    
    # ============================================================
    # PASO 2: Crear documento PDF
    # ============================================================
    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Contenedor para elementos del PDF
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # ============================================================
    # PASO 3: Encabezado del comprobante
    # ============================================================
    elements.append(Paragraph("LA FORNERÍA", title_style))
    elements.append(Paragraph("COMPROBANTE DE VENTA", styles['Heading2']))
    elements.append(Spacer(1, 0.5*cm))
    
    # ============================================================
    # PASO 4: Información de la venta
    # ============================================================
    info_data = [
        ['Folio:', venta.folio or f'VENTA-{venta.id}'],
        ['Fecha:', venta.fecha.strftime('%d/%m/%Y %H:%M')],
        ['Canal:', venta.canal_venta.capitalize()],
        ['Cliente:', venta.clientes.nombre if venta.clientes else 'Cliente Genérico'],
    ]
    
    info_table = Table(info_data, colWidths=[4*cm, 10*cm])
    info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elements.append(info_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # ============================================================
    # PASO 5: Detalles de productos
    # ============================================================
    detalles = DetalleVenta.objects.filter(ventas=venta).select_related('productos')
    
    # Encabezados de tabla
    detalles_data = [['Producto', 'Cant.', 'P. Unit.', 'Desct.', 'Subtotal']]
    
    # Agregar cada producto
    for detalle in detalles:
        subtotal = detalle.calcular_subtotal()
        detalles_data.append([
            detalle.productos.nombre[:30],  # Limitar longitud
            str(detalle.cantidad),
            f'${detalle.precio_unitario:,.0f}',
            f'{detalle.descuento_pct}%' if detalle.descuento_pct else '-',
            f'${subtotal:,.0f}',
        ])
    
    detalles_table = Table(detalles_data, colWidths=[8*cm, 2*cm, 2.5*cm, 2*cm, 3*cm])
    detalles_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    elements.append(detalles_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # ============================================================
    # PASO 6: Totales
    # ============================================================
    totales_data = [
        ['Subtotal Neto:', f'${venta.total_sin_iva:,.0f}'],
        ['IVA (19%):', f'${venta.total_iva:,.0f}'],
        ['Descuento:', f'${venta.descuento:,.0f}'],
        ['TOTAL:', f'${venta.total_con_iva:,.0f}'],
    ]
    
    totales_table = Table(totales_data, colWidths=[10*cm, 4*cm])
    totales_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica'),
        ('FONTNAME', (0, -1), (1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -2), 10),
        ('FONTSIZE', (0, -1), (1, -1), 12),
        ('TEXTCOLOR', (0, -1), (1, -1), colors.HexColor('#0066cc')),
    ]))
    
    elements.append(totales_table)
    elements.append(Spacer(1, 0.3*cm))
    
    # Información de pago
    if venta.monto_pagado:
        pago_data = [
            ['Monto Pagado:', f'${venta.monto_pagado:,.0f}'],
            ['Vuelto:', f'${venta.vuelto:,.0f}'],
        ]
        pago_table = Table(pago_data, colWidths=[10*cm, 4*cm])
        pago_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))
        elements.append(pago_table)
    
    # ============================================================
    # PASO 7: Pie de página con datos fiscales
    # ============================================================
    elements.append(Spacer(1, 1*cm))
    elements.append(Paragraph(
        "Gracias por su compra",
        ParagraphStyle('Footer', parent=styles['Normal'], alignment=TA_CENTER)
    ))
    elements.append(Spacer(1, 0.2*cm))
    elements.append(Paragraph(
        "RUT: 76.123.456-7 | Dirección: Av. Principal 123, Santiago",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, alignment=TA_CENTER)
    ))
    
    # ============================================================
    # PASO 8: Construir PDF
    # ============================================================
    doc.build(elements)
    
    return response


# ================================================================
# =        VISTA: COMPROBANTE HTML (Fallback)                   =
# ================================================================

@login_required
def comprobante_html_view(request, venta_id):
    """
    Genera un comprobante de venta en formato HTML (fallback si no hay reportlab).
    
    Args:
        request: HttpRequest
        venta_id: ID de la venta
        
    Returns:
        HttpResponse: Página HTML con el comprobante
    """
    
    venta = get_object_or_404(Ventas, pk=venta_id)
    detalles = DetalleVenta.objects.filter(ventas=venta).select_related('productos')
    
    context = {
        'venta': venta,
        'detalles': detalles,
    }
    
    return render(request, 'comprobante.html', context)

