import os
from flask import Flask, render_template, request, jsonify
import database

app = Flask(__name__)

# Ensure DB is initialized
database.init_db()

@app.route('/')
def index():
    return render_template('index.html')

# 1. Dashboard Stats
@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        stats = database.get_dashboard_stats()
        return jsonify({"success": True, "stats": stats})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 2. Vehicles
@app.route('/api/vehicles', methods=['GET', 'POST'])
def handle_vehicles():
    if request.method == 'GET':
        vehicles = database.get_all_vehicles()
        return jsonify({"success": True, "vehicles": vehicles})
    
    data = request.json or {}
    try:
        vid = database.add_vehicle(
            plate=data.get('plate'),
            brand=data.get('brand'),
            model=data.get('model'),
            category=data.get('category', 'Sedán'),
            year=int(data.get('year', 2024)),
            transmission=data.get('transmission', 'Automático'),
            fuel_type=data.get('fuel_type', 'Gasolina'),
            daily_rate=float(data.get('daily_rate', 70.0)),
            mileage=int(data.get('mileage', 0)),
            fuel_level=int(data.get('fuel_level', 100)),
            seats=int(data.get('seats', 5)),
            deposit=float(data.get('deposit', 500.0)),
            features=data.get('features', ''),
            image_icon=data.get('image_icon', 'fa-car')
        )
        return jsonify({"success": True, "vehicle_id": vid, "message": "Veículo adicionado com sucesso!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/vehicles/<int:vid>/status', methods=['POST'])
def update_veh_status(vid):
    data = request.json or {}
    new_status = data.get('status')
    if not new_status:
        return jsonify({"success": False, "error": "Status não fornecido."}), 400
    try:
        database.update_vehicle_status(vid, new_status)
        return jsonify({"success": True, "message": f"Estado atualizado para {new_status}"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 3. Clients
@app.route('/api/clients', methods=['GET', 'POST'])
def handle_clients():
    if request.method == 'GET':
        clients = database.get_all_clients()
        return jsonify({"success": True, "clients": clients})
    
    data = request.json or {}
    try:
        cid = database.add_client(
            full_name=data.get('full_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            license_number=data.get('license_number'),
            license_expiry=data.get('license_expiry'),
            nationality=data.get('nationality', 'Portugal'),
            client_type=data.get('client_type', 'Particular'),
            notes=data.get('notes', '')
        )
        return jsonify({"success": True, "client_id": cid, "message": "Cliente cadastrado com sucesso!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# 4. Availability Search
@app.route('/api/availability', methods=['GET'])
def check_availability():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    category = request.args.get('category', 'Todas')
    
    if not start_date or not end_date:
        return jsonify({"success": False, "error": "Datas de levantamento e devolução são obrigatórias."}), 400
    
    try:
        available_vehicles = database.check_vehicle_availability(start_date, end_date, category)
        return jsonify({
            "success": True,
            "start_date": start_date,
            "end_date": end_date,
            "category": category,
            "count": len(available_vehicles),
            "vehicles": available_vehicles
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 5. Rentals & Bookings
@app.route('/api/rentals', methods=['GET', 'POST'])
def handle_rentals():
    if request.method == 'GET':
        rentals = database.get_all_rentals()
        return jsonify({"success": True, "rentals": rentals})
    
    data = request.json or {}
    try:
        rental_id, code, contract_num = database.create_rental(
            vehicle_id=int(data.get('vehicle_id')),
            client_id=int(data.get('client_id')),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            pickup_loc=data.get('pickup_location', 'Balcão Central'),
            return_loc=data.get('return_location', 'Balcão Central'),
            total_days=int(data.get('total_days', 1)),
            daily_price=float(data.get('daily_price', 0.0)),
            extras_price=float(data.get('extras_price', 0.0)),
            total_amount=float(data.get('total_amount', 0.0)),
            paid_amount=float(data.get('paid_amount', 0.0)),
            deposit_amount=float(data.get('deposit_amount', 500.0)),
            extras=data.get('extras', 'Sem extras'),
            insurance_type=data.get('insurance_type', 'Básico')
        )
        return jsonify({
            "success": True,
            "rental_id": rental_id,
            "rental_code": code,
            "contract_number": contract_num,
            "message": f"Reserva {code} e Contrato {contract_num} criados com sucesso!"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/rentals/<int:rid>/status', methods=['POST'])
def handle_rental_status(rid):
    data = request.json or {}
    status = data.get('status')
    final_km = data.get('final_km')
    final_fuel = data.get('final_fuel')
    
    if final_km:
        final_km = int(final_km)
    if final_fuel:
        final_fuel = int(final_fuel)
        
    success = database.update_rental_status(rid, status, final_km, final_fuel)
    if success:
        return jsonify({"success": True, "message": f"Reserva atualizada para {status}"})
    return jsonify({"success": False, "error": "Reserva não encontrada."}), 404

# 6. Contracts
@app.route('/api/contracts', methods=['GET'])
def get_contracts():
    contracts = database.get_all_contracts()
    return jsonify({"success": True, "contracts": contracts})

# 7. Pricing
@app.route('/api/pricing', methods=['GET', 'POST'])
def handle_pricing():
    if request.method == 'GET':
        pricing = database.get_all_pricing()
        return jsonify({"success": True, "pricing": pricing})
    
    data = request.json or {}
    try:
        database.add_pricing_rule(
            title=data.get('title'),
            category=data.get('category', 'Todos'),
            season=data.get('season', 'Padrão'),
            multiplier=float(data.get('multiplier', 1.0)),
            min_days=int(data.get('min_days', 1)),
            description=data.get('description', '')
        )
        return jsonify({"success": True, "message": "Regra tarifária adicionada com sucesso!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# 8. Payments
@app.route('/api/payments', methods=['GET', 'POST'])
def handle_payments():
    if request.method == 'GET':
        payments = database.get_all_payments()
        return jsonify({"success": True, "payments": payments})
    
    data = request.json or {}
    try:
        ref = database.add_payment(
            rental_id=int(data.get('rental_id')),
            amount=float(data.get('amount')),
            payment_type=data.get('payment_type', 'Aluguer'),
            method=data.get('method', 'Cartão de Crédito')
        )
        if ref:
            return jsonify({"success": True, "reference": ref, "message": "Pagamento registado com sucesso!"})
        return jsonify({"success": False, "error": "Reserva não encontrada."}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6965))
    print(f">> DrivePulse Rent-a-Car Server rodando em http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
