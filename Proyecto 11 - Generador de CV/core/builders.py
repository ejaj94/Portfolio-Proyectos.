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
        name_str = personal.get('name') or "Enmanuel Jimenez"
        title_str = personal.get('title') or "Engenheiro de Software"
        phone_str = personal.get('phone') or ""
        email_str = personal.get('email') or ""
        address_str = personal.get('address') or ""
        github_str = personal.get('github') or ""
        linkedin_str = personal.get('linkedin') or ""

        contact_lines = []
        if phone_str: contact_lines.append(f"<b>Telemóvel:</b> {phone_str}")
        if email_str: contact_lines.append(f"<b>E-mail:</b> {email_str}")
        if address_str: contact_lines.append(f"<b>Morada:</b> {address_str}")
        if github_str: contact_lines.append(f"<b>GitHub:</b> {github_str}")
        if linkedin_str: contact_lines.append(f"<b>LinkedIn:</b> {linkedin_str}")

        contact_text = "<br/>".join(contact_lines) if contact_lines else "Contacto disponível a pedido"
        
        header_left = [
            Paragraph(name_str, styles['name']),
            Paragraph(title_str, styles['title']),
            Paragraph(contact_text, styles['contact'])
        ]
        
        photo_flowable = None
        if photo_path and os.path.exists(photo_path):
            try:
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
        profile_text = content.get_profile_text()
        if profile_text:
            story.append(Paragraph(content.get_profile_title(), styles['section']))
            story.append(HRFlowable(width="100%", thickness=0.5, color=C_SECONDARY, spaceAfter=6, spaceBefore=2))
            story.append(Paragraph(profile_text, styles['body']))
            story.append(Spacer(1, 4))
        
        # 3. EXPERIENCIA LABORAL
        experience = content.get_experience()
        if experience:
            story.append(Paragraph(content.get_experience_section_title(), styles['section']))
            story.append(HRFlowable(width="100%", thickness=0.5, color=C_SECONDARY, spaceAfter=6, spaceBefore=2))
            
            for i, exp in enumerate(experience):
                if i == 2:
                    story.append(PageBreak())
                    story.append(Paragraph(content.get_experience_section_title() + " (Cont.)", styles['section']))
                    story.append(HRFlowable(width="100%", thickness=0.5, color=C_SECONDARY, spaceAfter=6, spaceBefore=2))
                    
                title = exp.get('title') or ""
                subtitle = exp.get('subtitle') or ""
                date = exp.get('date') or ""
                bullets = exp.get('bullets') or []

                exp_header = [
                    [Paragraph(title, styles['entry_title']), Paragraph(date, styles['entry_date'])],
                    [Paragraph(subtitle, styles['entry_subtitle']), Paragraph("", styles['entry_date'])]
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
                
                for bullet in bullets:
                    if bullet and isinstance(bullet, str):
                        story.append(Paragraph(f"&bull; {bullet}", styles['bullet']))
                story.append(Spacer(1, 6))
            
        # 4. HABILIDADES TÉCNICAS
        skills = content.get_skills()
        if skills:
            story.append(Paragraph(content.get_skills_section_title(), styles['section']))
            story.append(HRFlowable(width="100%", thickness=0.5, color=C_SECONDARY, spaceAfter=6, spaceBefore=2))
            
            skills_data = []
            for item in skills:
                if isinstance(item, (tuple, list)) and len(item) >= 2:
                    group, items_str = item[0], item[1]
                else:
                    group, items_str = "", str(item)

                if group:
                    skills_data.append([
                        Paragraph(f"<b>{group}:</b>", styles['body']),
                        Paragraph(str(items_str), styles['body'])
                    ])
                else:
                    skills_data.append([
                        Paragraph(str(items_str), styles['body']),
                        ""
                    ])
                
            if skills_data:
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
        education = content.get_education()
        if education:
            story.append(Paragraph(content.get_education_section_title(), styles['section']))
            story.append(HRFlowable(width="100%", thickness=0.5, color=C_SECONDARY, spaceAfter=6, spaceBefore=2))
            
            for edu in education:
                title = edu.get('title') or ""
                subtitle = edu.get('subtitle') or ""
                date = edu.get('date') or ""
                bullets = edu.get('bullets') or []

                edu_header = [
                    [Paragraph(title, styles['entry_title']), Paragraph(date, styles['entry_date'])],
                    [Paragraph(subtitle, styles['entry_subtitle']), Paragraph("", styles['entry_date'])]
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
                
                for bullet in bullets:
                    if bullet and isinstance(bullet, str):
                        story.append(Paragraph(f"&bull; {bullet}", styles['bullet']))
                story.append(Spacer(1, 4))
                
        # 6. IDIOMAS
        languages = content.get_languages()
        if languages:
            story.append(Paragraph(content.get_languages_section_title(), styles['section']))
            story.append(HRFlowable(width="100%", thickness=0.5, color=C_SECONDARY, spaceAfter=4, spaceBefore=2))
            
            for item in languages:
                if isinstance(item, (tuple, list)) and len(item) >= 2:
                    lang, level = str(item[0]), str(item[1])
                else:
                    lang, level = str(item), "Fluente"
                story.append(Paragraph(f"&bull; <b>{lang}:</b> {level}", styles['bullet']))
                story.append(Spacer(1, 2))
        
        return story


class LetterStoryBuilder:
    @staticmethod
    def build_letter_story(content: CVContentProvider, styles: dict) -> list:
        story = []
        if not content.has_cover_letter():
            return story
        letter_data = content.get_cover_letter_content()
        personal = content.get_personal_info()
        
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
        
        story.append(Paragraph(letter_data.get('date_location', ''), styles['letter_date']))
        story.append(Paragraph(letter_data.get('salutation', ''), styles['letter_salutation']))
        for para in letter_data.get('paragraphs', []):
            story.append(Paragraph(para, styles['letter_body']))
            
        story.append(Spacer(1, 15))
        story.append(Paragraph(letter_data.get('farewell', "Atentamente,"), styles['letter_body']))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"<b>{letter_data.get('signature', '')}</b>", styles['letter_salutation']))
        story.append(Paragraph(letter_data.get('signature_title', ''), styles['letter_footer']))
        
        return story
