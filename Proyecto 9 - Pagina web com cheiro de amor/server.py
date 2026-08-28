import http.server
import socketserver
import os
import json
import sqlite3
from urllib.parse import parse_qs, urlparse

PORT = 8080
DIRECTORY = r"C:\Users\ANGEL RAFAEL\Desktop\Portfolio de programacion\Proyectos reales\Com cheiro de amor pagina web Stephanie Santos"
DB_PATH = os.path.join(DIRECTORY, "workshops.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workshop_registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            workshop_type TEXT NOT NULL,
            participants INTEGER DEFAULT 1,
            notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path == '/api/workshop-register':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(body)
                name = data.get('name', '').strip()
                email = data.get('email', '').strip()
                phone = data.get('phone', '').strip()
                w_type = data.get('workshop_type', '').strip()
                participants = int(data.get('participants', 1))
                notes = data.get('notes', '').strip()

                if not name or not email or not phone:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': False, 'error': 'Campos obrigatórios em falta'}).encode('utf-8'))
                    return

                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO workshop_registrations (name, email, phone, workshop_type, participants, notes)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (name, email, phone, w_type, participants, notes))
                conn.commit()
                reg_id = cursor.lastrowid
                conn.close()

                print(f"Recorded registration #{reg_id}: {name} ({email}) for {w_type}")

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response_data = {
                    'success': True,
                    'id': reg_id,
                    'message': 'Inscrição guardada na base de dados SQLite com sucesso!'
                }
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode('utf-8'))
        else:
            self.send_error(404, "Endpoint not found")

    def do_GET(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path == '/api/workshop-registrations':
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('SELECT id, name, email, phone, workshop_type, participants, notes, created_at FROM workshop_registrations ORDER BY created_at DESC')
                rows = cursor.fetchall()
                conn.close()

                registrations = [
                    {
                        'id': r[0], 'name': r[1], 'email': r[2], 'phone': r[3],
                        'workshop_type': r[4], 'participants': r[5], 'notes': r[6], 'created_at': r[7]
                    } for r in rows
                ]

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'registrations': registrations}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode('utf-8'))
        else:
            super().do_GET()

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

if __name__ == "__main__":
    init_db()
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"Serving HTTP & Database API on port {PORT} from {DIRECTORY}...")
        httpd.serve_forever()
