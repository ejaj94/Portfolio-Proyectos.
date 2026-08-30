import os
from flask import Flask, render_template, request, jsonify, send_file
from network_engine import NetworkMonitorEngine
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
engine = NetworkMonitorEngine()


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/network-scan", methods=["POST"])
def network_scan():
    data = request.get_json() or {}
    net_range = data.get("range", "192.168.1.0/24").strip()

    try:
        result = engine.run_network_scan(network_range=net_range)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@app.route("/api/generate-pdf", methods=["POST"])
def generate_pdf():
    try:
        scan_res = engine.run_network_scan()
        pdf_path = os.path.join(app.root_path, "reporte_seguridad_pro.pdf")

        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        # Encabezado del Informe Profesional (pt-PT)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "Relatorio de Inventario e Seguranca de Rede PRO")

        c.setFont("Helvetica", 10)
        c.drawString(50, height - 70, f"Data da Analise: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(50, height - 85, f"Gama de Rede: {scan_res['network_range']}")
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

            ports_str = ", ".join(map(str, dev['active_ports'])) if dev['active_ports'] else "Nenhum"
            c.drawString(70, y, f"Portas Detetadas: {ports_str} | Pontuacao de Seguranca: {dev['security_score']}/100")
            y -= 15

            c.drawString(70, y, f"Recomendacao: {dev['recommendation']}")
            y -= 25

        c.save()

        return send_file(pdf_path, as_attachment=True, download_name="Relatorio_Inventario_Rede_PRO.pdf")
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


if __name__ == "__main__":
    print("Iniciando Network Security & Inventory Scanner PRO en http://localhost:5006")
    app.run(host="0.0.0.0", port=5006, debug=False)
