import os
import sqlite3
import random
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, Response, redirect, url_for
from database import DB_PATH, init_db

app = Flask(__name__)
app.secret_key = 'socialpost_ai_secret_key_ejajtech'

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

# Helper generator logic
TEMPLATES_COPY = {
    "Instagram": [
        "✨ {topic} é o segredo para transformar os seus resultados! Na era digital, quem domina esta estratégia posiciona-se à frente no mercado.\n\n📌 3 passos essenciais:\n1️⃣ Defina o objetivo claro da sua mensagem.\n2️⃣ Crie ganchos visuais irresistíveis nos primeiros 3 segundos.\n3️⃣ Interaja ativamente com a sua audiência.\n\nQual destas etapas é o maior desafio na sua empresa?",
        "🔥 Atenção! Se deseja elevar a sua marca, precisa de dominar {topic}.\n\nA maior parte das marcas falha porque foca nos atributos em vez dos benefícios reais para o cliente. Quando muda a perspetiva, a conversão dispara!\n\nPronto para dar o próximo passo?",
        "💡 Sabia que {topic} pode aumentar o envolvimento da sua conta em até 40%?\n\nA nossa equipa na EJAJ TECH testou e comprovou: o conteúdo bem estruturado gera confiança imediata e atrai clientes qualificados sem necessidade de orçamentos gigantescos."
    ],
    "LinkedIn": [
        "🚀 No cenário empresarial atual, {topic} tornou-se um pilar estratégico indispensável para equipas de alta performance.\n\nComo líderes e gestores, é nossa responsabilidade otimizar processos e adotar ferramentas que garantam eficiência e consistência de longo prazo.\n\nAs 3 principais tendências que observamos:\n• Digitalização e automação inteligente\n• Análise de dados orientada a decisões\n• Comunicação transparente com os stakeholders\n\nPartilhe a sua perspetiva nos comentários abaixo.",
        "📊 Reflectindo sobre a evolução de {topic} no nosso setor...\n\nAs empresas que investem em inovação contínua e na capacitação das suas equipas alcançam resultados sustentáveis 3x mais rápido.\n\nA questão não é SE deve adotar esta abordagem, mas sim QUANDO e COMO executá-la com excelência."
    ],
    "TikTok": [
        "🔥 Ninguém te contou isto sobre {topic}! 😱\n\nSe queres explodir os teus resultados esta semana, faz exatamente isto nos teus próximos posts:\n1. Aplica o gancho visual no 1º segundo\n2. Mantém o ritmo dinâmico\n3. Finaliza com uma pergunta forte!\n\nSalva este vídeo para não esqueceres! 📌",
        "⚡ O erro nº 1 que toda a gente comete ao trabalhar com {topic}! 👇\n\nParas de perder tempo com estratégias desatualizadas. Assiste até ao fim para veres a solução rápida e eficaz!"
    ],
    "Twitter/X": [
        "⚡ {topic} em 3 frases curtas:\n\n1. O conteúdo certo no momento certo cria autoridade.\n2. A consistência diária vence o talento esporádico.\n3. Medir métricas reais é o único caminho para escalar.\n\nConcorda? RT para espalhar!",
        "💡 Dica rápida de produtividade sobre {topic}:\nReduza os processos manuais, automatize a publicação e foque 100% na criação de valor para o seu cliente final."
    ],
    "Facebook": [
        "📢 Novidade imperdível para os nossos clientes e parceiros! Hoje queremos partilhar uma reflexão importante sobre {topic}.\n\nAcreditamos que a inovação constante e a atenção ao detalhe são o segredo para construir relações de confiança a longo prazo.\n\nVisite o nosso website e descubra como podemos ajudar a sua empresa a crescer!"
    ]
}

HASHTAG_PACKS = {
    "Tecnologia & SaaS": ["#SaaS", "#TechTrends", "#SoftwareEngineers", "#InovacaoDigital", "#EJAJTECH", "#StartupPortugal", "#AI"],
    "Marketing & Redes Sociais": ["#SocialMediaMarketing", "#ContentStrategy", "#MarketingDigital", "#Copywriting", "#Hashtags", "#Branding"],
    "Negócios & Empreendedorismo": ["#Empreendedorismo", "#BusinessGrowth", "#Lideranca", "#GestaoEmpresarial", "#Sucesso", "#Networking"],
    "Fitness & Saúde": ["#SaudeEBemEstar", "#VidaSaudavel", "#FitnessMotivation", "#TreinoDiario", "#Nutricao", "#Mindset"],
    "Geral": ["#Inovacao", "#PortugalTech", "#DicasUteis", "#Tendencias2026", "#Qualidade", "#SucessoGarantido"]
}

CTA_OPTIONS = {
    "Vendas": "🛍️ Clique no link da bio e aproveite a nossa oferta especial hoje mesmo!",
    "Engagement": "💬 Deixe a sua opinião nos comentários: qual é a sua experiência com este tema?",
    "Leads": "📩 Envie-nos uma mensagem privada ou solicite uma demonstração gratuita no nosso site!",
    "Partilha": "🔄 Partilhe este post com alguém que precisa de ver estas dicas hoje!",
    "Guardar": "📌 Guarde este post para consultar mais tarde quando estiver a planear a sua estratégia!"
}

MEDIA_SUGGESTIONS = [
    "Carrossel interativo de 5 slides com design minimalista e contraste alto",
    "Reels/Short de 15 segundos com texto sobreposto dinâmico e transições rápidas",
    "Infográfico limpo com métricas e ícones explicativos",
    "Fotografia profissional HD com o produto/serviço em contexto real",
    "Vídeo POV dos bastidores da equipa a trabalhar no projeto"
]

@app.route('/')
def index():
    conn = get_db_connection()
    recent_posts = [dict(r) for r in conn.execute('SELECT * FROM posts ORDER BY id DESC LIMIT 5').fetchall()]
    total_posts = conn.execute('SELECT COUNT(*) FROM posts').fetchone()[0]
    scheduled_count = conn.execute("SELECT COUNT(*) FROM posts WHERE status = 'Agendado'").fetchone()[0]
    conn.close()
    return render_template('index.html', recent_posts=recent_posts, total_posts=total_posts, scheduled_count=scheduled_count)

@app.route('/calendar')
def calendar():
    conn = get_db_connection()
    posts = [dict(r) for r in conn.execute('SELECT * FROM posts ORDER BY scheduled_date ASC, scheduled_time ASC').fetchall()]
    conn.close()
    return render_template('calendar.html', posts=posts)

@app.route('/library')
def library():
    conn = get_db_connection()
    platform_filter = request.args.get('platform', '')
    status_filter = request.args.get('status', '')
    
    query = 'SELECT * FROM posts WHERE 1=1'
    params = []
    
    if platform_filter:
        query += ' AND platform = ?'
        params.append(platform_filter)
    if status_filter:
        query += ' AND status = ?'
        params.append(status_filter)
        
    query += ' ORDER BY id DESC'
    posts = [dict(r) for r in conn.execute(query, params).fetchall()]
    conn.close()
    return render_template('library.html', posts=posts, platform_filter=platform_filter, status_filter=status_filter)

@app.route('/analytics')
def analytics():
    conn = get_db_connection()
    posts_by_platform = [dict(r) for r in conn.execute('SELECT platform, COUNT(*) as count FROM posts GROUP BY platform').fetchall()]
    posts_by_status = [dict(r) for r in conn.execute('SELECT status, COUNT(*) as count FROM posts GROUP BY status').fetchall()]
    total_posts = conn.execute('SELECT COUNT(*) FROM posts').fetchone()[0]
    conn.close()
    return render_template('analytics.html', posts_by_platform=posts_by_platform, posts_by_status=posts_by_status, total_posts=total_posts)

@app.route('/api/generate', methods=['POST'])
def api_generate():
    data = request.json or {}
    topic = data.get('topic', 'Inovação e Produtividade').strip()
    platform = data.get('platform', 'Instagram')
    tone = data.get('tone', 'Profissional & Educacional')
    cta_type = data.get('cta_type', 'Engagement')
    
    # Pick copy template
    templates = TEMPLATES_COPY.get(platform, TEMPLATES_COPY['Instagram'])
    raw_template = random.choice(templates)
    copy_generated = raw_template.format(topic=topic)
    
    # Pick hashtags
    niche_pack = HASHTAG_PACKS.get("Tecnologia & SaaS") + HASHTAG_PACKS.get("Marketing & Redes Sociais") + HASHTAG_PACKS.get("Geral")
    selected_tags = random.sample(niche_pack, min(6, len(niche_pack)))
    hashtags_generated = " ".join(selected_tags)
    
    # Pick CTA
    cta_generated = CTA_OPTIONS.get(cta_type, CTA_OPTIONS['Engagement'])
    
    # Media suggestion
    media_generated = random.choice(MEDIA_SUGGESTIONS)
    
    return jsonify({
        'success': True,
        'topic': topic,
        'platform': platform,
        'tone': tone,
        'copy': copy_generated,
        'hashtags': hashtags_generated,
        'cta': cta_generated,
        'media_suggestion': media_generated
    })

@app.route('/api/posts/save', methods=['POST'])
def api_save_post():
    data = request.json or {}
    topic = data.get('topic', 'Novo Conteúdo')
    platform = data.get('platform', 'Instagram')
    tone = data.get('tone', 'Profissional')
    copy_text = data.get('copy', '')
    hashtags = data.get('hashtags', '')
    cta = data.get('cta', '')
    media_suggestion = data.get('media_suggestion', '')
    scheduled_date = data.get('scheduled_date', (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'))
    scheduled_time = data.get('scheduled_time', '12:00')
    status = data.get('status', 'Agendado')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO posts (topic, platform, tone, copy, hashtags, cta, media_suggestion, scheduled_date, scheduled_time, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (topic, platform, tone, copy_text, hashtags, cta, media_suggestion, scheduled_date, scheduled_time, status))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'success': True, 'id': new_id, 'message': 'Post guardado no calendário com sucesso!'})

@app.route('/api/posts/schedule', methods=['POST'])
def api_schedule_post():
    data = request.json or {}
    post_id = data.get('id')
    scheduled_date = data.get('scheduled_date')
    scheduled_time = data.get('scheduled_time')
    status = data.get('status', 'Agendado')
    
    if not post_id:
        return jsonify({'success': False, 'message': 'ID de post em falta'}), 400
        
    conn = get_db_connection()
    conn.execute('''
        UPDATE posts SET scheduled_date = ?, scheduled_time = ?, status = ? WHERE id = ?
    ''', (scheduled_date, scheduled_time, status, post_id))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Agendamento atualizado com êxito!'})

@app.route('/api/posts/delete/<int:post_id>', methods=['DELETE'])
def api_delete_post(post_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Post eliminado com sucesso!'})

@app.route('/api/export')
def api_export():
    fmt = request.args.get('format', 'json')
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts ORDER BY id DESC').fetchall()
    conn.close()
    
    posts_list = [dict(row) for row in posts]
    
    if fmt == 'json':
        return Response(
            json.dumps(posts_list, indent=2, ensure_ascii=False),
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment;filename=socialpost_calendar.json'}
        )
    elif fmt == 'csv':
        csv_lines = ["ID,Tema,Plataforma,Tom,Copy,Hashtags,CTA,Data,Hora,Estado"]
        for p in posts_list:
            copy_clean = p['copy'].replace('\n', ' ').replace(',', ';')
            csv_lines.append(f"{p['id']},\"{p['topic']}\",\"{p['platform']}\",\"{p['tone']}\",\"{copy_clean}\",\"{p['hashtags']}\",\"{p['cta']}\",\"{p['scheduled_date']}\",\"{p['scheduled_time']}\",\"{p['status']}\"")
        csv_data = "\n".join(csv_lines)
        return Response(
            csv_data,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment;filename=socialpost_calendar.csv'}
        )
    return jsonify({'error': 'Formato inválido'}), 400

if __name__ == '__main__':
    print("[SERVER] SOCIALPOST AI SaaS a iniciar na porta 6350...")
    app.run(host='0.0.0.0', port=6350, debug=False)
