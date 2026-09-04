import os
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import database

app = Flask(__name__)
app.secret_key = 'ejajtech_messenger_chat_secret_2026'

# Inicializar BD
database.init_db()

# ID de Usuario Activo por defecto (Enmanuel Jimenez)
CURRENT_USER_ID = 1

@app.route('/')
def index():
    active_conv_id = request.args.get('conv_id', type=int)

    conn = database.get_db_connection()
    cursor = conn.cursor()

    # Obtener perfil del usuario actual
    cursor.execute('SELECT * FROM users WHERE id = ?', (CURRENT_USER_ID,))
    current_user = cursor.fetchone()

    # Obtener lista de conversaciones
    cursor.execute('''
        SELECT c.*, 
               m.unread_count,
               (SELECT content FROM messages msg WHERE msg.conversation_id = c.id ORDER BY msg.created_at DESC LIMIT 1) as last_message,
               (SELECT created_at FROM messages msg WHERE msg.conversation_id = c.id ORDER BY msg.created_at DESC LIMIT 1) as last_message_time
        FROM conversations c
        JOIN conversation_members m ON c.id = m.conversation_id
        WHERE m.user_id = ?
        ORDER BY c.last_message_at DESC
    ''', (CURRENT_USER_ID,))
    raw_conversations = cursor.fetchall()

    conversations = []
    for conv in raw_conversations:
        conv_dict = dict(conv)
        if conv_dict['type'] == 'direct':
            # Buscar el otro usuario en el chat directo
            cursor.execute('''
                SELECT u.name, u.avatar_url, u.status, u.role
                FROM users u
                JOIN conversation_members cm ON u.id = cm.user_id
                WHERE cm.conversation_id = ? AND u.id != ?
            ''', (conv_dict['id'], CURRENT_USER_ID))
            other_user = cursor.fetchone()
            if other_user:
                conv_dict['display_name'] = other_user['name']
                conv_dict['display_avatar'] = other_user['avatar_url']
                conv_dict['display_status'] = other_user['status']
                conv_dict['display_role'] = other_user['role']
        else:
            conv_dict['display_name'] = conv_dict['name']
            conv_dict['display_avatar'] = conv_dict['icon_url'] or 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=150'
            conv_dict['display_status'] = 'group'
            conv_dict['display_role'] = 'Canal de Equipo'

        conversations.append(conv_dict)

    if not active_conv_id and len(conversations) > 0:
        active_conv_id = conversations[0]['id']

    # Obtener mensajes de la conversación activa
    active_conversation = None
    messages = []
    if active_conv_id:
        cursor.execute('SELECT * FROM conversations WHERE id = ?', (active_conv_id,))
        conv_row = cursor.fetchone()
        if conv_row:
            active_conversation = dict(conv_row)
            if active_conversation['type'] == 'direct':
                cursor.execute('''
                    SELECT u.id as other_id, u.name, u.avatar_url, u.status, u.role, u.custom_status
                    FROM users u
                    JOIN conversation_members cm ON u.id = cm.user_id
                    WHERE cm.conversation_id = ? AND u.id != ?
                ''', (active_conv_id, CURRENT_USER_ID))
                other_u = cursor.fetchone()
                if other_u:
                    active_conversation['display_name'] = other_u['name']
                    active_conversation['display_avatar'] = other_u['avatar_url']
                    active_conversation['display_status'] = other_u['status']
                    active_conversation['display_role'] = other_u['role']
                    active_conversation['custom_status'] = other_u['custom_status']
                    active_conversation['other_user_id'] = other_u['other_id']
            else:
                active_conversation['display_name'] = active_conversation['name']
                active_conversation['display_avatar'] = active_conversation['icon_url']
                active_conversation['display_status'] = 'group'
                active_conversation['display_role'] = 'Canal de Equipo'

            # Cargar Mensajes
            cursor.execute('''
                SELECT m.*, u.name as sender_name, u.avatar_url as sender_avatar, u.username as sender_username
                FROM messages m
                JOIN users u ON m.sender_id = u.id
                WHERE m.conversation_id = ?
                ORDER BY m.created_at ASC
            ''', (active_conv_id,))
            raw_messages = cursor.fetchall()

            for msg in raw_messages:
                m_dict = dict(msg)
                # Reacciones
                cursor.execute('''
                    SELECT r.emoji, r.user_id, u.name as user_name
                    FROM reactions r
                    JOIN users u ON r.user_id = u.id
                    WHERE r.message_id = ?
                ''', (m_dict['id'],))
                m_dict['reactions'] = [dict(r) for r in cursor.fetchall()]
                messages.append(m_dict)

            # Limpiar unread count
            cursor.execute('''
                UPDATE conversation_members
                SET unread_count = 0
                WHERE conversation_id = ? AND user_id = ?
            ''', (active_conv_id, CURRENT_USER_ID))
            conn.commit()

    # Todos los usuarios para iniciar chat
    cursor.execute('SELECT * FROM users WHERE id != ?', (CURRENT_USER_ID,))
    all_users = cursor.fetchall()

    conn.close()

    return render_template(
        'index.html',
        current_user=current_user,
        conversations=conversations,
        active_conversation=active_conversation,
        messages=messages,
        all_users=all_users
    )


# --- APIs REST DE MENSAJERÍA ---

@app.route('/api/conversations/<int:conv_id>/messages', methods=['GET'])
def api_get_messages(conv_id):
    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT m.*, u.name as sender_name, u.avatar_url as sender_avatar
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE m.conversation_id = ?
        ORDER BY m.created_at ASC
    ''', (conv_id,))
    messages = [dict(m) for m in cursor.fetchall()]

    for msg in messages:
        cursor.execute('''
            SELECT r.emoji, r.user_id, u.name as user_name
            FROM reactions r
            JOIN users u ON r.user_id = u.id
            WHERE r.message_id = ?
        ''', (msg['id'],))
        msg['reactions'] = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return jsonify({'success': True, 'messages': messages})


@app.route('/api/conversations/<int:conv_id>/send', methods=['POST'])
def api_send_message(conv_id):
    data = request.json or {}
    content = data.get('content', '').strip()
    media_url = data.get('media_url')

    if not content:
        return jsonify({'success': False, 'message': 'El mensaje no puede estar vacío'}), 400

    conn = database.get_db_connection()
    cursor = conn.cursor()

    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
        INSERT INTO messages (conversation_id, sender_id, content, media_url, status, created_at)
        VALUES (?, ?, ?, ?, 'read', ?)
    ''', (conv_id, CURRENT_USER_ID, content, media_url, now_str))
    
    new_message_id = cursor.lastrowid

    # Actualizar last_message_at en la conversación
    cursor.execute('UPDATE conversations SET last_message_at = ? WHERE id = ?', (now_str, conv_id))

    # Incrementar unread count para otros miembros
    cursor.execute('''
        UPDATE conversation_members
        SET unread_count = unread_count + 1
        WHERE conversation_id = ? AND user_id != ?
    ''', (conv_id, CURRENT_USER_ID))

    # Obtener datos del remitente
    cursor.execute('SELECT name, avatar_url FROM users WHERE id = ?', (CURRENT_USER_ID,))
    user_info = cursor.fetchone()

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': {
            'id': new_message_id,
            'conversation_id': conv_id,
            'sender_id': CURRENT_USER_ID,
            'sender_name': user_info['name'],
            'sender_avatar': user_info['avatar_url'],
            'content': content,
            'media_url': media_url,
            'status': 'read',
            'created_at': now_str,
            'reactions': []
        }
    })


@app.route('/api/messages/<int:msg_id>/react', methods=['POST'])
def api_react_message(msg_id):
    data = request.json or {}
    emoji = data.get('emoji', '👍')

    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM reactions WHERE message_id = ? AND user_id = ? AND emoji = ?', (msg_id, CURRENT_USER_ID, emoji))
    existing = cursor.fetchone()

    if existing:
        cursor.execute('DELETE FROM reactions WHERE message_id = ? AND user_id = ? AND emoji = ?', (msg_id, CURRENT_USER_ID, emoji))
        action = 'removed'
    else:
        cursor.execute('INSERT INTO reactions (message_id, user_id, emoji) VALUES (?, ?, ?)', (msg_id, CURRENT_USER_ID, emoji))
        action = 'added'

    conn.commit()
    conn.close()

    return jsonify({'success': True, 'action': action, 'emoji': emoji})


@app.route('/api/user/status', methods=['POST'])
def api_update_status():
    data = request.json or {}
    new_status = data.get('status', 'online')

    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET status = ?, last_seen = CURRENT_TIMESTAMP WHERE id = ?', (new_status, CURRENT_USER_ID))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'status': new_status})


@app.route('/api/conversations/start-direct', methods=['POST'])
def api_start_direct():
    data = request.json or {}
    target_user_id = data.get('user_id')

    if not target_user_id:
        return jsonify({'success': False, 'message': 'Usuario no especificado'}), 400

    conn = database.get_db_connection()
    cursor = conn.cursor()

    # Comprobar si ya existe chat directo
    cursor.execute('''
        SELECT cm1.conversation_id
        FROM conversation_members cm1
        JOIN conversation_members cm2 ON cm1.conversation_id = cm2.conversation_id
        JOIN conversations c ON cm1.conversation_id = c.id
        WHERE cm1.user_id = ? AND cm2.user_id = ? AND c.type = 'direct'
    ''', (CURRENT_USER_ID, target_user_id))

    row = cursor.fetchone()
    if row:
        conv_id = row['conversation_id']
    else:
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO conversations (type, created_at, last_message_at) VALUES ('direct', ?, ?)", (now_str, now_str))
        conv_id = cursor.lastrowid
        cursor.execute("INSERT INTO conversation_members (conversation_id, user_id) VALUES (?, ?)", (conv_id, CURRENT_USER_ID))
        cursor.execute("INSERT INTO conversation_members (conversation_id, user_id) VALUES (?, ?)", (conv_id, target_user_id))
        conn.commit()

    conn.close()
    return jsonify({'success': True, 'conversation_id': conv_id})


if __name__ == '__main__':
    print("=" * 60)
    print(" [CONNECT-CHAT SaaS] EJAJ TECH Facebook Messenger Blue Suite")
    print(" Servidor Flask corriendo en http://127.0.0.1:5990")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5990, debug=True)
