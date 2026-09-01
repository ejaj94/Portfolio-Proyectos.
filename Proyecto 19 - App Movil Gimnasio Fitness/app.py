import os
import sys
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

ENROLLMENTS_DB = []
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


@app.route("/api/enroll", methods=["POST"])
def enroll_member():
    try:
        data = request.get_json() or {}
        full_name = data.get("full_name", "").strip()
        phone = data.get("phone", "").strip()
        email = data.get("email", "").strip()
        plan_name = data.get("plan_name", "Plano Premium VIP").strip()
        monthly_price = data.get("monthly_price", 49.90)
        start_date = data.get("start_date", "").strip()
        addons = data.get("addons", [])
        notes = data.get("notes", "").strip()

        if not full_name or not phone or not email:
            return jsonify({
                "success": False,
                "message": "Por favor, preencha o seu nome, telemóvel e e-mail."
            }), 400

        member_id = f"FIT-{len(ENROLLMENTS_DB) + 801}"
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

        addons_text = ", ".join(addons) if addons else "Nenhum extra selecionado"

        new_enrollment = {
            "id": member_id,
            "full_name": full_name,
            "phone": phone,
            "email": email,
            "plan_name": plan_name,
            "monthly_price": monthly_price,
            "start_date": start_date if start_date else "Imediato",
            "addons": addons,
            "notes": notes,
            "status": "Inscrição Ativa",
            "created_at": created_at
        }

        ENROLLMENTS_DB.append(new_enrollment)
        print(f"[+] Nova Inscrição no Ginásio: {member_id} | {full_name} | Plano: {plan_name} ({monthly_price}€/mês)")

        wa_text = f"🏋️ *NOVA INSCRIÇÃO FITCLUB GYM VILAMOURA* 💪\n\n" \
                  f"📌 *Matrícula*: {member_id}\n" \
                  f"👤 *Atleta*: {full_name}\n" \
                  f"📞 *Telemóvel*: {phone}\n" \
                  f"✉️ *Email*: {email}\n" \
                  f"🏆 *Plano*: {plan_name} ({monthly_price:.2f}€/mês)\n" \
                  f"📅 *Início*: {start_date if start_date else 'Imediato'}\n" \
                  f"✨ *Extras*: {addons_text}\n" \
                  f"📝 *Obs*: {notes if notes else 'Sem observações'}"

        return jsonify({
            "success": True,
            "message": "Matrícula realizada com sucesso!",
            "enrollment": new_enrollment,
            "whatsapp_url": f"https://wa.me/351123456789?text={request.headers.get('Origin', '') and wa_text}"
        })

    except Exception as e:
        print(f"[!] Erro na matrícula: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/class-booking", methods=["POST"])
def book_class():
    try:
        data = request.get_json() or {}
        class_name = data.get("class_name", "").strip()
        class_time = data.get("class_time", "").strip()
        athlete_name = data.get("athlete_name", "").strip()
        athlete_phone = data.get("athlete_phone", "").strip()

        if not class_name or not athlete_name or not athlete_phone:
            return jsonify({"success": False, "message": "Preencha todos os campos da reserva."}), 400

        booking_id = f"CLASS-{len(BOOKINGS_DB) + 101}"
        booking = {
            "id": booking_id,
            "class_name": class_name,
            "class_time": class_time,
            "athlete_name": athlete_name,
            "athlete_phone": athlete_phone,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        BOOKINGS_DB.append(booking)
        print(f"[+] Reserva de Aula: {booking_id} | {class_name} | {athlete_name}")

        wa_text = f"🔥 *RESERVA DE AULA FITCLUB GYM* 🏋️\n\n" \
                  f"📌 *Reserva*: {booking_id}\n" \
                  f"🎯 *Aula*: {class_name}\n" \
                  f"🕒 *Horário*: {class_time}\n" \
                  f"👤 *Atleta*: {athlete_name}\n" \
                  f"📞 *Telemóvel*: {athlete_phone}"

        return jsonify({
            "success": True,
            "message": f"Lugar reservado com sucesso para {class_name}!",
            "booking": booking,
            "whatsapp_url": f"https://wa.me/351123456789?text={wa_text}"
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


if __name__ == "__main__":
    print("Iniciando FITCLUB GYM Mobile Web App em http://localhost:5057")
    app.run(host="0.0.0.0", port=5057, debug=False)
