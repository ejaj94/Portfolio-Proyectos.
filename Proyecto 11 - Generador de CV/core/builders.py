import os
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, Image
from reportlab.lib.styles import ParagraphStyle
from core.models import CVContentProvider
from core.styles import C_PRIMARY, C_SECONDARY

class CVStoryBuilder:
    """
    Clase responsable de estructurar la secuencia de elementos (Flowables) del CV (SRP).
    """

    @staticmethod
    def build_cv_story(content: CVContentProvider, styles: dict, photo_path: str = None) -> list:
        story = []
        
        # 1. ENCABEZADO CON O SIN FOTO
        personal = content.get_personal_info()
        contact_lines = [
            f"<b>Telemóvel:</b> {personal['phone']}",
            f"<b>E-mail:</b> {personal['email']}",
            f"<b>Morada:</b> {personal['address']}",
            f"<b>GitHub:</b> {personal['github']}",
            f"<b>LinkedIn:</b> {personal['linkedin']}"
        ]
        contact_text = "<br/>".join(contact_lines)
        
        header_left = [
            Paragraph(personal['name'], styles['name']),
            Paragraph(personal['title'], styles['title']),
            Paragraph(contact_text, styles['contact'])
        ]
        
        photo_flowable = None
        if photo_path and os.path.exists(photo_path):
            try:
                # Ajustamos dimensiones proporcionales
                photo_flowable = Image(photo_path, width=80, height=96)
                photo_flowable.hAlign = 'RIGHT'
            except Exception as e:
                print(f"[WARN] No se pudo cargar la imagen de perfil: {e}")
                
        if photo_flowable:
            header_table = Table([[header_left, photo_flowable]], colWidths=[420, 100])
        else:
            header_table = Table([[header_left]], colWidths=[520])
            
        header_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 6))
        story.append(HRFlowable(width="100%", thickness=1.5, color=C_PRIMARY, spaceAfter=8, spaceBefore=4))
        
        # 2. PERFIL PROFESIONAL
        story.append(Paragraph(content.get_profile_title(), styles['section']))
        story.append(HRFlowable(width="100%", thickness=0.5, color=C_SECONDARY, spaceAfter=6, spaceBefore=2))
        story.append(Paragraph(content.get_profile_text(), styles['body']))
        story.append(Spacer(1, 4))
        
        # 3. EXPERIENCIA LABORAL
        story.append(Paragraph(content.get_experience_section_title(), styles['section']))
        story.append(HRFlowable(width="100%", thickness=0.5, color=C_SECONDARY, spaceAfter=6, spaceBefore=2))
        
        experience = content.get_experience()
        
        # Añadimos las dos primeras experiencias en la página 1
        for i, exp in enumerate(experience):
            if i == 2:
                # Salto de página para mantener estructura limpia antes de la tercera experiencia
                story.append(PageBreak())
                story.append(Paragraph(content.get_experience_section_title() + " (Cont.)", styles['section']))
                story.append(HRFlowable(width="100%", thickness=0.5, color=C_SECONDARY, spaceAfter=6, spaceBefore=2))
                
            # Tabla de cabecera de la experiencia
            exp_header = [
                [Paragraph(exp['title'], styles['entry_title']), Paragraph(exp['date'], styles['entry_date'])],
                [Paragraph(exp['subtitle'], styles['entry_subtitle']), Paragraph("", styles['entry_date'])]
            ]
            exp_table = Table(exp_header, colWidths=[400, 120])
            exp_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 1),
                ('TOPPADDING', (0,0), (-1,-1), 1),
            ]))
            story.append(exp_table)
            story.append(Spacer(1, 3))
            
            for bullet in exp['bullets']:
                story.append(Paragraph(f"&bull; {bullet}", styles['bullet']))
            story.append(Spacer(1, 6))
            
        # 4. HABILIDADES TÉCNICAS
        story.append(Paragraph(content.get_skills_section_title(), styles['section']))
        story.append(HRFlowable(width="100%", thickness=0.5, color=C_SECONDARY, spaceAfter=6, spaceBefore=2))
        
        skills_data = []
        for group, items in content.get_skills():
            skills_data.append([
                Paragraph(f"<b>{group}:</b>", styles['body']),
                Paragraph(items, styles['body'])
            ])
            
        skills_table = Table(skills_data, colWidths=[130, 390])
        skills_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(skills_table)
        story.append(Spacer(1, 6))
        
        # 5. EDUCACIÓN Y CERTIFICADOS
        story.append(Paragraph(content.get_education_section_title(), styles['section']))
        story.append(HRFlowable(width="100%", thickness=0.5, color=C_SECONDARY, spaceAfter=6, spaceBefore=2))
        
        for edu in content.get_education():
            edu_header = [
                [Paragraph(edu['title'], styles['entry_title']), Paragraph(edu['date'], styles['entry_date'])],
                [Paragraph(edu['subtitle'], styles['entry_subtitle']), Paragraph("", styles['entry_date'])]
            ]
            edu_table = Table(edu_header, colWidths=[400, 120])
            edu_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 1),
                ('TOPPADDING', (0,0), (-1,-1), 1),
            ]))
            story.append(edu_table)
            story.append(Spacer(1, 3))
            
            for bullet in edu['bullets']:
                story.append(Paragraph(f"&bull; {bullet}", styles['bullet']))
            story.append(Spacer(1, 4))
            
        # Certificados
        certs = content.get_certificates()
        if certs:
            story.append(Paragraph(f"<b>{content.get_certificates_subtitle()}:</b>", styles['body']))
            for cert in certs:
                story.append(Paragraph(f"&bull; {cert}", styles['bullet']))
            story.append(Spacer(1, 6))
            
        # 6. IDIOMAS
        story.append(Paragraph(content.get_languages_section_title(), styles['section']))
        story.append(HRFlowable(width="100%", thickness=0.5, color=C_SECONDARY, spaceAfter=4, spaceBefore=2))
        
        lang_data = []
        for lang, level in content.get_languages():
            lang_data.append(Paragraph(f"&bull; <b>{lang}:</b> {level}", styles['body']))
            
        # Tabla de 1 fila y 3 columnas para los idiomas
        if len(lang_data) >= 3:
            lang_table = Table([lang_data[:3]], colWidths=[120, 220, 180])
        else:
            lang_table = Table([lang_data], colWidths=[150] * len(lang_data))
            
        lang_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(lang_table)
        
        return story


class LetterStoryBuilder:
    """
    Clase responsable de estructurar el contenido de la Carta de Presentación (SRP).
    """

    @staticmethod
    def build_letter_story(content: CVContentProvider, styles: dict) -> list:
        story = []
        
        if not content.has_cover_letter():
            return story
            
        letter_data = content.get_cover_letter_content()
        personal = content.get_personal_info()
        
        # Encabezado
        contact_info = f"{personal['address']}<br/>+351 911 151 993<br/>{personal['email']}"
        header_table = Table([
            [Paragraph(f"<b>{personal['name']}</b>", styles['letter_name']), Paragraph(contact_info, styles['letter_contact'])]
        ], colWidths=[240, 240])
        
        header_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(header_table)
        story.append(Paragraph(personal['title'], styles['letter_title']))
        story.append(HRFlowable(width="100%", thickness=1, color=C_PRIMARY, spaceAfter=20, spaceBefore=0))
        
        # Fecha
        story.append(Paragraph(letter_data['date_location'], styles['letter_date']))
        
        # Destinatario y cuerpo
        story.append(Paragraph(letter_data['salutation'], styles['letter_salutation']))
        for para in letter_data['paragraphs']:
            story.append(Paragraph(para, styles['letter_body']))
            
        # Cierre y Firma
        story.append(Spacer(1, 15))
        story.append(Paragraph(letter_data.get('farewell', "Atentamente,"), styles['letter_body']))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"<b>{letter_data['signature']}</b>", styles['letter_salutation']))
        story.append(Paragraph(letter_data['signature_title'], styles['letter_footer']))
        
        return story
