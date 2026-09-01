import os
import sys
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

ORDERS_DB = []


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0, post-check=0, pre-check=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/order", methods=["POST"])
def create_order():
    try:
        data = request.get_json() or {}
        client_name = data.get("client_name", "").strip()
        client_phone = data.get("client_phone", "").strip()
        delivery_address = data.get("delivery_address", "").strip()
        order_type = data.get("order_type", "Delivery").strip()
        payment_method = data.get("payment_method", "MB WAY").strip()
        cart_items = data.get("items", [])
        total_amount = data.get("total_amount", 0.0)
        notes = data.get("notes", "").strip()

        if not client_name or not client_phone or not cart_items:
            return jsonify({
                "success": False,
                "message": "Por favor, preencha o seu nome, telemóvel e adicione produtos ao carrinho."
            }), 400

        order_id = f"CRUNCH-{len(ORDERS_DB) + 301}"
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

        items_summary = []
        for it in cart_items:
            items_summary.append(f"• {it.get('quantity', 1)}x {it.get('name')} ({it.get('price', '0.00')}€)")

        items_text = "\n".join(items_summary)

        new_order = {
            "id": order_id,
            "client_name": client_name,
            "client_phone": client_phone,
            "delivery_address": delivery_address if order_type == "Delivery" else "Levantamento em Loja (Vilamoura)",
            "order_type": order_type,
            "payment_method": payment_method,
            "items": cart_items,
            "total_amount": total_amount,
            "notes": notes,
            "status": "Em Preparação",
            "created_at": created_at
        }

        ORDERS_DB.append(new_order)
        print(f"[+] Novo Pedido Fast Food (Vilamoura): {order_id} | {client_name} | Total: {total_amount}€ | Tipo: {order_type}")

        wa_text = f"🍔 *NOVO PEDIDO BURGER & CRUNCH VILAMOURA* 🚀\n\n" \
                  f"📌 *Código*: {order_id}\n" \
                  f"👤 *Cliente*: {client_name}\n" \
                  f"📞 *Telemóvel*: {client_phone}\n" \
                  f"🛵 *Modalidade*: {order_type}\n" \
                  f"📍 *Morada*: {delivery_address if order_type == 'Delivery' else 'Levantamento no Restaurante em Vilamoura'}\n" \
                  f"💳 *Pagamento*: {payment_method}\n\n" \
                  f"🛒 *ITENS DO PEDIDO*:\n{items_text}\n\n" \
                  f"💰 *TOTAL*: {total_amount:.2f}€\n" \
                  f"📝 *Observações*: {notes if notes else 'Nenhuma'}"

        return jsonify({
            "success": True,
            "message": "Pedido efetuado com sucesso!",
            "order": new_order,
            "whatsapp_url": f"https://wa.me/351123456789?text={request.headers.get('Origin', '') and wa_text}"
        })

    except Exception as e:
        print(f"[!] Erro no pedido fast food: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/orders-list", methods=["GET"])
def list_orders():
    return jsonify({"success": True, "count": len(ORDERS_DB), "orders": ORDERS_DB})


if __name__ == "__main__":
    print("Iniciando BURGER & CRUNCH Fast Food Web App (Vilamoura) em http://localhost:5043")
    app.run(host="0.0.0.0", port=5043, debug=False)
