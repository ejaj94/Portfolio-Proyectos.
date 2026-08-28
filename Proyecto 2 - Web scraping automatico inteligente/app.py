import time
import threading
import re
import webbrowser
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# Cabeceras anti-caché a todas las respuestas de Flask
@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Estado global del monitor
monitor_state = {
    "running": False,
    "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
    "target_price": 60.00,
    "interval": 60,
    "countdown": 60,
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
    if len(monitor_state["logs"]) > 100:
        monitor_state["logs"].pop(0)


def extraer_precio_html(soup):
    """Buscador inteligente de precios soportando múltiples tiendas web."""
    # 1. Buscar en meta tags (OpenGraph / Microdata)
    meta_price = soup.find("meta", property=re.compile(r"price|amount", re.I)) or soup.find("meta", itemprop="price")
    if meta_price and meta_price.get("content"):
        return meta_price["content"].strip()

    # 2. Lista de selectores CSS comunes para e-commerce
    selectores = [
        "span.price", "div.price", ".price", ".product-price",
        ".price_color", "span.amount", ".current-price",
        "span.a-price-whole", "span[itemprop='price']"
    ]

    for sel in selectores:
        elem = soup.select_one(sel)
        if elem and elem.text.strip():
            return elem.text.strip()

    # 3. Búsqueda por Regex en texto que contenga $, € o £
    texto_precio = soup.find(text=re.compile(r"[\$\€\£]\s*\d+[\.,]?\d*"))
    if texto_precio:
        return texto_precio.strip()

    return None


def ejecutar_scraping():
    url = monitor_state["url"].strip()
    ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    monitor_state["last_check"] = ahora

    # Limpiar y convertir presupuesto aceptando comas o puntos (ej: 10,0 o 10.0)
    try:
        presupuesto_str = str(monitor_state["target_price"]).replace(",", ".")
        presupuesto = float(presupuesto_str)
    except ValueError:
        add_log("[ERROR] El presupuesto debe ser un número válido.")
        monitor_state["last_price"] = "Presupuesto inválido"
        return

    if not url:
        add_log("[ERROR] La URL está vacía.")
        monitor_state["last_price"] = "URL vacía"
        return

    try:
        respuesta = requests.get(url, headers=headers, timeout=10)
        
        if respuesta.status_code != 200:
            msg_error = f"Error HTTP {respuesta.status_code}"
            if respuesta.status_code == 402:
                msg_error = "Error 402: Tienda no disponible / Suscripción requerida"
            elif respuesta.status_code == 404:
                msg_error = "Error 404: Producto o página no encontrada"

            add_log(f"[WARN] {msg_error}")
            monitor_state["last_price"] = msg_error
            monitor_state["is_offer"] = False
            return

        sopa = BeautifulSoup(respuesta.content, "html.parser")
        precio_texto = extraer_precio_html(sopa)

        if not precio_texto:
            add_log("[WARN] No se pudo localizar la etiqueta de precio en la página web.")
            monitor_state["last_price"] = "Etiqueta no encontrada"
            monitor_state["is_offer"] = False
            return

        # Limpiar texto del precio (quitar $, €, £, espacios)
        precio_limpio = re.sub(r"[^\d\.,]", "", precio_texto).replace(",", ".")
        precio_final = float(precio_limpio)

        monitor_state["last_price"] = f"${precio_final:.2f}" if "$" not in precio_texto and "€" not in precio_texto else precio_texto

        if precio_final <= presupuesto:
            monitor_state["is_offer"] = True
            monitor_state["status_text"] = "OFERTA DETECTADA!"
            add_log(f"[OFERTA] Precio encontrado: {precio_texto} (Presupuesto: ${presupuesto:.2f})")
        else:
            monitor_state["is_offer"] = False
            if monitor_state["running"]:
                monitor_state["status_text"] = "Vigilando activo"
            add_log(f"[INFO] Precio leído: {precio_texto} (Presupuesto: ${presupuesto:.2f})")

    except requests.exceptions.RequestException as err:
        add_log(f"[ERROR] Error de conexión HTTP: {err}")
        monitor_state["last_price"] = "Error de conexión"
        monitor_state["is_offer"] = False
    except Exception as ex:
        add_log(f"[ERROR] Error inesperado: {ex}")
        monitor_state["last_price"] = "Error inesperado"
        monitor_state["is_offer"] = False


def bucle_monitoreo():
    add_log(f"[INICIO] Servicio de vigilancia iniciado (revisión cada {monitor_state['interval']}s).")
    monitor_state["status_text"] = "Vigilando activo"

    while monitor_state["running"]:
        ejecutar_scraping()
        intervalo = monitor_state.get("interval", 60)
        
        # Conteo regresivo en tiempo real
        for restante in range(max(1, intervalo), 0, -1):
            if not monitor_state["running"]:
                break
            monitor_state["countdown"] = restante
            time.sleep(1)

    monitor_state["countdown"] = 0
    monitor_state["status_text"] = "Detenido"
    add_log("[STOP] Vigilancia detenida por el usuario.")


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🕷️ Monitor de Precios Inteligente - Localhost Web GUI</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f3f4f6;
            color: #111827;
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        }
        .header-box {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
        }
        .card {
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        .form-label {
            color: #1f2937 !important;
            font-weight: 700 !important;
        }
        .form-control {
            background-color: #ffffff;
            border: 2px solid #d1d5db;
            color: #111827;
            font-weight: 600;
        }
        .form-control:focus {
            background-color: #ffffff;
            color: #111827;
            border-color: #2563eb;
            box-shadow: 0 0 0 0.25rem rgba(37, 99, 235, 0.25);
        }
        .stat-card {
            background-color: #f8fafc;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
        }
        .log-box {
            background-color: #0f172a;
            color: #38bdf8;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 0.92rem;
            height: 320px;
            overflow-y: auto;
            border-radius: 8px;
            padding: 15px;
            border: 2px solid #1e293b;
        }
        .badge-status {
            font-size: 1.1rem;
            padding: 8px 18px;
            border-radius: 20px;
            font-weight: 700;
        }
        .btn-custom-start {
            background-color: #16a34a;
            color: #ffffff;
            border: none;
        }
        .btn-custom-start:hover {
            background-color: #15803d;
            color: #ffffff;
        }
        .btn-custom-stop {
            background-color: #dc2626;
            color: #ffffff;
            border: none;
        }
        .btn-custom-stop:hover {
            background-color: #b91c1c;
            color: #ffffff;
        }
        .btn-custom-scan {
            background-color: #2563eb;
            color: #ffffff;
            border: none;
        }
        .btn-custom-scan:hover {
            background-color: #1d4ed8;
            color: #ffffff;
        }
        .timer-badge {
            background-color: #eff6ff;
            color: #1d4ed8;
            border: 2px solid #bfdbfe;
            border-radius: 8px;
            padding: 6px 14px;
            font-weight: 700;
        }
    </style>
</head>
<body class="py-4">
    <div class="container" style="max-width: 920px;">
        <!-- Encabezado -->
        <div class="header-box p-4 mb-4 text-center">
            <h2 class="fw-bold mb-1">🕷️ Monitor de Precios Inteligente</h2>
            <p class="mb-0 text-white-50 fs-6">Web Scraper Automático en Tiempo Real (http://localhost:5050)</p>
        </div>

        <!-- Panel de Configuración -->
        <div class="card p-4 mb-4">
            <h4 class="fw-bold mb-3 text-dark">⚙️ Configuración del Rastreador</h4>
            <div class="row g-3">
                <div class="col-12">
                    <label class="form-label">URL del Producto:</label>
                    <input type="url" id="inputUrl" class="form-control form-control-lg" value="{{ state.url }}">
                </div>
                <div class="col-md-6">
                    <label class="form-label">Presupuesto Objetivo ($):</label>
                    <input type="text" id="inputPrice" class="form-control form-control-lg" value="{{ state.target_price }}">
                </div>
                <div class="col-md-6">
                    <label class="form-label">Frecuencia de Revisión (segundos):</label>
                    <input type="number" id="inputInterval" class="form-control form-control-lg" value="{{ state.interval }}">
                </div>
            </div>

            <div class="d-flex flex-wrap gap-3 mt-4">
                <button id="btnStart" onclick="startMonitor()" class="btn btn-custom-start btn-lg fw-bold px-4">▶ Iniciar Vigilancia</button>
                <button id="btnStop" onclick="stopMonitor()" class="btn btn-custom-stop btn-lg fw-bold px-4" disabled>⏹ Detener</button>
                <button id="btnScan" onclick="scanNow()" class="btn btn-custom-scan btn-lg fw-bold px-4">⚡ Escanear Ahora</button>
            </div>
        </div>

        <!-- Panel de Estado -->
        <div class="card p-4 mb-4">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h4 class="fw-bold mb-0 text-dark">📊 Estado del Servicio</h4>
                <div class="d-flex align-items-center gap-2">
                    <span id="textTimer" class="timer-badge">⏱️ Próxima revisión: --</span>
                    <span id="badgeStatus" class="badge bg-secondary badge-status">Cargando...</span>
                </div>
            </div>
            <div class="row text-center g-3">
                <div class="col-md-6">
                    <div class="p-3 stat-card">
                        <small class="text-secondary d-block fw-bold mb-1">Último Precio Leído</small>
                        <span id="textLastPrice" class="fs-3 fw-bold text-primary">--</span>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="p-3 stat-card">
                        <small class="text-secondary d-block fw-bold mb-1">Última Revisión</small>
                        <span id="textLastCheck" class="fs-4 fw-bold text-dark">--</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Historial de Logs -->
        <div class="card p-4">
            <h4 class="fw-bold mb-3 text-dark">📜 Historial de Registros (Logs)</h4>
            <div id="logBox" class="log-box"></div>
        </div>
    </div>

    <script>
        async function updateStatus() {
            try {
                const res = await fetch('/api/status?t=' + new Date().getTime());
                const data = await res.json();

                const btnStart = document.getElementById('btnStart');
                const btnStop = document.getElementById('btnStop');
                const badgeStatus = document.getElementById('badgeStatus');
                const textLastPrice = document.getElementById('textLastPrice');
                const textLastCheck = document.getElementById('textLastCheck');
                const textTimer = document.getElementById('textTimer');
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

                if (data.running) {
                    textTimer.innerText = '⏱️ Próxima revisión en: ' + data.countdown + 's';
                } else {
                    textTimer.innerText = '⏱️ Próxima revisión: Inactivo';
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
            const price = document.getElementById('inputPrice').value;
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
            const price = document.getElementById('inputPrice').value;

            await fetch('/api/scan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url, target_price: price })
            });
            updateStatus();
        }

        setInterval(updateStatus, 1000);
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
    
    price_val = str(data.get("target_price", monitor_state["target_price"])).replace(",", ".")
    try:
        monitor_state["target_price"] = float(price_val)
    except ValueError:
        pass
        
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
        price_val = str(data["target_price"]).replace(",", ".")
        try:
            monitor_state["target_price"] = float(price_val)
        except ValueError:
            pass

    add_log("[SCAN] Iniciando escaneo instantaneo via API Web...")
    threading.Thread(target=ejecutar_scraping, daemon=True).start()
    return jsonify({"success": True})


def open_browser():
    time.sleep(1.2)
    webbrowser.open("http://localhost:5050")


if __name__ == "__main__":
    print("Iniciando Servidor Web con Contador en http://localhost:5050 ...")
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host="127.0.0.1", port=5050, debug=False)
