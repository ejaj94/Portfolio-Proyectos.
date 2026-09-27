import os
import sqlite3

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'presentation40.db')

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects_showcase_40 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day_number INTEGER NOT NULL,
            title TEXT NOT NULL,
            subtitle TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            tech_stack TEXT NOT NULL,
            impact_highlight TEXT NOT NULL,
            badge_color TEXT NOT NULL
        );
    """)

    projects = [
        (31, "NovaTrends E-Commerce Store", "Loja Virtual de Tendências & Checkout Otimizado", "E-Commerce AI",
         "Plataforma de e-commerce moderna com recomendação de produtos por inteligência artificial, checkout ultra-rápido e integração de pagamentos.",
         "Python, Flask, AI Recommendation Engine, SQLite3", "Aumento de 40% na conversão de vendas online.", "badge-neon-pink"),

        (32, "MindHabit SaaS", "App de Monitorização de Hábitos & Produtividade", "Saúde & Produtividade",
         "Aplicação de acompanhamento de rotinas, métricas de bem-estar mental, registo de objetivos e análise estatística de hábitos.",
         "Python, Flask, Chart.js, Mobile-First UI", "Melhoria comprovada de 85% na consistência de hábitos.", "badge-neon-cyan"),

        (33, "SocialPost com AI", "Gerador Inteligente de Conteúdos & Marketing", "Inteligência Artificial",
         "Motor de geração de conteúdos publicitários para redes sociais alimentado por IA, criação de copy envolvente e hashtags otimizadas.",
         "Python, OpenAI API, Flask, Custom AI Prompts", "Produção instantânea de conteúdos publicitários.", "badge-neon-purple"),

        (34, "Presupuesto PRO", "Gerador Avançado de Orçamentos Empresariais", "Gestão & Finanças",
         "Plataforma de elaboração de orçamentos técnicos com margens de lucro automatizadas, cálculo de impostos e exportação PDF corporativa.",
         "Python, ReportLab PDF, Flask, SQLite3", "Redução de 90% no tempo de criação de propostas.", "badge-neon-green"),

        (35, "Sunset Travel SaaS", "Plataforma de Agência de Viagens & Reservas", "Turismo & Viagens",
         "Portal de viagens de luxo com motor de busca de destinos, itinerários personalizados, agendamento de voos e gestão de pacotes.",
         "Python, REST APIs, Maps Integration, Flask", "Digitalização completa de agências de turismo.", "badge-neon-pink"),

        (36, "Gerador de Faturas IA", "Emissão Inteligente & Leitura de Recibos OCR", "Finanças & IA",
         "Sistema de faturação inteligente com reconhecimento ótico de caracteres (OCR) para leitura de despesas e emissão automatizada.",
         "Python, Tesseract OCR, Flask, SQLite3", "Eliminação de erros de introdução manual de despesas.", "badge-neon-cyan"),

        (37, "QR Menu Gerador com IA", "Menu Digital Gastronómico & Gerador QR", "Restauração & IA",
         "Criação dinâmica de cartões de restaurante com leitura de código QR, atualização imediata de pratos e sugestões gastronómicas por IA.",
         "Python, QR Code Engine, Flask, Tailwind CSS", "Modernização sem contacto para espaços gastronómicos.", "badge-neon-purple"),

        (38, "Agenda Automática AI", "Motor Inteligente de Agendamento & Lembretes", "Automação SaaS",
         "Gestão autónoma de horários de atendimento com resolução de conflitos de agenda por IA e disparo de notificações por WhatsApp.",
         "Python, WhatsApp API, Calendar Engine, Flask", "Zero sobreposição de agendamentos de clientes.", "badge-neon-green"),

        (39, "Calculadora de Rentabilidade", "Análise Financeira & Simulação de ROI", "Fintech & Análise",
         "Ferramenta de simulação de retorno de investimento (ROI), cálculo de margem operacional e projeção financeira para startups.",
         "Python, Financial Algorithms, Chart.js, Flask", "Clareza absoluta na viabilidade financeira de projetos.", "badge-neon-pink"),

        (40, "Gerador de Propostas Comerciais", "Plataforma de Engenharia de Vendas SaaS", "Vendas & IA Enterprise",
         "Motor de geração de propostas comerciais de alta engenharia de software com cláusulas jurídicas automáticas e assinatura digital.",
         "Python, ReportLab Engine, Signature JS, Flask", "Aumento da taxa de fecho de contratos em 50%.", "badge-neon-cyan")
    ]

    cursor.executemany("""
        INSERT INTO projects_showcase_40 (day_number, title, subtitle, category, description, tech_stack, impact_highlight, badge_color)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, projects)

    conn.commit()
    conn.close()
    print("[DB] Base de dados da Apresentação Especial Dia 40 (presentation40.db) inicializada com sucesso!")

if __name__ == '__main__':
    init_db()
