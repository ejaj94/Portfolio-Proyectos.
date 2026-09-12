import sqlite3
import os
from datetime import datetime, date, timedelta

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'cliniccraft.db')

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Patients Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_code TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        nif TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        birth_date TEXT NOT NULL,
        insurance TEXT NOT NULL DEFAULT 'Particular',
        blood_type TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)

    # 2. Professionals Table (Médicos, Enfermeiros, Especialistas)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS professionals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialty TEXT NOT NULL,
        license_no TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        consultation_fee REAL NOT NULL DEFAULT 70.0,
        status TEXT NOT NULL DEFAULT 'Ativo',
        created_at TEXT NOT NULL
    );
    """)

    # 3. Appointments Table (Citas)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_code TEXT NOT NULL UNIQUE,
        patient_id INTEGER NOT NULL,
        professional_id INTEGER NOT NULL,
        appointment_date TEXT NOT NULL,
        appointment_time TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Confirmada', -- Confirmada, Em Espera, Realizada, Cancelada
        reason TEXT NOT NULL,
        fee REAL NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES patients (id),
        FOREIGN KEY (professional_id) REFERENCES professionals (id)
    );
    """)

    # 4. Consultations Table (Consultas Clínicas)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consultations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_id INTEGER NOT NULL,
        patient_id INTEGER NOT NULL,
        professional_id INTEGER NOT NULL,
        diagnosis TEXT NOT NULL,
        symptoms TEXT NOT NULL,
        prescription TEXT NOT NULL,
        vitals TEXT NOT NULL,
        consultation_date TEXT NOT NULL,
        FOREIGN KEY (appointment_id) REFERENCES appointments (id),
        FOREIGN KEY (patient_id) REFERENCES patients (id),
        FOREIGN KEY (professional_id) REFERENCES professionals (id)
    );
    """)

    # 5. Documents Table (Documentos Clínicos & Exames)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_code TEXT NOT NULL UNIQUE,
        patient_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        doc_type TEXT NOT NULL, -- Exame, Relatório, Atestado, Consentimento
        file_name TEXT NOT NULL,
        upload_date TEXT NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES patients (id)
    );
    """)

    # 6. Payments Table (Pagos & Faturação)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_code TEXT NOT NULL UNIQUE,
        appointment_id INTEGER NOT NULL,
        patient_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        payment_method TEXT NOT NULL, -- Multibanco, MB WAY, Cartão, Dinheiro
        status TEXT NOT NULL DEFAULT 'Pago', -- Pago, Pendente, Reembolsado
        payment_date TEXT NOT NULL,
        FOREIGN KEY (appointment_id) REFERENCES appointments (id),
        FOREIGN KEY (patient_id) REFERENCES patients (id)
    );
    """)

    # --- SEED DATA ---
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    today = date.today()

    # Seed Patients
    patients_data = [
        ("PAC-1001", "Helena Ferreira Rodrigues", "255400192", "helena.rodrigues@email.pt", "+351 912 345 111", "1988-04-12", "Multicare", "A+", now_str),
        ("PAC-1002", "Gonçalo Afonso Ramos", "244300281", "goncalo.ramos@email.pt", "+351 913 456 222", "1994-09-25", "Médis", "O+", now_str),
        ("PAC-1003", "Teresa Maria Carmo", "233200370", "teresa.carmo@email.pt", "+351 914 567 333", "1975-12-03", "ADSE", "B+", now_str),
        ("PAC-1004", "Diogo Bernardo Silva", "222100469", "diogo.silva@email.pt", "+351 915 678 444", "1999-07-18", "Particular", "AB-", now_str)
    ]
    cursor.executemany("""
    INSERT INTO patients (patient_code, name, nif, email, phone, birth_date, insurance, blood_type, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, patients_data)

    # Seed Professionals
    professionals_data = [
        ("Dr. Enmanuel Jimenez", "Medicina Geral & Familiar", "OM-99201", "enmanuel.jimenez@cliniccraft.pt", "+351 911 151 993", 75.0, "Ativo", now_str),
        ("Dra. Beatriz Albuquerque", "Cardiologia Especializada", "OM-44812", "beatriz.albuquerque@cliniccraft.pt", "+351 916 123 777", 90.0, "Ativo", now_str),
        ("Dr. Ricardo Fonseca", "Ortopedia & Traumatologia", "OM-66304", "ricardo.fonseca@cliniccraft.pt", "+351 917 234 888", 85.0, "Ativo", now_str),
        ("Enfª. Carmo Vasconcelos", "Enfermagem & Triagem", "OE-11209", "carmo.vasconcelos@cliniccraft.pt", "+351 918 345 999", 40.0, "Ativo", now_str)
    ]
    cursor.executemany("""
    INSERT INTO professionals (name, specialty, license_no, email, phone, consultation_fee, status, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, professionals_data)

    # Seed Appointments
    appts_data = [
        ("CIT-2026-701", 1, 1, today.strftime("%Y-%m-%d"), "09:30", "Confirmada", "Consulta de avaliação geral e exames de rotina.", 75.0, now_str),
        ("CIT-2026-702", 2, 2, today.strftime("%Y-%m-%d"), "11:00", "Confirmada", "Eletrocardiograma e rastreio de hipertensão.", 90.0, now_str),
        ("CIT-2026-703", 3, 3, (today + timedelta(days=2)).strftime("%Y-%m-%d"), "15:00", "Confirmada", "Avaliação articular de joelho pós-lesão desportiva.", 85.0, now_str),
        ("CIT-2026-704", 4, 1, (today - timedelta(days=3)).strftime("%Y-%m-%d"), "14:30", "Realizada", "Consulta de seguimento de tratamento bronquítico.", 75.0, (today - timedelta(days=4)).strftime("%Y-%m-%d %H:%M"))
    ]
    cursor.executemany("""
    INSERT INTO appointments (appointment_code, patient_id, professional_id, appointment_date, appointment_time, status, reason, fee, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, appts_data)

    # Seed Consultations
    consultations_data = [
        (4, 4, 1, "Bronquite agudizada de etiologia viral.", "Tosse seca persistente, febrícula (37.8ºC), astenia.", "Amoxicilina 875mg + Ác. Clavulânico 125mg 12/12h por 8 dias. Xarope mucolítico.", "TA: 120/80 mmHg | FC: 74 bpm | Temp: 36.6ºC | SpO2: 98%", (today - timedelta(days=3)).strftime("%Y-%m-%d %H:%M"))
    ]
    cursor.executemany("""
    INSERT INTO consultations (appointment_id, patient_id, professional_id, diagnosis, symptoms, prescription, vitals, consultation_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, consultations_data)

    # Seed Documents
    documents_data = [
        ("DOC-2026-101", 1, "Hemograma Completo & Perfil Lipídico", "Exame", "hemograma_helena_rodrigues.pdf", (today - timedelta(days=5)).strftime("%Y-%m-%d")),
        ("DOC-2026-102", 2, "Eletrocardiograma de Repouso 12 Derivações", "Exame", "ecg_goncalo_ramos.pdf", (today - timedelta(days=2)).strftime("%Y-%m-%d")),
        ("DOC-2026-103", 4, "Atestado Médico de Incapacidade Temporária", "Atestado", "atestado_diogo_silva.pdf", (today - timedelta(days=3)).strftime("%Y-%m-%d"))
    ]
    cursor.executemany("""
    INSERT INTO documents (document_code, patient_id, title, doc_type, file_name, upload_date)
    VALUES (?, ?, ?, ?, ?, ?)
    """, documents_data)

    # Seed Payments
    payments_data = [
        ("FT-2026-901", 4, 4, 75.0, "MB WAY", "Pago", (today - timedelta(days=3)).strftime("%Y-%m-%d 15:10")),
        ("FT-2026-902", 1, 1, 75.0, "Multibanco", "Pago", today.strftime("%Y-%m-%d 09:45")),
        ("FT-2026-903", 2, 2, 90.0, "Cartão", "Pendente", today.strftime("%Y-%m-%d 11:15"))
    ]
    cursor.executemany("""
    INSERT INTO payments (invoice_code, appointment_id, patient_id, amount, payment_method, status, payment_date)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, payments_data)

    conn.commit()
    conn.close()
    print("[Database OK] cliniccraft.db criada e populada com sucesso.")

if __name__ == '__main__':
    init_db()
