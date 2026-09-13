import sqlite3
import os
import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'newsletter_saas.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Subscribers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            tier TEXT DEFAULT 'Gratuito',
            status TEXT DEFAULT 'Ativo',
            open_rate REAL DEFAULT 0.0,
            subscribed_at TEXT NOT NULL
        )
    ''')

    # Templates Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            header_subtitle TEXT,
            content_html TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    # Issues / Newsletters Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue_number INTEGER,
            title TEXT NOT NULL,
            subject TEXT NOT NULL,
            preview_text TEXT,
            template_id INTEGER,
            content_html TEXT NOT NULL,
            status TEXT DEFAULT 'Rascunho', -- Rascunho, Programado, Publicado
            scheduled_at TEXT,
            published_at TEXT,
            recipients_count INTEGER DEFAULT 0,
            opens_count INTEGER DEFAULT 0,
            clicks_count INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            FOREIGN KEY (template_id) REFERENCES templates (id)
        )
    ''')

    # Seed initial data if empty
    cursor.execute('SELECT COUNT(*) FROM subscribers')
    if cursor.fetchone()[0] == 0:
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        past_date_1 = (datetime.datetime.now() - datetime.timedelta(days=15)).strftime("%Y-%m-%d %H:%M")
        past_date_2 = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d %H:%M")

        # Seed subscribers
        initial_subscribers = [
            ('Sofia Duarte', 'sofia.duarte@editorial.pt', 'VIP', 'Ativo', 92.5, past_date_2),
            ('Gonçalo Ribeiro', 'g.ribeiro@techjournal.com', 'Premium', 'Ativo', 88.0, past_date_2),
            ('Mariana Fonseca', 'mariana.fonseca@designhub.io', 'Gratuito', 'Ativo', 75.4, past_date_1),
            ('Tiapo Martins', 'tiago.m@startups.pt', 'Premium', 'Ativo', 81.2, past_date_1),
            ('Beatriz Neves', 'b.neves@media-group.com', 'VIP', 'Ativo', 95.0, now_str),
            ('João Pedro Silva', 'joao.silva@curator.org', 'Gratuito', 'Pendente', 0.0, now_str),
            ('Camila Torres', 'camila.t@futurenews.io', 'Premium', 'Ativo', 84.7, now_str),
            ('Rodrigo Mendes', 'rodrigo.mendes@investor.pt', 'VIP', 'Ativo', 96.1, past_date_1)
        ]

        cursor.executemany('''
            INSERT INTO subscribers (name, email, tier, status, open_rate, subscribed_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', initial_subscribers)

        # Seed templates
        initial_templates = [
            (
                'Digest Semanal de Tendências',
                'Digest',
                'As principais leituras e análises curadas da semana',
                '''<div style="font-family: Georgia, serif; max-width: 640px; margin: 0 auto; color: #1a1917; line-height: 1.7;">
                    <header style="border-bottom: 2px solid #c85a32; padding-bottom: 1.5rem; margin-bottom: 2rem;">
                        <h1 style="font-size: 2.2rem; color: #1b4332; margin-bottom: 0.5rem;">The Weekly Chronicle</h1>
                        <p style="color: #64748b; font-style: italic; font-size: 1rem;">Edição #{{issue_number}} • Curadoria Editorial de Excelência</p>
                    </header>
                    <section>
                        <h2 style="color: #c85a32; font-size: 1.5rem;">Olá {{name}},</h2>
                        <p>Bem-vindo à nossa edição semanal. Hoje exploramos o impacto da transformação digital e as tendências mais marcantes do setor.</p>
                        <hr style="border: none; border-top: 1px solid #e8e4df; margin: 2rem 0;" />
                        <h3 style="font-size: 1.3rem;">1. O Novo Paradigma da Edição Digital</h3>
                        <p>A personalização de conteúdos atingiu um patamar onde a relevância contextual determina o sucesso de uma publicação...</p>
                        <a href="#" style="background: #c85a32; color: #ffffff; padding: 0.75rem 1.5rem; border-radius: 6px; text-decoration: none; display: inline-block; font-weight: bold; margin-top: 1rem;">Ler Artigo Completo</a>
                    </section>
                    <footer style="margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid #e8e4df; font-size: 0.85rem; color: #64748b; text-align: center;">
                        <p>© 2026 The Weekly Chronicle. Recebeu este e-mail por estar inscrito na nossa newsletter.</p>
                        <p><a href="{{unsubscribe_link}}" style="color: #c85a32;">Cancelar subscrição</a></p>
                    </footer>
                </div>''',
                past_date_2
            ),
            (
                'Edição Especial Deep Dive',
                'Deep Dive',
                'Análise aprofundada e relatórios exclusivos para leitores VIP',
                '''<div style="font-family: Georgia, serif; max-width: 640px; margin: 0 auto; color: #1a1917; line-height: 1.7;">
                    <div style="background: #1b4332; color: #ffffff; padding: 2rem; border-radius: 8px; text-align: center; margin-bottom: 2rem;">
                        <span style="background: #c85a32; color: #fff; padding: 0.3rem 0.8rem; border-radius: 4px; font-size: 0.75rem; text-transform: uppercase; font-weight: bold; font-family: sans-serif;">Relatório Exclusivo</span>
                        <h1 style="font-size: 2rem; margin-top: 1rem; color: #ffffff;">Deep Dive: O Futuro do Jornalismo</h1>
                    </div>
                    <p>Caro(a) <strong>{{name}}</strong>,</p>
                    <p>Nesta edição especial, analisámos mais de 50 dados de mercado para trazer uma visão clara e objetiva sobre o futuro da monetização de conteúdos.</p>
                    <div style="background: #faf8f5; border-left: 4px solid #c85a32; padding: 1.25rem; margin: 1.5rem 0; font-style: italic;">
                        "A confiança dos leitores é a única moeda que não desvaloriza na era da informação."
                    </div>
                </div>''',
                past_date_1
            ),
            (
                'Flash News & Anúncios',
                'Notícias',
                'Atualizações rápidas e comunicados urgentes para a comunidade',
                '''<div style="font-family: Georgia, serif; max-width: 640px; margin: 0 auto; color: #1a1917; line-height: 1.6;">
                    <h2 style="color: #1b4332; font-size: 1.8rem; border-bottom: 2px solid #1b4332; padding-bottom: 0.5rem;">Flash Update</h2>
                    <p style="margin-top: 1rem;">Olá {{name}}, temos novidades de última hora para partilhar com a nossa comunidade de leitores.</p>
                    <div style="border: 1px solid #e8e4df; padding: 1.5rem; border-radius: 8px; margin: 1.5rem 0; background: #ffffff;">
                        <h3 style="color: #c85a32; margin-top: 0;">Novo Lançamento Confirmado</h3>
                        <p>Lançámos oficialmente a nova plataforma de conteúdos interativos com acesso antecipado para membros.</p>
                    </div>
                </div>''',
                now_str
            )
        ]

        cursor.executemany('''
            INSERT INTO templates (title, category, header_subtitle, content_html, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', initial_templates)

        # Seed issues
        initial_issues = [
            (
                101,
                'Edição #101 — A Nova Era da Publicação Digital & Inteligência Criativa',
                '📰 Edição #101: O futuro do jornalismo independente e curadoria de conteúdo',
                'Análise completa sobre as novas ferramentas de publicação e o impacto no engagement dos leitores.',
                1,
                '''<div style="font-family: Georgia, serif; max-width: 640px; margin: 0 auto; color: #1a1917;"><h1>Edição #101 — Publicação Digital</h1><p>Conteúdo de excelência para os nossos subscritores VIP e leitores atentos...</p></div>''',
                'Publicado',
                None,
                past_date_1,
                8,
                7,
                4,
                past_date_1
            ),
            (
                102,
                'Edição #102 — O Poder dos Micro-Pubs e newsletters Comunitárias',
                '🚀 Edição #102: Como criar comunidades altamente engajadas à volta da sua marca',
                'Descubra o estudo de caso dos criadores de maior sucesso da década.',
                2,
                '''<div style="font-family: Georgia, serif; max-width: 640px; margin: 0 auto; color: #1a1917;"><h1>Edição #102 — Micro-Pubs</h1><p>Estratégias avançadas de retenção e monetização de audiências...</p></div>''',
                'Publicado',
                None,
                now_str,
                8,
                6,
                3,
                now_str
            ),
            (
                103,
                'Edição #103 — Tendências Globais de Média & Inteligência Artificial',
                '💡 Edição #103: IA na redação e automação de newsletters sem perder o toque humano',
                'Uma discussão aprofundada sobre ética, automatização e curadoria editorial.',
                1,
                '''<div style="font-family: Georgia, serif; max-width: 640px; margin: 0 auto; color: #1a1917;"><h1>Edição #103 — Tendências Globais</h1><p>Próxima edição agendada para o final desta semana...</p></div>''',
                'Programado',
                '2026-09-18 10:00',
                None,
                8,
                0,
                0,
                now_str
            )
        ]

        cursor.executemany('''
            INSERT INTO issues (issue_number, title, subject, preview_text, template_id, content_html, status, scheduled_at, published_at, recipients_count, opens_count, clicks_count, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', initial_issues)

        conn.commit()

    conn.close()

if __name__ == '__main__':
    init_db()
    print("Base de dados newsletter_saas.db inicializada com sucesso!")
