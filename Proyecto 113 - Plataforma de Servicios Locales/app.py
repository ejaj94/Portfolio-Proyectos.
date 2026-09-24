import os
from flask import Flask, render_template, request, jsonify
import database

app = Flask(__name__)

# Ensure Database is ready
database.init_db()

@app.route('/')
def index():
    return render_template('index.html')

# 1. Marketplace Stats
@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        stats = database.get_marketplace_stats()
        return jsonify({"success": True, "stats": stats})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 2. Professionals API
@app.route('/api/professionals', methods=['GET', 'POST'])
def handle_professionals():
    if request.method == 'GET':
        category = request.args.get('category')
        city = request.args.get('city')
        min_rating = request.args.get('min_rating')
        status = request.args.get('status')
        pros = database.get_all_professionals(category, city, min_rating, status)
        return jsonify({"success": True, "professionals": pros})
    
    data = request.json or {}
    try:
        pro_id = database.add_professional(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            category=data.get('category', 'Geral'),
            city=data.get('city', 'Lisboa'),
            hourly_rate=float(data.get('hourly_rate', 25.0)),
            bio=data.get('bio', ''),
            experience_years=int(data.get('experience_years', 3)),
            address=data.get('address', '')
        )
        return jsonify({"success": True, "pro_id": pro_id, "message": "Profissional registado com sucesso!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/professionals/<int:pro_id>/status', methods=['POST'])
def update_pro_status(pro_id):
    data = request.json or {}
    new_status = data.get('status')
    if not new_status:
        return jsonify({"success": False, "error": "Estado não fornecido."}), 400
    try:
        database.update_professional_status(pro_id, new_status)
        return jsonify({"success": True, "message": f"Estado atualizado para {new_status}"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 3. Services API
@app.route('/api/services', methods=['GET', 'POST'])
def handle_services():
    if request.method == 'GET':
        category = request.args.get('category')
        services = database.get_all_services(category)
        return jsonify({"success": True, "services": services})
    
    data = request.json or {}
    try:
        sid = database.add_service(
            professional_id=int(data.get('professional_id')),
            title=data.get('title'),
            category=data.get('category'),
            description=data.get('description'),
            price=float(data.get('price')),
            price_type=data.get('price_type', 'Por Hora'),
            estimated_hours=float(data.get('estimated_hours', 2.0))
        )
        return jsonify({"success": True, "service_id": sid, "message": "Serviço adicionado ao catálogo!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# 4. Bookings API
@app.route('/api/bookings', methods=['GET', 'POST'])
def handle_bookings():
    if request.method == 'GET':
        bookings = database.get_all_bookings()
        return jsonify({"success": True, "bookings": bookings})
    
    data = request.json or {}
    try:
        booking_id, code = database.create_booking(
            service_id=int(data.get('service_id')),
            client_name=data.get('client_name'),
            client_phone=data.get('client_phone'),
            client_email=data.get('client_email'),
            service_address=data.get('service_address'),
            city=data.get('city', 'Lisboa'),
            booking_date=data.get('booking_date'),
            time_slot=data.get('time_slot', '09:00 - 11:00'),
            notes=data.get('notes', '')
        )
        return jsonify({
            "success": True, 
            "booking_id": booking_id, 
            "booking_code": code,
            "message": f"Agendamento {code} confirmado com sucesso!"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/bookings/<int:bid>/status', methods=['POST'])
def update_b_status(bid):
    data = request.json or {}
    new_status = data.get('status')
    if not new_status:
        return jsonify({"success": False, "error": "Estado não fornecido."}), 400
    try:
        database.update_booking_status(bid, new_status)
        return jsonify({"success": True, "message": f"Agendamento atualizado para {new_status}"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 5. Reviews API
@app.route('/api/reviews', methods=['GET', 'POST'])
def handle_reviews():
    if request.method == 'GET':
        pro_id = request.args.get('pro_id')
        reviews = database.get_all_reviews(pro_id)
        return jsonify({"success": True, "reviews": reviews})
    
    data = request.json or {}
    try:
        database.add_review(
            professional_id=int(data.get('professional_id')),
            booking_id=data.get('booking_id'),
            client_name=data.get('client_name'),
            rating=int(data.get('rating', 5)),
            comment=data.get('comment')
        )
        return jsonify({"success": True, "message": "Avaliação publicada e média atualizada!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# 6. Messages & Chat API
@app.route('/api/messages', methods=['GET', 'POST'])
def handle_messages():
    if request.method == 'GET':
        pro_id = request.args.get('pro_id')
        if pro_id:
            msgs = database.get_messages_for_pro(int(pro_id))
            return jsonify({"success": True, "messages": msgs})
        convs = database.get_all_conversations()
        return jsonify({"success": True, "conversations": convs})
    
    data = request.json or {}
    try:
        mid = database.send_message(
            professional_id=int(data.get('professional_id')),
            client_name=data.get('client_name'),
            sender=data.get('sender', 'client'),
            message_text=data.get('message_text')
        )
        return jsonify({"success": True, "message_id": mid, "message": "Mensagem enviada!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6966))
    print(f">> LocalPro Marketplace Server rodando em http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
