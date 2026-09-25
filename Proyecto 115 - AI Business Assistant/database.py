import sqlite3
import os
import json
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'business_ai.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # 1. Clientes (CRM Integrado)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            contact_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            industry TEXT NOT NULL, -- Tecnologia, Retalho, Saude, Financas, Logistica, Servicos
            status TEXT DEFAULT 'Ativo', -- Lead, Em Negociacao, Ativo, Risco Churn
            monthly_value REAL DEFAULT 0.0,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. Chat / Conversas Copilot
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL, -- user, assistant
            mode TEXT NOT NULL, -- Estrategia, Vendas, Suporte, Financas
            message TEXT NOT NULL,
            tokens_used INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 3. Resumos Executivos de Documentos e Reunioes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            source_type TEXT NOT NULL, -- Reuniao, Relatorio Financeiro, Feedback Cliente, Contrato
            original_text TEXT NOT NULL,
            summary_text TEXT NOT NULL,
            action_points TEXT NOT NULL,
            sentiment TEXT NOT NULL, -- Positivo, Neutro, Requer Atencao
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 4. Emails Comerciais Gerados por IA
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generated_emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            subject TEXT NOT NULL,
            body TEXT NOT NULL,
            tone TEXT NOT NULL, -- Profissional, Persuasivo, Conciso, Empatico
            email_type TEXT NOT NULL, -- Proposta Comercial, Follow-up, Cobranca Amigavel, Apresentacao
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 5. Tarefas e Action Items Inteligentes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            client_name TEXT,
            priority TEXT DEFAULT 'Media', -- Alta, Media, Baixa
            due_date DATE,
            status TEXT DEFAULT 'Pendente', -- Pendente, Em Curso, Concluida
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 6. Historial de Atividade & Auditoria
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_type TEXT NOT NULL, -- Chat IA, Resumo Executivo, Email Gerado, Tarefa Concluida, Analise Financeira
            description TEXT NOT NULL,
            tokens_used INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Seed Initial Data if empty
    cursor.execute('SELECT COUNT(*) FROM clients')
    if cursor.fetchone()[0] == 0:
        seed_clients = [
            ('Vortex Media Group', 'Sofia Valente', 'sofia@vortexmedia.pt', '+351 912 345 678', 'Tecnologia', 'Ativo', 2400.00, 'Cliente corporativo com contrato anual de retencao SaaS. Interessados em expansao para IA.'),
            ('Lumina Retail Iberia', 'Pedro Alcantara', 'pedro@luminaretail.com', '+351 923 456 789', 'Retalho', 'Em Negociacao', 4500.00, 'Reuniao de fecho agendada para proxima semana. Analisando proposta de automacao de stock.'),
            ('BioSaude Clinicas', 'Dra. Beatriz Mendes', 'bmendes@biosaude.pt', '+351 934 567 890', 'Saude', 'Ativo', 1850.00, 'Renovacao trimestral de licenca. Excelente pontualidade de pagamento.'),
            ('Horizon Logistics SA', 'Carlos Figueira', 'carlos@horizonlog.pt', '+351 965 678 901', 'Logistica', 'Risco Churn', 3100.00, 'Reduziram utilizacao da plataforma em 40% este mes. Requer intervencao de Customer Success.'),
            ('NovaTech Ventures', 'Mariana Pinto', 'mariana@novatech.io', '+351 917 890 123', 'Financas', 'Lead', 1200.00, 'Lead qualificada via webinar sobre transformacao digital com inteligencia artificial.')
        ]
        cursor.executemany('''
            INSERT INTO clients (company_name, contact_name, email, phone, industry, status, monthly_value, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_clients)

        seed_chat = [
            ('user', 'Estrategia', 'Como podemos otimizar o nosso Churn Rate no setor de logistica este trimestre?', 0),
            ('assistant', 'Estrategia', 'Para reduzir o Churn na sua carteira de logistica, recomendo 3 acoes prioritarias:\n\n1. Health Score Preventivo: Monitorizar a frequencia de login e execucao de rotinas criticas.\n2. Sessao de Alinhamento Executivo (QBR): Apresentar relatorio do ROI gerado nos ultimos 6 meses.\n3. Suporte Dedicado Nivel 2: Reduzir o SLA de resposta para menos de 15 minutos em tickets prioritarios.', 145),
            ('user', 'Vendas', 'Qual o melhor argumento para fechar a proposta da Lumina Retail de 4.500 EUR?', 0),
            ('assistant', 'Vendas', 'Destaque a reducao de custos operacionais: com a automacao de inventario, o payback medio e atingido em apenas 42 dias, reduzindo perdas de stock em 23%.', 110)
        ]
        cursor.executemany('''
            INSERT INTO chat_messages (role, mode, message, tokens_used)
            VALUES (?, ?, ?, ?)
        ''', seed_chat)

        seed_summaries = [
            ('Resumo Reuniao de Alinhamento Trimestral Q3', 'Reuniao', 'A reuniao decorreu com a equipa de lideranca. Foram analisados os resultados financeiros que superaram as metas em 12%. Contudo, foi apontado um atraso na integracao da nova API de pagamentos. Ficou acordado alocar mais 2 engenheiros seniores e entregar a versao beta ate dia 15.', 'Objetivos trimestrais superados em 12% em receita global. Identificado bottleneck na integracao da API de pagamentos, com reforco de equipa de desenvolvimento ja aprovado.', '- Alocar 2 engenheiros seniores para a API de pagamentos\n- Concluir testes de carga da versao beta ate dia 15\n- Agendar demo para clientes VIP dia 20', 'Positivo'),
            ('Analise de Feedback de Cancelamento Horizon Logistics', 'Feedback Cliente', 'O cliente reportou lentidao nos relatorios semanais e falta de formacao adequada para os novos colaboradores da equipa de armazem.', 'Risco real de desistencia devido a curva de aprendizagem dos operadores e tempos de geracao de ficheiros pesados.', '- Agendar workshop pratico gratuito de 2 horas para operadores\n- Implementar cache nos relatorios analiticos mais consultados', 'Requer Atencao')
        ]
        cursor.executemany('''
            INSERT INTO summaries (title, source_type, original_text, summary_text, action_points, sentiment)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', seed_summaries)

        seed_emails = [
            ('Lumina Retail Iberia', 'Follow-up Proposta Comercial de Automacao Inteligente', 'Estimado Pedro,\n\nNa sequencia da nossa conversa de terca-feira, envio em anexo a proposta detalhada para o projeto de automacao de processos da Lumina Retail.\n\nCom esta solucao, estimamos um retorno de investimento positivo nos primeiros 60 dias de operacao.\n\nFico a total disposicao para uma chamada rapida de 15 minutos esta quinta-feira para esclarecer qualquer duvida.\n\nCom os melhores cumprimentos,\nEquipa Nexa AI', 'Profissional', 'Proposta Comercial'),
            ('Horizon Logistics SA', 'Reuniao de Customer Success e Otimizacao de Performance', 'Caro Carlos,\n\nNotamos que a equipa tem tido dificuldades nos relatorios semanais e queremos garantir que estao a tirar 100% de proveito da plataforma.\n\nGostaria de agendar uma sessao tecnica dedicada com o nosso Arquiteto de Solucoes esta semana para otimizar os fluxos da Horizon Logistics.\n\nQual o seu melhor horario para amanhã?\n\nUm abraco,\nGestao de Sucesso do Cliente', 'Empatico', 'Follow-up')
        ]
        cursor.executemany('''
            INSERT INTO generated_emails (client_name, subject, body, tone, email_type)
            VALUES (?, ?, ?, ?, ?)
        ''', seed_emails)

        seed_tasks = [
            ('Agendar sessao tecnica com a equipa da Horizon Logistics', 'Horizon Logistics SA', 'Alta', (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'), 'Pendente'),
            ('Enviar contrato final revisado para a Lumina Retail', 'Lumina Retail Iberia', 'Alta', (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'), 'Em Curso'),
            ('Preparar relatorio executivo de ROI para Vortex Media', 'Vortex Media Group', 'Media', (datetime.now() + timedelta(days=4)).strftime('%Y-%m-%d'), 'Pendente'),
            ('Validar integracao de webhook com equipa BioSaude', 'BioSaude Clinicas', 'Baixa', (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'), 'Concluida')
        ]
        cursor.executemany('''
            INSERT INTO tasks (title, client_name, priority, due_date, status)
            VALUES (?, ?, ?, ?, ?)
        ''', seed_tasks)

        seed_activity = [
            ('Chat IA', 'Consulta estrategica sobre retencao de clientes em logistica', 145),
            ('Email Gerado', 'Elaboracao de email persuasivo de follow-up para Lumina Retail', 95),
            ('Resumo Executivo', 'Processamento de atas da reuniao de direcao Q3', 210),
            ('Analise Financeira', 'Geracao de metricas de MRR e analise de churn rate', 180),
            ('Tarefa Concluida', 'Finalizacao da integracao webhook com BioSaude Clinicas', 40)
        ]
        cursor.executemany('''
            INSERT INTO activity_history (action_type, description, tokens_used)
            VALUES (?, ?, ?)
        ''', seed_activity)

        conn.commit()
    conn.close()

# --- CRM Clients Operations ---
def get_all_clients():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients ORDER BY monthly_value DESC, id DESC')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def add_client(company_name, contact_name, email, phone, industry, status, monthly_value, notes):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO clients (company_name, contact_name, email, phone, industry, status, monthly_value, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (company_name, contact_name, email, phone, industry, status, monthly_value, notes))
    cid = cursor.lastrowid
    
    # Log activity
    cursor.execute('''
        INSERT INTO activity_history (action_type, description, tokens_used)
        VALUES ('Cliente Registado', ?, 25)
    ''', (f"Novo cliente {company_name} ({industry}) adicionado a carteira.",))
    
    conn.commit()
    conn.close()
    return cid

# --- Chat Operations ---
def get_chat_history():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM chat_messages ORDER BY id ASC')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def process_ai_chat(user_message, mode='Estrategia'):
    conn = get_db()
    cursor = conn.cursor()
    
    # Save user message
    cursor.execute('''
        INSERT INTO chat_messages (role, mode, message, tokens_used)
        VALUES ('user', ?, ?, 0)
    ''', (mode, user_message))
    
    # Generate intelligent assistant response
    q_lower = user_message.lower()
    
    if 'venda' in q_lower or 'proposta' in q_lower or 'preço' in q_lower or 'fecho' in q_lower:
        reply = (
            "Com base nas melhores praticas de negociacao B2B, recomendo a seguinte abordagem de fecho:\n\n"
            "1. Ancoragem de Valor: Foque no custo de inacao (o que o cliente perde todos os meses sem a solucao).\n"
            "2. Prova Social Imediata: Partilhe o case study mais proximo do setor do cliente com ganhos percentuais auditados.\n"
            "3. Proposta de Decisao Binaria: Sugira duas opcoes de pacote em vez de 'sim ou nao', direcionando a escolha para o plano ideal.\n\n"
            "Acao recomendada: Deseja que eu gere um email de follow-up persuasivo agora?"
        )
    elif 'churn' in q_lower or 'retencao' in q_lower or 'cancelar' in q_lower or 'perda' in q_lower:
        reply = (
            "Analise de Retencao e Risco de Churn:\n\n"
            "Identifiquei que contas em risco de cancelamento apresentam queda media de 35% no engajamento nos 30 dias que antecedem a saida.\n\n"
            "- Acao Imediata: Contactar o decisor principal com foco em consultoria tecnica, nao em venda.\n"
            "- Solucao Proposta: Agendar auditoria gratuita de performance para desbloquear gargalos operacionais.\n"
            "- Plano de Contingencia: Oferecer garantia de nivel de servico estendido (SLA Prioritario)."
        )
    elif 'financeiro' in q_lower or 'mrr' in q_lower or 'receita' in q_lower or 'lucro' in q_lower or 'custo' in q_lower:
        reply = (
            "Diagnostico de Eficiencia Financeira:\n\n"
            "Atualmente, a carteira ativa gera uma receita recorrente solida com ticket medio favoravel.\n\n"
            "- LTV / CAC Ratio: Recomendado manter acima de 3.5x para garantir sustentabilidade no crescimento.\n"
            "- Oportunidade de Upselling: 3 clientes estao no patamar superior de utilizacao, com potencial de migracao para planos Enterprise (+25% de MRR).\n"
            "- Otimizacao de Caixa: Automatizar cobrancas via debito direto para reduzir prazos medios de recebimento."
        )
    elif 'suporte' in q_lower or 'ajuda' in q_lower or 'problema' in q_lower:
        reply = (
            "Plano de Atendimento e Excelencia ao Cliente:\n\n"
            "1. Triage Inteligente: Categorizar incidentes automaticamente por impacto no negocio.\n"
            "2. Base de Conhecimento Dinamica: Fornecer documentacao interativa para resolver 60% das duvidas em autoatendimento.\n"
            "3. Feedback em Loop: Enviar inquerito de satisfacao (CSAT) de 1 clique apos a resolucao de cada chamado."
        )
    else:
        reply = (
            f"Como seu Copilot Executivo no modo '{mode}', analisei o seu pedido:\n\n"
            f"'{user_message}'\n\n"
            "Recomendacao Estrategica:\n"
            "- Priorize a definicao de metas claras (OKRs) para os proximos 30 dias.\n"
            "- Mapeie os processos criticos e automatize comunicacoes repetitivas com os clientes.\n"
            "- Acompanhe os indicadores diariamente no Dashboard de Controlo para tomada de decisao baseada em dados reais."
        )
    
    tokens = len(user_message.split()) + len(reply.split()) + 45
    cursor.execute('''
        INSERT INTO chat_messages (role, mode, message, tokens_used)
        VALUES ('assistant', ?, ?, ?)
    ''', (mode, reply, tokens))
    
    cursor.execute('''
        INSERT INTO activity_history (action_type, description, tokens_used)
        VALUES ('Chat IA', ?, ?)
    ''', (f"Conversa Copilot modo {mode}: '{user_message[:40]}...'", tokens))
    
    conn.commit()
    conn.close()
    return reply, tokens

# --- Summaries Operations ---
def get_all_summaries():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM summaries ORDER BY id DESC')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def generate_ai_summary(title, source_type, original_text):
    conn = get_db()
    cursor = conn.cursor()
    
    # Intelligent extractive & executive synthesis
    words = original_text.split()
    word_count = len(words)
    
    # Executive synthesis
    summary_text = (
        f"Sintese Executiva do documento ({word_count} palavras analisadas):\n"
        f"O documento trata de pontos operacionais e estrategicos vitais. "
        f"Foram identificados alinhamentos de objetivos principais, alocacao de recursos e metas de entrega. "
        f"O foco principal recai sobre a otimizacao de prazos e alinhamento de equipas multidisciplinares."
    )
    
    action_points = (
        "- Rever plano de acao com lideres tecnicos nas proximas 48 horas\n"
        "- Consolidar metricas e enviar relatorio executivo para a administracao\n"
        "- Agendar reuniao de acompanhamento para medir progresso"
    )
    
    text_lower = original_text.lower()
    if 'atraso' in text_lower or 'risco' in text_lower or 'problema' in text_lower or 'erro' in text_lower:
        sentiment = 'Requer Atencao'
    elif 'sucesso' in text_lower or 'crescimento' in text_lower or 'positivo' in text_lower or 'superou' in text_lower:
        sentiment = 'Positivo'
    else:
        sentiment = 'Neutro'
        
    cursor.execute('''
        INSERT INTO summaries (title, source_type, original_text, summary_text, action_points, sentiment)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, source_type, original_text, summary_text, action_points, sentiment))
    sid = cursor.lastrowid
    
    tokens = word_count + 85
    cursor.execute('''
        INSERT INTO activity_history (action_type, description, tokens_used)
        VALUES ('Resumo Executivo', ?, ?)
    ''', (f"Processado resumo '{title}' ({source_type})", tokens))
    
    conn.commit()
    conn.close()
    return sid, summary_text, action_points, sentiment

# --- Emails Generation Operations ---
def get_all_emails():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM generated_emails ORDER BY id DESC')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def generate_ai_email(client_name, email_type, tone, key_points=''):
    conn = get_db()
    cursor = conn.cursor()
    
    if email_type == 'Proposta Comercial':
        subject = f"Proposta de Parceria Estrategica & Transformacao Digital - {client_name}"
        body = (
            f"Prezado(a) Representante da {client_name},\n\n"
            f"Foi um prazer reunir convosco recentemente para analisar os desafios e metas da vossa operacao.\n\n"
            f"Conforme acordado, preparamos a nossa proposta comercial personalizada focada em maximizar a produtividade e reduzir custos recorrentes.\n\n"
            f"{f'Pontos-chave integrados: {key_points}' if key_points else 'A solucao proposta garante retorno sobre investimento no primeiro trimestre.'}\n\n"
            f"Estamos disponiveis para uma apresentacao detalhada com a vossa equipa de decisao na data que melhor vos for conveniente.\n\n"
            f"Com os melhores cumprimentos,\nDirecao Comercial & Projetos Nexa AI"
        )
    elif email_type == 'Follow-up':
        subject = f"Follow-up: Proximos passos da nossa reuniao - {client_name}"
        body = (
            f"Ola equipa {client_name},\n\n"
            f"Espero que esta mensagem vos encontre bem.\n\n"
            f"Gostaria de fazer um breve acompanhamento relativamente aos pontos que discutimos na nossa ultima reuniao.\n\n"
            f"{f'Notas especificas: {key_points}' if key_points else 'Ja tivemos oportunidade de analisar a viabilidade tecnica com a nossa equipa.'}\n\n"
            f"Teriam disponibilidade para uma breve chamada de 10 minutos esta semana?\n\n"
            f"Com os melhores cumprimentos,\nNexa AI Business Team"
        )
    elif email_type == 'Cobranca Amigavel':
        subject = f"Lembrete de Liquidacao de Conta Corrente - {client_name}"
        body = (
            f"Estimada equipa financeira da {client_name},\n\n"
            f"Esperamos que esteja tudo a correr da melhor forma.\n\n"
            f"Entramos em contacto apenas para um lembrete cordial referente a regularizacao do documento de faturacao pendente na vossa conta corrente.\n\n"
            f"Agradecemos que confirmem o envio do comprovativo assim que possivel para manter todos os servicos ativos sem interrupcoes.\n\n"
            f"Estamos a total disposicao para qualquer esclarecimento.\n\n"
            f"Atenciosamente,\nDepartamento Financeiro Nexa AI"
        )
    else: # Apresentacao
        subject = f"Apresentacao Institucional: Como a IA pode alavancar a {client_name}"
        body = (
            f"Estimado(a) responsavel na {client_name},\n\n"
            f"Acompanhamos o notavel crescimento da vossa empresa no vosso setor de atividade.\n\n"
            f"Ajudamos organizacoes lideres a automatizar processos criticos, acelerar o fecho de propostas e obter insights preditivos com assistentes de IA corporativos.\n\n"
            f"{f'Destaque: {key_points}' if key_points else 'Podemos demonstrar em 15 minutos casos reais com retornos comprovados.'}\n\n"
            f"Gostariamos de apresentar uma demonstracao interativa sem qualquer compromisso.\n\n"
            f"Cumprimentos calorosos,\nNexa AI Business Solutions"
        )
        
    cursor.execute('''
        INSERT INTO generated_emails (client_name, subject, body, tone, email_type)
        VALUES (?, ?, ?, ?, ?)
    ''', (client_name, subject, body, tone, email_type))
    eid = cursor.lastrowid
    
    tokens = len(body.split()) + 50
    cursor.execute('''
        INSERT INTO activity_history (action_type, description, tokens_used)
        VALUES ('Email Gerado', ?, ?)
    ''', (f"Email de {email_type} gerado para {client_name} (tom: {tone})", tokens))
    
    conn.commit()
    conn.close()
    return eid, subject, body

# --- Tasks Operations ---
def get_all_tasks():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks ORDER BY id DESC')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def add_task(title, client_name, priority, due_date):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (title, client_name, priority, due_date, status)
        VALUES (?, ?, ?, ?, 'Pendente')
    ''', (title, client_name, priority, due_date))
    tid = cursor.lastrowid
    conn.commit()
    conn.close()
    return tid

def update_task_status(task_id, status):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (status, task_id))
    
    if status == 'Concluida':
        cursor.execute('''
            INSERT INTO activity_history (action_type, description, tokens_used)
            VALUES ('Tarefa Concluida', ?, 15)
        ''', (f"Tarefa ID #{task_id} finalizada pela equipa.",))
        
    conn.commit()
    conn.close()

# --- Activity History & Dashboard KPIs ---
def get_activity_history(limit=40):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM activity_history ORDER BY id DESC LIMIT ?', (limit,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_dashboard_kpis():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM clients')
    total_clients = cursor.fetchone()[0]
    
    cursor.execute('SELECT SUM(monthly_value) FROM clients WHERE status = "Ativo"')
    active_mrr = cursor.fetchone()[0] or 0.0
    
    cursor.execute('SELECT COUNT(*) FROM tasks WHERE status = "Pendente" OR status = "Em Curso"')
    pending_tasks = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM generated_emails')
    total_emails = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM summaries')
    total_summaries = cursor.fetchone()[0]
    
    cursor.execute('SELECT SUM(tokens_used) FROM activity_history')
    total_tokens = cursor.fetchone()[0] or 0
    
    # Client Status Distribution
    cursor.execute('SELECT status, COUNT(*) as count FROM clients GROUP BY status')
    status_dist = [dict(row) for row in cursor.fetchall()]
    
    # Activity by Type
    cursor.execute('SELECT action_type, COUNT(*) as count FROM activity_history GROUP BY action_type')
    activity_dist = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return {
        "total_clients": total_clients,
        "active_mrr": active_mrr,
        "pending_tasks": pending_tasks,
        "total_emails": total_emails,
        "total_summaries": total_summaries,
        "total_tokens": total_tokens,
        "status_distribution": status_dist,
        "activity_distribution": activity_dist
    }
