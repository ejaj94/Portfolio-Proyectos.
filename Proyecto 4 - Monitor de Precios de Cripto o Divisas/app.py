import os
from flask import Flask, render_template, request, jsonify
from Cripto_chek import CryptoMonitorEngine, DEFAULT_CRYPTOS, DEFAULT_FOREX

app = Flask(__name__)
engine = CryptoMonitorEngine()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/prices", methods=["GET"])
def get_prices():
    try:
        crypto_data = engine.get_multiple_tickers(DEFAULT_CRYPTOS)
        forex_data = engine.get_multiple_tickers(DEFAULT_FOREX)
        return jsonify({
            "success": True,
            "cryptos": crypto_data,
            "forex": forex_data
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@app.route("/api/custom-price", methods=["POST"])
def get_custom_price():
    data = request.get_json() or {}
    symbol = data.get("symbol", "").strip().upper()
    if not symbol:
        return jsonify({"success": False, "message": "Debes especificar un símbolo (ej: BTC-USD)."}), 400

    try:
        info = engine.get_ticker_info(symbol)
        if info.get("price", 0) <= 0:
            return jsonify({"success": False, "message": f"No se encontraron datos para el símbolo '{symbol}'."}), 404
        return jsonify({"success": True, "data": info})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@app.route("/api/history/<path:symbol>", methods=["GET"])
def get_symbol_history(symbol):
    period = request.args.get("period", "1d")
    interval = "15m" if period == "1d" else "1h" if period == "7d" else "1d"

    try:
        hist = engine.get_history(symbol, period=period, interval=interval)
        return jsonify(hist)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@app.route("/api/convert", methods=["POST"])
def convert_currency():
    data = request.get_json() or {}
    from_sym = data.get("from_symbol", "BTC-USD").strip().upper()
    amount = float(data.get("amount", 1.0))

    try:
        info = engine.get_ticker_info(from_sym)
        price = info.get("price", 0.0)
        total_usd = amount * price

        return jsonify({
            "success": True,
            "from_symbol": from_sym,
            "amount": amount,
            "price_usd": price,
            "total_usd": round(total_usd, 2)
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


if __name__ == "__main__":
    print("Iniciando Monitor de Cripto y Divisas PRO en http://localhost:5004")
    app.run(host="0.0.0.0", port=5004, debug=False)
