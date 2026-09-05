import os
import sqlite3
import json
import threading
from io import BytesIO
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, Response, redirect, url_for, send_file
from database import DB_PATH, init_db

# ReportLab PDF imports
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

app = Flask(__name__)
app.secret_key = 'presupuesto_pro_saas_ejajtech_key'

# Custom Jinja Filter for Currency & Escaping
@app.template_filter('currency')
def currency_filter(value):
    try:
        val = float(value)
        return f"€ {val:,.2f}".replace(',', ' ').replace('.', ',').replace(' ', '.')
    except Exception:
        return f"€ {value}"

@app.template_filter('escapejs')
def escapejs_filter(val):
    if not val:
        return ""
    return json.dumps(str(val))[1:-1]

# Ensure DB exists
if not os.path.exists(DB_PATH):
    init_db()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    quotes = [dict(r) for r in conn.execute('''
        SELECT q.*, c.name as client_name, c.company as client_company
        FROM quotes q
        JOIN clients c ON q.client_id = c.id
        ORDER BY q.id DESC
    ''').fetchall()]
    
    total_val = conn.execute('SELECT SUM(total) FROM quotes').fetchone()[0] or 0.0
    approved_val = conn.execute("SELECT SUM(total) FROM quotes WHERE status = 'Aprovado'").fetchone()[0] or 0.0
    pending_count = conn.execute("SELECT COUNT(*) FROM quotes WHERE status = 'Pendente'").fetchone()[0] or 0
    total_count = len(quotes)
    
    conn.close()
    return render_template('index.html', quotes=quotes, total_val=total_val, approved_val=approved_val, pending_count=pending_count, total_count=total_count)

@app.route('/quotes/new', methods=['GET', 'POST'])
def new_quote():
    conn = get_db_connection()
    if request.method == 'POST':
        data = request.json or {}
        client_id = data.get('client_id')
        issue_date = data.get('issue_date', datetime.now().strftime('%Y-%m-%d'))
        valid_until = data.get('valid_until', (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'))
        tax_rate = float(data.get('tax_rate', 23.0))
        notes = data.get('notes', 'Condições de pagamento: 50% na aprovação e 50% após entrega final.')
        items = data.get('items', [])
        
        # Calculate totals
        subtotal = 0.0
        for item in items:
            qty = float(item.get('quantity', 1))
            price = float(item.get('unit_price', 0))
            subtotal += qty * price
            
        tax_amount = round(subtotal * (tax_rate / 100.0), 2)
        total = round(subtotal + tax_amount, 2)
        
        # Generate quote number
        last_id = conn.execute('SELECT MAX(id) FROM quotes').fetchone()[0] or 0
        quote_number = f"ORC-2026-{(last_id + 1):03d}"
        
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO quotes (quote_number, client_id, issue_date, valid_until, subtotal, tax_rate, tax_amount, total, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (quote_number, client_id, issue_date, valid_until, subtotal, tax_rate, tax_amount, total, 'Pendente', notes))
        
        quote_id = cursor.lastrowid
        
        for item in items:
            qty = float(item.get('quantity', 1))
            price = float(item.get('unit_price', 0))
            total_price = round(qty * price, 2)
            cursor.execute('''
                INSERT INTO quote_items (quote_id, description, quantity, unit_price, total_price)
                VALUES (?, ?, ?, ?, ?)
            ''', (quote_id, item.get('description', ''), qty, price, total_price))
            
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'quote_id': quote_id, 'quote_number': quote_number})
        
    clients = [dict(r) for r in conn.execute('SELECT * FROM clients ORDER BY name ASC').fetchall()]
    conn.close()
    return render_template('new_quote.html', clients=clients)

@app.route('/quotes/<int:quote_id>')
def quote_detail(quote_id):
    conn = get_db_connection()
    quote_row = conn.execute('''
        SELECT q.*, c.name as client_name, c.company as client_company, c.nif as client_nif, c.email as client_email, c.phone as client_phone, c.address as client_address
        FROM quotes q
        JOIN clients c ON q.client_id = c.id
        WHERE q.id = ?
    ''', (quote_id,)).fetchone()
    
    if not quote_row:
        conn.close()
        return "Orçamento não encontrado", 404
        
    quote = dict(quote_row)
    items = [dict(r) for r in conn.execute('SELECT * FROM quote_items WHERE quote_id = ?', (quote_id,)).fetchall()]
    conn.close()
    return render_template('quote_detail.html', quote=quote, items=items)

@app.route('/quotes/<int:quote_id>/pdf')
def generate_pdf(quote_id):
    conn = get_db_connection()
    quote_row = conn.execute('''
        SELECT q.*, c.name as client_name, c.company as client_company, c.nif as client_nif, c.email as client_email, c.phone as client_phone, c.address as client_address
        FROM quotes q
        JOIN clients c ON q.client_id = c.id
        WHERE q.id = ?
    ''', (quote_id,)).fetchone()
    
    if not quote_row:
        conn.close()
        return "Orçamento não encontrado", 404
        
    quote = dict(quote_row)
    items = [dict(r) for r in conn.execute('SELECT * FROM quote_items WHERE quote_id = ?', (quote_id,)).fetchall()]
    conn.close()
    
    # ReportLab PDF Generation
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Custom Palette
    COLOR_PRIMARY = colors.HexColor('#0F1117')    # Executive Dark Onyx
    COLOR_ACCENT = colors.HexColor('#1E293B')     # Charcoal Slate
    COLOR_TEXT = colors.HexColor('#334155')       # Slate Dark Text
    COLOR_MUTED = colors.HexColor('#64748B')      # Slate Gray
    COLOR_LIGHT_BG = colors.HexColor('#F8FAFC')   # Off-white table header
    COLOR_BORDER = colors.HexColor('#E2E8F0')     # Border Slate
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=COLOR_PRIMARY
    )
    
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=COLOR_MUTED
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=COLOR_TEXT
    )
    
    bold_style = ParagraphStyle(
        'DocBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=COLOR_PRIMARY
    )

    # 1. Header Table (Company Info Left, Quote Details Right)
    company_info = """
    <b>EJAJ TECH — Engenharia de Software SaaS</b><br/>
    NIF: PT509988776<br/>
    Email: contacto@ejajtech.com | Tel: +351 911 151 993<br/>
    Web: www.ejajtech.com | Instagram: @ejajtech
    """
    
    quote_info = f"""
    <font size="14" color="#0F1117"><b>PROPOSTA COMERCIAL</b></font><br/><br/>
    <b>Número:</b> {quote['quote_number']}<br/>
    <b>Data Emissão:</b> {quote['issue_date']}<br/>
    <b>Válido Até:</b> {quote['valid_until']}<br/>
    <b>Estado:</b> {quote['status']}
    """
    
    header_data = [
        [Paragraph(company_info, body_style), Paragraph(quote_info, body_style)]
    ]
    
    header_table = Table(header_data, colWidths=[3.5*inch, 3.7*inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (1,0), (1,0), 'RIGHT')
    ]))
    story.append(header_table)
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BORDER, spaceBefore=5, spaceAfter=15))
    
    # 2. Client Info Card Table
    client_html = f"""
    <b>DADOS DO CLIENTE</b><br/>
    <b>Empresa / Cliente:</b> {quote['client_company']} ({quote['client_name']})<br/>
    <b>NIF:</b> {quote['client_nif']}<br/>
    <b>Email:</b> {quote['client_email']} | <b>Telefone:</b> {quote['client_phone']}<br/>
    <b>Morada:</b> {quote['client_address']}
    """
    
    client_table = Table([[Paragraph(client_html, body_style)]], colWidths=[7.2*inch])
    client_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), COLOR_LIGHT_BG),
        ('BOX', (0,0), (0,0), 1, COLOR_BORDER),
        ('PADDING', (0,0), (0,0), 10),
    ]))
    story.append(client_table)
    story.append(Spacer(1, 20))
    
    # 3. Items Table
    table_data = [
        [
            Paragraph("<b>Descrição do Serviço / Requisito</b>", bold_style),
            Paragraph("<b>Qtd</b>", bold_style),
            Paragraph("<b>Preço Unit.</b>", bold_style),
            Paragraph("<b>Total Liquid.</b>", bold_style)
        ]
    ]
    
    for item in items:
        table_data.append([
            Paragraph(item['description'], body_style),
            Paragraph(f"{item['quantity']:.0f}", body_style),
            Paragraph(f"€ {item['unit_price']:,.2f}".replace('.', ','), body_style),
            Paragraph(f"€ {item['total_price']:,.2f}".replace('.', ','), body_style)
        ])
        
    items_table = Table(table_data, colWidths=[4.1*inch, 0.7*inch, 1.2*inch, 1.2*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_ACCENT),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('TOPPADDING', (0,0), (-1,0), 8),
        ('ALIGN', (1,0), (-1,-1), 'RIGHT'),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    # Override header font color
    for i in range(4):
        table_data[0][i].style.textColor = colors.white
        
    story.append(items_table)
    story.append(Spacer(1, 15))
    
    # 4. Totals Summary
    subtotal_str = f"€ {quote['subtotal']:,.2f}".replace('.', ',')
    tax_str = f"€ {quote['tax_amount']:,.2f}".replace('.', ',')
    total_str = f"€ {quote['total']:,.2f}".replace('.', ',')
    
    totals_data = [
        [Paragraph("<b>Subtotal Líquido:</b>", body_style), Paragraph(subtotal_str, body_style)],
        [Paragraph(f"<b>IVA ({quote['tax_rate']:.0f}%):</b>", body_style), Paragraph(tax_str, body_style)],
        [Paragraph("<font size='11'><b>VALOR TOTAL:</b></font>", bold_style), Paragraph(f"<font size='11'><b>{total_str}</b></font>", bold_style)]
    ]
    
    totals_table = Table(totals_data, colWidths=[2.2*inch, 1.5*inch])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LINEBELOW', (0,-1), (-1,-1), 1.5, COLOR_PRIMARY)
    ]))
    
    summary_wrapper = Table([[Paragraph("", body_style), totals_table]], colWidths=[3.5*inch, 3.7*inch])
    summary_wrapper.setStyle(TableStyle([('ALIGN', (1,0), (1,0), 'RIGHT')]))
    story.append(summary_wrapper)
    story.append(Spacer(1, 20))
    
    # 5. Terms & Signature
    notes_html = f"""
    <b>TERMOS E CONDIÇÕES DE PAGAMENTO</b><br/>
    {quote['notes']}<br/>
    <i>Esta proposta comercial tem validade de 30 dias após a data de emissão. Os preços apresentados incluem IVA à taxa legal em vigor.</i>
    """
    story.append(Paragraph(notes_html, body_style))
    story.append(Spacer(1, 30))
    
    sig_html = """
    ___________________________________________________<br/>
    <b>Enmanuel Jimenez</b> — Founder & Lead Architect<br/>
    <b>EJAJ TECH — Software Engineering Studio</b>
    """
    story.append(Paragraph(sig_html, body_style))
    
    doc.build(story)
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{quote['quote_number']}_EJAJTECH.pdf",
        mimetype='application/pdf'
    )

@app.route('/api/quotes/status', methods=['POST'])
def update_status():
    data = request.json or {}
    quote_id = data.get('id')
    status = data.get('status')
    
    if not quote_id or not status:
        return jsonify({'success': False, 'message': 'Dados em falta'}), 400
        
    conn = get_db_connection()
    conn.execute('UPDATE quotes SET status = ? WHERE id = ?', (status, quote_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': f'Estado do orçamento atualizado para {status}!'})

@app.route('/api/quotes/send_email', methods=['POST'])
def send_email_quote():
    data = request.json or {}
    quote_id = data.get('id')
    email_to = data.get('email')
    
    # Async simulation of SMTP quote dispatch
    def async_send():
        import time
        time.sleep(1) # Simulates SMTP handshake
        print(f"[SMTP EMAIL] Orçamento #{quote_id} enviado com sucesso para {email_to} com anexo PDF.")
        
    threading.Thread(target=async_send).start()
    return jsonify({'success': True, 'message': f'Orçamento enviado por e-mail com sucesso para {email_to}!'})

@app.route('/clients', methods=['GET', 'POST'])
def clients():
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form.get('name')
        company = request.form.get('company')
        nif = request.form.get('nif')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clients (name, company, nif, email, phone, address)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, company, nif, email, phone, address))
        conn.commit()
        conn.close()
        return redirect(url_for('clients'))
        
    clients_list = [dict(r) for r in conn.execute('''
        SELECT c.*, COUNT(q.id) as total_quotes, COALESCE(SUM(q.total), 0.0) as total_spent
        FROM clients c
        LEFT JOIN quotes q ON c.id = q.client_id
        GROUP BY c.id
        ORDER BY c.name ASC
    ''').fetchall()]
    conn.close()
    return render_template('clients.html', clients=clients_list)

if __name__ == '__main__':
    print("[SERVER] PRESUPUESTO PRO SaaS a iniciar na porta 6400...")
    app.run(host='0.0.0.0', port=6400, debug=False)
