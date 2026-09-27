from flask import Flask, render_template, request, jsonify
from database import init_db, add_proposal, add_message, add_review, get_all_freelancers, get_all_services, get_all_proposals, get_all_messages, get_all_reviews

app = Flask(__name__)
PORT = 6963

init_db()

@app.route('/')
def index():
    freelancers = get_all_freelancers()
    services = get_all_services()
    proposals = get_all_proposals()
    messages = get_all_messages()
    reviews = get_all_reviews()
    return render_template('index.html', freelancers=freelancers, services=services, proposals=proposals, messages=messages, reviews=reviews)

@app.route('/api/proposals', methods=['POST'])
def submit_proposal():
    data = request.json or {}
    service_title = data.get('service_title', 'Servico Geral').strip()
    client_name = data.get('client_name', 'Cliente Exemplo').strip()
    client_email = data.get('client_email', 'cliente@empresa.com').strip()
    bid_amount = float(data.get('bid_amount', 300.00))
    delivery_days = int(data.get('delivery_days', 3))
    cover_letter = data.get('cover_letter', 'Proposta enviada via FreelanceCraft AI.').strip()

    if not service_title or not client_name or not client_email:
        return jsonify({"error": "Dados da proposta incompletos."}), 400

    prop_id = add_proposal(service_title, client_name, client_email, bid_amount, delivery_days, cover_letter)
    return jsonify({
        "success": True,
        "message": "Proposta enviada com sucesso ao freelancer!",
        "proposal_id": prop_id
    })

@app.route('/api/messages', methods=['GET', 'POST'])
def handle_messages():
    if request.method == 'POST':
        data = request.json or {}
        sender = data.get('sender_name', 'Cliente Exemplo').strip()
        receiver = data.get('receiver_name', 'Angel Rafael').strip()
        text = data.get('message_text', '').strip()

        if not text:
            return jsonify({"error": "Mensagem vazia."}), 400

        msg_id = add_message(sender, receiver, text)
        return jsonify({"success": True, "message_id": msg_id})
    
    return jsonify(get_all_messages())

@app.route('/api/reviews', methods=['POST'])
def submit_review():
    data = request.json or {}
    freelancer_name = data.get('freelancer_name', 'Angel Rafael').strip()
    client_name = data.get('client_name', 'Cliente Exemplo').strip()
    rating = int(data.get('rating', 5))
    comment = data.get('comment', 'Excelente trabalho!').strip()

    add_review(freelancer_name, client_name, rating, comment)
    return jsonify({"success": True, "message": "Avaliacao registada com sucesso!"})

if __name__ == '__main__':
    print(f"Servidor FreelanceCraft AI iniciado na porta {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=True)
