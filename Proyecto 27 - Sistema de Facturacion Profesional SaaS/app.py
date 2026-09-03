import os
from datetime import datetime
from flask import Flask, render_template, jsonify, request, send_file, make_response
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

app = Flask(__name__)

# Strict anti-cache headers
@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Initial Mock Database for Invoicing SaaS
clientes_db = [
    {"id": "CLI-501", "nome": "Algarve Tech Solutions, Lda.", "nif": "PT509887766", "email": "financeiro@algarvetech.pt", "morada": "Av. 5 de Outubro 120, Faro"},
    {"id": "CLI-502", "nome": "Marina Resort & Spa Hotel", "nif": "PT502334455", "email": "contabilidade@marinaresort.pt", "morada": "Marina de Albufeira Lote 4"},
    {"id": "CLI-503", "nome": "Veloce Luxury Motors", "nif": "PT511223344", "email": "gerencia@velocemotors.pt", "morada": "Estrada de Vale do Lobo 88, Almancil"},
    {"id": "CLI-504", "nome": "Clínica Estética Quinta do Lago", "nif": "PT508776655", "email": "faturacao@clinicavip.pt", "morada": "Quinta do Lago Shopping, Almancil"}
]

produtos_servicos_db = [
    {"sku": "SERV-01", "nome": "Consultoria em Arquitetura de Software SaaS", "preco": 150.00, "iva": 23},
    {"sku": "SERV-02", "nome": "Desenvolvimento de Plataforma Web Enterprise", "preco": 2500.00, "iva": 23},
    {"sku": "SERV-03", "nome": "Serviço de Manutenção & Suporte Mensal", "preco": 450.00, "iva": 23},
    {"sku": "SERV-04", "nome": "Formação Técnica de Equipas de Engenharia", "preco": 800.00, "iva": 23}
]

faturas_db = [
    {
        "id": "FT-2026/001",
        "cliente_nome": "Algarve Tech Solutions, Lda.",
        "cliente_nif": "PT509887766",
        "cliente_morada": "Av. 5 de Outubro 120, Faro",
        "data_emissao": "2026-09-01",
        "data_vencimento": "2026-09-15",
        "estado": "Paga",        # Paga, Pendente, Anulada
        "itens": [
            {"descricao": "Desenvolvimento de Plataforma Web Enterprise", "qtd": 1, "preco": 2500.00, "iva_pct": 23, "subtotal": 2500.00, "valor_iva": 575.00, "total": 3075.00}
        ],
        "base_tributavel": 2500.00,
        "total_iva": 575.00,
        "total_fatura": 3075.00
    },
    {
        "id": "FT-2026/002",
        "cliente_nome": "Marina Resort & Spa Hotel",
        "cliente_nif": "PT502334455",
        "cliente_morada": "Marina de Albufeira Lote 4",
        "data_emissao": "2026-09-02",
        "data_vencimento": "2026-09-16",
        "estado": "Pendente",
        "itens": [
            {"descricao": "Consultoria em Arquitetura de Software SaaS", "qtd": 10, "preco": 150.00, "iva_pct": 23, "subtotal": 1500.00, "valor_iva": 345.00, "total": 1845.00},
            {"descricao": "Serviço de Manutenção & Suporte Mensal", "qtd": 2, "preco": 450.00, "iva_pct": 23, "subtotal": 900.00, "valor_iva": 207.00, "total": 1107.00}
        ],
        "base_tributavel": 2400.00,
        "total_iva": 552.00,
        "total_fatura": 2952.00
    }
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/clientes", methods=["GET"])
def get_clientes():
    return jsonify(clientes_db)

@app.route("/api/produtos", methods=["GET"])
def get_produtos():
    return jsonify(produtos_servicos_db)

@app.route("/api/faturas", methods=["GET"])
def get_faturas():
    return jsonify(faturas_db)

@app.route("/api/faturas/criar", methods=["POST"])
def criar_fatura():
    data = request.json or {}
    new_num = f"FT-2026/{len(faturas_db) + 1:03d}"
    
    itens = data.get("itens", [])
    base_trib = sum(item.get("subtotal", 0.0) for item in itens)
    total_iva = sum(item.get("valor_iva", 0.0) for item in itens)
    total_fat = base_trib + total_iva
    
    nova_fatura = {
        "id": new_num,
        "cliente_nome": data.get("cliente_nome", "Cliente Final"),
        "cliente_nif": data.get("cliente_nif", "PT999999990"),
        "cliente_morada": data.get("cliente_morada", "Portugal"),
        "data_emissao": datetime.now().strftime("%Y-%m-%d"),
        "data_vencimento": data.get("data_vencimento", "2026-09-30"),
        "estado": "Pendente",
        "itens": itens,
        "base_tributavel": base_trib,
        "total_iva": total_iva,
        "total_fatura": total_fat
    }
    
    faturas_db.insert(0, nova_fatura)
    return jsonify({"success": True, "fatura": nova_fatura})

@app.route("/api/faturas/estado/<fatura_id>", methods=["POST"])
def alterar_estado(fatura_id):
    data = request.json or {}
    novo_estado = data.get("estado", "Paga")
    
    for f in faturas_db:
        if f["id"] == fatura_id:
            f["estado"] = novo_estado
            return jsonify({"success": True, "fatura": f})
            
    return jsonify({"success": False, "message": "Fatura não encontrada"}), 404

@app.route("/api/stats", methods=["GET"])
def get_stats():
    total_faturado = sum(f["total_fatura"] for f in faturas_db if f["estado"] != "Anulada")
    total_pendente = sum(f["total_fatura"] for f in faturas_db if f["estado"] == "Pendente")
    total_iva = sum(f["total_iva"] for f in faturas_db if f["estado"] != "Anulada")
    
    return jsonify({
        "total_faturado": f"{total_faturado:,.2f} €".replace(",", " ").replace(".", ","),
        "total_pendente": f"{total_pendente:,.2f} €".replace(",", " ").replace(".", ","),
        "total_iva": f"{total_iva:,.2f} €".replace(",", " ").replace(".", ","),
        "total_faturas": len(faturas_db)
    })

# ReportLab PDF Generation Endpoint
@app.route("/api/faturas/pdf/<path:fatura_id>", methods=["GET"])
def gerar_pdf_fatura(fatura_id):
    fatura = next((f for f in faturas_db if f["id"] == fatura_id), None)
    if not fatura:
        return "Fatura não encontrada", 404
        
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    c_navy = colors.HexColor("#1e3a8a")
    c_slate = colors.HexColor("#475569")
    c_light = colors.HexColor("#f8fafc")
    c_border = colors.HexColor("#cbd5e1")
    
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=22, textColor=c_navy)
    sub_style = ParagraphStyle('Sub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=c_slate)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=9, textColor=c_slate)
    header_table_style = ParagraphStyle('TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, textColor=colors.white)
    
    story = []
    
    # Header Title & Issuer Info
    story.append(Paragraph("EJAJ TECH — SOFTWARE SUITE", title_style))
    story.append(Paragraph("EJAJ Billing & Invoicing Systems • NIF: PT299888777", sub_style))
    story.append(Paragraph("Avenida 5 de Outubro, Edifício Executive, Faro • Portugal", body_style))
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_navy, spaceAfter=15))
    
    # Invoice Metadata & Client Box
    meta_text = f"<b>FATURA CERTIFICADA:</b> {fatura['id']}<br/><b>Data de Emissão:</b> {fatura['data_emissao']}<br/><b>Data Vencimento:</b> {fatura['data_vencimento']}<br/><b>Estado:</b> {fatura['estado'].upper()}"
    client_text = f"<b>CLIENTE:</b> {fatura['cliente_nome']}<br/><b>NIF / VAT:</b> {fatura['cliente_nif']}<br/><b>Morada:</b> {fatura['cliente_morada']}"
    
    t_info = Table([[Paragraph(meta_text, body_style), Paragraph(client_text, body_style)]], colWidths=[260, 272])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_light),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_info)
    story.append(Spacer(1, 20))
    
    # Invoice Items Table
    table_data = [[
        Paragraph("Descrição do Artigo / Serviço", header_table_style),
        Paragraph("Qtd", header_table_style),
        Paragraph("Preço Un. (€)", header_table_style),
        Paragraph("IVA %", header_table_style),
        Paragraph("Total (€)", header_table_style)
    ]]
    
    for item in fatura["itens"]:
        table_data.append([
            Paragraph(item["descricao"], body_style),
            Paragraph(str(item["qtd"]), body_style),
            Paragraph(f"{item['preco']:.2f} €", body_style),
            Paragraph(f"{item['iva_pct']}%", body_style),
            Paragraph(f"{item['total']:.2f} €", body_style)
        ])
        
    t_items = Table(table_data, colWidths=[240, 50, 80, 50, 112])
    t_items.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_items)
    story.append(Spacer(1, 15))
    
    # Financial Totals Summary
    tot_text = f"<b>Base Imponível:</b> {fatura['base_tributavel']:.2f} €<br/><b>Montante IVA (23%):</b> {fatura['total_iva']:.2f} €<br/><font size=12 color='#1e3a8a'><b>TOTAL A PAGAR: {fatura['total_fatura']:.2f} €</b></font>"
    t_tot = Table([[Paragraph("", body_style), Paragraph(tot_text, body_style)]], colWidths=[300, 232])
    t_tot.setStyle(TableStyle([
        ('BACKGROUND', (1,0), (1,0), c_light),
        ('BOX', (1,0), (1,0), 1, c_navy),
        ('PADDING', (1,0), (1,0), 10),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
    ]))
    story.append(t_tot)
    story.append(Spacer(1, 25))
    
    story.append(Paragraph("<i>Processado por computador • Software de Facturação EJAJ TECH v4.2</i>", ParagraphStyle('Foot', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8, textColor=c_slate, alignment=1)))
    
    doc.build(story)
    buffer.seek(0)
    
    response = make_response(send_file(buffer, mimetype="application/pdf", as_attachment=False, download_name=f"{fatura_id.replace('/', '_')}.pdf"))
    return response

if __name__ == "__main__":
    print("Iniciando SISTEMA DE FACTURAÇÃO PROFISSIONAL SAAS em http://localhost:5300")
    app.run(host="0.0.0.0", port=5300, debug=False)
