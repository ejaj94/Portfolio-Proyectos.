import os
import sqlite3

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'presentation30.db')

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects_showcase_30 (
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
        (21, "EJAJ TECH Billing System", "Sistema de Faturação & Emissão de Documentos", "Faturação & Finanças",
         "Plataforma certificada de emissão de faturas, recibos e notas de crédito com cálculo automático de impostos e exportação PDF.",
         "Python, Flask, ReportLab PDF, SQLite3", "Conformidade fiscal e automação de cobranças.", "badge-yellow"),

        (22, "EJAJ Analytics PRO", "Plataforma de Business Intelligence & Dashboard", "Analytics & BI",
         "Dashboard de análise preditiva de negócios, retenção de clientes, gráficos dinâmicos de faturação e métricas de desempenho.",
         "Python, Flask, Chart.js, Pandas, Data Pipelines", "Tomada de decisão baseada em dados reais.", "badge-yellow"),

        (23, "EJAJ VetLux", "Gestão Veterinária de Luxo & Fichas Clínicas", "Medicina Veterinária",
         "Sistema de gestão clínica para animais de estimação VIP, registo de vacinação, histórico cirúrgico e lembretes por SMS.",
         "Python, Flask, Medical Records DB, SQLite3", "Aumento da fidelização de clientes de clínicas veterinárias.", "badge-yellow"),

        (24, "EJAJ Media Manager", "Gestão de Conteúdos Digitais & Média", "Gestão de Conteúdo",
         "Organização centralizada de ativos digitais, vídeos corporativos, imagens em alta definição e catálogo de ficheiros.",
         "Python, Pillow, File Processing, Flask UI", "Redução de 70% no tempo de busca de ficheiros de media.", "badge-yellow"),

        (25, "EJAJ Auto Performance", "Oficina de Carros de Luxo & Competição", "Automóvel & Competição",
         "Gestão de ordens de reparação para veículos de alta gama, stock de peças de competição e agendamento de telemetria.",
         "Python, Flask, Order Tracking, SQLite3", "Otimização de fluxos de trabalho em oficinas de prestígio.", "badge-yellow"),

        (26, "VetCare SaaS", "Gestão de Clínicas & Hospitais Veterinários", "Saúde Animal",
         "Plataforma completa de receção de animais, internamento, agendamento de consultas médicas e gestão de medicamentos.",
         "Python, Flask, Medical Schema, REST API", "Controlo total de stock e agenda clínica.", "badge-yellow"),

        (27, "Lumen Gestão de Academia Universitária", "Plataforma de Ensino & Gestão Escolar", "Educação & Ensino",
         "Gestão de turmas, pauta de notas, controlo de assiduidade de alunos e emissão de certificados académicos.",
         "Python, Flask, Educational DB, PDF Generator", "Digitalização integral da secretaria universitária.", "badge-yellow"),

        (28, "Resolv IT SaaS", "Gestão de Tickets & Suporte Técnico IT", "Gestão de TI & Suporte",
         "Sistema Helpdesk de tickets de suporte, atribuição de técnicos, Nível de Serviço (SLA) e resolução de incidentes.",
         "Python, Flask, WebSockets, SLA Engine", "Redução de 45% no tempo médio de resposta de suporte.", "badge-yellow"),

        (29, "Recortador de Enlaces PRO", "Encurtador Inteligente & Análise de Links", "Ferramentas Web",
         "Encurtamento de URLs corporativas com estatísticas de cliques em tempo real, geolocalização e geração de código QR.",
         "Python, Flask, QR Code Engine, SQLite3", "Rastreio avançado de campanhas de marketing digital.", "badge-yellow"),

        (30, "Desafio 30 Dias EJAJ TECH", "Plataforma de Metas, Hábitos & Produtividade", "Produtividade & Desafio",
         "Plataforma comemorativa do marco de 30 dias de criação de software, acompanhamento de hábitos diários e hábitos de código.",
         "Python, Flask, Interactive UI, SQLite3", "30 dias ininterruptos de superação técnica e engenharia.", "badge-yellow")
    ]

    cursor.executemany("""
        INSERT INTO projects_showcase_30 (day_number, title, subtitle, category, description, tech_stack, impact_highlight, badge_color)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, projects)

    conn.commit()
    conn.close()
    print("[DB] Base de dados da Apresentação Especial Dia 30 (presentation30.db) inicializada com sucesso!")

if __name__ == '__main__':
    init_db()
