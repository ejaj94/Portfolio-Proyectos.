import os
import sqlite3

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'presentation.db')

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects_showcase (
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
        (0, "Calculadora de Metabolismo & Caloria SaaS", "Plataforma de Nutrição & Treino para Gimnásios", "Saúde & Fitness", 
         "Cálculo preciso de Taxa Metabólica Basal (BMR), gasto calórico diário e distribuição de macronutrientes para atletas e sócios.",
         "Python, Flask, SQLite3, HTML5/CSS3, JavaScript", "Otimização de rotinas alimentares em mais de 15% para atletas.", "badge-cyan"),
        
        (1, "Web Scraper & Monitor de Preços E-Commerce", "Inteligência de Mercado & Alertas de Stock", "E-Commerce & Scrape", 
         "Extração automatizada de dados de preços em tempo real com comparação competitiva e notificação de variação de mercado.",
         "Python, BeautifulSoup4, Requests, Pandas, Flask", "Poupança média de 25% na aquisição de inventário online.", "badge-lime"),

        (2, "Organizador Inteligente de Ficheiros PRO", "Automatização de Sistema de Ficheiros", "Utilitários System", 
         "Classificação inteligente de ficheiros por extensão, data e metadados, limpando diretórios saturados em segundos.",
         "Python, OS/Shutil, Threading, GUI Customizada", "Redução de 90% no tempo gasto a organizar pastas de trabalho.", "badge-blue"),

        (3, "Crypto & Forex Monitor PRO", "Painel Financeiro & Cotações em Tempo Real", "Fintech & Cripto", 
         "Monitorização ao vivo de ativos de criptomoedas, pares Forex e tendências de mercado com alertas visuais de volatilidade.",
         "Python, REST APIs, WebSockets, Chart.js, Flask", "Acompanhamento de mais de 50 ativos financeiros simultâneos.", "badge-amber"),

        (4, "Network Security & Cyber Firewall PRO", "Segurança de Redes & Análise de Tráfego", "Cibersegurança", 
         "Sistema de monitorização de pacotes de rede, deteção de anomalias IP e bloqueio preventivo de acessos não autorizados.",
         "Python, Scapy, Socket, Firewall Rules Engine", "Deteção preventiva de intrusões e escaneamento de portas.", "badge-purple"),

        (5, "Sentinel Node PRO", "Monitorização de Servidores & Infraestrutura Cloud", "DevOps & Cloud", 
         "Telemetria em tempo real de carga de CPU, consumo de RAM, saúde de discos e disponibilidade de serviços de infraestrutura.",
         "Python, Psutil, Flask Daemon, WebSockets", "Garantia de 99.9% de tempo de atividade em servidores monitorizados.", "badge-cyan"),

        (6, "Gestor Pro DB", "Administração & Backup de Bases de Dados Relacionais", "Enterprise DB", 
         "Gestão simplificada de schemas SQLite/PostgreSQL, execução de queries SQL otimizadas e automação de backups preventivos.",
         "Python, SQLite3, SQL Alchemy, Custom Grid UI", "Prevenção total de perda de dados críticos de empresas.", "badge-lime"),

        (7, "LogLivre SaaS", "Plataforma Logística & Gestão de Entregas", "Logística & Frota", 
         "Gestão integrada de rotas de frota, rastreio de encomendas em tempo real e controlo de custos operacionais de transporte.",
         "Python, Flask, Maps Integration, SQLite3", "Redução de 20% no tempo de rota de entregas urbanas.", "badge-blue"),

        (8, "Com Cheiro de Amor E-Commerce", "Plataforma de Vendas de Cosmética & Perfumaria", "E-Commerce SaaS", 
         "Loja virtual premium com catálogo de fragrâncias, carrinho interativo, gestão de stocks e checkout otimizado.",
         "Python, Flask, Payment API, Custom CSS Dark/Light", "Aumento da taxa de conversão de vendas em ambiente digital.", "badge-amber"),

        (9, "EJAJ Studio Branding & Marcas", "Gerador de Identidade Visual & Certificados", "Branding & Design", 
         "Criação automatizada de etiquetas de produto, logos empresariais, marcas de água e emissão de certificados digitais.",
         "Python, Pillow Image Processing, ReportLab PDF", "Produção instantânea de material corporativo em alta resolução.", "badge-purple")
    ]

    cursor.executemany("""
        INSERT INTO projects_showcase (day_number, title, subtitle, category, description, tech_stack, impact_highlight, badge_color)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, projects)

    conn.commit()
    conn.close()
    print("[DB] Base de dados da Apresentação Especial Dia 10 (presentation.db) inicializada com sucesso!")

if __name__ == '__main__':
    init_db()
