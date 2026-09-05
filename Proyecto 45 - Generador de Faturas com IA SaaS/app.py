import os
import sqlite3
import json
import re
import random
from datetime import datetime, timedelta
from io import BytesIO
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from database import DB_PATH, init_db

# ReportLab imports for PDF generation
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

app = Flask(__name__)
app.secret_key = 'ejajtech_ai_invoice_generator_secret_key'

# Custom Filters
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
    clients = [dict(r) for r in conn.execute('SELECT * FROM clients ORDER BY name ASC').fetchall()]
    recent_invoices = [dict(r) for r in conn.execute('''
        SELECT i.*, c.name as client_name 
        FROM invoices i 
        JOIN clients c ON i.client_id = c.id 
        ORDER BY i.id DESC LIMIT 5
    ''').fetchall()]
    
    total_invoiced = conn.execute('SELECT SUM(total) FROM invoices').fetchone()[0] or 0.0
    paid_invoiced = conn.execute("SELECT SUM(total) FROM invoices WHERE status = 'Paga'").fetchone()[0] or 0.0
    pending_invoiced = conn.execute("SELECT SUM(total) FROM invoices WHERE status = 'Pendente'").fetchone()[0] or 0.0
    
    conn.close()
    return render_template('index.html', clients=clients, recent_invoices=recent_invoices, total_invoiced=total_invoiced, paid_invoiced=paid_invoiced, pending_invoiced=pending_invoiced)

@app.route('/history')
def history():
    q = request.args.get('q', '').strip()
    status_filter = request.args.get('status', '').strip()
    
    conn = get_db_connection()
    sql = '''
        SELECT i.*, c.name as client_name, c.nif as client_nif
        FROM invoices i
        JOIN clients c ON i.client_id = c.id
        WHERE 1=1
    '''
    params = []
    
    if q:
        sql += ' AND (i.invoice_number LIKE ? OR c.name LIKE ? OR c.nif LIKE ? OR i.notes LIKE ?)'
        params.extend([f'%{q}%', f'%{q}%', f'%{q}%', f'%{q}%'])
    if status_filter:
        sql += ' AND i.status = ?'
        params.append(status_filter)
        
    sql += ' ORDER BY i.id DESC'
    invoices = [dict(r) for r in conn.execute(sql, params).fetchall()]
    conn.close()
    
    return render_template('history.html', invoices=invoices, q=q, status_filter=status_filter)

@app.route('/invoice/<int:invoice_id>')
def view_invoice(invoice_id):
    conn = get_db_connection()
    invoice_row = conn.execute('''
        SELECT i.*, c.name as client_name, c.nif as client_nif, c.address as client_address, c.email as client_email, c.phone as client_phone
        FROM invoices i
        JOIN clients c ON i.client_id = c.id
        WHERE i.id = ?
    ''', (invoice_id,)).fetchone()
    
    if not invoice_row:
        conn.close()
        return "Fatura não encontrada", 404
        
    invoice = dict(invoice_row)
    items = [dict(r) for r in conn.execute('SELECT * FROM invoice_items WHERE invoice_id = ?', (invoice_id,)).fetchall()]
    conn.close()
    
    return render_template('invoice_view.html', invoice=invoice, items=items)

# API ENDPOINTS
@app.route('/api/ai/parse', methods=['POST'])
def api_ai_parse():
    data = request.json or {}
    prompt = data.get('prompt', '').strip()
    
    if not prompt:
        return jsonify({'success': False, 'message': 'Por favor introduza a descrição do trabalho para a IA processar.'}), 400
        
    # Smart AI Parsing Engine simulation
    prompt_lower = prompt.lower()
    
    # 1. Detect Client
    conn = get_db_connection()
    clients = [dict(r) for r in conn.execute('SELECT * FROM clients').fetchall()]
    selected_client = None
    
    for c in clients:
        if c['name'].lower() in prompt_lower or c['name'].split()[0].lower() in prompt_lower:
            selected_client = c
            break
            
    if not selected_client:
        selected_client = clients[0] if clients else {
            'id': 1, 'name': 'Cliente Genérico Lda', 'nif': '500123456', 
            'address': 'Av. da Liberdade 100, Lisboa', 'email': 'cliente@empresa.pt', 'phone': '+351 912 345 678'
        }
        
    # 2. Extract Line Items & Amounts
    items = []
    # Pattern matching for euro amounts e.g., "1200€ por desenvolvimento", "300 euros de hosting"
    matches = re.findall(r'(\d+[\d\s\.,]*)\s*(?:€|euros?)\s*(?:por|de|para)?\s*([^,\.\n]+)', prompt, re.IGNORECASE)
    
    if matches:
        for match in matches:
            price_str = match[0].replace(' ', '').replace(',', '.')
            try:
                price = float(price_str)
            except Exception:
                price = 100.0
            desc = match[1].strip().capitalize()
            if not desc:
                desc = "Serviços de Consultoria Técnica"
            items.append({
                'description': desc,
                'quantity': 1.0,
                'unit_price': price,
                'total_price': price
            })
    else:
        # Fallback intelligent breakdown
        sentences = [s.strip() for s in re.split(r'[,;\n\.]', prompt) if len(s.strip()) > 3]
        if sentences:
            base_price = 450.0
            for i, s in enumerate(sentences[:4]):
                items.append({
                    'description': s.capitalize(),
                    'quantity': 1.0,
                    'unit_price': round(base_price + (i * 150.0), 2),
                    'total_price': round(base_price + (i * 150.0), 2)
                })
        else:
            items = [
                {'description': 'Desenvolvimento de Aplicação Web Personalizada', 'quantity': 1.0, 'unit_price': 1200.0, 'total_price': 1200.0},
                {'description': 'Integração de Base de Dados & APIs REST', 'quantity': 1.0, 'unit_price': 450.0, 'total_price': 450.0}
            ]
            
    # Detect VAT rate
    vat_rate = 23.0
    if 'isento' in prompt_lower or '0%' in prompt_lower:
        vat_rate = 0.0
    elif '13%' in prompt_lower:
        vat_rate = 13.0
    elif '6%' in prompt_lower:
        vat_rate = 6.0
        
    subtotal = sum(item['total_price'] for item in items)
    vat_amount = round(subtotal * (vat_rate / 100.0), 2)
    total = round(subtotal + vat_amount, 2)
    
    conn.close()
    return jsonify({
        'success': True,
        'message': 'Fatura gerada com sucesso pela Inteligência Artificial!',
        'parsed_data': {
            'client': selected_client,
            'items': items,
            'subtotal': subtotal,
            'vat_rate': vat_rate,
            'vat_amount': vat_amount,
            'total': total,
            'suggested_notes': f'Fatura gerada via IA EJAJ TECH em {datetime.now().strftime("%d/%m/%Y")}.'
        }
    })

@app.route('/api/invoice/create', methods=['POST'])
def api_invoice_create():
    data = request.json or {}
    client_id = data.get('client_id')
    items = data.get('items', [])
    vat_rate = float(data.get('vat_rate', 23.0))
    notes = data.get('notes', 'Obrigado pela preferência nos nossos serviços.')
    due_days = int(data.get('due_days', 15))
    
    if not client_id or not items:
        return jsonify({'success': False, 'message': 'Cliente e pelo menos 1 item são obrigatórios.'}), 400
        
    subtotal = sum(float(it.get('quantity', 1)) * float(it.get('unit_price', 0)) for it in items)
    vat_amount = round(subtotal * (vat_rate / 100.0), 2)
    total = round(subtotal + vat_amount, 2)
    
    issue_date = datetime.now().strftime('%Y-%m-%d')
    due_date = (datetime.now() + timedelta(days=due_days)).strftime('%Y-%m-%d')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Generate sequential invoice number
    count = cursor.execute('SELECT COUNT(*) FROM invoices').fetchone()[0] + 1
    invoice_number = f"FT 2026/{count:03d}"
    
    cursor.execute('''
        INSERT INTO invoices (invoice_number, client_id, issue_date, due_date, subtotal, vat_rate, vat_amount, total, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (invoice_number, client_id, issue_date, due_date, subtotal, vat_rate, vat_amount, total, 'Pendente', notes))
    
    invoice_id = cursor.lastrowid
    
    for it in items:
        qty = float(it.get('quantity', 1))
        unit = float(it.get('unit_price', 0))
        tot = round(qty * unit, 2)
        cursor.execute('''
            INSERT INTO invoice_items (invoice_id, description, quantity, unit_price, total_price)
            VALUES (?, ?, ?, ?, ?)
        ''', (invoice_id, it.get('description', 'Serviço'), qty, unit, tot))
        
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'invoice_id': invoice_id,
        'invoice_number': invoice_number,
        'message': f'Fatura {invoice_number} emitida com sucesso!'
    })

@app.route('/api/invoice/<int:invoice_id>/status', methods=['POST'])
def api_invoice_status(invoice_id):
    data = request.json or {}
    new_status = data.get('status', 'Pendente')
    
    conn = get_db_connection()
    conn.execute('UPDATE invoices SET status = ? WHERE id = ?', (new_status, invoice_id))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': f'Estado da fatura atualizado para: {new_status}'})

@app.route('/api/invoice/<int:invoice_id>/pdf')
def api_invoice_pdf(invoice_id):
    conn = get_db_connection()
    invoice_row = conn.execute('''
        SELECT i.*, c.name as client_name, c.nif as client_nif, c.address as client_address, c.email as client_email, c.phone as client_phone
        FROM invoices i
        JOIN clients c ON i.client_id = c.id
        WHERE i.id = ?
    ''', (invoice_id,)).fetchone()
    
    if not invoice_row:
        conn.close()
        return "Fatura não encontrada", 404
        
    invoice = dict(invoice_row)
    items = [dict(r) for r in conn.execute('SELECT * FROM invoice_items WHERE invoice_id = ?', (invoice_id,)).fetchall()]
    conn.close()
    
    if not HAS_REPORTLAB:
        # Fallback redirect to printable HTML view
        return redirect(url_for('view_invoice', invoice_id=invoice_id))
        
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#00B0FF'), # Neon Blue
        fontName='Helvetica-Bold'
    )
    
    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155')
    )
    
    story.append(Paragraph(f"FATURA OFICIAL — {invoice['invoice_number']}", title_style))
    story.append(Paragraph(f"EJAJ TECH — Soluções Digitais & Inteligência Artificial", meta_style))
    story.append(Spacer(1, 15))
    
    # Header Info Table
    header_data = [
        [
            Paragraph(f"<b>EMISSOR:</b><br/><b>EJAJ TECH Lda</b><br/>NIF: 599111519<br/>Av. da Liberdade 100, Lisboa<br/>contacto@ejajtech.com", meta_style),
            Paragraph(f"<b>CLIENTE:</b><br/><b>{invoice['client_name']}</b><br/>NIF: {invoice['client_nif']}<br/>{invoice['client_address']}<br/>{invoice['client_email']}", meta_style)
        ],
        [
            Paragraph(f"<b>Data de Emissão:</b> {invoice['issue_date']}<br/><b>Data de Vencimento:</b> {invoice['due_date']}", meta_style),
            Paragraph(f"<b>Estado:</b> <font color='#00E676'><b>{invoice['status'].upper()}</b></font>", meta_style)
        ]
    ]
    t_header = Table(header_data, colWidths=[260, 260])
    t_header.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
    ]))
    story.append(t_header)
    story.append(Spacer(1, 20))
    
    # Line Items Table
    table_data = [['Item / Descrição do Serviço', 'Qtd', 'Preço Unitário', 'Total']]
    for it in items:
        table_data.append([
            it['description'],
            f"{it['quantity']:,.1f}",
            f"€ {it['unit_price']:,.2f}",
            f"€ {it['total_price']:,.2f}"
        ])
        
    table_data.append(['', '', 'Subtotal:', f"€ {invoice['subtotal']:,.2f}"])
    table_data.append(['', '', f"IVA ({invoice['vat_rate']:.0f}%):", f"€ {invoice['vat_amount']:,.2f}"])
    table_data.append(['', '', 'TOTAL FATURA:', f"€ {invoice['total']:,.2f}"])
    
    t_items = Table(table_data, colWidths=[270, 50, 100, 100])
    t_items.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#00B0FF')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (1,0), (-1,-1), 'RIGHT'),
        ('GRID', (0,0), (-1,-4), 0.5, colors.HexColor('#CBD5E1')),
        ('LINEBELOW', (0,-3), (-1,-1), 1, colors.HexColor('#00E676')),
        ('FONTNAME', (2,-1), (-1,-1), 'Helvetica-Bold'),
    ]))
    story.append(t_items)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph(f"<b>Notas:</b> {invoice['notes'] or 'Processado via IA EJAJ TECH.'}", meta_style))
    
    doc.build(story)
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{invoice['invoice_number'].replace('/', '_')}.pdf",
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    print("[SERVER] AI Invoice Generator SaaS a iniciar na porta 6700...")
    app.run(host='0.0.0.0', port=6700, debug=False)
