import sqlite3
import os
import json
import time
import random
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'automations.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # 1. Integrations (Connected Apps & Services)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS integrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            service_key TEXT UNIQUE NOT NULL,
            icon TEXT NOT NULL,
            category TEXT NOT NULL, -- Comunicação, Pagamentos, Produtividade, IA, Dados
            auth_type TEXT NOT NULL, -- API Key, Webhook, OAuth2
            status TEXT DEFAULT 'Conectado', -- Conectado, Desconectado, Pendente
            connected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            config_data TEXT
        )
    ''')

    # 2. Triggers (Disparadores de Eventos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS triggers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            integration_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            event_type TEXT UNIQUE NOT NULL,
            description TEXT NOT NULL,
            icon TEXT NOT NULL,
            sample_payload TEXT NOT NULL,
            FOREIGN KEY (integration_id) REFERENCES integrations(id)
        )
    ''')

    # 3. Actions (Tarefas Executadas)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            integration_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            action_type TEXT UNIQUE NOT NULL,
            description TEXT NOT NULL,
            icon TEXT NOT NULL,
            FOREIGN KEY (integration_id) REFERENCES integrations(id)
        )
    ''')

    # 4. Workflows (Fluxos Automatizados)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workflows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            trigger_id INTEGER NOT NULL,
            action_id INTEGER NOT NULL,
            condition_field TEXT, -- ex: amount, status, priority, email
            condition_operator TEXT, -- >, <, ==, !=, contains
            condition_value TEXT, -- ex: 100, VIP, high
            action_template TEXT, -- Template de mensagem / dados para envio
            is_active INTEGER DEFAULT 1,
            total_runs INTEGER DEFAULT 0,
            success_runs INTEGER DEFAULT 0,
            last_run_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (trigger_id) REFERENCES triggers(id),
            FOREIGN KEY (action_id) REFERENCES actions(id)
        )
    ''')

    # 5. Execution History (Logs de Execução em Tempo Real)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS execution_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workflow_id INTEGER NOT NULL,
            workflow_title TEXT NOT NULL,
            trigger_name TEXT NOT NULL,
            action_name TEXT NOT NULL,
            status TEXT NOT NULL, -- Sucesso, Filtrado, Erro
            execution_time_ms INTEGER NOT NULL,
            input_payload TEXT,
            output_payload TEXT,
            error_message TEXT,
            executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (workflow_id) REFERENCES workflows(id)
        )
    ''')

    # Seed Initial Data if empty
    cursor.execute('SELECT COUNT(*) FROM integrations')
    if cursor.fetchone()[0] == 0:
        seed_integrations = [
            ('Stripe Payments', 'stripe', 'fa-brands fa-stripe', 'Pagamentos', 'API Key', 'Conectado', '{"webhook_endpoint": "https://api.autoflow.dev/v1/wh/stripe", "mode": "live"}'),
            ('Slack Corporate', 'slack', 'fa-brands fa-slack', 'Comunicação', 'OAuth2', 'Conectado', '{"default_channel": "#vendas-alertas", "team_id": "T099881"}'),
            ('Gmail / Google Workspace', 'gmail', 'fa-solid fa-envelope', 'Comunicação', 'OAuth2', 'Conectado', '{"sender": "notifications@empresa.com", "daily_quota": 2000}'),
            ('Webhooks HTTP', 'webhook', 'fa-solid fa-network-wired', 'Dados', 'Webhook URL', 'Conectado', '{"secret_header": "X-AutoFlow-Signature"}'),
            ('Google Sheets', 'sheets', 'fa-solid fa-table', 'Produtividade', 'OAuth2', 'Conectado', '{"spreadsheet_id": "1A2B3C4D5E_SHEET_LEADS"}'),
            ('OpenAI GPT-4o', 'openai', 'fa-solid fa-robot', 'IA', 'API Key', 'Conectado', '{"model": "gpt-4o", "temperature": 0.3}'),
            ('Discord Community', 'discord', 'fa-brands fa-discord', 'Comunicação', 'Webhook URL', 'Conectado', '{"webhook_url": "https://discord.com/api/webhooks/999/xxx"}')
        ]
        cursor.executemany('''
            INSERT INTO integrations (name, service_key, icon, category, auth_type, status, config_data)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', seed_integrations)

        seed_triggers = [
            (1, 'Novo Pagamento Aprovado', 'stripe.payment_intent.succeeded', 'Dispara sempre que um cliente conclui um pagamento com sucesso.', 'fa-credit-card', '{"amount": 250.00, "currency": "eur", "customer_email": "carlos.silva@corp.pt", "tier": "Enterprise"}'),
            (4, 'Webhook Recebido (JSON Payload)', 'webhook.payload.received', 'Dispara ao receber requisição HTTP POST no endpoint seguro.', 'fa-satellite-dish', '{"event": "lead_submission", "lead_score": 85, "company": "Vortex Media", "email": "info@vortex.io"}'),
            (3, 'Novo Email com Assunto Relevante', 'gmail.email.received', 'Dispara quando entra email com palavras-chave prioritárias.', 'fa-inbox', '{"sender": "ceo@startup.co", "subject": "Urgente: Proposta Parceria", "priority": "high"}'),
            (4, 'Cron / Agendador Recorrente', 'cron.schedule.hourly', 'Dispara de hora em hora para rotinas de sincronização e backup.', 'fa-clock', '{"timestamp": "2026-09-25T07:00:00Z", "batch_size": 50}')
        ]
        cursor.executemany('''
            INSERT INTO triggers (integration_id, name, event_type, description, icon, sample_payload)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', seed_triggers)

        seed_actions = [
            (2, 'Enviar Mensagem para Canal Slack', 'slack.post_message', 'Publica notificação formatada com blocos ricos num canal do Slack.', 'fa-hashtag'),
            (3, 'Enviar Email Transacional Automático', 'gmail.send_message', 'Dispara email personalizado com anexos ou templates HTML.', 'fa-paper-plane'),
            (5, 'Adicionar Linha em Google Sheets', 'sheets.append_row', 'Regista os dados da transação ou lead numa folha de cálculo.', 'fa-file-excel'),
            (7, 'Notificar Servidor Discord', 'discord.send_embed', 'Envia um embed colorido com alerta para moderadores/equipa.', 'fa-bell'),
            (6, 'Análise de Texto com IA (OpenAI)', 'openai.analyze_sentiment', 'Processa o conteúdo recebido com inteligência artificial para resumo ou classificação.', 'fa-brain')
        ]
        cursor.executemany('''
            INSERT INTO actions (integration_id, name, action_type, description, icon)
            VALUES (?, ?, ?, ?, ?)
        ''', seed_actions)

        seed_workflows = [
            ('Alerta Slack: Vendas Enterprise Stripe', 'Notifica a equipa no canal #vendas sempre que entra uma faturacao acima de 100 EUR.', 1, 1, 'amount', '>', '100', '[ALERTA] Novo pagamento confirmado de {{amount}} EUR de {{customer_email}}!', 1, 42, 40),
            ('Sincronizacao de Novos Leads para Google Sheets', 'Regista automaticamente dados de leads qualificadas diretamente na folha de calculo.', 2, 3, 'lead_score', '>=', '70', 'Registo automatico: {{company}} (Score: {{lead_score}})', 1, 28, 27),
            ('Resposta Automatica a Emails Urgentes', 'Envia resposta automatica imediata garantindo atendimento de suporte prioritario.', 3, 2, 'priority', '==', 'high', 'Ola! Recebemos a sua mensagem com prioridade alta e estamos a analisar o caso.', 1, 15, 15),
            ('Alerta Discord para Vendas Globais', 'Publica notificacao em tempo real no Discord para toda a comunidade de fundadores.', 1, 4, 'currency', '==', 'eur', '[DISCORD] Venda internacional registada em EUR: {{amount}} EUR', 1, 33, 31)
        ]
        cursor.executemany('''
            INSERT INTO workflows (title, description, trigger_id, action_id, condition_field, condition_operator, condition_value, action_template, is_active, total_runs, success_runs)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_workflows)

        # Seed Execution History
        now = datetime.now()
        hist_records = [
            (1, 'Alerta Slack: Vendas Enterprise Stripe', 'Novo Pagamento Aprovado', 'Enviar Mensagem para Canal Slack', 'Sucesso', 118, '{"amount": 250.00, "customer_email": "carlos.silva@corp.pt"}', '{"status": 200, "channel": "#vendas-alertas", "ts": "1727245600"}', None, (now - timedelta(minutes=12)).strftime('%Y-%m-%d %H:%M:%S')),
            (1, 'Alerta Slack: Vendas Enterprise Stripe', 'Novo Pagamento Aprovado', 'Enviar Mensagem para Canal Slack', 'Filtrado', 32, '{"amount": 49.00, "customer_email": "tiago@micro.pt"}', '{"condition_evaluated": false, "reason": "49.00 not > 100"}', None, (now - timedelta(minutes=35)).strftime('%Y-%m-%d %H:%M:%S')),
            (2, 'Sincronização de Novos Leads para Google Sheets', 'Webhook Recebido (JSON Payload)', 'Adicionar Linha em Google Sheets', 'Sucesso', 164, '{"company": "Vortex Media", "lead_score": 85}', '{"status": 200, "updated_range": "Leads!A45:E45"}', None, (now - timedelta(minutes=58)).strftime('%Y-%m-%d %H:%M:%S')),
            (3, 'Resposta Automática a Emails Urgentes', 'Novo Email com Assunto Relevante', 'Enviar Email Transacional Automático', 'Sucesso', 210, '{"priority": "high", "sender": "ceo@startup.co"}', '{"status": 200, "message_id": "<MSG_9921_OK>"}', None, (now - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')),
            (4, 'Alerta Discord para Vendas Globais', 'Novo Pagamento Aprovado', 'Notificar Servidor Discord', 'Sucesso', 88, '{"amount": 180.00, "currency": "eur"}', '{"status": 204, "webhook": "sent"}', None, (now - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S'))
        ]
        cursor.executemany('''
            INSERT INTO execution_history (workflow_id, workflow_title, trigger_name, action_name, status, execution_time_ms, input_payload, output_payload, error_message, executed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', hist_records)

        conn.commit()
    conn.close()

# --- Integrations ---
def get_all_integrations():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM integrations ORDER BY id ASC')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def update_integration_status(integration_id, status):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE integrations SET status = ? WHERE id = ?', (status, integration_id))
    conn.commit()
    conn.close()

# --- Triggers & Actions ---
def get_all_triggers():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT t.*, i.name as integration_name, i.service_key
        FROM triggers t
        JOIN integrations i ON t.integration_id = i.id
        ORDER BY t.id ASC
    ''')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_all_actions():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT a.*, i.name as integration_name, i.service_key
        FROM actions a
        JOIN integrations i ON a.integration_id = i.id
        ORDER BY a.id ASC
    ''')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

# --- Workflows ---
def get_all_workflows():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT w.*, 
               t.name as trigger_name, t.icon as trigger_icon, t.event_type, t.sample_payload,
               a.name as action_name, a.icon as action_icon, a.action_type
        FROM workflows w
        JOIN triggers t ON w.trigger_id = t.id
        JOIN actions a ON w.action_id = a.id
        ORDER BY w.id DESC
    ''')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def add_workflow(title, description, trigger_id, action_id, condition_field, condition_operator, condition_value, action_template):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO workflows (title, description, trigger_id, action_id, condition_field, condition_operator, condition_value, action_template, is_active, total_runs, success_runs)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, 0, 0)
    ''', (title, description, trigger_id, action_id, condition_field, condition_operator, condition_value, action_template))
    wid = cursor.lastrowid
    conn.commit()
    conn.close()
    return wid

def toggle_workflow_status(workflow_id, is_active):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE workflows SET is_active = ? WHERE id = ?', (is_active, workflow_id))
    conn.commit()
    conn.close()

def delete_workflow(workflow_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM execution_history WHERE workflow_id = ?', (workflow_id,))
    cursor.execute('DELETE FROM workflows WHERE id = ?', (workflow_id,))
    conn.commit()
    conn.close()

# --- Automation Execution Engine ---
def execute_workflow_engine(workflow_id, custom_payload=None):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT w.*, t.name as trigger_name, t.sample_payload, a.name as action_name, a.action_type
        FROM workflows w
        JOIN triggers t ON w.trigger_id = t.id
        JOIN actions a ON w.action_id = a.id
        WHERE w.id = ?
    ''', (workflow_id,))
    wf = cursor.fetchone()
    if not wf:
        conn.close()
        return None

    wf = dict(wf)
    payload = custom_payload if custom_payload else json.loads(wf['sample_payload'])

    # Evaluate Condition
    c_field = wf.get('condition_field')
    c_op = wf.get('condition_operator')
    c_val = wf.get('condition_value')

    passed_condition = True
    reason = "Sem filtro condicional"

    if c_field and c_field in payload:
        actual_val = payload[c_field]
        try:
            # Numeric evaluation
            actual_num = float(actual_val)
            target_num = float(c_val)
            if c_op == '>': passed_condition = (actual_num > target_num)
            elif c_op == '>=': passed_condition = (actual_num >= target_num)
            elif c_op == '<': passed_condition = (actual_num < target_num)
            elif c_op == '<=': passed_condition = (actual_num <= target_num)
            elif c_op == '==': passed_condition = (actual_num == target_num)
            elif c_op == '!=': passed_condition = (actual_num != target_num)
        except (ValueError, TypeError):
            # String evaluation
            s_actual = str(actual_val).lower()
            s_target = str(c_val).lower()
            if c_op == '==': passed_condition = (s_actual == s_target)
            elif c_op == '!=': passed_condition = (s_actual != s_target)
            elif c_op == 'contains': passed_condition = (s_target in s_actual)

        if not passed_condition:
            reason = f"Condição '{c_field} {c_op} {c_val}' não foi satisfeita. Valor recebido: '{actual_val}'"

    exec_time_ms = random.randint(45, 190)
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if not passed_condition:
        status = 'Filtrado'
        output_payload = json.dumps({"condition_met": False, "reason": reason})
        err_msg = None
    else:
        status = 'Sucesso'
        output_payload = json.dumps({
            "status": 200,
            "action": wf['action_name'],
            "executed": True,
            "message_dispatched": wf['action_template'] or "Ação executada com sucesso",
            "dispatch_id": f"EVT-{random.randint(10000, 99999)}"
        })
        err_msg = None

    # Update workflow counters
    success_inc = 1 if status == 'Sucesso' else 0
    cursor.execute('''
        UPDATE workflows 
        SET total_runs = total_runs + 1,
            success_runs = success_runs + ?,
            last_run_at = ?
        WHERE id = ?
    ''', (success_inc, now_str, workflow_id))

    # Insert execution history log
    cursor.execute('''
        INSERT INTO execution_history (workflow_id, workflow_title, trigger_name, action_name, status, execution_time_ms, input_payload, output_payload, error_message, executed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (workflow_id, wf['title'], wf['trigger_name'], wf['action_name'], status, exec_time_ms, json.dumps(payload), output_payload, err_msg, now_str))

    log_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {
        "log_id": log_id,
        "workflow_id": workflow_id,
        "title": wf['title'],
        "status": status,
        "execution_time_ms": exec_time_ms,
        "input": payload,
        "output": json.loads(output_payload),
        "executed_at": now_str
    }

# --- Execution Logs ---
def get_execution_history(limit=50):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM execution_history ORDER BY id DESC LIMIT ?', (limit,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

# --- Dashboard Metrics ---
def get_dashboard_metrics():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM workflows WHERE is_active = 1')
    active_workflows = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM workflows')
    total_workflows = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM execution_history')
    total_executions = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM execution_history WHERE status = "Sucesso"')
    success_executions = cursor.fetchone()[0]

    success_rate = round((success_executions / total_executions * 100), 1) if total_executions > 0 else 100.0

    cursor.execute('SELECT AVG(execution_time_ms) FROM execution_history')
    avg_speed = round(cursor.fetchone()[0] or 95.0)

    cursor.execute('SELECT COUNT(*) FROM integrations WHERE status = "Conectado"')
    connected_apps = cursor.fetchone()[0]

    # Daily executions breakdown
    cursor.execute('''
        SELECT status, COUNT(*) as count 
        FROM execution_history 
        GROUP BY status
    ''')
    status_breakdown = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return {
        "active_workflows": active_workflows,
        "total_workflows": total_workflows,
        "total_executions": total_executions,
        "success_rate": success_rate,
        "avg_speed_ms": avg_speed,
        "connected_apps": connected_apps,
        "status_breakdown": status_breakdown
    }
