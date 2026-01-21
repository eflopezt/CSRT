#!/usr/bin/env python
"""
Script para generar el Manual de Usuario para Responsables de Área
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors
from datetime import datetime

def generar_manual():
    """Genera el manual en PDF"""
    
    # Crear el documento
    filename = "Manual_Usuario_Responsables_Area.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4,
                           rightMargin=2*cm, leftMargin=2*cm,
                           topMargin=2*cm, bottomMargin=2*cm)
    
    # Contenedor para los elementos del PDF
    story = []
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Estilo para título principal
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Estilo para subtítulos
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    # Estilo para texto normal
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=10
    )
    
    # Estilo para notas importantes
    note_style = ParagraphStyle(
        'NoteStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#e67e22'),
        leftIndent=20,
        rightIndent=20,
        spaceAfter=10,
        borderColor=colors.HexColor('#e67e22'),
        borderWidth=1,
        borderPadding=10
    )
    
    # PORTADA
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("MANUAL DE USUARIO", title_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Sistema de Gestión de Roster", 
                          ParagraphStyle('subtitle', parent=styles['Normal'], 
                                       fontSize=18, alignment=TA_CENTER, 
                                       textColor=colors.HexColor('#7f8c8d'))))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Para Responsables de Área", 
                          ParagraphStyle('subtitle2', parent=styles['Normal'], 
                                       fontSize=14, alignment=TA_CENTER,
                                       textColor=colors.HexColor('#95a5a6'))))
    story.append(Spacer(1, 1*inch))
    
    # Información del documento
    info_data = [
        ["Versión:", "1.0"],
        ["Fecha:", datetime.now().strftime("%d/%m/%Y")],
        ["Aplicación:", "CSRT - Control de Personal"]
    ]
    
    info_table = Table(info_data, colWidths=[3*cm, 5*cm])
    info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#34495e')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(info_table)
    story.append(PageBreak())
    
    # ÍNDICE
    story.append(Paragraph("ÍNDICE", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    indice = [
        "1. Introducción",
        "2. Acceso al Sistema",
        "3. Menú Principal",
        "4. Gestión de Personal",
        "5. Roster Matricial",
        "6. Códigos del Roster",
        "7. Preguntas Frecuentes"
    ]
    
    for item in indice:
        story.append(Paragraph(f"• {item}", normal_style))
    
    story.append(PageBreak())
    
    # 1. INTRODUCCIÓN
    story.append(Paragraph("1. INTRODUCCIÓN", heading_style))
    story.append(Paragraph(
        "Bienvenido al Sistema de Gestión de Roster. Este manual le guiará en el uso de las "
        "funcionalidades principales disponibles para Responsables de Área.",
        normal_style
    ))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Objetivo del Sistema:</b>", normal_style))
    story.append(Paragraph(
        "El sistema le permite visualizar y gestionar el roster del personal a su cargo, "
        "registrando días trabajados, días libres y otros códigos de asistencia.",
        normal_style
    ))
    story.append(Spacer(1, 0.3*inch))
    
    # 2. ACCESO AL SISTEMA
    story.append(Paragraph("2. ACCESO AL SISTEMA", heading_style))
    
    story.append(Paragraph("<b>Paso 1: Ingrese a la URL del sistema</b>", normal_style))
    story.append(Paragraph(
        "Abra su navegador web (Chrome, Firefox, Edge) e ingrese la dirección web proporcionada "
        "por su administrador del sistema.",
        normal_style
    ))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>Paso 2: Ingrese sus credenciales</b>", normal_style))
    
    # Tabla de ejemplo de login
    login_data = [
        ["Campo", "Descripción"],
        ["Usuario", "Su número de DNI"],
        ["Contraseña", "Proporcionada por el administrador"]
    ]
    
    login_table = Table(login_data, colWidths=[4*cm, 10*cm])
    login_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(login_table)
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph(
        "⚠️ <b>IMPORTANTE:</b> Mantenga su contraseña segura y no la comparta con nadie.",
        note_style
    ))
    
    story.append(PageBreak())
    
    # 3. MENÚ PRINCIPAL
    story.append(Paragraph("3. MENÚ PRINCIPAL", heading_style))
    story.append(Paragraph(
        "Una vez autenticado, verá el panel principal con las siguientes opciones:",
        normal_style
    ))
    story.append(Spacer(1, 0.1*inch))
    
    menu_data = [
        ["Opción", "Descripción"],
        ["Personal", "Ver lista completa del personal a su cargo"],
        ["Roster", "Acceder al roster matricial para registrar asistencias"],
        ["Reportes", "Consultar estadísticas y días acumulados"],
    ]
    
    menu_table = Table(menu_data, colWidths=[4*cm, 10*cm])
    menu_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ecc71')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(menu_table)
    story.append(PageBreak())
    
    # 4. GESTIÓN DE PERSONAL
    story.append(Paragraph("4. GESTIÓN DE PERSONAL", heading_style))
    story.append(Paragraph(
        "En esta sección puede visualizar la información del personal asignado a su área:",
        normal_style
    ))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("• Ver datos completos (DNI, nombres, régimen de turno)", normal_style))
    story.append(Paragraph("• Consultar días libres acumulados al 31/12/2025", normal_style))
    story.append(Paragraph("• Ver días libres ganados y pendientes", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph(
        "💡 <b>Consejo:</b> Use el campo de búsqueda para encontrar rápidamente a un trabajador "
        "por DNI o nombre.",
        note_style
    ))
    
    story.append(PageBreak())
    
    # 5. ROSTER MATRICIAL
    story.append(Paragraph("5. ROSTER MATRICIAL", heading_style))
    story.append(Paragraph(
        "El Roster Matricial es la herramienta principal para registrar la asistencia diaria.",
        normal_style
    ))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Características Principales:</b>", normal_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph(
        "• <b>Vista Mensual:</b> Muestra todos los días del mes en columnas",
        normal_style
    ))
    story.append(Paragraph(
        "• <b>Personal en Filas:</b> Cada fila representa a un trabajador",
        normal_style
    ))
    story.append(Paragraph(
        "• <b>Paginación:</b> Puede elegir ver 10, 20, 50, 100 o todos los trabajadores",
        normal_style
    ))
    story.append(Paragraph(
        "• <b>Modo Compacto:</b> Botón para alternar entre vista normal y compacta",
        normal_style
    ))
    story.append(Paragraph(
        "• <b>Colores Diferenciados:</b> Cada código tiene un color específico para fácil identificación",
        normal_style
    ))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Cómo Registrar Asistencia:</b>", normal_style))
    story.append(Spacer(1, 0.1*inch))
    
    pasos_registro = [
        ["Paso", "Acción"],
        ["1", "Seleccione el mes y año que desea gestionar"],
        ["2", "Ubique la fila del trabajador"],
        ["3", "Haga clic en el día que desea registrar"],
        ["4", "Seleccione el código correspondiente de la lista desplegable"],
        ["5", "El sistema guarda automáticamente el cambio"]
    ]
    
    pasos_table = Table(pasos_registro, colWidths=[2*cm, 12*cm])
    pasos_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9b59b6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lavender),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(pasos_table)
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph(
        "✅ <b>Guardado Automático:</b> No necesita hacer clic en ningún botón guardar. "
        "El sistema registra automáticamente cada cambio.",
        note_style
    ))
    
    story.append(PageBreak())
    
    # 6. CÓDIGOS DEL ROSTER
    story.append(Paragraph("6. CÓDIGOS DEL ROSTER", heading_style))
    story.append(Paragraph(
        "Es fundamental conocer los códigos disponibles y su significado:",
        normal_style
    ))
    story.append(Spacer(1, 0.2*inch))
    
    codigos_data = [
        ["Código", "Significado", "Color", "Observación"],
        ["T", "Trabajo Presencial", "Verde", "Genera días libres según régimen"],
        ["TR", "Trabajo Remoto", "Azul celeste", "Cada 5 días TR = 2 días libres"],
        ["DL", "Día Libre", "Azul", "Día libre ganado por trabajo"],
        ["DLA", "Día Libre Acumulado", "Amarillo", "Descuenta del saldo al 31/12/25"],
        ["DOL", "Compensación Horario", "Gris", "Por horario extendido"],
        ["DM", "Descanso Médico", "Rojo", "Con certificado médico"],
        ["V", "Vacaciones", "Morado", "Vacaciones aprobadas"],
        ["F", "Feriado No Recuperable", "Amarillo fuerte", "Feriado nacional"],
        ["FC", "Feriado Compensable", "Amarillo pálido", "Se trabaja otro día"],
    ]
    
    codigos_table = Table(codigos_data, colWidths=[2*cm, 4*cm, 3*cm, 5*cm])
    codigos_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fadbd8')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(codigos_table)
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Reglas Importantes para DLA:</b>", normal_style))
    story.append(Paragraph(
        "• Solo puede usar DLA si tiene saldo disponible al 31/12/2025",
        normal_style
    ))
    story.append(Paragraph(
        "• Máximo 7 días DLA consecutivos permitidos",
        normal_style
    ))
    story.append(Paragraph(
        "• El sistema bloqueará el ingreso si no cumple estas condiciones",
        normal_style
    ))
    
    story.append(PageBreak())
    
    # 7. PREGUNTAS FRECUENTES
    story.append(Paragraph("7. PREGUNTAS FRECUENTES", heading_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>¿Puedo modificar registros de meses anteriores?</b>", normal_style))
    story.append(Paragraph(
        "Sí, puede modificar cualquier mes siempre y cuando tenga los permisos necesarios.",
        normal_style
    ))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>¿Qué pasa si me equivoco al ingresar un código?</b>", normal_style))
    story.append(Paragraph(
        "Puede cambiarlo inmediatamente seleccionando el día nuevamente y eligiendo el código correcto.",
        normal_style
    ))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>¿Cómo sé si mis cambios se guardaron?</b>", normal_style))
    story.append(Paragraph(
        "La celda mostrará un color verde brevemente indicando que se guardó exitosamente.",
        normal_style
    ))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>¿Por qué no puedo ingresar DLA para un trabajador?</b>", normal_style))
    story.append(Paragraph(
        "Puede ser porque: 1) No tiene saldo disponible al 31/12/2025, o 2) Ya tiene 7 días DLA consecutivos.",
        normal_style
    ))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>¿Puedo exportar el roster a Excel?</b>", normal_style))
    story.append(Paragraph(
        "Sí, use el botón 'Exportar' en la parte superior para descargar un archivo Excel con el roster del mes.",
        normal_style
    ))
    story.append(Spacer(1, 0.3*inch))
    
    # CONTACTO
    story.append(Paragraph(
        "⚠️ <b>SOPORTE TÉCNICO:</b> Para cualquier consulta o problema, contacte al "
        "administrador del sistema o al área de TI de su organización.",
        note_style
    ))
    
    story.append(PageBreak())
    
    # PÁGINA FINAL
    story.append(Spacer(1, 3*inch))
    story.append(Paragraph(
        "Este manual es un documento de referencia rápida. "
        "Para mayor información, consulte con el administrador del sistema.",
        ParagraphStyle('footer', parent=styles['Normal'], 
                      fontSize=10, alignment=TA_CENTER,
                      textColor=colors.grey)
    ))
    
    # Construir el PDF
    doc.build(story)
    print(f"✅ Manual generado exitosamente: {filename}")
    return filename

if __name__ == "__main__":
    generar_manual()
