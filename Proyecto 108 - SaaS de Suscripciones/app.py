from flask import Flask, render_template, request, jsonify
from database import init_db, add_subscription, cancel_subscription, get_all_subscriptions, get_all_invoices, get_saas_metrics

app = Flask(__name__)
PORT = 6961

init_db()

@app.route('/')
def index():
    metrics = get_saas_metrics()
    subscriptions = get_all_subscriptions()
    invoices = get_all_invoices()
    return render_template('index.html', metrics=metrics, subscriptions=subscriptions, invoices=invoices)

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    data = request.json or {}
    user_name = data.get('user_name', 'Utilizador Exemplo').strip()
    user_email = data.get('user_email', 'user@subcraft.ai').strip()
    plan_name = data.get('plan_name', 'Pro Plan').strip()
    billing_cycle = data.get('billing_cycle', 'Mensal').strip()
    amount = float(data.get('amount', 29.00))
    payment_method = data.get('payment_method', 'Cartao de Credito').strip()

    if not user_name or not user_email or not plan_name:
        return jsonify({"error": "Dados de subscricao incompletos."}), 400

    sub_id = add_subscription(user_name, user_email, plan_name, billing_cycle, amount, payment_method)
    
    return jsonify({
        "success": True,
        "message": f"Subscricao do {plan_name} ativada com sucesso!",
        "subscription_id": sub_id
    })

@app.route('/api/cancel', methods=['POST'])
def cancel():
    data = request.json or {}
    sub_id = data.get('subscription_id')
    reason = data.get('reason', 'Nao especificado').strip()

    if not sub_id:
        return jsonify({"error": "ID de subscricao invalido."}), 400

    cancel_subscription(sub_id, reason)
    return jsonify({
        "success": True,
        "message": "Subscricao cancelada com sucesso."
    })

@app.route('/api/metrics')
def metrics():
    return jsonify(get_saas_metrics())

@app.route('/api/invoices')
def invoices():
    return jsonify(get_all_invoices())

if __name__ == '__main__':
    print(f"Servidor SubCraft AI iniciado na porta {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=True)
