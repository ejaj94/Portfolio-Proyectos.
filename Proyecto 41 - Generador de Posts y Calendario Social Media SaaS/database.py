import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'posts.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table for Posts & Calendar
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            platform TEXT NOT NULL,
            tone TEXT NOT NULL,
            copy TEXT NOT NULL,
            hashtags TEXT NOT NULL,
            cta TEXT NOT NULL,
            media_suggestion TEXT,
            scheduled_date TEXT,
            scheduled_time TEXT,
            status TEXT DEFAULT 'Agendado',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Check if table is empty
    cursor.execute('SELECT COUNT(*) FROM posts')
    if cursor.fetchone()[0] == 0:
        today = datetime.now()
        
        seed_posts = [
            (
                "Lançamento de Software SaaS de Logística & Entregas",
                "Instagram",
                "Vendedor & Persuasivo",
                "🚀 Transforme a operação de entregas do seu negócio! Com o nosso novo sistema telemétrico em tempo real, você acompanha cada estafeta no mapa, aceita pagamentos via MB WAY e reduz o tempo de entrega em até 35%.\n\nPronto para elevar o nível da sua frota?",
                "#Logistica #SaaS #EntregasExpress #EJAJTECH #InovacaoDigital #ECommercePortugal",
                "👉 Clique no link da bio e solicite uma demonstração gratuita hoje mesmo!",
                "Carrossel dinâmico com ecrãs da app do cliente e mapa GPS",
                (today + timedelta(days=1)).strftime('%Y-%m-%d'),
                "10:00",
                "Agendado"
            ),
            (
                "Dicas de Alta Performance & Gestão de Hábitos",
                "LinkedIn",
                "Profissional & Educacional",
                "💡 A consistência é o motor do sucesso no empreendedorismo. Estabelecer rotinas claras e monitorizar pequenos progressos diários cria um efeito acumulativo extraordinário.\n\n3 hábitos fundamentais dos líderes de topo:\n1️⃣ Blocos de Foco Profundo (Deep Work de 2h)\n2️⃣ Monitorização diária de OKRs\n3️⃣ Priorização do sono e regeneração cognitiva.",
                "#Lideranca #Produtividade #HighPerformance #Empreendedorismo #Mindset #Gestao",
                "💬 Qual destas rotinas já faz parte do seu dia a dia? Partilhe nos comentários!",
                "Infográfico minimalista com os 3 pilares da neuro-performance",
                (today + timedelta(days=2)).strftime('%Y-%m-%d'),
                "14:30",
                "Agendado"
            ),
            (
                "Promoção Especial de Verão - Coleção Moda Sustentável",
                "Instagram",
                "Descontraído & Entusiasta",
                "☀️ O verão pede frescura, elegância e responsabilidade ambiental! A nossa nova coleção sustentável chegou com tecidos 100% orgânicos e cortes contemporâneos para arrasar em qualquer ocasião.",
                "#ModaSustentavel #Verao2026 #EstiloOrgânico #TendenciasModa #FashionPortugal",
                "🛍️ Garanta 20% de desconto na primeira compra com o cupão: VERAO20",
                "Reels de 15s com transição rápida de looks na praia",
                (today + timedelta(days=3)).strftime('%Y-%m-%d'),
                "18:00",
                "Agendado"
            ),
            (
                "Lançamento de Imóvel de Luxo em Vale do Lobo",
                "Facebook",
                "Exclusivo & Elegante",
                "🏡 Moradia T5 de Arquitetura Contemporânea em Vale do Lobo. Com vista panorâmica para o mar, piscina de bordo infinito e acabamentos em mármore natural, este imóvel redefine o conceito de viver com requinte no Algarve.",
                "#ImobiliarioDeLuxo #ValeDoLobo #AlgarveRealEstate #LuxuryHomes #InvestimentoAlgarve",
                "📞 Agende a sua visita privada exclusiva connosco através de mensagem direta.",
                "Galeria de fotos HD com ângulos exteriores e interiores",
                (today + timedelta(days=4)).strftime('%Y-%m-%d'),
                "11:15",
                "Agendado"
            ),
            (
                "Bastidores do Desenvolvimento de Apps na EJAJ TECH",
                "TikTok",
                "Viral & Divertido",
                "🔥 Quando o código compila à primeira tentativa e o servidor não vai abaixo! Um dia típico no nosso estúdio de engenharia de software criando sistemas SaaS de alto nível.",
                "#DevLife #Programacao #TechTikTok #EJAJTECH #SoftwareEngineer #HumorDev",
                "⚡ Comente 'CÓDIGO' se também comemora quando o deploy passa sem erros!",
                "Vídeo POV com música de tendência e reação hilariante dos devs",
                (today + timedelta(days=5)).strftime('%Y-%m-%d'),
                "19:30",
                "Publicado"
            ),
            (
                "Menos Cliques, Mais Vendas: O Futuro do E-Commerce",
                "Twitter/X",
                "Direto & Persuasivo",
                "⚡ Reduzir 1 segundo no tempo de carregamento da sua loja online pode aumentar a taxa de conversão em até 27%. A velocidade não é um luxo, é faturação direta.",
                "#Ecommerce #WebPerformance #ConversionRate #TechTips #VendasOnline",
                "👇 Leia a nossa análise completa no blog da EJAJ TECH.",
                "Imagem de comparação de velocidade de carregamento (Antes vs Depois)",
                (today + timedelta(days=6)).strftime('%Y-%m-%d'),
                "09:45",
                "Agendado"
            ),
            (
                "Alimentação Saudável e Energia para o Trabalho",
                "Instagram",
                "Educacional & Inspirador",
                "🥗 Sabia que o que come ao almoço afeta diretamente o seu pico de atenção à tarde? Alimentos ricos em ómega-3 e antioxidantes ajudam a evitar a fadiga pós-refeição e mantêm a clareza mental.",
                "#NutricaoInteligente #SaudeCorporativa #BemEstar #FocoMental #VidaSaudavel",
                "📌 Guarde este post para planear as suas refeições da próxima semana!",
                "Carrossel com lista de 5 alimentos super-potentes para o cérebro",
                (today + timedelta(days=7)).strftime('%Y-%m-%d'),
                "12:30",
                "Rascunho"
            ),
            (
                "Workshop de Inteligência Artificial para Pequenas Empresas",
                "LinkedIn",
                "Profissional & Convocatório",
                "🤖 A Inteligência Artificial deixou de ser o futuro para se tornar o presente imediato da competitividade empresarial. No próximo dia 15, realizamos um workshop prático sobre como automatizar o atendimento ao cliente e a geração de marketing.",
                "#AI #InteligenciaArtificial #WorkshopTech #Automatizacao #InovacaoEmpresarial",
                "🎟️ Inscrições gratuitas mas limitadas! Garanta a sua vaga no link abaixo.",
                "Banner do evento com data, horário e destaques do programa",
                (today + timedelta(days=8)).strftime('%Y-%m-%d'),
                "16:00",
                "Agendado"
            )
        ]
        
        cursor.executemany('''
            INSERT INTO posts (topic, platform, tone, copy, hashtags, cta, media_suggestion, scheduled_date, scheduled_time, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_posts)
        
    conn.commit()
    conn.close()
    print("[OK] Base de dados posts.db inicializada com sucesso para SOCIALPOST AI.")

if __name__ == '__main__':
    init_db()
