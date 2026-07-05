from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

# Paleta de colores profesionales unificada
C_PRIMARY = colors.HexColor("#0F2042")    # Slate Blue / Azul Marino Profundo
C_SECONDARY = colors.HexColor("#2A6F97")  # Teal Blue / Azul Medio
C_TEXT = colors.HexColor("#2B2D42")       # Charcoal / Texto Oscuro
C_TEXT_LIGHT = colors.HexColor("#5C677D") # Steel / Texto Claro

def get_cv_styles():
    """
    Crea y retorna un diccionario de estilos de párrafo personalizados para ReportLab (SRP).
    """
    styles = getSampleStyleSheet()
    cv_styles = {}
    
    cv_styles['name'] = ParagraphStyle(
        'CV_Name',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=C_PRIMARY,
        spaceAfter=4
    )
    
    cv_styles['title'] = ParagraphStyle(
        'CV_Title',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14.5,
        textColor=C_SECONDARY,
        spaceAfter=6
    )
    
    cv_styles['contact'] = ParagraphStyle(
        'CV_Contact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=C_TEXT_LIGHT
    )
    
    cv_styles['section'] = ParagraphStyle(
        'CV_Section',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15.5,
        textColor=C_PRIMARY,
        spaceBefore=8,
        spaceAfter=3
    )
    
    cv_styles['body'] = ParagraphStyle(
        'CV_Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=C_TEXT,
        alignment=TA_JUSTIFY,
        spaceAfter=5
    )
    
    cv_styles['entry_title'] = ParagraphStyle(
        'CV_EntryTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=C_PRIMARY
    )
    
    cv_styles['entry_subtitle'] = ParagraphStyle(
        'CV_EntrySubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=12.5,
        textColor=C_SECONDARY
    )
    
    cv_styles['entry_date'] = ParagraphStyle(
        'CV_EntryDate',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12.5,
        textColor=C_TEXT_LIGHT,
        alignment=TA_RIGHT
    )
    
    cv_styles['bullet'] = ParagraphStyle(
        'CV_Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=C_TEXT,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2.5
    )
    
    # Estilos para Cartas de Presentación
    cv_styles['letter_name'] = ParagraphStyle(
        'Letter_Name',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=C_PRIMARY,
        spaceAfter=2
    )
    
    cv_styles['letter_title'] = ParagraphStyle(
        'Letter_Title',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=C_SECONDARY,
        spaceAfter=15
    )
    
    cv_styles['letter_contact'] = ParagraphStyle(
        'Letter_Contact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=C_TEXT_LIGHT,
        alignment=TA_RIGHT
    )
    
    cv_styles['letter_body'] = ParagraphStyle(
        'Letter_Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=C_TEXT,
        alignment=TA_JUSTIFY,
        spaceAfter=12
    )
    
    cv_styles['letter_salutation'] = ParagraphStyle(
        'Letter_Salutation',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=C_PRIMARY,
        spaceAfter=10
    )
    
    cv_styles['letter_date'] = ParagraphStyle(
        'Letter_Date', 
        parent=styles['Normal'], 
        fontName='Helvetica-Oblique', 
        fontSize=9, 
        spaceAfter=15
    )
    
    cv_styles['letter_footer'] = ParagraphStyle(
        'Letter_Footer', 
        parent=styles['Normal'], 
        fontName='Helvetica', 
        fontSize=9, 
        textColor=C_TEXT_LIGHT
    )

    return cv_styles
