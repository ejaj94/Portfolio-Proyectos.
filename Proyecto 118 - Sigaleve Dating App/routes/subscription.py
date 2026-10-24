"""
routes/subscription.py — Blueprint para Planos, Checkout e Gestão de Subscrições.
"""
import datetime
from flask import Blueprint, jsonify, request, session
from services.common import load_users, save_users

subscription_bp = Blueprint("subscription", __name__)


@subscription_bp.route("/api/v1/subscription/plans", methods=["GET"])
def api_subscription_plans():
    return jsonify({
        "plans": [
            {
                "id": "plus_1m",
                "name": "Sigaleve Plus",
                "duration": "1 Mês",
                "price": "14.99",
                "currency": "EUR",
                "symbol": "€",
                "badge": "Popular",
                "features": [
                    "Gostos (Likes) Ilimitados",
                    "Saber quem gostou de ti",
                    "5 Super Likes gratuitos por semana",
                    "1 Boost gratuito por mês",
                    "Retroceder ilimitado (Undo)",
                    "Modo Incógnito e Localização Seletiva",
                    "Cifra reforçada de dados clínicos"
                ]
            },
            {
                "id": "plus_6m",
                "name": "Sigaleve Plus Semestral",
                "duration": "6 Meses",
                "price": "9.99",
                "per_month": "9.99€/mês",
                "total": "59.94€",
                "currency": "EUR",
                "symbol": "€",
                "badge": "Poupa 33%",
                "features": [
                    "Todas as vantagens do Sigaleve Plus",
                    "Prioridade máxima na fila de descoberta",
                    "Filtro avançado por compatibilidade clínica",
                    "Suporte prioritário 24/7"
                ]
            },
            {
                "id": "platinum_12m",
                "name": "Sigaleve Platinum VIP",
                "duration": "12 Meses",
                "price": "6.99",
                "per_month": "6.99€/mês",
                "total": "83.88€",
                "currency": "EUR",
                "symbol": "€",
                "badge": "Melhor Valor",
                "features": [
                    "Tudo incluído + Distintivo VIP exclusivo",
                    "Mensagens prioritárias antes do Match",
                    "Verificação médica de perfil com selo dourado",
                    "Total confidencialidade com faturação discreta"
                ]
            }
        ]
    }), 200


@subscription_bp.route("/api/v1/subscription/subscribe", methods=["POST"])
def api_subscribe():
    data = request.get_json(silent=True) or {}
    if not session.get("user_id"):
        return jsonify({"success": False, "error": "Autenticação necessária"}), 401
    card_number = str(data.get("card_number", "")).replace(" ", "")
    card_holder = str(data.get("card_holder", "")).strip()
    exp_date = str(data.get("exp_date", "")).strip()
    cvv = str(data.get("cvv", "")).strip()
    plan_id = str(data.get("plan_id", "plus_1m"))

    if not card_holder:
        return jsonify({"success": False, "error": "Introduz o nome do titular do cartão."}), 400
    if len(card_number) < 13 or not card_number.isdigit():
        return jsonify({"success": False, "error": "Número de cartão de crédito/débito inválido."}), 400
    if len(cvv) < 3 or not cvv.isdigit():
        return jsonify({"success": False, "error": "Código CVV inválido (deve conter 3 ou 4 dígitos)."}), 400
    if "/" not in exp_date:
        return jsonify({"success": False, "error": "Data de validade inválida (formato MM/AA)."}), 400

    email = session.get("user_email")
    if not email:
        return jsonify({"success": False, "error": "Sessão não iniciada."}), 401
    users = load_users()
    if email not in users:
        return jsonify({"success": False, "error": "Utilizador não encontrado."}), 404

    card_brand = "Visa" if card_number.startswith("4") else ("Mastercard" if card_number.startswith("5") else "Cartão Seguro")
    last4 = card_number[-4:] if len(card_number) >= 4 else "0000"

    plan_names = {
        "plus_1m": "Sigaleve Plus (1 Mês)",
        "plus_6m": "Sigaleve Plus (6 Meses)",
        "plus_12m": "Sigaleve Plus (12 Meses)",
        "gold_1m": "Sigaleve Gold (1 Mês)",
        "gold_6m": "Sigaleve Gold (6 Meses)",
        "gold_12m": "Sigaleve Gold (12 Meses)",
        "platinum_1m": "Sigaleve Platinum VIP (1 Mês)",
        "platinum_6m": "Sigaleve Platinum VIP (6 Meses)",
        "platinum_12m": "Sigaleve Platinum VIP (12 Meses)"
    }
    plan_title = plan_names.get(plan_id, f"Sigaleve {plan_id.replace('_', ' ').upper()}")

    now = datetime.datetime.now(datetime.timezone.utc)
    sub_info = {
        "active": True,
        "plan_id": plan_id,
        "plan_name": plan_title,
        "card_brand": card_brand,
        "card_last4": last4,
        "card_holder": card_holder.upper(),
        "card_exp": exp_date,
        "started_at": now.isoformat(),
        "next_billing": (now + datetime.timedelta(days=30)).strftime("%d de %B, %Y")
    }

    users[email]["is_plus"] = True
    users[email]["subscription"] = sub_info
    save_users(users)

    return jsonify({
        "success": True,
        "message": f"Subscrição {plan_title} ativada com sucesso!",
        "subscription": sub_info,
        "is_plus": True
    }), 200


@subscription_bp.route("/api/v1/subscription/cancel", methods=["POST"])
def api_cancel_subscription():
    email = session.get("user_email")
    if not email:
        return jsonify({"success": False, "error": "Sessão não iniciada."}), 401
    users = load_users()
    if email not in users:
        return jsonify({"success": False, "error": "Utilizador não encontrado."}), 404

    users[email]["is_plus"] = False
    users[email]["subscription"] = None
    save_users(users)

    return jsonify({
        "success": True,
        "message": "A tua subscrição foi cancelada com sucesso. O teu perfil voltou ao plano gratuito."
    }), 200
