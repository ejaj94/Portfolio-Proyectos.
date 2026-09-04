import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'chat.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabla Usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            avatar_url TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'online',
            custom_status TEXT,
            last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tabla Conversaciones (Directas o Grupos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            type TEXT NOT NULL DEFAULT 'direct',
            icon_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_message_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tabla Miembros de Conversación
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversation_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            role TEXT DEFAULT 'member',
            unread_count INTEGER DEFAULT 0,
            is_muted INTEGER DEFAULT 0,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')

    # Tabla Mensajes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            sender_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            media_url TEXT,
            reply_to_id INTEGER,
            status TEXT NOT NULL DEFAULT 'read',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
            FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')

    # Tabla Reacciones
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            emoji TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE(message_id, user_id, emoji)
        )
    ''')

    conn.commit()
    conn.close()
    seed_initial_data()

def seed_initial_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Seed Usuarios
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        users_data = [
            ('Enmanuel Jimenez', 'enmanuel', 'enmanuel@ejajtech.com', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150', 'Founder & Lead Architect', 'online', 'Construyendo el futuro con EJAJ TECH 🚀'),
            ('Ana Rodrigues', 'ana.ui', 'ana.rodrigues@ejajtech.com', 'https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150', 'Lead UI/UX Designer', 'online', 'Perfeccionando la interfaz Messenger Blue ✨'),
            ('Carlos Silva', 'carlos.dev', 'carlos.silva@ejajtech.com', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150', 'Senior Backend Engineer', 'away', 'En reunión con el equipo de infraestructura ☕'),
            ('Sofia Costa', 'sofia.pm', 'sofia.costa@ejajtech.com', 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150', 'Senior Product Manager', 'dnd', 'Evaluando roadmap del Proyecto 36 📋'),
            ('Tiago Mendes', 'tiago.mobile', 'tiago.mendes@ejajtech.com', 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150', 'Fullstack App Lead', 'offline', 'De vuelta en 1 hora')
        ]
        cursor.executemany('''
            INSERT INTO users (name, username, email, avatar_url, role, status, custom_status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', users_data)

    # Seed Conversaciones
    cursor.execute('SELECT COUNT(*) FROM conversations')
    if cursor.fetchone()[0] == 0:
        now = datetime.now()
        
        # 1. Grupo Dev & Arch
        cursor.execute('''
            INSERT INTO conversations (name, type, icon_url, created_at, last_message_at)
            VALUES ('#general-dev-ejajtech', 'group', 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=150', ?, ?)
        ''', ((now - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'), now.strftime('%Y-%m-%d %H:%M:%S')))
        conv_group_id = cursor.lastrowid

        # Members Grupo
        cursor.executemany('''
            INSERT INTO conversation_members (conversation_id, user_id, role, unread_count)
            VALUES (?, ?, ?, ?)
        ''', [
            (conv_group_id, 1, 'admin', 0),
            (conv_group_id, 2, 'member', 0),
            (conv_group_id, 3, 'member', 0),
            (conv_group_id, 4, 'member', 0),
            (conv_group_id, 5, 'member', 0)
        ])

        # 2. Chat Directo Enmanuel <-> Ana
        cursor.execute('''
            INSERT INTO conversations (name, type, created_at, last_message_at)
            VALUES (NULL, 'direct', ?, ?)
        ''', ((now - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'), now.strftime('%Y-%m-%d %H:%M:%S')))
        conv_ana_id = cursor.lastrowid

        cursor.executemany('''
            INSERT INTO conversation_members (conversation_id, user_id, unread_count)
            VALUES (?, ?, ?)
        ''', [
            (conv_ana_id, 1, 0),
            (conv_ana_id, 2, 0)
        ])

        # 3. Chat Directo Enmanuel <-> Carlos
        cursor.execute('''
            INSERT INTO conversations (name, type, created_at, last_message_at)
            VALUES (NULL, 'direct', ?, ?)
        ''', ((now - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S'), (now - timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')))
        conv_carlos_id = cursor.lastrowid

        cursor.executemany('''
            INSERT INTO conversation_members (conversation_id, user_id, unread_count)
            VALUES (?, ?, ?)
        ''', [
            (conv_carlos_id, 1, 0),
            (conv_carlos_id, 3, 1)
        ])

        # Seed Mensajes en Group
        messages_group = [
            (conv_group_id, 1, '¡Hola equipo! Bienvenidos al nuevo canal de mensajería **CONNECT-CHAT SaaS** de EJAJ TECH 🚀', None, 'read', (now - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')),
            (conv_group_id, 2, '¡Quedó espectacular la paleta de colores azul Messenger (#0866FF)! La velocidad de respuesta es al instante. 👍', None, 'read', (now - timedelta(hours=1, minutes=45)).strftime('%Y-%m-%d %H:%M:%S')),
            (conv_group_id, 3, 'Los endpoints REST de la API de mensajería están corriendo con una latencia de menos de 15ms. Excelente trabajo Enmanuel.', None, 'read', (now - timedelta(hours=1, minutes=30)).strftime('%Y-%m-%d %H:%M:%S')),
            (conv_group_id, 4, '¿Tenemos lista la integración de notificaciones y confirmación de lectura azul ✓✓?', None, 'read', (now - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')),
            (conv_group_id, 1, '¡Así es Sofia! Todo funcionando al 100%. Pueden probar enviando mensajes y reacciones.', None, 'read', (now - timedelta(minutes=20)).strftime('%Y-%m-%d %H:%M:%S'))
        ]

        cursor.executemany('''
            INSERT INTO messages (conversation_id, sender_id, content, media_url, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', messages_group)

        # Seed Mensajes Directos Ana
        messages_ana = [
            (conv_ana_id, 2, 'Hola Enmanuel, ¿qué opinas de los iconos y botones de reacción flotantes en los chats directos?', None, 'read', (now - timedelta(minutes=45)).strftime('%Y-%m-%d %H:%M:%S')),
            (conv_ana_id, 1, 'Están geniales Ana. La animación de escritura "Escribiendo..." y los contadores en rojo de mensajes sin leer le dan una estética idéntica a Facebook Messenger.', None, 'read', (now - timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S'))
        ]

        cursor.executemany('''
            INSERT INTO messages (conversation_id, sender_id, content, media_url, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', messages_ana)

        # Seed Mensajes Directos Carlos
        messages_carlos = [
            (conv_carlos_id, 3, 'Enmanuel, dejé listas las funciones de la base de datos SQLite para soportar hilos ilimitados y reacciones por mensaje.', None, 'read', (now - timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S'))
        ]

        cursor.executemany('''
            INSERT INTO messages (conversation_id, sender_id, content, media_url, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', messages_carlos)

        # Seed Reacciones
        reactions_data = [
            (1, 2, '🚀'),
            (1, 3, '👍'),
            (2, 1, '❤️'),
            (2, 4, '🔥'),
            (6, 1, '👍')
        ]
        cursor.executemany('''
            INSERT INTO reactions (message_id, user_id, emoji)
            VALUES (?, ?, ?)
        ''', reactions_data)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("[OK] Base de datos chat.db inicializada con exito para Proyecto 36.")
