import os
import sys
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

RESERVATIONS_DB = []


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0, post-check=0, pre-check=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/booking", methods=["POST"])
def create_reservation():
    try:
        data = request.get_json() or {}
        client_name = data.get("client_name", "").strip()
        client_phone = data.get("client_phone", "").strip()
        client_email = data.get("client_email", "").strip()
        guests = data.get("guests", "2 Pessoas").strip()
        seating_area = data.get("seating_area", "Salão Principal de Luxo").strip()
        res_date = data.get("res_date", "").strip()
        res_time = data.get("res_time", "").strip()
        dietary_notes = data.get("notes", "").strip()

        if not client_name or not client_phone or not guests or not res_date or not res_time:
            return jsonify({
                "success": False,
                "message": "Por favor, preencha todos os campos obrigatórios da reserva."
            }), 400

        res_id = f"LETOILE-{len(RESERVATIONS_DB) + 201}"
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

        new_res = {
            "id": res_id,
            "client_name": client_name,
            "client_phone": client_phone,
            "client_email": client_email,
            "guests": guests,
            "seating_area": seating_area,
            "res_date": res_date,
            "res_time": res_time,
            "notes": dietary_notes,
            "status": "Mesa Confirmada",
            "created_at": created_at
        }

        RESERVATIONS_DB.append(new_res)
        print(f"[+] Nova Reserva Gourmet Confirmada (Lagos): {res_id} | {client_name} | {guests} | {res_date} às {res_time}")

        wa_text = f"Olá L'Étoile Gourmet! Gostaria de confirmar a minha reserva de mesa:\n\n" \
                  f"📌 *Código*: {res_id}\n" \
                  f"👤 *Nome*: {client_name}\n" \
                  f"👥 *Pessoas*: {guests}\n" \
                  f"🍷 *Área*: {seating_area}\n" \
                  f"📅 *Data*: {res_date}\n" \
                  f"⏰ *Hora*: {res_time}\n" \
                  f"📞 *Contacto*: {client_phone}"

        return jsonify({
            "success": True,
            "message": "Reserva de mesa efetuada com sucesso!",
            "reservation": new_res,
            "whatsapp_url": f"https://wa.me/351911151993?text={request.headers.get('Origin', '') and wa_text}"
        })

    except Exception as e:
        print(f"[!] Erro na reserva gourmet: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/reservations-list", methods=["GET"])
def list_reservations():
    return jsonify({"success": True, "count": len(RESERVATIONS_DB), "reservations": RESERVATIONS_DB})


if __name__ == "__main__":
    print("Iniciando Restaurante L'Étoile Gourmet (Lagos, Algarve) em http://localhost:5023")
    app.run(host="0.0.0.0", port=5023, debug=False)
