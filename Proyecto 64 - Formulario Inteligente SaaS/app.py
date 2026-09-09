import os
import sqlite3
import json
import csv
import io
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, Response

app = Flask(__name__)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'forms.db')

@app.template_filter('from_json')
def from_json_filter(value):
    try:
        return json.loads(value) if value else []
    except Exception:
        return []


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def slugify(text):
    import re
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text or 'formulario-sem-titulo'

@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM forms ORDER BY id DESC")
    forms_raw = cursor.fetchall()
    
    forms = []
    total_responses = 0
    for f in forms_raw:
        f_dict = dict(f)
        cursor.execute("SELECT COUNT(*) as cnt FROM form_responses WHERE form_id = ?", (f['id'],))
        resp_count = cursor.fetchone()['cnt']
        f_dict['response_count'] = resp_count
        total_responses += resp_count
        forms.append(f_dict)

    conn.close()
    return render_template('dashboard.html', forms=forms, total_forms=len(forms), total_responses=total_responses)

@app.route('/builder')
def builder_page():
    form_id = request.args.get('id')
    form_data = None
    if form_id:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM forms WHERE id = ?", (form_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            form_data = dict(row)

    return render_template('builder.html', form_data=form_data)

@app.route('/form/<slug>')
def public_form_page(slug):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM forms WHERE slug = ?", (slug,))
    form_row = cursor.fetchone()
    conn.close()

    if not form_row:
        return render_template('public_form.html', error="Formulário não encontrado."), 404

    form_dict = dict(form_row)
    fields = json.loads(form_dict.get('fields_json', '[]'))
    return render_template('public_form.html', form_data=form_dict, fields=fields)

@app.route('/form/<slug>/submit', methods=['POST'])
def public_form_submit(slug):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM forms WHERE slug = ?", (slug,))
    form_row = cursor.fetchone()

    if not form_row:
        conn.close()
        return jsonify({'success': False, 'message': 'Formulário não encontrado.'}), 404

    form_id = form_row['id']
    fields = json.loads(form_row['fields_json'])

    # Parse submitted form answers
    answers = {}
    errors = []
    for field in fields:
        field_id = field['id']
        label = field['label']
        is_required = field.get('required', False)
        
        # Handle checkbox multi-values vs single inputs
        if field['type'] == 'checkbox':
            val = request.form.getlist(field_id)
            if is_required and not val:
                errors.append(f"O campo '{label}' é obrigatório.")
            answers[field_id] = val
        else:
            val = request.form.get(field_id, '').strip()
            if is_required and not val:
                errors.append(f"O campo '{label}' é obrigatório.")
            answers[field_id] = val

    if errors:
        conn.close()
        return jsonify({'success': False, 'message': errors[0], 'errors': errors}), 400

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    user_ip = request.remote_addr or '127.0.0.1'

    cursor.execute("""
    INSERT INTO form_responses (form_id, answers_json, user_ip, submitted_at)
    VALUES (?, ?, ?, ?)
    """, (form_id, json.dumps(answers), user_ip, now_str))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': 'Obrigado! A sua resposta foi submetida com sucesso.'
    })

@app.route('/responses/<int:form_id>')
def responses_page(form_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM forms WHERE id = ?", (form_id,))
    form_row = cursor.fetchone()

    if not form_row:
        conn.close()
        return redirect(url_for('dashboard'))

    form_dict = dict(form_row)
    fields = json.loads(form_dict['fields_json'])

    cursor.execute("SELECT * FROM form_responses WHERE form_id = ? ORDER BY id DESC", (form_id,))
    responses_raw = cursor.fetchall()
    conn.close()

    parsed_responses = []
    for r in responses_raw:
        r_dict = dict(r)
        r_dict['answers'] = json.loads(r['answers_json'])
        parsed_responses.append(r_dict)

    return render_template('responses.html', form_data=form_dict, fields=fields, responses=parsed_responses)

@app.route('/analytics/<int:form_id>')
def analytics_page(form_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM forms WHERE id = ?", (form_id,))
    form_row = cursor.fetchone()

    if not form_row:
        conn.close()
        return redirect(url_for('dashboard'))

    form_dict = dict(form_row)
    fields = json.loads(form_dict['fields_json'])

    cursor.execute("SELECT * FROM form_responses WHERE form_id = ? ORDER BY id DESC", (form_id,))
    responses_raw = cursor.fetchall()
    conn.close()

    total_submissions = len(responses_raw)

    # Compute summary breakdown for rating, radio, checkbox, dropdown
    analytics_summary = {}
    for f in fields:
        f_id = f['id']
        f_type = f['type']
        if f_type in ['radio', 'dropdown', 'rating', 'checkbox']:
            counts = {}
            for r in responses_raw:
                ans_map = json.loads(r['answers_json'])
                val = ans_map.get(f_id)
                if isinstance(val, list):
                    for item in val:
                        counts[item] = counts.get(item, 0) + 1
                elif val:
                    counts[str(val)] = counts.get(str(val), 0) + 1
            analytics_summary[f_id] = {
                'label': f['label'],
                'type': f_type,
                'counts': counts
            }

    return render_template('analytics.html', form_data=form_dict, total_submissions=total_submissions, summary=analytics_summary)

# REST API ENDPOINTS

@app.route('/api/form/save', methods=['POST'])
def api_save_form():
    try:
        data = request.get_json() or {}
        form_id = data.get('id')
        title = data.get('title', 'Novo Formulário').strip()
        description = data.get('description', '').strip()
        theme_color = data.get('theme_color', '#8B5CF6').strip()
        fields = data.get('fields', [])

        if not title:
            return jsonify({'success': False, 'message': 'O título do formulário é obrigatório.'}), 400

        base_slug = slugify(title)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()

        if form_id:
            # Update existing form
            cursor.execute("""
            UPDATE forms
            SET title = ?, description = ?, fields_json = ?, theme_color = ?
            WHERE id = ?
            """, (title, description, json.dumps(fields), theme_color, form_id))
            target_id = form_id
        else:
            # Create new form with unique slug
            slug = base_slug
            counter = 1
            while True:
                cursor.execute("SELECT id FROM forms WHERE slug = ?", (slug,))
                if not cursor.fetchone():
                    break
                slug = f"{base_slug}-{counter}"
                counter += 1

            cursor.execute("""
            INSERT INTO forms (title, description, slug, fields_json, theme_color, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (title, description, slug, json.dumps(fields), theme_color, now_str))
            target_id = cursor.lastrowid

        conn.commit()

        # Retrieve saved slug
        cursor.execute("SELECT slug FROM forms WHERE id = ?", (target_id,))
        saved_slug = cursor.fetchone()['slug']
        conn.close()

        return jsonify({
            'success': True,
            'form_id': target_id,
            'slug': saved_slug,
            'message': f'Formulário "{title}" guardado com sucesso!'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/form/delete/<int:form_id>', methods=['POST', 'DELETE'])
def api_delete_form(form_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM forms WHERE id = ?", (form_id,))
        cursor.execute("DELETE FROM form_responses WHERE form_id = ?", (form_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Formulário e respostas eliminados com sucesso.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/form/export/<int:form_id>/<fmt>')
def api_export_responses(form_id, fmt):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM forms WHERE id = ?", (form_id,))
    form_row = cursor.fetchone()

    if not form_row:
        conn.close()
        return redirect(url_for('dashboard'))

    form_dict = dict(form_row)
    fields = json.loads(form_dict['fields_json'])

    cursor.execute("SELECT * FROM form_responses WHERE form_id = ? ORDER BY id ASC", (form_id,))
    responses_raw = cursor.fetchall()
    conn.close()

    filename_base = slugify(form_dict['title'])

    if fmt.lower() == 'json':
        output_list = []
        for r in responses_raw:
            r_answers = json.loads(r['answers_json'])
            # Map field ids to readable labels
            readable_answers = {}
            for f in fields:
                f_id = f['id']
                readable_answers[f['label']] = r_answers.get(f_id, '')
            output_list.append({
                'response_id': r['id'],
                'submitted_at': r['submitted_at'],
                'user_ip': r['user_ip'],
                'answers': readable_answers
            })
        
        json_data = json.dumps(output_list, indent=2, ensure_ascii=False)
        return Response(
            json_data,
            mimetype='application/json',
            headers={'Content-Disposition': f'attachment; filename=respostas_{filename_base}.json'}
        )
    else:
        # Export CSV
        output = io.StringIO()
        writer = csv.writer(output)

        headers = ['ID Resposta', 'Data / Hora', 'Endereço IP'] + [f['label'] for f in fields]
        writer.writerow(headers)

        for r in responses_raw:
            r_answers = json.loads(r['answers_json'])
            row = [r['id'], r['submitted_at'], r['user_ip']]
            for f in fields:
                val = r_answers.get(f['id'], '')
                if isinstance(val, list):
                    val = ', '.join(val)
                row.append(str(val))
            writer.writerow(row)

        csv_content = output.getvalue()
        return Response(
            csv_content,
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename=respostas_{filename_base}.csv'}
        )

if __name__ == '__main__':
    print("[Starting] EJAJ TECH - FormCraft AI SaaS na porta 6917...")
    app.run(host='127.0.0.1', port=6917, debug=False, use_reloader=False)
