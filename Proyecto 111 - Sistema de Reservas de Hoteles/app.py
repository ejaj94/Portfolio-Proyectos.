from flask import Flask, render_template, request, jsonify
from datetime import datetime
from database import (
    init_db, get_all_rooms, add_room, update_room_status,
    get_all_clients, add_client,
    check_availability, get_all_bookings, create_booking, update_booking_status,
    get_all_pricing, add_pricing_rule,
    get_all_payments, add_payment,
    get_dashboard_stats
)

app = Flask(__name__)
PORT = 6964

init_db()

@app.route('/')
def index():
    stats = get_dashboard_stats()
    rooms = get_all_rooms()
    bookings = get_all_bookings()
    clients = get_all_clients()
    pricing = get_all_pricing()
    payments = get_all_payments()
    return render_template(
        'index.html',
        stats=stats,
        rooms=rooms,
        bookings=bookings,
        clients=clients,
        pricing=pricing,
        payments=payments
    )

@app.route('/api/stats', methods=['GET'])
def api_stats():
    return jsonify(get_dashboard_stats())

@app.route('/api/rooms', methods=['GET', 'POST'])
def handle_rooms():
    if request.method == 'POST':
        data = request.json or {}
        room_number = data.get('room_number', '').strip()
        room_type = data.get('room_type', 'Standard Double').strip()
        title = data.get('title', '').strip()
        capacity = int(data.get('capacity', 2))
        base_price = float(data.get('base_price', 100.0))
        floor = int(data.get('floor', 1))
        amenities = data.get('amenities', 'Wi-Fi, AC, TV 4K').strip()
        icon = data.get('icon', 'fa-bed').strip()
        description = data.get('description', '').strip()

        if not room_number or not title:
            return jsonify({"error": "Número do quarto e título são obrigatórios."}), 400

        try:
            room_id = add_room(room_number, room_type, title, capacity, base_price, floor, amenities, icon, description)
            return jsonify({"success": True, "message": "Quarto adicionado com sucesso!", "room_id": room_id})
        except Exception as e:
            return jsonify({"error": f"Erro ao adicionar quarto: {str(e)}"}), 400

    return jsonify(get_all_rooms())

@app.route('/api/rooms/<int:room_id>/status', methods=['PUT'])
def handle_room_status(room_id):
    data = request.json or {}
    new_status = data.get('status', 'Disponível').strip()
    update_room_status(room_id, new_status)
    return jsonify({"success": True, "message": f"Estado do quarto alterado para '{new_status}'."})

@app.route('/api/availability', methods=['GET'])
def handle_availability():
    check_in = request.args.get('check_in', '').strip()
    check_out = request.args.get('check_out', '').strip()
    room_type = request.args.get('room_type', '').strip()

    if not check_in or not check_out:
        return jsonify({"error": "Datas de check-in e check-out obrigatórias."}), 400

    try:
        d1 = datetime.strptime(check_in, '%Y-%m-%d')
        d2 = datetime.strptime(check_out, '%Y-%m-%d')
        nights = (d2 - d1).days
        if nights <= 0:
            return jsonify({"error": "Data de check-out deve ser posterior ao check-in."}), 400
    except ValueError:
        return jsonify({"error": "Formato de data inválido (YYYY-MM-DD)."}), 400

    available_rooms = check_availability(check_in, check_out, room_type)
    
    # Calculate total per room for requested nights
    for r in available_rooms:
        r['nights'] = nights
        r['total_estimate'] = round(r['base_price'] * nights, 2)

    return jsonify({
        "success": True,
        "nights": nights,
        "available_count": len(available_rooms),
        "rooms": available_rooms
    })

@app.route('/api/bookings', methods=['GET', 'POST'])
def handle_bookings():
    if request.method == 'POST':
        data = request.json or {}
        room_id = int(data.get('room_id', 0))
        client_id = data.get('client_id')
        
        # If client does not exist, create client on the fly
        if not client_id:
            c_name = data.get('client_name', '').strip()
            c_email = data.get('client_email', '').strip()
            c_phone = data.get('client_phone', '').strip()
            c_doc = data.get('client_doc', '').strip()
            c_nat = data.get('client_nat', 'Portugal').strip()
            c_vip = data.get('client_vip', 'Standard').strip()
            if not c_name or not c_email:
                return jsonify({"error": "Dados do cliente incompletos."}), 400
            client_id = add_client(c_name, c_email, c_phone, c_doc, c_nat, c_vip, 'Registado durante reserva.')
        else:
            client_id = int(client_id)

        check_in = data.get('check_in', '').strip()
        check_out = data.get('check_out', '').strip()
        guests_count = int(data.get('guests_count', 2))
        total_price = float(data.get('total_price', 0.0))
        paid_amount = float(data.get('paid_amount', 0.0))
        payment_method = data.get('payment_method', 'Cartão de Crédito').strip()
        special_requests = data.get('special_requests', '').strip()

        if not check_in or not check_out or total_price <= 0:
            return jsonify({"error": "Dados de reserva inválidos ou preço total nulo."}), 400

        booking_id, code = create_booking(
            room_id, client_id, check_in, check_out,
            guests_count, total_price, paid_amount, payment_method, special_requests
        )
        return jsonify({
            "success": True,
            "message": f"Reserva {code} confirmada com sucesso!",
            "booking_id": booking_id,
            "booking_code": code
        })

    return jsonify(get_all_bookings())

@app.route('/api/bookings/<int:booking_id>/status', methods=['PUT'])
def handle_booking_status(booking_id):
    data = request.json or {}
    new_status = data.get('status', 'Check-in').strip()
    success = update_booking_status(booking_id, new_status)
    if not success:
        return jsonify({"error": "Reserva não encontrada."}), 404
    return jsonify({"success": True, "message": f"Estado da reserva atualizado para '{new_status}'!"})

@app.route('/api/clients', methods=['GET', 'POST'])
def handle_clients():
    if request.method == 'POST':
        data = request.json or {}
        full_name = data.get('full_name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        document_id = data.get('document_id', '').strip()
        nationality = data.get('nationality', 'Portugal').strip()
        vip_level = data.get('vip_level', 'Standard').strip()
        notes = data.get('notes', '').strip()

        if not full_name or not email:
            return jsonify({"error": "Nome e email são obrigatórios."}), 400

        try:
            cid = add_client(full_name, email, phone, document_id, nationality, vip_level, notes)
            return jsonify({"success": True, "message": "Hóspede registado com sucesso!", "client_id": cid})
        except Exception as e:
            return jsonify({"error": f"Erro ao registar hóspede: {str(e)}"}), 400

    return jsonify(get_all_clients())

@app.route('/api/pricing', methods=['GET', 'POST'])
def handle_pricing():
    if request.method == 'POST':
        data = request.json or {}
        name = data.get('name', '').strip()
        season_type = data.get('season_type', 'Época Alta').strip()
        multiplier = float(data.get('multiplier', 1.0))
        description = data.get('description', '').strip()

        if not name:
            return jsonify({"error": "Nome da regra é obrigatório."}), 400

        add_pricing_rule(name, season_type, multiplier, description)
        return jsonify({"success": True, "message": "Regra de preço adicionada com sucesso!"})

    return jsonify(get_all_pricing())

@app.route('/api/payments', methods=['GET', 'POST'])
def handle_payments():
    if request.method == 'POST':
        data = request.json or {}
        booking_id = int(data.get('booking_id', 0))
        amount = float(data.get('amount', 0.0))
        method = data.get('method', 'Cartão de Crédito').strip()

        if booking_id <= 0 or amount <= 0:
            return jsonify({"error": "Reserva inválida ou montante inferior a zero."}), 400

        ref = add_payment(booking_id, amount, method)
        if not ref:
            return jsonify({"error": "Reserva não encontrada."}), 404
        return jsonify({"success": True, "message": "Pagamento registado com sucesso!", "reference": ref})

    return jsonify(get_all_payments())

if __name__ == '__main__':
    print(f"GrandHotel Suite PMS ativo na porta {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=True)
