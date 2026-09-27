from flask import Flask, render_template, request, jsonify
from database import init_db, add_member, renew_member, get_all_members, get_all_perks, get_all_payments, get_membership_metrics

app = Flask(__name__)
PORT = 6962

init_db()

@app.route('/')
def index():
    metrics = get_membership_metrics()
    members = get_all_members()
    perks = get_all_perks()
    payments = get_all_payments()
    return render_template('index.html', metrics=metrics, members=members, perks=perks, payments=payments)

@app.route('/api/membership/join', methods=['POST'])
def join_membership():
    data = request.json or {}
    name = data.get('name', 'Membro VIP').strip()
    email = data.get('email', 'membro@membercraft.ai').strip()
    tier = data.get('tier', 'Gold').strip()
    amount_paid = float(data.get('amount_paid', 39.00))
    payment_method = data.get('payment_method', 'Cartao de Credito').strip()

    if not name or not email or not tier:
        return jsonify({"error": "Dados de membresia incompletos."}), 400

    member_id = add_member(name, email, tier, amount_paid, payment_method)
    
    return jsonify({
        "success": True,
        "message": f"Membresia {tier} ativada com sucesso para {name}!",
        "member_id": member_id
    })

@app.route('/api/membership/renew', methods=['POST'])
def renew():
    data = request.json or {}
    member_id = data.get('member_id')
    
    if not member_id:
        return jsonify({"error": "ID de membro invalido."}), 400

    renew_member(member_id)
    return jsonify({
        "success": True,
        "message": "Membresia renovada com sucesso por mais 30 dias!"
    })

@app.route('/api/members')
def members_list():
    return jsonify(get_all_members())

@app.route('/api/perks')
def perks_list():
    return jsonify(get_all_perks())

if __name__ == '__main__':
    print(f"Servidor MemberCraft AI iniciado na porta {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=True)
