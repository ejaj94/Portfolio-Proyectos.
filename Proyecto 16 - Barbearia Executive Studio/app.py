import os
import sys
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

BOOKINGS_DB = []


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
def create_booking():
    try:
        data = request.get_json() or {}
        client_name = data.get("client_name", "").strip()
        client_phone = data.get("client_phone", "").strip()
        client_email = data.get("client_email", "").strip()
        service = data.get("service", "").strip()
        barber = data.get("barber", "").strip()
        booking_date = data.get("booking_date", "").strip()
        booking_time = data.get("booking_time", "").strip()
        notes = data.get("notes", "").strip()

        if not client_name or not client_phone or not service or not booking_date or not booking_time:
            return jsonify({
                "success": False,
                "message": "Por favor, preencha todos os campos obrigatórios da reserva."
            }), 400

        booking_id = f"IMP-{len(BOOKINGS_DB) + 101}"
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

        new_booking = {
            "id": booking_id,
            "client_name": client_name,
            "client_phone": client_phone,
            "client_email": client_email,
            "service": service,
            "barber": barber or "Qualquer Barbeiro Disponível",
            "booking_date": booking_date,
            "booking_time": booking_time,
            "notes": notes,
            "status": "Confirmada",
            "created_at": created_at
        }

        BOOKINGS_DB.append(new_booking)

        wa_text = f"Olá Barbearia Império! Gostaria de confirmar a minha marcação:\n\n" \
                  f"📌 *Código*: {booking_id}\n" \
                  f"👤 *Nome*: {client_name}\n" \
                  f"💈 *Serviço*: {service}\n" \
                  f"✂️ *Barbeiro*: {barber}\n" \
                  f"📅 *Data*: {booking_date}\n" \
                  f"⏰ *Hora*: {booking_time}\n" \
                  f"📞 *Contacto*: {client_phone}"

        return jsonify({
            "success": True,
            "message": "Marcação realizada com sucesso!",
            "booking": new_booking,
            "whatsapp_url": f"https://wa.me/351123256789?text={request.headers.get('Origin', '') and wa_text}"
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/bookings-list", methods=["GET"])
def list_bookings():
    return jsonify({"success": True, "count": len(BOOKINGS_DB), "bookings": BOOKINGS_DB})


if __name__ == "__main__":
    print("Iniciando Barbearia Império & Tradição Web App em http://localhost:5021")
    app.run(host="0.0.0.0", port=5021, debug=False)
