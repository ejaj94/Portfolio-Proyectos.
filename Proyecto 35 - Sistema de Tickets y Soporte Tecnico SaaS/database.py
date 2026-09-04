import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'helpdesk.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabla Agentes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            role TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Disponible',
            avatar_url TEXT,
            specialty TEXT NOT NULL,
            active_tickets INTEGER DEFAULT 0,
            resolved_tickets INTEGER DEFAULT 0
        )
    ''')

    # Tabla Tickets
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Abierto',
            client_name TEXT NOT NULL,
            client_email TEXT NOT NULL,
            agent_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            due_at TIMESTAMP NOT NULL,
            resolution_summary TEXT,
            FOREIGN KEY (agent_id) REFERENCES agents(id)
        )
    ''')

    # Tabla Comentarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            author_name TEXT NOT NULL,
            author_role TEXT NOT NULL,
            content TEXT NOT NULL,
            is_internal INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ticket_id) REFERENCES tickets(id) ON DELETE CASCADE
        )
    ''')

    # Tabla Historial de Auditoría
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            actor_name TEXT NOT NULL,
            action TEXT NOT NULL,
            details TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ticket_id) REFERENCES tickets(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
    seed_initial_data()

def seed_initial_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Verificar si ya existen agentes
    cursor.execute('SELECT COUNT(*) FROM agents')
    if cursor.fetchone()[0] == 0:
        agents_data = [
            ('Carlos Silva', 'carlos.silva@ejajtech.com', 'Senior Cloud & Linux Architect', 'Disponible', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150', 'Infraestructura & Servidores', 3, 142),
            ('Ana Rodrigues', 'ana.rodrigues@ejajtech.com', 'Cybersecurity & DevOps Specialist', 'En Llamada', 'https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150', 'Seguridad & Redes', 2, 98),
            ('Tiago Mendes', 'tiago.mendes@ejajtech.com', 'Fullstack Lead Engineer', 'Disponible', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150', 'SaaS & Web Software', 4, 215),
            ('Sofia Costa', 'sofia.costa@ejajtech.com', 'Database Administrator (DBA)', 'Ocupado', 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150', 'SQL Server & Postgres', 1, 87)
        ]
        cursor.executemany('''
            INSERT INTO agents (name, email, role, status, avatar_url, specialty, active_tickets, resolved_tickets)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', agents_data)

    # Verificar si ya existen tickets
    cursor.execute('SELECT COUNT(*) FROM tickets')
    if cursor.fetchone()[0] == 0:
        now = datetime.now()
        
        sample_tickets = [
            (
                'TCK-2026-8921',
                'Fallo crítico de Latencia en Clúster PostgreSQL Principal',
                'El clúster secundario de la base de datos de producción presenta spikes de latencia superiores a 4500ms durante la sincronización de logs.',
                'Base de Datos',
                'Crítica',
                'En Proceso',
                'Miguel Barros (AutoP peças)',
                'm.barros@autopecas.pt',
                4, # Sofia Costa
                (now - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'),
                now.strftime('%Y-%m-%d %H:%M:%S'),
                (now + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'),
                None
            ),
            (
                'TCK-2026-8922',
                'Configuración de Túnel VPN IPsec para Sucursal Porto',
                'Requerimos la apertura de puertos y enrutamiento seguro entre el gateway de la oficina central y la nueva sede.',
                'Redes',
                'Alta',
                'Abierto',
                'Helena Ferreira (Veloce Racing)',
                'helena@veloceracing.com',
                2, # Ana Rodrigues
                (now - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S'),
                now.strftime('%Y-%m-%d %H:%M:%S'),
                (now + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'),
                None
            ),
            (
                'TCK-2026-8923',
                'Error 500 al emitir facturas en pasarela de pagos Stripe',
                'Los clientes reportan time-out al intentar procesar suscripciones anuales mediante la API de facturación.',
                'Software',
                'Crítica',
                'Pendiente Cliente',
                'Rui Fonseca (Nexus Property)',
                'rui@nexusproperty.io',
                3, # Tiago Mendes
                (now - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S'),
                now.strftime('%Y-%m-%d %H:%M:%S'),
                (now - timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M:%S'),
                None
            ),
            (
                'TCK-2026-8924',
                'Aumento de cuota de almacenamiento en Servidor S3 Cloud',
                'Solicitamos duplicar la capacidad del bucket de backups automáticos de 2TB a 5TB.',
                'Cloud',
                'Media',
                'Resuelto',
                'Beatriz Lima (Clinica Vet Luxo)',
                'b.lima@vetluxo.pt',
                1, # Carlos Silva
                (now - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
                now.strftime('%Y-%m-%d %H:%M:%S'),
                (now + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
                'Se incrementó la cuota del bucket AWS S3 a 5TB con políticas de Lifecycle a Glacier habilitadas.'
            ),
            (
                'TCK-2026-8925',
                'Duda sobre renovación de licencia de software anual',
                'Consulta administrativa sobre los detalles de facturación electrónica en Portugal (Saft-PT).',
                'Facturación',
                'Baja',
                'Cerrado',
                'Gonçalo Neves (Executive Studio)',
                'gneves@executivestudio.com',
                1, # Carlos Silva
                (now - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'),
                now.strftime('%Y-%m-%d %H:%M:%S'),
                (now + timedelta(hours=20)).strftime('%Y-%m-%d %H:%M:%S'),
                'Se envió la guía explicativa del módulo de facturación SaaS EJAJ TECH.'
            )
        ]

        cursor.executemany('''
            INSERT INTO tickets (code, title, description, category, priority, status, client_name, client_email, agent_id, created_at, updated_at, due_at, resolution_summary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_tickets)

        # Seed Comments
        comments_data = [
            (1, 'Miguel Barros', 'Cliente', 'Hola equipo, la latencia está afectando el punto de venta. ¿Podrían revisar los índices de la tabla orders?', 0, (now - timedelta(minutes=50)).strftime('%Y-%m-%d %H:%M:%S')),
            (1, 'Sofia Costa', 'Agente', 'REVISIÓN INTERNA: He detectado un bloqueo de lecturas pesadas por un query de analítica sin LIMIT. Aplicando pkill al query y optimizando autovacuum.', 1, (now - timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M:%S')),
            (1, 'Sofia Costa', 'Agente', 'Hola Miguel, estamos ejecutando una desfragmentación de índices en caliente. La latencia ya descendió de 4500ms a 120ms. Seguimos monitoreando.', 0, (now - timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')),
            (3, 'Tiago Mendes', 'Agente', 'Estimado Rui, hemos verificado que los webhooks de Stripe están rebotando por un certificado SSL expirado en su dominio. Por favor renueven el cert.', 0, (now - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S'))
        ]

        cursor.executemany('''
            INSERT INTO comments (ticket_id, author_name, author_role, content, is_internal, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', comments_data)

        # Seed History Log
        history_data = [
            (1, 'Sistema', 'Creación', 'Ticket creado automáticamente desde portal con Prioridad Crítica', (now - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')),
            (1, 'Carlos Silva', 'Reasignación Agente', 'Asignado el caso a la especialista de BD Sofia Costa', (now - timedelta(minutes=55)).strftime('%Y-%m-%d %H:%M:%S')),
            (1, 'Sofia Costa', 'Cambio de Estado', 'Estado actualizado a En Proceso', (now - timedelta(minutes=40)).strftime('%Y-%m-%d %H:%M:%S')),
            (1, 'Sofia Costa', 'Nota Interna', 'Añadida nota técnica interna sobre autovacuum y lock de tablas', (now - timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M:%S')),
            (4, 'Carlos Silva', 'Resuelto', 'Ticket resuelto y notificado al cliente Beatriz Lima', (now - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S'))
        ]

        cursor.executemany('''
            INSERT INTO history_log (ticket_id, actor_name, action, details, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', history_data)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("[OK] Base de datos helpdesk.db inicializada con exito con tablas y seed data de demostracion.")
