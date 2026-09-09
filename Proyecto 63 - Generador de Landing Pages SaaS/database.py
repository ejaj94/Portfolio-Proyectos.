import os
import sqlite3
import json

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'landings.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table for saved landing pages
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_landings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        template_name TEXT NOT NULL,
        hero_headline TEXT NOT NULL,
        hero_subheadline TEXT,
        cta_text TEXT,
        primary_color TEXT NOT NULL,
        secondary_color TEXT NOT NULL,
        bg_color TEXT NOT NULL,
        features_json TEXT,
        testimonials_json TEXT,
        html_code TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)

    # Table for template presets
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS landing_templates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        primary_color TEXT NOT NULL,
        secondary_color TEXT NOT NULL,
        bg_color TEXT NOT NULL,
        default_headline TEXT NOT NULL,
        default_subheadline TEXT NOT NULL
    );
    """)

    # Seed Templates if empty
    cursor.execute("SELECT COUNT(*) FROM landing_templates")
    if cursor.fetchone()[0] == 0:
        seed_templates = [
            ("Cyber Tech SaaS", "Tecnologia", "#00F5D4", "#7000FF", "#0F172A", 
             "A Plataforma de Inteligência Artificial para alavancar a sua empresa", 
             "Automatize processos, aumente a produtividade e impulsione as suas vendas com tecnologia de ponta."),

            ("Lava Emerald Agency", "Agência Digital", "#10B981", "#064E3B", "#0A0A0C", 
             "Transformamos Ideias em Software de Alta Performance", 
             "Engenharia de software personalizada, design moderno e estratégias de crescimento para marcas exigentes."),

            ("Sunset Amber Fitness", "Saúde & Desporto", "#FFB703", "#FB8500", "#111827", 
             "Alcance a Sua Melhor Versão com Treino de Elite", 
             "Planos de treino personalizados, nutrição equilibrada e acompanhamento profissional 24/7."),

            ("Neon Coral E-Commerce", "Vendas Digitais", "#FF6B6B", "#FFDE59", "#1E293B", 
             "A Loja Online do Futuro Chegou ao Seu Negócio", 
             "Checkout ultra-rápido, recomendações inteligentes e integração total de pagamentos."),

            ("Obsidian Minimal SaaS", "Minimalista Pro", "#38BDF8", "#6366F1", "#020617", 
             "Simplicidade e Potência para a Gestão do Seu Negócio", 
             "Uma interface intuitiva projetada para maximizar a eficiência operacional da sua equipa.")
        ]

        cursor.executemany("""
            INSERT INTO landing_templates (name, category, primary_color, secondary_color, bg_color, default_headline, default_subheadline)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, seed_templates)

    # Seed 1 initial saved landing if empty
    cursor.execute("SELECT COUNT(*) FROM saved_landings")
    if cursor.fetchone()[0] == 0:
        sample_features = json.dumps([
            {"icon": "fa-rocket", "title": "Automação de Alta Velocidade", "desc": "Execute tarefas complexas em milissegundos com algoritmos otimizados."},
            {"icon": "fa-shield-halved", "title": "Segurança de Nível Empresarial", "desc": "Encriptação de ponta a ponta e conformidade com os mais altos padrões."},
            {"icon": "fa-chart-pie", "title": "Analytics em Tempo Real", "desc": "Painéis visuais intuitivos para acompanhar métricas e ROI ao segundo."}
        ])
        
        sample_testimonials = json.dumps([
            {"name": "Carlos Mendes", "role": "CEO TechGroup", "comment": "A landing page gerada aumentou a nossa taxa de conversão em mais de 45% nas primeiras duas semanas!", "rating": 5},
            {"name": "Ana Sofia Ramos", "role": "Diretora de Marketing", "comment": "Ferramenta incrível e ultra-rápida. Em minutos tínhamos uma página com aspeto de 5000€.", "rating": 5}
        ])

        sample_html = """<!DOCTYPE html><html lang="pt"><head><meta charset="UTF-8"><title>EJAJ TECH - Landing Page</title></head><body><h1>EJAJ TECH SaaS</h1></body></html>"""

        cursor.execute("""
            INSERT INTO saved_landings (title, template_name, hero_headline, hero_subheadline, cta_text, primary_color, secondary_color, bg_color, features_json, testimonials_json, html_code, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "Landing Oficial EJAJ TECH", "Cyber Tech SaaS",
            "A Plataforma de Inteligência Artificial para alavancar a sua empresa",
            "Automatize processos, aumente a produtividade e impulsione as suas vendas com tecnologia de ponta.",
            "Começar Agora Gratuitamente",
            "#00F5D4", "#7000FF", "#0F172A",
            sample_features, sample_testimonials, sample_html, "2026-09-09 10:45"
        ))

    conn.commit()
    conn.close()
    print("[Database OK] landings.db criada e populada com sucesso.")

if __name__ == '__main__':
    init_db()
