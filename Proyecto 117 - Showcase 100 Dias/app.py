import os
from flask import Flask, render_template, send_from_directory, jsonify, send_file

app = Flask(__name__)
PORT = 6970

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEOS_DIR = r"C:\Users\enman\Desktop\Portfolio de programacion\Proyectos reales\Pagina de programacion EJAJ Tech"

PROJECTS_DATA = [
    {
        "day": 91,
        "title": "Dia 91 - API Tester Pro",
        "name": "API Tester Pro",
        "tag": "PROJETO #91 | TESTES DE REST API",
        "subtitle": "Bancada Avançada de Teste & Inspeção de Requisições HTTP",
        "desc": "Ferramenta profissional e intuitiva para desenvolvedores realizarem testes de endpoints, inspeção de cabeçalhos HTTP, payload JSON e cronometragem de latência em milissegundos.",
        "video": "/videos/Proyecto 91 API Tester.mp4",
        "tech": ["Python Flask", "RESTful API", "Fetch Client", "Tailwind CSS"],
        "icon": "fa-solid fa-bolt",
        "highlights": ["Histórico de chamadas", "Inspeção de Headers", "Formatador JSON nativo"]
    },
    {
        "day": 92,
        "title": "Dia 92 - Image Compressor AI",
        "name": "Image Compressor AI",
        "tag": "PROJETO #92 | OTIMIZAÇÃO GRÁFICA",
        "subtitle": "Compressão Inteligente sem Perda de Fidelidade",
        "desc": "Sistema de compressão matemática para WebP, PNG e JPEG que reduz até 85% do peso dos ficheiros mantendo a acuidade visual cristalina para alta performance web.",
        "video": "/videos/Proyecto 92 Compress Picture.mp4",
        "tech": ["Python Pillow", "WebP Engine", "Blob Processing", "CSS Luxury Glass"],
        "icon": "fa-solid fa-file-image",
        "highlights": ["Redução de 85% de peso", "Conversão WebP em lote", "Preview comparativo instantâneo"]
    },
    {
        "day": 93,
        "title": "Dia 93 - SubCraft SaaS",
        "name": "SubCraft SaaS",
        "tag": "PROJETO #93 | GESTÃO DE ASSINATURAS",
        "subtitle": "Motor de Recorrência & Planos Empresariais",
        "desc": "Solução completa de monetização recorrente para empresas, gestão de tiers (Basic, Pro, Enterprise), faturas automatizadas e monitorização de churn rate.",
        "video": "/videos/Proyecto 93 Sub Craft.mp4",
        "tech": ["Flask ORM", "SQLite3", "Stripe Webhooks Concept", "Chart.js"],
        "icon": "fa-solid fa-credit-card",
        "highlights": ["Cálculo de MRR em tempo real", "Upgrade de planos 1-clique", "Controlo de Churn"]
    },
    {
        "day": 94,
        "title": "Dia 94 - MemberCraft",
        "name": "MemberCraft Portal",
        "tag": "PROJETO #94 | COMUNIDADES EXCLUSIVAS",
        "subtitle": "Ecossistema Fechado de Membros & Conteúdo VIP",
        "desc": "Portal de membresias e gestão de comunidades com controlo granular de acessos por tier, área de membros protegida e feed exclusivo de recursos para programadores.",
        "video": "/videos/Proyecto 94 Member Craft.mp4",
        "tech": ["Session Auth", "Role-Based Access", "Tailwind UI", "SQLite3"],
        "icon": "fa-solid fa-users-gear",
        "highlights": ["Acesso por níveis", "Salas exclusivas de membros", "Sistema de crachás VIP"]
    },
    {
        "day": 95,
        "title": "Dia 95 - FreelanceCraft",
        "name": "FreelanceCraft Hub",
        "tag": "PROJETO #95 | MARKETPLACE DE TALENTO",
        "subtitle": "Conexão Direta entre Clientes & Especialistas Digitais",
        "desc": "Marketplace bidirecional para contratação de freelancers de elite, submissão de propostas comerciais com marcos (milestones) e sistema de garantia de entrega.",
        "video": "/videos/Proyecto 95 Freelance Craft.mp4",
        "tech": ["REST API", "Milestone Tracking", "Live Chat Mockup", "Responsive CSS"],
        "icon": "fa-solid fa-briefcase",
        "highlights": ["Marcos de entrega (Milestones)", "Gestão de propostas", "Perfis com portfólio integrado"]
    },
    {
        "day": 96,
        "title": "Dia 96 - DrivePulse Rent-a-Car",
        "name": "DrivePulse Fleet OS",
        "tag": "PROJETO #96 | ALUGUER DE VEÍCULOS",
        "subtitle": "Gestão Operacional de Frotas & Contratos Digitais",
        "desc": "Plataforma de alta precisão para locação automóvel: catálogo segmentado por categorias (SUV, Elétricos, Luxury), calendário de reservas, cálculo de cauções e emissão de contratos.",
        "video": "/videos/Proyecto 96 DrivePulse.mp4",
        "tech": ["Fleet Logic", "Date Range Picker", "Contract Generator", "Glassmorphism UI"],
        "icon": "fa-solid fa-car-side",
        "highlights": ["Contratos digitais em tempo real", "Status de frota ao vivo", "Cálculo de depósitos de segurança"]
    },
    {
        "day": 97,
        "title": "Dia 97 - Grand Hotel Suite",
        "name": "Grand Hotel Suite 5-Star",
        "tag": "PROJETO #97 | HOSPITALITY TECH",
        "subtitle": "Motor de Reservas Hoteleiras & Experiência de Hóspedes",
        "desc": "Sistema de gestão hoteleira de padrão 5 estrelas: check-in express, gestão de quartos e suítes, mapa de disponibilidade em tempo real e serviços de concierge digital.",
        "video": "/videos/Proyecto 97 Grand Hotel Suite.mp4",
        "tech": ["Hospitality Engine", "Room Availability Grid", "Concierge Chat", "Tailwind Luxury"],
        "icon": "fa-solid fa-hotel",
        "highlights": ["Mapa de quartos interativo", "Check-in e Check-out automatizado", "Desglose de taxas turísticas"]
    },
    {
        "day": 98,
        "title": "Dia 98 - LocalPro Marketplace",
        "name": "LocalPro Services",
        "tag": "PROJETO #98 | SERVIÇOS DE PROXIMIDADE",
        "subtitle": "Localizador & Agendamento de Especialistas Certificados",
        "desc": "Plataforma de geolocalização e contratação de serviços residenciais e técnicos com avaliações verificadas, orçamentos rápidos e sistema de mensagens direto.",
        "video": "/videos/Proyecto 98 Local Pro.mp4",
        "tech": ["Geolocation Concept", "Service Booking", "Star Rating Engine", "Modern Dark UI"],
        "icon": "fa-solid fa-location-dot",
        "highlights": ["Busca por raio de proximidade", "Agendamento com confirmação SMS", "Avaliações 100% verificadas"]
    },
    {
        "day": 99,
        "title": "Dia 99 - AutoFlow OS",
        "name": "AutoFlow Enterprise",
        "tag": "PROJETO #99 | AUTOMAÇÃO INTELIGENTE",
        "subtitle": "Orquestrador de Triggers, Webhooks & Ações",
        "desc": "Motor de automação sem código capaz de encadear eventos em disparos condicionais (if/then), registar auditoria completa de execuções e integrar serviços em cadeia.",
        "video": "/videos/Proyecto 99 Auto Flow OS.mp4",
        "tech": ["Workflow Engine", "Event Listeners", "Execution Pipeline", "Reactive Nodes"],
        "icon": "fa-solid fa-diagram-project",
        "highlights": ["Disparadores por Webhook", "Lógica condicional if-else", "Histórico de execuções com log visual"]
    },
    {
        "day": 100,
        "title": "Dia 100 - NEXUS Business OS",
        "name": "NEXUS Business OS (Crowning Masterpiece)",
        "tag": "PROJETO #100 | O SISTEMA OPERATIVO SUPREMO",
        "subtitle": "A Unificação Total dos 100 Dias de Código",
        "desc": "O projeto ápice dos 100 dias: um sistema operacional empresarial tudo-em-um com CRM completo, Clientes 360°, Faturação oficial (23% IVA), Orçamentos convertíveis, Inventário inteligente, Tarefas, Calendário, Suporte Helpdesk e Copiloto de Inteligência Artificial.",
        "video": "/videos/Proyecto 100 Nexa AI.mp4",
        "tech": ["Python Flask", "SQLite ACID", "AI Business Brain", "Ultra 8K Cosmic Glass", "Chart.js"],
        "icon": "fa-solid fa-crown",
        "highlights": ["10 Módulos Empresariais Unificados", "Conversão de Orçamento a Fatura em 1 clique", "Copiloto IA Estratégico Autônomo"]
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/videos/<path:filename>')
def serve_video(filename):
    return send_from_directory(VIDEOS_DIR, filename)

@app.route('/logo')
def serve_logo():
    logo_path = os.path.join(VIDEOS_DIR, "EJAJ_TECH_Logo.jpg")
    if os.path.exists(logo_path):
        return send_file(logo_path, mimetype='image/jpeg')
    return ("", 404)

@app.route('/api/projects')
def get_projects():
    return jsonify({
        "success": True,
        "milestone": "100 DIAS & 100 PROJETOS CONCLUÍDOS",
        "total_days": 100,
        "community_members": "+3.500",
        "total_lines_of_code": "+500.000",
        "projects": PROJECTS_DATA
    })

if __name__ == '__main__':
    print(">> =================================================================")
    print(f">> EJAJ TECH - SHOWCASE DIA 100 & PROJETO 100 - GOLD EDITION INICIADO")
    print(f">> Aceder em http://localhost:{PORT}")
    print(">> =================================================================")
    app.run(host='0.0.0.0', port=PORT, debug=True)
