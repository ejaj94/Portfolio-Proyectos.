import os
import sqlite3
import json
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'workorders.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def generate_order_code():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM work_orders')
    count = cursor.fetchone()[0] + 1
    conn.close()
    return f"OT-2026-{1000 + count}"

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    
    # Stats
    cursor.execute('SELECT COUNT(*) FROM work_orders')
    total_orders = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM work_orders WHERE status = 'Pendente'")
    pending_orders = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM work_orders WHERE status = 'Em Progresso'")
    in_progress_orders = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM work_orders WHERE status = 'Concluída'")
    completed_orders = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(total_cost) FROM work_orders WHERE status = 'Concluída'")
    total_revenue_row = cursor.fetchone()[0]
    total_revenue = total_revenue_row if total_revenue_row else 0.0
    
    # Recent work orders
    cursor.execute('SELECT * FROM work_orders ORDER BY id DESC LIMIT 5')
    recent_orders = cursor.fetchall()
    
    cursor.execute('SELECT * FROM technicians WHERE status = "Disponível"')
    available_techs = cursor.fetchall()
    
    conn.close()
    
    return render_template('index.html',
                           total_orders=total_orders,
                           pending_orders=pending_orders,
                           in_progress_orders=in_progress_orders,
                           completed_orders=completed_orders,
                           total_revenue=total_revenue,
                           recent_orders=recent_orders,
                           available_techs=available_techs)

@app.route('/workorders')
def workorders_list():
    conn = get_db()
    cursor = conn.cursor()
    
    status_filter = request.args.get('status', '')
    priority_filter = request.args.get('priority', '')
    query_search = request.args.get('q', '').strip()
    
    sql = "SELECT * FROM work_orders WHERE 1=1"
    params = []
    
    if status_filter:
        sql += " AND status = ?"
        params.append(status_filter)
        
    if priority_filter:
        sql += " AND priority = ?"
        params.append(priority_filter)
        
    if query_search:
        sql += " AND (code LIKE ? OR client_name LIKE ? OR client_company LIKE ? OR title LIKE ?)"
        term = f"%{query_search}%"
        params.extend([term, term, term, term])
        
    sql += " ORDER BY id DESC"
    
    cursor.execute(sql, params)
    orders = cursor.fetchall()
    
    cursor.execute('SELECT * FROM technicians')
    techs = cursor.fetchall()
    
    conn.close()
    return render_template('workorders.html', orders=orders, techs=techs, status_filter=status_filter, priority_filter=priority_filter, query_search=query_search)

@app.route('/workorder/new', methods=['GET'])
def new_workorder_form():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM technicians')
    techs = cursor.fetchall()
    conn.close()
    
    next_code = generate_order_code()
    return render_template('workorder_form.html', techs=techs, next_code=next_code)

@app.route('/workorder/<code_id>')
def workorder_detail(code_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM work_orders WHERE code = ?', (code_id,))
    order = cursor.fetchone()
    
    if not order:
        conn.close()
        return "Folha de Serviço não encontrada", 404
        
    cursor.execute('SELECT * FROM work_order_materials WHERE work_order_id = ?', (order['id'],))
    materials = cursor.fetchall()
    
    cursor.execute('SELECT * FROM technicians')
    techs = cursor.fetchall()
    
    photos = []
    if order['photo_urls']:
        try:
            photos = json.loads(order['photo_urls'])
        except:
            photos = []
            
    conn.close()
    return render_template('workorder_view.html', order=order, materials=materials, techs=techs, photos=photos)

@app.route('/workorder/<code_id>/pdf')
def workorder_pdf(code_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM work_orders WHERE code = ?', (code_id,))
    order = cursor.fetchone()
    
    if not order:
        conn.close()
        return "Folha de Serviço não encontrada", 404
        
    cursor.execute('SELECT * FROM work_order_materials WHERE work_order_id = ?', (order['id'],))
    materials = cursor.fetchall()
    
    photos = []
    if order['photo_urls']:
        try:
            photos = json.loads(order['photo_urls'])
        except:
            photos = []
            
    conn.close()
    return render_template('workorder_pdf.html', order=order, materials=materials, photos=photos)

# API ENDPOINTS

@app.route('/api/workorders/create', methods=['POST'])
def api_create_workorder():
    try:
        data = request.get_json()
        code = generate_order_code()
        client_name = data.get('client_name', '').strip()
        client_company = data.get('client_company', '').strip()
        client_address = data.get('client_address', '').strip()
        client_phone = data.get('client_phone', '').strip()
        technician_name = data.get('technician_name', '').strip()
        priority = data.get('priority', 'Média')
        title = data.get('title', '').strip()
        problem_description = data.get('problem_description', '').strip()
        labor_hours = float(data.get('labor_hours', 0.0))
        labor_rate = float(data.get('labor_rate', 35.0))
        
        materials_list = data.get('materials', [])
        photo_urls_list = data.get('photo_urls', [])
        
        subtotal_materials = 0.0
        for mat in materials_list:
            qty = int(mat.get('quantity', 1))
            unit_p = float(mat.get('unit_price', 0.0))
            subtotal_materials += qty * unit_p
            
        total_cost = (labor_hours * labor_rate) + subtotal_materials
        photo_json = json.dumps(photo_urls_list)
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO work_orders (
                code, client_name, client_company, client_address, client_phone,
                technician_name, priority, status, title, problem_description,
                labor_hours, labor_rate, subtotal_materials, total_cost, photo_urls
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 'Pendente', ?, ?, ?, ?, ?, ?, ?)
        ''', (
            code, client_name, client_company, client_address, client_phone,
            technician_name, priority, title, problem_description,
            labor_hours, labor_rate, subtotal_materials, total_cost, photo_json
        ))
        
        wo_id = cursor.lastrowid
        
        for mat in materials_list:
            qty = int(mat.get('quantity', 1))
            unit_p = float(mat.get('unit_price', 0.0))
            t_price = qty * unit_p
            item_name = mat.get('item_name', '').strip()
            if item_name:
                cursor.execute('''
                    INSERT INTO work_order_materials (work_order_id, item_name, quantity, unit_price, total_price)
                    VALUES (?, ?, ?, ?, ?)
                ''', (wo_id, item_name, qty, unit_p, t_price))
                
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'code': code, 'message': 'Folha de Serviço criada com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/workorders/status', methods=['POST'])
def api_update_status():
    try:
        data = request.get_json()
        code = data.get('code')
        status = data.get('status')
        resolution_notes = data.get('resolution_notes', '')
        labor_hours = float(data.get('labor_hours', 0.0))
        labor_rate = float(data.get('labor_rate', 35.0))
        technician_name = data.get('technician_name')
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM work_orders WHERE code = ?', (code,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return jsonify({'success': False, 'message': 'Ordem não encontrada'}), 404
            
        wo_id = row['id']
        cursor.execute('SELECT SUM(total_price) FROM work_order_materials WHERE work_order_id = ?', (wo_id,))
        mat_subtotal_row = cursor.fetchone()[0]
        subtotal_materials = mat_subtotal_row if mat_subtotal_row else 0.0
        
        total_cost = (labor_hours * labor_rate) + subtotal_materials
        
        cursor.execute('''
            UPDATE work_orders
            SET status = ?, resolution_notes = ?, labor_hours = ?, labor_rate = ?, total_cost = ?, technician_name = COALESCE(?, technician_name)
            WHERE code = ?
        ''', (status, resolution_notes, labor_hours, labor_rate, total_cost, technician_name, code))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Ordem de trabalho atualizada com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/workorders/sign', methods=['POST'])
def api_sign_workorder():
    try:
        data = request.get_json()
        code = data.get('code')
        signature_data = data.get('signature_data')
        signed_by_name = data.get('signed_by_name')
        
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE work_orders
            SET signature_data = ?, signed_by_name = ?, signed_at = ?, status = 'Concluída'
            WHERE code = ?
        ''', (signature_data, signed_by_name, now_str, code))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Assinatura digital guardada e Ordem Concluída!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/workorders/add_material', methods=['POST'])
def api_add_material():
    try:
        data = request.get_json()
        code = data.get('code')
        item_name = data.get('item_name', '').strip()
        quantity = int(data.get('quantity', 1))
        unit_price = float(data.get('unit_price', 0.0))
        total_price = quantity * unit_price
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id, labor_hours, labor_rate FROM work_orders WHERE code = ?', (code,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return jsonify({'success': False, 'message': 'Ordem não encontrada'}), 404
            
        wo_id = row['id']
        cursor.execute('''
            INSERT INTO work_order_materials (work_order_id, item_name, quantity, unit_price, total_price)
            VALUES (?, ?, ?, ?, ?)
        ''', (wo_id, item_name, quantity, unit_price, total_price))
        
        # Recalculate totals
        cursor.execute('SELECT SUM(total_price) FROM work_order_materials WHERE work_order_id = ?', (wo_id,))
        subtotal_mat = cursor.fetchone()[0] or 0.0
        total_c = (row['labor_hours'] * row['labor_rate']) + subtotal_mat
        
        cursor.execute('UPDATE work_orders SET subtotal_materials = ?, total_cost = ? WHERE id = ?', (subtotal_mat, total_c, wo_id))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Material adicionado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/workorders/delete', methods=['POST'])
def api_delete_workorder():
    try:
        data = request.get_json()
        code = data.get('code')
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM work_orders WHERE code = ?', (code,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Folha de Serviço eliminada.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

if __name__ == '__main__':
    print("[Starting] EJAJ TECH - Sistema de Órdenes de Trabajo SaaS na porta 6904...")
    app.run(host='0.0.0.0', port=6904, debug=True)
