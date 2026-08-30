import os
from flask import Flask, render_template, request, jsonify, send_file
from simulador_red import NetworkSimulatorEngine
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
engine = NetworkSimulatorEngine()


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/simulate-scan", methods=["POST"])
def simulate_scan():
    data = request.get_json() or {}
    net_range = data.get("range", "192.168.1.0/24").strip()

    try:
        result = engine.run_simulated_scan(network_range=net_range)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@app.route("/api/generate-pdf", methods=["POST"])
def generate_pdf():
    try:
        scan_res = engine.run_simulated_scan()
        pdf_path = os.path.join(app.root_path, "reporte_simulado_demo.pdf")

        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        # Encabezado del Informe
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "Informe Didáctico de Inventario de Red (Simulado)")

        c.setFont("Helvetica", 10)
        c.drawString(50, height - 70, f"Fecha de Simulación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(50, height - 85, f"Rango Consultado: {scan_res['network_range']}")
        c.line(50, height - 95, 550, height - 95)

        y = height - 120
        for dev in scan_res["devices"]:
            if y < 100:
                c.showPage()
                y = height - 50

            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, f"Dispositivo: {dev['hostname']} ({dev['ip']})")
            y -= 18

            c.setFont("Helvetica", 10)
            c.drawString(70, y, f"Tipo: {dev['type']} | MAC: {dev['mac']} | Estado: {dev['status']}")
            y -= 15

            ports_str = ", ".join(map(str, dev['simulated_ports'])) if dev['simulated_ports'] else "Ninguno"
            c.drawString(70, y, f"Puertos Simulados: {ports_str} | Puntaje Seguridad: {dev['security_score']}/100")
            y -= 15

            c.drawString(70, y, f"Recomendación: {dev['recommendation']}")
            y -= 25

        c.save()

        return send_file(pdf_path, as_attachment=True, download_name="Reporte_Inventario_Red_Simulado.pdf")
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


if __name__ == "__main__":
    print("Iniciando Simulador Educativo de Inventario de Red en http://localhost:5005")
    app.run(host="0.0.0.0", port=5005, debug=False)
