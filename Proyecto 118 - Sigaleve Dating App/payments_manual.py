# ============================================================
# SIGALEVE — PAGAMENTOS MANUAIS (MB WAY) — FASE 1
# ============================================================
# Fluxo:
#   1. Usuário escolhe plano → POST /api/v1/subscription/mbway-request
#   2. Sistema gera referência única SGLV-XXXXXX e instruções (número MB Way
#      do dono, definido em SIGALEVE_MBWAY_NUMBER no .env)
#   3. Usuário paga no telemóvel → dono recebe a notificação MB Way
#   4. Dono confirma no painel admin (/admin/payments?token=..., protegido
#      por SIGALEVE_ADMIN_TOKEN no .env) → subscrição ativada na hora
#   5. Usuário vê o estado ao vivo (polling de 6s no modal)
# Nenhum dado de cartão circula — PCI-DSS safe. Stripe entra na fase 2.
# ============================================================
# Integração: init_payments(app, session, load_json_store, save_json_store,
# load_users, save_users) é chamado pelo preview_server DEPOIS de tudo
# definido. Nada executa no import (import seguro pra testes).
# ============================================================
import json as _json
import os as _os
import random as _random
import string as _string
import threading as _threading
import time as _time
from datetime import datetime as _datetime, timedelta as _timedelta
from flask import request as _request, jsonify as _jsonify

DATA_DIR = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "data")
PENDING_PAYMENTS_FILE = _os.path.join(DATA_DIR, "pending_payments.json")
PAYMENTS_LOCK = _threading.Lock()

PLAN_PRICES = {
    "plus_1m":  ("Sigaleve Plus (1 Mês)", 14.99, 30),
    "plus_6m":  ("Sigaleve Plus (6 Meses)", 59.94, 182),
    "plus_12m": ("Sigaleve Plus (12 Meses)", 95.88, 365),
    "gold_1m":  ("Sigaleve Gold (1 Mês)", 19.99, 30),
    "gold_6m":  ("Sigaleve Gold (6 Meses)", 79.94, 182),
    "gold_12m": ("Sigaleve Gold (12 Meses)", 131.88, 365),
    "platinum_1m":  ("Sigaleve Platinum VIP (1 Mês)", 29.99, 30),
    "platinum_6m":  ("Sigaleve Platinum VIP (6 Meses)", 119.94, 182),
    "platinum_12m": ("Sigaleve Platinum VIP (12 Meses)", 191.88, 365),
}


def init_payments(app, session, load_json_store, save_json_store, load_users, save_users):
    """Registra as rotas de pagamento MB Way no app principal."""
    pending_lock = PAYMENTS_LOCK

    def _load_pending():
        return load_json_store(PENDING_PAYMENTS_FILE, {})

    def _save_pending(d):
        save_json_store(PENDING_PAYMENTS_FILE, d)

    @app.route("/api/v1/subscription/mbway-request", methods=["POST"])
    def api_mbway_request():
        if not session.get("user_id"):
            return _jsonify({"success": False, "error": "Autenticação necessária"}), 401
        email = session.get("user_email")
        data = _request.get_json(silent=True) or {}
        plan_id = str(data.get("plan_id", "plus_1m")).strip()
        if plan_id not in PLAN_PRICES:
            return _jsonify({"success": False, "error": "Plano desconhecido."}), 400

        plan_name, price, days = PLAN_PRICES[plan_id]
        mbway_number = _os.environ.get("SIGALEVE_MBWAY_NUMBER", "").strip()
        if not mbway_number:
            return _jsonify({"success": False, "error": "Pagamentos temporariamente indisponíveis."}), 503

        ref = "SGLV-" + "".join(_random.choices(_string.ascii_uppercase + _string.digits, k=6))
        with pending_lock:
            pending = _load_pending()
            # auto-limpeza: pendências >24h saem da lista
            cutoff = _time.time() - 86400
            pending = {k: v for k, v in pending.items() if v.get("created_ts", 0) > cutoff}
            pending[ref] = {
                "email": email,
                "user_id": session.get("user_id"),
                "plan_id": plan_id,
                "plan_name": plan_name,
                "price": price,
                "days": days,
                "status": "pending",
                "created_ts": _time.time(),
                "created_at": _datetime.utcnow().isoformat() + "Z"
            }
            _save_pending(pending)

        price_fmt = f"{price:.2f}".replace(".", ",") + "€"
        return _jsonify({
            "success": True,
            "reference": ref,
            "price": price_fmt,
            "mbway_number": mbway_number,
            "plan_name": plan_name,
            "instructions": [
                "Abre a app do MB Way no teu telemóvel",
                f"Escolhe «Pagar com MB Way» e insere o número {mbway_number}",
                f"Valor exato: {price_fmt}",
                f"Na descrição/mensagem indica a referência {ref}",
                "A subscrição ativa automaticamente após confirmação (normalmente em minutos)"
            ]
        }), 200

    @app.route("/api/v1/subscription/mbway-status", methods=["GET"])
    def api_mbway_status():
        if not session.get("user_id"):
            return _jsonify({"success": False, "error": "Autenticação necessária"}), 401
        ref = _request.args.get("ref", "").strip().upper()
        with pending_lock:
            p = _load_pending().get(ref)
        if not p or p.get("email") != session.get("user_email"):
            return _jsonify({"success": False, "error": "Referência não encontrada."}), 404
        return _jsonify({"success": True, "status": p["status"], "plan_name": p["plan_name"]})

    def _activate_subscription(email, plan_id, plan_name, days, method="mbway", reference=""):
        """Ativa a subscrição de um usuário (chamado pela confirmação admin)."""
        users = load_users()
        if email not in users:
            return False, "Utilizador não encontrado."
        sub_info = {
            "active": True,
            "plan_id": plan_id,
            "plan_name": plan_name,
            "method": method,
            "reference": reference,
            "started_at": _datetime.utcnow().isoformat(),
            "expires_at": (_datetime.utcnow() + _timedelta(days=days)).isoformat(),
            "next_billing": (_datetime.utcnow() + _timedelta(days=days)).strftime("%d/%m/%Y")
        }
        users[email]["is_plus"] = True
        users[email]["subscription"] = sub_info
        save_users(users)
        return True, sub_info

    @app.route("/admin/payments", methods=["GET"])
    def admin_payments_page():
        token = _request.args.get("token", "").strip()
        if not token or token != _os.environ.get("SIGALEVE_ADMIN_TOKEN", ""):
            return "<h2 style='font-family:sans-serif;color:#b91c1c'>403 — Token inválido. Usa /admin/payments?token=SEU_TOKEN</h2>", 403
        with pending_lock:
            pending = _load_pending()
        rows = sorted(pending.values(), key=lambda p: -p.get("created_ts", 0))
        rows_html = ""
        for p in rows:
            ref = p.get("reference", "SGLV-?")
            status_color = {"pending": "#f59e0b", "paid": "#10b981", "rejected": "#6b7280"}.get(p["status"], "#6b7280")
            status_label = {"pending": "AGUARDA PAGAMENTO", "paid": "PAGO ✓", "rejected": "REJEITADO"}.get(p["status"], p["status"])
            btn = ""
            if p["status"] == "pending":
                btn = (
                    f"<button onclick=\"act('{ref}', 'confirm')\" style=\"background:#10b981;color:#fff;border:none;padding:6px 14px;border-radius:8px;font-weight:700;cursor:pointer;margin-right:6px\">✓ Recebi</button>"
                    f"<button onclick=\"act('{ref}', 'reject')\" style=\"background:#6b7280;color:#fff;border:none;padding:6px 14px;border-radius:8px;font-weight:700;cursor:pointer\">✗ Rejeitar</button>"
                )
            rows_html += (
                "<tr style=\"border-bottom:1px solid #e5e7eb\">"
                f"<td style=\"padding:10px\">{ref}</td>"
                f"<td style=\"padding:10px\">{p['email']}</td>"
                f"<td style=\"padding:10px\">{p['plan_name']}</td>"
                f"<td style=\"padding:10px\"><b>{p['price']:.2f}€</b></td>"
                f"<td style=\"padding:10px;color:{status_color};font-weight:700\">{status_label}</td>"
                f"<td style=\"padding:10px\">{p.get('created_at','')[:16].replace('T',' ')}</td>"
                f"<td style=\"padding:10px\">{btn}</td>"
                "</tr>"
            )
        return (
            "<!doctype html><html lang=\"pt\"><head><meta charset=\"utf-8\">"
            "<title>Sigaleve — Pagamentos MB Way</title></head>"
            "<body style=\"font-family:-apple-system,sans-serif;margin:24px;background:#fafafa\">"
            "<h1 style=\"font-size:22px\">💳 Pagamentos MB Way</h1>"
            "<p style=\"color:#6b7280;font-size:13px\">Confirma os pagamentos que recebeste no teu MB Way — a subscrição ativa no ato.</p>"
            "<table style=\"width:100%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.1)\">"
            "<tr style=\"background:#f3f4f6;text-align:left;font-size:12px;text-transform:uppercase;color:#6b7280\">"
            "<th style=\"padding:10px\">Ref</th><th style=\"padding:10px\">Usuário</th><th style=\"padding:10px\">Plano</th>"
            "<th style=\"padding:10px\">Valor</th><th style=\"padding:10px\">Estado</th><th style=\"padding:10px\">Pedido</th><th style=\"padding:10px\">Ação</th></tr>"
            + (rows_html or "<tr><td colspan=\"7\" style=\"padding:24px;text-align:center;color:#6b7280\">Sem pedidos.</td></tr>")
            + "</table>"
            f"<script>async function act(ref, action) {{ const r = await fetch('/admin/payments/act', {{ method: 'POST', headers: {{'Content-Type': 'application/json'}}, body: JSON.stringify({{ token: '{token}', reference: ref, action: action }}) }}); if (r.ok) location.reload(); else alert('Falhou: ' + (await r.text())); }}</script>"
            "</body></html>"
        )

    @app.route("/admin/payments/act", methods=["POST"])
    def admin_payments_act():
        data = _request.get_json(silent=True) or {}
        token = str(data.get("token", "")).strip()
        if not token or token != _os.environ.get("SIGALEVE_ADMIN_TOKEN", ""):
            return _jsonify({"success": False, "error": "Token inválido"}), 403
        ref = str(data.get("reference", "")).strip().upper()
        action = str(data.get("action", "")).strip()
        with pending_lock:
            pending = _load_pending()
            p = pending.get(ref)
            if not p:
                return _jsonify({"success": False, "error": "Referência não encontrada"}), 404
            if action == "confirm":
                ok, info = _activate_subscription(p["email"], p["plan_id"], p["plan_name"], p["days"], method="mbway", reference=ref)
                if not ok:
                    return _jsonify({"success": False, "error": info}), 400
                p["status"] = "paid"
                p["paid_ts"] = _time.time()
                pending[ref] = p
                _save_pending(pending)
                return _jsonify({"success": True, "message": f"Subscrição de {p['email']} ativada ({p['plan_name']})."}), 200
            elif action == "reject":
                p["status"] = "rejected"
                pending[ref] = p
                _save_pending(pending)
                return _jsonify({"success": True, "message": "Pedido rejeitado."}), 200
        return _jsonify({"success": False, "error": "Ação desconhecida"}), 400

    return {"routes": ["mbway-request", "mbway-status", "admin/payments"]}
