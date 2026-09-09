import os
import sqlite3
import json
import csv
import io
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, Response

app = Flask(__name__)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'surveys.db')

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
    return text or 'inquerito-sem-titulo'

def calculate_nps(scores):
    if not scores:
        return 0, 0, 0, 0
    total = len(scores)
    detractors = sum(1 for s in scores if s <= 6)
    passives = sum(1 for s in scores if 7 <= s <= 8)
    promoters = sum(1 for s in scores if s >= 9)
    
    nps_score = round(((promoters - detractors) / total) * 100)
    return nps_score, promoters, passives, detractors

@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM surveys ORDER BY id DESC")
    surveys_raw = cursor.fetchall()
    
    surveys = []
    total_responses = 0
    all_nps_scores = []

    for s in surveys_raw:
        s_dict = dict(s)
        cursor.execute("SELECT answers_json FROM survey_responses WHERE survey_id = ?", (s['id'],))
        resp_rows = cursor.fetchall()
        resp_count = len(resp_rows)
        s_dict['response_count'] = resp_count
        total_responses += resp_count

        # Gather NPS scores for survey
        questions = json.loads(s['questions_json'])
        nps_q_id = next((q['id'] for q in questions if q.get('type') == 'nps'), None)
        
        survey_nps_scores = []
        if nps_q_id:
            for r in resp_rows:
                ans = json.loads(r['answers_json'])
                val = ans.get(nps_q_id)
                if val is not None and str(val).isdigit():
                    score = int(val)
                    survey_nps_scores.append(score)
                    all_nps_scores.append(score)

        s_nps, _, _, _ = calculate_nps(survey_nps_scores)
        s_dict['nps_score'] = s_nps if survey_nps_scores else None
        surveys.append(s_dict)

    global_nps, _, _, _ = calculate_nps(all_nps_scores)
    conn.close()

    return render_template(
        'dashboard.html',
        surveys=surveys,
        total_surveys=len(surveys),
        total_responses=total_responses,
        global_nps=global_nps if all_nps_scores else '--'
    )

@app.route('/create')
def create_page():
    survey_id = request.args.get('id')
    survey_data = None
    if survey_id:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM surveys WHERE id = ?", (survey_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            survey_data = dict(row)

    return render_template('create.html', survey_data=survey_data)

@app.route('/survey/<slug>')
def public_survey_page(slug):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM surveys WHERE slug = ?", (slug,))
    survey_row = cursor.fetchone()
    conn.close()

    if not survey_row:
        return render_template('public_survey.html', error="Inquérito não encontrado."), 404

    survey_dict = dict(survey_row)
    questions = json.loads(survey_dict.get('questions_json', '[]'))
    return render_template('public_survey.html', survey_data=survey_dict, questions=questions)

@app.route('/survey/<slug>/submit', methods=['POST'])
def public_survey_submit(slug):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM surveys WHERE slug = ?", (slug,))
    survey_row = cursor.fetchone()

    if not survey_row:
        conn.close()
        return jsonify({'success': False, 'message': 'Inquérito não encontrado.'}), 404

    survey_id = survey_row['id']
    questions = json.loads(survey_row['questions_json'])

    answers = {}
    errors = []

    for q in questions:
        q_id = q['id']
        q_title = q['title']
        is_required = q.get('required', False)

        val = request.form.get(q_id, '').strip()
        if is_required and not val:
            errors.append(f"A pergunta '{q_title}' é de resposta obrigatória.")
        answers[q_id] = val

    if errors:
        conn.close()
        return jsonify({'success': False, 'message': errors[0], 'errors': errors}), 400

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    user_ip = request.remote_addr or '127.0.0.1'

    cursor.execute("""
    INSERT INTO survey_responses (survey_id, answers_json, user_ip, submitted_at)
    VALUES (?, ?, ?, ?)
    """, (survey_id, json.dumps(answers), user_ip, now_str))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': 'Obrigado! A sua participação foi registada com sucesso.'
    })

@app.route('/results/<int:survey_id>')
def results_page(survey_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM surveys WHERE id = ?", (survey_id,))
    survey_row = cursor.fetchone()

    if not survey_row:
        conn.close()
        return redirect(url_for('dashboard'))

    survey_dict = dict(survey_row)
    questions = json.loads(survey_dict['questions_json'])

    cursor.execute("SELECT * FROM survey_responses WHERE survey_id = ? ORDER BY id DESC", (survey_id,))
    responses_raw = cursor.fetchall()
    conn.close()

    total_responses = len(responses_raw)
    question_results = {}

    for q in questions:
        q_id = q['id']
        q_type = q['type']

        if q_type == 'nps':
            nps_scores = []
            for r in responses_raw:
                ans = json.loads(r['answers_json'])
                val = ans.get(q_id)
                if val is not None and str(val).isdigit():
                    nps_scores.append(int(val))

            score, promoters, passives, detractors = calculate_nps(nps_scores)
            question_results[q_id] = {
                'title': q['title'],
                'type': 'nps',
                'nps_score': score,
                'total': len(nps_scores),
                'promoters': promoters,
                'passives': passives,
                'detractors': detractors
            }

        elif q_type in ['likert', 'choice', 'yesno']:
            counts = {}
            for r in responses_raw:
                ans = json.loads(r['answers_json'])
                val = ans.get(q_id)
                if val:
                    counts[str(val)] = counts.get(str(val), 0) + 1

            question_results[q_id] = {
                'title': q['title'],
                'type': q_type,
                'counts': counts,
                'total': sum(counts.values())
            }

        elif q_type == 'text':
            comments = []
            for r in responses_raw:
                ans = json.loads(r['answers_json'])
                val = ans.get(q_id)
                if val:
                    comments.append({
                        'text': val,
                        'date': r['submitted_at']
                    })

            question_results[q_id] = {
                'title': q['title'],
                'type': 'text',
                'comments': comments
            }

    return render_template(
        'results.html',
        survey_data=survey_dict,
        total_responses=total_responses,
        results=question_results
    )

@app.route('/responses/<int:survey_id>')
def responses_page(survey_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM surveys WHERE id = ?", (survey_id,))
    survey_row = cursor.fetchone()

    if not survey_row:
        conn.close()
        return redirect(url_for('dashboard'))

    survey_dict = dict(survey_row)
    questions = json.loads(survey_dict['questions_json'])

    cursor.execute("SELECT * FROM survey_responses WHERE survey_id = ? ORDER BY id DESC", (survey_id,))
    responses_raw = cursor.fetchall()
    conn.close()

    parsed_responses = []
    for r in responses_raw:
        r_dict = dict(r)
        r_dict['answers'] = json.loads(r['answers_json'])
        parsed_responses.append(r_dict)

    return render_template('responses.html', survey_data=survey_dict, questions=questions, responses=parsed_responses)

# REST API ENDPOINTS

@app.route('/api/survey/save', methods=['POST'])
def api_save_survey():
    try:
        data = request.get_json() or {}
        survey_id = data.get('id')
        title = data.get('title', 'Novo Inquérito').strip()
        description = data.get('description', '').strip()
        theme_color = data.get('theme_color', '#10B981').strip()
        questions = data.get('questions', [])

        if not title:
            return jsonify({'success': False, 'message': 'O título do inquérito é obrigatório.'}), 400

        base_slug = slugify(title)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()

        if survey_id:
            cursor.execute("""
            UPDATE surveys
            SET title = ?, description = ?, questions_json = ?, theme_color = ?
            WHERE id = ?
            """, (title, description, json.dumps(questions), theme_color, survey_id))
            target_id = survey_id
        else:
            slug = base_slug
            counter = 1
            while True:
                cursor.execute("SELECT id FROM surveys WHERE slug = ?", (slug,))
                if not cursor.fetchone():
                    break
                slug = f"{base_slug}-{counter}"
                counter += 1

            cursor.execute("""
            INSERT INTO surveys (title, description, slug, questions_json, theme_color, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (title, description, slug, json.dumps(questions), theme_color, now_str))
            target_id = cursor.lastrowid

        conn.commit()

        cursor.execute("SELECT slug FROM surveys WHERE id = ?", (target_id,))
        saved_slug = cursor.fetchone()['slug']
        conn.close()

        return jsonify({
            'success': True,
            'survey_id': target_id,
            'slug': saved_slug,
            'message': f'Inquérito "{title}" guardado com sucesso!'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/survey/delete/<int:survey_id>', methods=['POST', 'DELETE'])
def api_delete_survey(survey_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM surveys WHERE id = ?", (survey_id,))
        cursor.execute("DELETE FROM survey_responses WHERE survey_id = ?", (survey_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Inquérito e respostas eliminados com sucesso.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/survey/export/<int:survey_id>/<fmt>')
def api_export_responses(survey_id, fmt):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM surveys WHERE id = ?", (survey_id,))
    survey_row = cursor.fetchone()

    if not survey_row:
        conn.close()
        return redirect(url_for('dashboard'))

    survey_dict = dict(survey_row)
    questions = json.loads(survey_dict['questions_json'])

    cursor.execute("SELECT * FROM survey_responses WHERE survey_id = ? ORDER BY id ASC", (survey_id,))
    responses_raw = cursor.fetchall()
    conn.close()

    filename_base = slugify(survey_dict['title'])

    if fmt.lower() == 'json':
        output_list = []
        for r in responses_raw:
            r_answers = json.loads(r['answers_json'])
            readable_answers = {}
            for q in questions:
                q_id = q['id']
                readable_answers[q['title']] = r_answers.get(q_id, '')
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
            headers={'Content-Disposition': f'attachment; filename=inquerito_{filename_base}.json'}
        )
    else:
        output = io.StringIO()
        writer = csv.writer(output)

        headers = ['ID Resposta', 'Data / Hora', 'Endereço IP'] + [q['title'] for q in questions]
        writer.writerow(headers)

        for r in responses_raw:
            r_answers = json.loads(r['answers_json'])
            row = [r['id'], r['submitted_at'], r['user_ip']]
            for q in questions:
                val = r_answers.get(q['id'], '')
                row.append(str(val))
            writer.writerow(row)

        csv_content = output.getvalue()
        return Response(
            csv_content,
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename=inquerito_{filename_base}.csv'}
        )

if __name__ == '__main__':
    print("[Starting] EJAJ TECH - SurveyPulse AI SaaS na porta 6918...")
    app.run(host='127.0.0.1', port=6918, debug=False, use_reloader=False)
