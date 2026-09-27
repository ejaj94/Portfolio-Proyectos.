from flask import Flask, render_template, send_from_directory, jsonify
import os

app = Flask(__name__)
PORT = 6960

VIDEOS_DIR = r"C:\Users\enman\Desktop\Portfolio de programacion\Proyectos reales\Pagina de programacion EJAJ Tech"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/videos/<path:filename>')
def serve_video(filename):
    return send_from_directory(VIDEOS_DIR, filename)

if __name__ == '__main__':
    print(f"Servidor Showcase 90 Dias EJAJ Tech iniciado na porta {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=True)
