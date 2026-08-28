import time
import threading
import webbrowser
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# Estado global del monitor
monitor_state = {
    "running": False,
    "url": "https://www.trendyventa.com/products/smart-lock-fingerprint-padlock",
    "target_price": 10.00,
    "interval": 60,
    "last_price": None,
    "last_check": None,
    "is_offer": False,
    "status_text": "Detenido",
    "logs": []
}

monitor_thread = None
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def add_log(message):
    ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    entry = f"[{ahora}] {message}"
    monitor_state["logs"].append(entry)
    # Conservar últimos 100 registros
    if len(monitor_state["logs"]) > 100:
        monitor_state["logs"].pop(0)


def ejecutar_scraping():
    url = monitor_state["url"]
    presupuesto = monitor_state["target_price"]

    if not url:
        add_log("[ERROR] La URL esta vacia.")
        return

    try:
        respuesta = requests.get(url, headers=headers, timeout=10)
        if respuesta.status_code != 200:
            add_log(f"[WARN] Servidor respondio con codigo HTTP: {respuesta.status_code}")
            return

        sopa = BeautifulSoup(respuesta.content, "html.parser")
        precio_etiqueta = sopa.find("span", class_="price")

        if not precio_etiqueta:
            add_log("[WARN] No se encontro el elemento 'span.price' en el HTML de la pagina.")
            return

        precio_texto = precio_etiqueta.text.strip()
        precio_limpio = precio_texto.replace("$", "").replace(",", "")
        precio_final = float(precio_limpio)

        ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        monitor_state["last_price"] = precio_texto
        monitor_state["last_check"] = ahora

        if precio_final <= presupuesto:
            monitor_state["is_offer"] = True
            monitor_state["status_text"] = "OFERTA DETECTADA!"
            add_log(f"[OFERTA] Precio: {precio_texto} (Presupuesto: ${presupuesto:.2f})")
        else:
            monitor_state["is_offer"] = False
            if monitor_state["running"]:
                monitor_state["status_text"] = "Vigilando activo"
            add_log(f"[INFO] Precio leido: {precio_texto} (Presupuesto: ${presupuesto:.2f})")

    except requests.exceptions.RequestException as err:
        add_log(f"[ERROR] Error de conexion HTTP: {err}")
    except Exception as ex:
        add_log(f"[ERROR] Error inesperado durante el scraping: {ex}")


def bucle_monitoreo():
    add_log(f"[INICIO] Servicio de vigilancia iniciado en localhost (cada {monitor_state['interval']}s).")
    monitor_state["status_text"] = "Vigilando activo"

    while monitor_state["running"]:
        ejecutar_scraping()
        intervalo = monitor_state.get("interval", 60)
        for _ in range(max(1, intervalo)):
            if not monitor_state["running"]:
                break
            time.sleep(1)

    monitor_state["status_text"] = "Detenido"
    add_log("[STOP] Vigilancia detenida.")


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🕷️ Monitor de Precios Inteligente - Localhost Web GUI</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #121212;
            color: #e0e0e0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .card {
            background-color: #1e1e1e;
            border: 1px solid #333;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }
        .form-control, .form-select {
            background-color: #2b2b2b;
            border: 1px solid #444;
            color: #fff;
        }
        .form-control:focus {
            background-color: #333;
            color: #fff;
            border-color: #0d6efd;
            box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
        }
        .log-box {
            background-color: #0a0a0a;
            color: #00ff66;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 0.9rem;
            height: 320px;
            overflow-y: auto;
            border-radius: 8px;
            padding: 15px;
            border: 1px solid #222;
        }
        .badge-status {
            font-size: 1.1rem;
            padding: 8px 16px;
            border-radius: 20px;
        }
    </style>
</head>
<body class="py-4">
    <div class="container" style="max-width: 900px;">
        <div class="card p-4 mb-4 text-center">
            <h2 class="fw-bold mb-1">🕷️ Monitor de Precios Inteligente</h2>
            <p class="text-secondary mb-0">Web Scraper Automático en Tiempo Real (http://localhost:5000)</p>
        </div>

        <div class="card p-4 mb-4">
            <h5 class="fw-bold mb-3">⚙️ Configuración del Rastreador</h5>
            <div class="row g-3">
                <div class="col-12">
                    <label class="form-label text-secondary fw-semibold">URL del Producto:</label>
                    <input type="url" id="inputUrl" class="form-control" value="{{ state.url }}">
                </div>
                <div class="col-md-6">
                    <label class="form-label text-secondary fw-semibold">Presupuesto Objetivo ($):</label>
                    <input type="number" step="0.01" id="inputPrice" class="form-control" value="{{ state.target_price }}">
                </div>
                <div class="col-md-6">
                    <label class="form-label text-secondary fw-semibold">Frecuencia de Revisión (segundos):</label>
                    <input type="number" id="inputInterval" class="form-control" value="{{ state.interval }}">
                </div>
            </div>

            <div class="d-flex flex-wrap gap-2 mt-4">
                <button id="btnStart" onclick="startMonitor()" class="btn btn-success fw-bold px-4">▶ Iniciar Vigilancia</button>
                <button id="btnStop" onclick="stopMonitor()" class="btn btn-danger fw-bold px-4" disabled>⏹ Detener</button>
                <button id="btnScan" onclick="scanNow()" class="btn btn-info text-white fw-bold px-4">⚡ Escanear Ahora</button>
            </div>
        </div>

        <div class="card p-4 mb-4">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="fw-bold mb-0">📊 Estado del Servicio</h5>
                <span id="badgeStatus" class="badge bg-secondary badge-status">Cargando...</span>
            </div>
            <div class="row text-center g-3">
                <div class="col-md-6">
                    <div class="p-3 border border-secondary rounded">
                        <small class="text-secondary d-block">Último Precio Leído</small>
                        <span id="textLastPrice" class="fs-3 fw-bold text-warning">--</span>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="p-3 border border-secondary rounded">
                        <small class="text-secondary d-block">Última Revisión</small>
                        <span id="textLastCheck" class="fs-5 fw-semibold text-info">--</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="card p-4">
            <h5 class="fw-bold mb-3">📜 Historial de Registros (Logs)</h5>
            <div id="logBox" class="log-box"></div>
        </div>
    </div>

    <script>
        async function updateStatus() {
            try {
                const res = await fetch('/api/status');
                const data = await res.json();

                const btnStart = document.getElementById('btnStart');
                const btnStop = document.getElementById('btnStop');
                const badgeStatus = document.getElementById('badgeStatus');
                const textLastPrice = document.getElementById('textLastPrice');
                const textLastCheck = document.getElementById('textLastCheck');
                const logBox = document.getElementById('logBox');

                btnStart.disabled = data.running;
                btnStop.disabled = !data.running;

                if (data.is_offer) {
                    badgeStatus.className = 'badge bg-success badge-status';
                    badgeStatus.innerText = '🔔 ¡OFERTA ENCONTRADA!';
                } else if (data.running) {
                    badgeStatus.className = 'badge bg-primary badge-status';
                    badgeStatus.innerText = '🟢 Vigilando Activo';
                } else {
                    badgeStatus.className = 'badge bg-secondary badge-status';
                    badgeStatus.innerText = '🔴 Detenido';
                }

                textLastPrice.innerText = data.last_price || '--';
                textLastCheck.innerText = data.last_check || '--';

                logBox.innerHTML = data.logs.map(log => `<div>${log}</div>`).join('');
                logBox.scrollTop = logBox.scrollHeight;
            } catch (err) {
                console.error(err);
            }
        }

        async function startMonitor() {
            const url = document.getElementById('inputUrl').value;
            const price = parseFloat(document.getElementById('inputPrice').value);
            const interval = parseInt(document.getElementById('inputInterval').value);

            await fetch('/api/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url, target_price: price, interval })
            });
            updateStatus();
        }

        async function stopMonitor() {
            await fetch('/api/stop', { method: 'POST' });
            updateStatus();
        }

        async function scanNow() {
            const url = document.getElementById('inputUrl').value;
            const price = parseFloat(document.getElementById('inputPrice').value);

            await fetch('/api/scan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url, target_price: price })
            });
            updateStatus();
        }

        setInterval(updateStatus, 2000);
        updateStatus();
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, state=monitor_state)


@app.route("/api/status")
def status():
    return jsonify(monitor_state)


@app.route("/api/start", methods=["POST"])
def api_start():
    data = request.json or {}
    monitor_state["url"] = data.get("url", monitor_state["url"])
    monitor_state["target_price"] = float(data.get("target_price", monitor_state["target_price"]))
    monitor_state["interval"] = int(data.get("interval", monitor_state["interval"]))

    if not monitor_state["running"]:
        monitor_state["running"] = True
        global monitor_thread
        monitor_thread = threading.Thread(target=bucle_monitoreo, daemon=True)
        monitor_thread.start()

    return jsonify({"success": True, "state": monitor_state})


@app.route("/api/stop", methods=["POST"])
def api_stop():
    monitor_state["running"] = False
    return jsonify({"success": True})


@app.route("/api/scan", methods=["POST"])
def api_scan():
    data = request.json or {}
    if "url" in data:
        monitor_state["url"] = data["url"]
    if "target_price" in data:
        monitor_state["target_price"] = float(data["target_price"])

    add_log("[SCAN] Iniciando escaneo instantaneo via API Web...")
    threading.Thread(target=ejecutar_scraping, daemon=True).start()
    return jsonify({"success": True})


def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://localhost:5000")


if __name__ == "__main__":
    print("Iniciando Servidor Web en http://localhost:5000 ...")
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host="127.0.0.1", port=5000, debug=False)
