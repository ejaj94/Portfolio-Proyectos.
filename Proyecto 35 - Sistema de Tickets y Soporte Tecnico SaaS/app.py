import os
import random
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import database

app = Flask(__name__)
app.secret_key = 'ejajtech_helpdesk_secret_key_2026'

# Inicializar BD al arrancar
database.init_db()

SLA_HOURS = {
    'Crítica': 2,
    'Alta': 4,
    'Media': 12,
    'Baja': 24
}

# --- RUTAS DE NAVEGACIÓN (HTML) ---

@app.route('/')
def index():
    conn = database.get_db_connection()
    cursor = conn.cursor()

    # Parámetros de filtrado
    status_filter = request.args.get('status', 'all')
    priority_filter = request.args.get('priority', 'all')
    category_filter = request.args.get('category', 'all')
    search_query = request.args.get('q', '')

    query = '''
        SELECT t.*, a.name as agent_name, a.avatar_url as agent_avatar
        FROM tickets t
        LEFT JOIN agents a ON t.agent_id = a.id
        WHERE 1=1
    '''
    params = []

    if status_filter != 'all':
        query += ' AND t.status = ?'
        params.append(status_filter)
    if priority_filter != 'all':
        query += ' AND t.priority = ?'
        params.append(priority_filter)
    if category_filter != 'all':
        query += ' AND t.category = ?'
        params.append(category_filter)
    if search_query:
        query += ' AND (t.title LIKE ? OR t.code LIKE ? OR t.client_name LIKE ? OR t.client_email LIKE ?)'
        wildcard = f'%{search_query}%'
        params.extend([wildcard, wildcard, wildcard, wildcard])

    query += ' ORDER BY CASE t.priority WHEN "Crítica" THEN 1 WHEN "Alta" THEN 2 WHEN "Media" THEN 3 ELSE 4 END, t.created_at DESC'

    cursor.execute(query, params)
    tickets = cursor.fetchall()

    # KPIs
    cursor.execute('SELECT COUNT(*) FROM tickets')
    total_tickets = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM tickets WHERE status = "Abierto"')
    open_tickets = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM tickets WHERE status = "En Proceso"')
    in_progress_tickets = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM tickets WHERE status = "Pendiente Cliente"')
    pending_tickets = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM tickets WHERE status IN ("Resuelto", "Cerrado")')
    resolved_tickets = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM tickets WHERE priority = "Crítica" AND status NOT IN ("Resuelto", "Cerrado")')
    critical_active = cursor.fetchone()[0]

    cursor.execute('SELECT * FROM agents')
    agents = cursor.fetchall()

    conn.close()

    return render_template(
        'index.html',
        tickets=tickets,
        agents=agents,
        total_tickets=total_tickets,
        open_tickets=open_tickets,
        in_progress_tickets=in_progress_tickets,
        pending_tickets=pending_tickets,
        resolved_tickets=resolved_tickets,
        critical_active=critical_active,
        status_filter=status_filter,
        priority_filter=priority_filter,
        category_filter=category_filter,
        search_query=search_query
    )

@app.route('/kanban')
def kanban():
    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT t.*, a.name as agent_name, a.avatar_url as agent_avatar
        FROM tickets t
        LEFT JOIN agents a ON t.agent_id = a.id
        ORDER BY t.created_at DESC
    ''')
    all_tickets = cursor.fetchall()

    columns = {
        'Abierto': [t for t in all_tickets if t['status'] == 'Abierto'],
        'En Proceso': [t for t in all_tickets if t['status'] == 'En Proceso'],
        'Pendiente Cliente': [t for t in all_tickets if t['status'] == 'Pendiente Cliente'],
        'Resuelto': [t for t in all_tickets if t['status'] == 'Resuelto'],
        'Cerrado': [t for t in all_tickets if t['status'] == 'Cerrado']
    }

    cursor.execute('SELECT * FROM agents')
    agents = cursor.fetchall()

    conn.close()
    return render_template('kanban.html', columns=columns, agents=agents)

@app.route('/ticket/<int:ticket_id>')
def ticket_detail(ticket_id):
    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT t.*, a.name as agent_name, a.email as agent_email, a.role as agent_role, a.avatar_url as agent_avatar, a.specialty as agent_specialty
        FROM tickets t
        LEFT JOIN agents a ON t.agent_id = a.id
        WHERE t.id = ?
    ''', (ticket_id,))
    ticket = cursor.fetchone()

    if not ticket:
        conn.close()
        flash('El ticket solicitado no existe.', 'danger')
        return redirect(url_for('index'))

    # Comentarios
    cursor.execute('''
        SELECT * FROM comments
        WHERE ticket_id = ?
        ORDER BY created_at ASC
    ''', (ticket_id,))
    comments = cursor.fetchall()

    # Historial de Auditoría
    cursor.execute('''
        SELECT * FROM history_log
        WHERE ticket_id = ?
        ORDER BY created_at DESC
    ''', (ticket_id,))
    history = cursor.fetchall()

    # Todos los agentes para modal de reasignación
    cursor.execute('SELECT * FROM agents')
    agents = cursor.fetchall()

    conn.close()
    return render_template('ticket_detail.html', ticket=ticket, comments=comments, history=history, agents=agents)

@app.route('/create', methods=['GET', 'POST'])
def create_ticket():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', 'Software')
        priority = request.form.get('priority', 'Media')
        client_name = request.form.get('client_name', '').strip()
        client_email = request.form.get('client_email', '').strip()
        agent_id = request.form.get('agent_id')

        if not title or not description or not client_name or not client_email:
            flash('Por favor complete todos los campos obligatorios.', 'danger')
            return redirect(url_for('create_ticket'))

        agent_id = int(agent_id) if agent_id and agent_id.isdigit() else None
        
        # Generar Código único
        code_num = random.randint(1000, 9999)
        code = f"TCK-2026-{code_num}"

        # Calcular SLA Due At
        hours = SLA_HOURS.get(priority, 12)
        due_at = (datetime.now() + timedelta(hours=hours)).strftime('%Y-%m-%d %H:%M:%S')

        conn = database.get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO tickets (code, title, description, category, priority, status, client_name, client_email, agent_id, due_at)
            VALUES (?, ?, ?, ?, ?, 'Abierto', ?, ?, ?, ?)
        ''', (code, title, description, category, priority, client_name, client_email, agent_id, due_at))
        
        new_ticket_id = cursor.lastrowid

        # Registrar en Historial
        actor = client_name
        cursor.execute('''
            INSERT INTO history_log (ticket_id, actor_name, action, details)
            VALUES (?, ?, 'Creación', ?)
        ''', (new_ticket_id, actor, f"Ticket registrado por el cliente con Prioridad {priority} (SLA: {hours}h)"))

        if agent_id:
            cursor.execute('SELECT name FROM agents WHERE id = ?', (agent_id,))
            ag = cursor.fetchone()
            ag_name = ag[0] if ag else f"Agente #{agent_id}"
            cursor.execute('''
                INSERT INTO history_log (ticket_id, actor_name, action, details)
                VALUES (?, 'Sistema', 'Reasignación Agente', ?)
            ''', (new_ticket_id, f"Ticket asignado a {ag_name}"))

            cursor.execute('UPDATE agents SET active_tickets = active_tickets + 1 WHERE id = ?', (agent_id,))

        conn.commit()
        conn.close()

        flash(f'¡Ticket {code} creado con éxito!', 'success')
        return redirect(url_for('ticket_detail', ticket_id=new_ticket_id))

    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM agents')
    agents = cursor.fetchall()
    conn.close()

    return render_template('create_ticket.html', agents=agents)

@app.route('/agents')
def agents():
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT a.*, 
               (SELECT COUNT(*) FROM tickets t WHERE t.agent_id = a.id AND t.status IN ('Abierto', 'En Proceso', 'Pendiente Cliente')) as open_count,
               (SELECT COUNT(*) FROM tickets t WHERE t.agent_id = a.id AND t.status IN ('Resuelto', 'Cerrado')) as closed_count
        FROM agents a
    ''')
    agents_list = cursor.fetchall()
    conn.close()

    return render_template('agents.html', agents=agents_list)


# --- APIs REST (JSON) ---

@app.route('/api/tickets/<int:ticket_id>/update-status', methods=['POST'])
def api_update_status(ticket_id):
    data = request.json or {}
    new_status = data.get('status')
    actor = data.get('actor', 'Agente Soporte')

    if not new_status:
        return jsonify({'success': False, 'message': 'Estado inválido'}), 400

    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT status, agent_id FROM tickets WHERE id = ?', (ticket_id,))
    ticket = cursor.fetchone()

    if not ticket:
        conn.close()
        return jsonify({'success': False, 'message': 'Ticket no encontrado'}), 404

    old_status = ticket['status']
    agent_id = ticket['agent_id']

    cursor.execute('UPDATE tickets SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?', (new_status, ticket_id))

    # Si pasa a Resuelto o Cerrado, actualizar contadores de agente
    if new_status in ('Resuelto', 'Cerrado') and old_status not in ('Resuelto', 'Cerrado') and agent_id:
        cursor.execute('UPDATE agents SET active_tickets = MAX(0, active_tickets - 1), resolved_tickets = resolved_tickets + 1 WHERE id = ?', (agent_id,))
    elif old_status in ('Resuelto', 'Cerrado') and new_status not in ('Resuelto', 'Cerrado') and agent_id:
        cursor.execute('UPDATE agents SET active_tickets = active_tickets + 1 WHERE id = ?', (agent_id,))

    # Registrar Auditoría
    cursor.execute('''
        INSERT INTO history_log (ticket_id, actor_name, action, details)
        VALUES (?, ?, 'Cambio de Estado', ?)
    ''', (ticket_id, actor, f"Estado actualizado de '{old_status}' a '{new_status}'"))

    conn.commit()
    conn.close()

    return jsonify({'success': True, 'old_status': old_status, 'new_status': new_status})

@app.route('/api/tickets/<int:ticket_id>/update-priority', methods=['POST'])
def api_update_priority(ticket_id):
    data = request.json or {}
    new_priority = data.get('priority')
    actor = data.get('actor', 'Agente Soporte')

    if not new_priority or new_priority not in SLA_HOURS:
        return jsonify({'success': False, 'message': 'Prioridad inválida'}), 400

    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT priority, created_at FROM tickets WHERE id = ?', (ticket_id,))
    ticket = cursor.fetchone()

    if not ticket:
        conn.close()
        return jsonify({'success': False, 'message': 'Ticket no encontrado'}), 404

    old_priority = ticket['priority']
    created_dt = datetime.strptime(ticket['created_at'], '%Y-%m-%d %H:%M:%S') if ' ' in ticket['created_at'] else datetime.now()
    new_due_at = (created_dt + timedelta(hours=SLA_HOURS[new_priority])).strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('UPDATE tickets SET priority = ?, due_at = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?', (new_priority, new_due_at, ticket_id))

    cursor.execute('''
        INSERT INTO history_log (ticket_id, actor_name, action, details)
        VALUES (?, ?, 'Cambio de Prioridad', ?)
    ''', (ticket_id, actor, f"Prioridad ajustada de '{old_priority}' a '{new_priority}' (Nuevo SLA: {new_due_at})"))

    conn.commit()
    conn.close()

    return jsonify({'success': True, 'old_priority': old_priority, 'new_priority': new_priority, 'new_due_at': new_due_at})

@app.route('/api/tickets/<int:ticket_id>/reassign', methods=['POST'])
def api_reassign_agent(ticket_id):
    data = request.json or {}
    new_agent_id = data.get('agent_id')
    actor = data.get('actor', 'Administrador')

    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT agent_id FROM tickets WHERE id = ?', (ticket_id,))
    ticket = cursor.fetchone()

    if not ticket:
        conn.close()
        return jsonify({'success': False, 'message': 'Ticket no encontrado'}), 404

    old_agent_id = ticket['agent_id']

    new_agent_name = "Sin Asignar"
    if new_agent_id:
        cursor.execute('SELECT name FROM agents WHERE id = ?', (new_agent_id,))
        ag = cursor.fetchone()
        if ag:
            new_agent_name = ag['name']

    cursor.execute('UPDATE tickets SET agent_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?', (new_agent_id, ticket_id))

    if old_agent_id:
        cursor.execute('UPDATE agents SET active_tickets = MAX(0, active_tickets - 1) WHERE id = ?', (old_agent_id,))
    if new_agent_id:
        cursor.execute('UPDATE agents SET active_tickets = active_tickets + 1 WHERE id = ?', (new_agent_id,))

    cursor.execute('''
        INSERT INTO history_log (ticket_id, actor_name, action, details)
        VALUES (?, ?, 'Reasignación Agente', ?)
    ''', (ticket_id, actor, f"Ticket reasignado a: {new_agent_name}"))

    conn.commit()
    conn.close()

    return jsonify({'success': True, 'new_agent_id': new_agent_id, 'new_agent_name': new_agent_name})

@app.route('/api/tickets/<int:ticket_id>/comment', methods=['POST'])
def api_add_comment(ticket_id):
    data = request.form if request.form else (request.json or {})
    author_name = data.get('author_name', 'Agente Soporte').strip()
    author_role = data.get('author_role', 'Agente').strip()
    content = data.get('content', '').strip()
    is_internal = 1 if str(data.get('is_internal')).lower() in ('1', 'true', 'on') else 0

    if not content:
        if request.is_json:
            return jsonify({'success': False, 'message': 'El contenido no puede estar vacío'}), 400
        flash('El comentario no puede estar vacío.', 'danger')
        return redirect(url_for('ticket_detail', ticket_id=ticket_id))

    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO comments (ticket_id, author_name, author_role, content, is_internal)
        VALUES (?, ?, ?, ?, ?)
    ''', (ticket_id, author_name, author_role, content, is_internal))

    # Log de Auditoría
    action_type = "Nota Interna" if is_internal else "Comentario Público"
    cursor.execute('''
        INSERT INTO history_log (ticket_id, actor_name, action, details)
        VALUES (?, ?, ?, ?)
    ''', (ticket_id, author_name, action_type, f"Añadido {action_type.lower()}: '{content[:40]}...'"))

    cursor.execute('UPDATE tickets SET updated_at = CURRENT_TIMESTAMP WHERE id = ?', (ticket_id,))

    conn.commit()
    conn.close()

    if request.is_json:
        return jsonify({'success': True, 'content': content, 'is_internal': is_internal})

    flash('Comentario publicado correctamente.', 'success')
    return redirect(url_for('ticket_detail', ticket_id=ticket_id))

@app.route('/api/stats')
def api_stats():
    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT category, COUNT(*) as count FROM tickets GROUP BY category')
    categories = cursor.fetchall()

    cursor.execute('SELECT priority, COUNT(*) as count FROM tickets GROUP BY priority')
    priorities = cursor.fetchall()

    cursor.execute('SELECT status, COUNT(*) as count FROM tickets GROUP BY status')
    statuses = cursor.fetchall()

    conn.close()

    return jsonify({
        'categories': [{'name': c['category'], 'count': c['count']} for c in categories],
        'priorities': [{'name': p['priority'], 'count': p['count']} for p in priorities],
        'statuses': [{'name': s['status'], 'count': s['count']} for s in statuses]
    })


if __name__ == '__main__':
    print("=" * 60)
    print(" [RESOLV-IT SaaS] EJAJ TECH Support Helpdesk Suite")
    print(" Servidor Flask corriendo en http://127.0.0.1:5980")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5980, debug=True)
