import os
import sqlite3

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'presentation20.db')

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects_showcase_20 (
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
        (11, "Portfolio Fullstack Professional EJAJ TECH", "Apresentação & Plataforma de Serviços", "Portfólio & Web",
         "Plataforma centralizada de apresentação do engenheiro Enmanuel Jimenez com amostra de ecossistemas digitais.",
         "Python, Flask, HTML5/CSS3, JavaScript, WebGL", "Aumento da visibilidade de marca corporativa.", "badge-cyan"),

        (12, "EJAJ TECH Barbearia SaaS", "Gestão de Barbearia & Agendamento Online", "Serviços & Gestão",
         "Sistema completo de agendamento de cortes, gestão de barbeiros, comissões e faturação instantânea.",
         "Python, Flask, SQLite3, WhatsApp API Integration", "Redução de 80% em faltas não justificadas de clientes.", "badge-lime"),

        (13, "EJAJ TECH Restaurante Gourmet POS", "Gestão Gastronómica & KDS de Cozinha", "Restauração & POS",
         "Terminal POS para restauração de luxo com envio de comandas para o ecrã da cozinha e faturação simplificada.",
         "Python, Flask, WebSockets, SQLite3, Custom CSS", "Aumento de 30% na velocidade do serviço de mesa.", "badge-amber"),

        (14, "EJAJ TECH FitClub SaaS", "Gestão de Ginásios & Controlo de Sócios", "Saúde & Fitness",
         "Gestão de catracas, planos de mensalidades, fichas de treino personalizadas e controlo de pagamentos.",
         "Python, Flask, Chart.js, SQLite3", "Faturação recorrente automatizada para clubes de fitness.", "badge-blue"),

        (15, "Vale do Lobo Luxury Real Estate", "Portal Imobiliário de Empreendimentos de Luxo", "Imobiliário Luxo",
         "Catálogo interativo de vivendas e apartamentos no Algarve com agendamento de visitas VIP e tour virtual.",
         "Python, Flask, Google Maps API, Responsive Grid", "Angariação e contacto direto com investidores internacionais.", "badge-purple"),

        (16, "Veloce Luxury Stand EJAJ TECH", "Gestão de Stand de Automóveis de Alta Gama", "Automóvel Luxo",
         "Plataforma de exposição de supercarros, simulação de financiamento bancário e agendamento de test-drives.",
         "Python, Flask, Financial Calc Engine, SQLite3", "Digitalização completa do processo de venda automóvel.", "badge-cyan"),

        (17, "Quinta do Lago Clínica Dentária", "Gestão Clínica & Odontologia Avançada", "Saúde & Medicina",
         "Ficha médica dentária interativa, agendamento de consultas por especialidade e lembretes por SMS/WhatsApp.",
         "Python, Flask, Medical DB Schema, Calendar UI", "Otimização da agenda de médicos dentistas especialistas.", "badge-lime"),

        (18, "Marina Albufeira Resort Deluxe", "Sistema SaaS de Hotelaria & Reserva de Suites", "Hotelaria & Turismo",
         "Gestão de reservas de quartos, serviços de quarto (room-service), taxas turísticas e check-in/check-out rápido.",
         "Python, Flask, Multi-currency, SQLite3", "Melhoria na experiência do hóspede e faturação hoteleira.", "badge-amber"),

        (19, "Booking SaaS EJAJ TECH", "Motor Universal de Agendamentos & Marcações", "Agendamentos SaaS",
         "Motor multi-empresa para marcações de serviços com integração de calendário e notificações automáticas.",
         "Python, Flask, REST API, Calendar Engine", "Automação total da agenda comercial de prestadores de serviços.", "badge-blue"),

        (20, "EJAJ CRM Enterprise", "Plataforma de Gestão de Relações com Clientes", "Enterprise CRM",
         "Gestão de funil de vendas, pipelines de negociação, histórico de interações e acompanhamento de leads.",
         "Python, Flask, Chart.js, Advanced Filtering", "Aumento da taxa de fecho de contratos em 35%.", "badge-purple")
    ]

    cursor.executemany("""
        INSERT INTO projects_showcase_20 (day_number, title, subtitle, category, description, tech_stack, impact_highlight, badge_color)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, projects)

    conn.commit()
    conn.close()
    print("[DB] Base de dados da Apresentação Especial Dia 20 (presentation20.db) inicializada com sucesso!")

if __name__ == '__main__':
    init_db()
