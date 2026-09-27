import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'chatbot.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def root_redirect():
    return redirect('/admin')

@app.route('/admin')
def admin_dashboard():
    conn = get_db()
    cursor = conn.cursor()

    # 1. Total Conversations
    cursor.execute("SELECT COUNT(*) FROM conversations")
    total_convs = cursor.fetchone()[0]

    # 2. Total FAQs Active
    cursor.execute("SELECT COUNT(*) FROM faqs WHERE is_active = 1")
    total_faqs = cursor.fetchone()[0]

    # 3. Total KB Articles
    cursor.execute("SELECT COUNT(*) FROM knowledge_base")
    total_kb = cursor.fetchone()[0]

    # 4. Total Messages Exchanged
    cursor.execute("SELECT COUNT(*) FROM chat_messages")
    total_messages = cursor.fetchone()[0]

    # 5. Recent Conversations
    cursor.execute("SELECT * FROM conversations ORDER BY id DESC LIMIT 5")
    recent_convs = cursor.fetchall()

    # 6. Bot Settings
    cursor.execute("SELECT * FROM bot_settings LIMIT 1")
    settings = cursor.fetchone()

    conn.close()
    return render_template('admin_dashboard.html',
                           total_convs=total_convs,
                           total_faqs=total_faqs,
                           total_kb=total_kb,
                           total_messages=total_messages,
                           recent_convs=recent_convs,
                           settings=settings)

@app.route('/chat')
def chat_widget_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bot_settings LIMIT 1")
    settings = cursor.fetchone()
    cursor.execute("SELECT * FROM faqs WHERE is_active = 1 LIMIT 4")
    quick_faqs = cursor.fetchall()
    conn.close()
    return render_template('chat_widget.html', settings=settings, quick_faqs=quick_faqs)

@app.route('/admin/faqs')
def admin_faqs_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM faqs ORDER BY id DESC")
    faqs = cursor.fetchall()
    conn.close()
    return render_template('admin_faqs.html', faqs=faqs)

@app.route('/admin/kb')
def admin_kb_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM knowledge_base ORDER BY id DESC")
    articles = cursor.fetchall()
    conn.close()
    return render_template('admin_kb.html', articles=articles)

@app.route('/admin/history')
def admin_history_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM conversations ORDER BY id DESC")
    convs = cursor.fetchall()

    conv_messages = {}
    for c in convs:
        cursor.execute("SELECT * FROM chat_messages WHERE conversation_id = ? ORDER BY id ASC", (c['id'],))
        conv_messages[c['id']] = cursor.fetchall()

    conn.close()
    return render_template('admin_history.html', convs=convs, conv_messages=conv_messages)

# REST API ENDPOINTS

@app.route('/api/chat/message', methods=['POST'])
def api_chat_message():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip().lower()
        conv_id = data.get('conversation_id', 1)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        if not user_message:
            return jsonify({'success': False, 'reply': 'Por favor introduza uma mensagem.'})

        conn = get_db()
        cursor = conn.cursor()

        # Log User Message
        cursor.execute("""
            INSERT INTO chat_messages (conversation_id, sender, message_text, timestamp)
            VALUES (?, ?, ?, ?)
        """, (conv_id, 'user', user_message, now_str))

        # Check Bot Settings for fallback
        cursor.execute("SELECT * FROM bot_settings LIMIT 1")
        settings = cursor.fetchone()
        fallback_text = settings['fallback_message'] if settings else "Não compreendi. Digite 'AJUDA' para falar com o suporte."

        bot_reply = None
        matched_faq_id = None

        # Check explicit trigger word "AJUDA" or "WHATSAPP"
        if 'ajuda' in user_message or 'whatsapp' in user_message or 'humano' in user_message:
            bot_reply = "🟢 Um especialista de suporte humano da EJAJ TECH pode ajudá-lo diretamente via WhatsApp! Clique aqui para falar connosco: https://wa.me/351911151993?text=AJUDA"
        else:
            # Match keywords in FAQs table
            cursor.execute("SELECT * FROM faqs WHERE is_active = 1")
            faqs = cursor.fetchall()

            for faq in faqs:
                keywords = [k.strip().lower() for k in faq['keywords'].split(',')]
                for kw in keywords:
                    if kw and kw in user_message:
                        bot_reply = faq['answer']
                        matched_faq_id = faq['id']
                        break
                if bot_reply:
                    break

            # If no FAQ matched, search Knowledge Base articles
            if not bot_reply:
                cursor.execute("SELECT * FROM knowledge_base")
                kb_articles = cursor.fetchall()
                for art in kb_articles:
                    if art['title'].lower() in user_message or art['category'].lower() in user_message:
                        bot_reply = f"📚 Encontrei o artigo '{art['title']}': {art['content'][:180]}..."
                        break

        # Fallback if still no match
        if not bot_reply:
            bot_reply = fallback_text

        # Log Bot Response Message
        cursor.execute("""
            INSERT INTO chat_messages (conversation_id, sender, message_text, timestamp)
            VALUES (?, ?, ?, ?)
        """, (conv_id, 'bot', bot_reply, now_str))

        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'reply': bot_reply,
            'matched_faq_id': matched_faq_id,
            'timestamp': now_str
        })
    except Exception as e:
        return jsonify({'success': False, 'reply': f'Erro no bot: {str(e)}'}), 400

@app.route('/api/faq/add', methods=['POST'])
def api_add_faq():
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        answer = data.get('answer', '').strip()
        category = data.get('category', 'Geral').strip()
        keywords = data.get('keywords', '').strip()

        if not question or not answer:
            return jsonify({'success': False, 'message': 'Pergunta e resposta são obrigatórias.'}), 400

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO faqs (question, answer, category, keywords, is_active)
            VALUES (?, ?, ?, ?, 1)
        """, (question, answer, category, keywords))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Nova FAQ adicionada com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/faq/delete/<int:faq_id>', methods=['POST', 'DELETE'])
def api_delete_faq(faq_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM faqs WHERE id = ?", (faq_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'FAQ removida com sucesso.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/kb/add', methods=['POST'])
def api_add_kb():
    try:
        data = request.get_json()
        title = data.get('title', '').strip()
        category = data.get('category', 'Geral').strip()
        content = data.get('content', '').strip()
        now_date = datetime.now().strftime("%Y-%m-%d")

        if not title or not content:
            return jsonify({'success': False, 'message': 'Título e conteúdo são obrigatórios.'}), 400

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO knowledge_base (title, category, content, views_count, updated_at)
            VALUES (?, ?, ?, 0, ?)
        """, (title, category, content, now_date))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Artigo da Base de Conhecimento publicado!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

if __name__ == '__main__':
    print("[Starting] EJAJ TECH - BotCorp AI Chatbot SaaS na porta 6914...")
    app.run(host='0.0.0.0', port=6914, debug=True)
