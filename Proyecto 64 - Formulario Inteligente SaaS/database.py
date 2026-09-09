import sqlite3
import os
import json
from datetime import datetime

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'forms.db')

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table for Forms
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS forms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        slug TEXT UNIQUE NOT NULL,
        fields_json TEXT NOT NULL,
        theme_color TEXT DEFAULT '#8B5CF6',
        created_at TEXT NOT NULL
    )
    """)

    # Table for Form Responses
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS form_responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        form_id INTEGER NOT NULL,
        answers_json TEXT NOT NULL,
        user_ip TEXT,
        submitted_at TEXT NOT NULL,
        FOREIGN KEY (form_id) REFERENCES forms (id) ON DELETE CASCADE
    )
    """)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Seed Template 1: Pesquisa de Satisfação de Cliente
    fields_t1 = [
        {
            "id": "f_1",
            "type": "text",
            "label": "Nome Completo",
            "placeholder": "Introduza o seu nome",
            "required": True,
            "help": "Para podermos identificar o seu registo."
        },
        {
            "id": "f_2",
            "type": "email",
            "label": "Endereço de E-mail empresarial",
            "placeholder": "exemplo@empresa.pt",
            "required": True,
            "help": "Prometemos não enviar spam."
        },
        {
            "id": "f_3",
            "type": "rating",
            "label": "Como avalia a qualidade do nosso serviço?",
            "required": True,
            "help": "De 1 (Insatisfeito) a 5 (Muito Satisfeito)"
        },
        {
            "id": "f_4",
            "type": "radio",
            "label": "Recomendaria a EJAJ TECH a um colega ou parceiro?",
            "options": ["Com certeza absoluta", "Muito provavelmente", "Pouco provável", "Não recomendaria"],
            "required": True
        },
        {
            "id": "f_5",
            "type": "textarea",
            "label": "Comentários ou Sugestões de Melhoria",
            "placeholder": "Escreva aqui a sua opinião detalhada...",
            "required": False
        }
    ]

    # Seed Template 2: Inscrição em Evento EJAJ TECH
    fields_t2 = [
        {
            "id": "f_201",
            "type": "text",
            "label": "Nome do Participante",
            "placeholder": "Seu nome completo",
            "required": True
        },
        {
            "id": "f_202",
            "type": "email",
            "label": "E-mail de Contacto",
            "placeholder": "utilizador@dominio.pt",
            "required": True
        },
        {
            "id": "f_203",
            "type": "phone",
            "label": "Número de Telefone / WhatsApp",
            "placeholder": "+351 912 345 678",
            "required": True
        },
        {
            "id": "f_204",
            "type": "dropdown",
            "label": "Sessão de Interesse no Evento",
            "options": ["Workshop de IA & Automação SaaS", "Engenharia de Sistemas Cloud", "Desenvolvimento Web de Alta Performance"],
            "required": True
        },
        {
            "id": "f_205",
            "type": "checkbox",
            "label": "Interesses Adicionais",
            "options": ["Consultoria Personalizada", "Demonstração de Software", "Networking com CEOs"],
            "required": False
        }
    ]

    # Seed Template 3: Suporte Técnico
    fields_t3 = [
        {
            "id": "f_301",
            "type": "text",
            "label": "Título da Ocorrência",
            "placeholder": "Descreva brevemente o problema",
            "required": True
        },
        {
            "id": "f_302",
            "type": "dropdown",
            "label": "Nível de Urgência",
            "options": ["Baixa (Dúvida)", "Média (Incidente menor)", "Alta (Sistema Inoperacional)"],
            "required": True
        },
        {
            "id": "f_303",
            "type": "textarea",
            "label": "Descrição Detalhada do Problema",
            "placeholder": "Descreva os passos para reproduzir o erro...",
            "required": True
        }
    ]

    # Insert seed forms
    cursor.execute("""
    INSERT INTO forms (title, description, slug, fields_json, theme_color, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "Pesquisa de Satisfação de Cliente 🏆",
        "Formulário para recolha de feedback valioso sobre os nossos serviços e soluções digitais.",
        "pesquisa-satisfacao-cliente",
        json.dumps(fields_t1),
        "#8B5CF6",
        now
    ))
    f1_id = cursor.lastrowid

    cursor.execute("""
    INSERT INTO forms (title, description, slug, fields_json, theme_color, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "Inscrição em Evento EJAJ TECH 🚀",
        "Garanta o seu lugar na nossa conferência de tecnologia e inovação software.",
        "inscricao-evento-ejaj",
        json.dumps(fields_t2),
        "#06B6D4",
        now
    ))
    f2_id = cursor.lastrowid

    cursor.execute("""
    INSERT INTO forms (title, description, slug, fields_json, theme_color, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "Formulário de Suporte & Contacto Técnico 🛠️",
        "Abra um pedido de assistência rápida com a nossa equipa de engenheiros.",
        "suporte-contacto-tecnico",
        json.dumps(fields_t3),
        "#10B981",
        now
    ))

    # Insert sample seed responses for Form 1
    resp1 = {
        "f_1": "Carlos Eduardo Silva",
        "f_2": "carlos.silva@techportugal.pt",
        "f_3": "5",
        "f_4": "Com certeza absoluta",
        "f_5": "Excelente plataforma! A facilidade de utilização e o desempenho do sistema superaram todas as expetativas."
    }
    resp2 = {
        "f_1": "Mariana Santos",
        "f_2": "mariana.santos@innov.pt",
        "f_3": "4",
        "f_4": "Muito provavelmente",
        "f_5": "Muito bom serviço. Gostaria de ver mais opções de gráficos no painel de controlo."
    }

    cursor.execute("""
    INSERT INTO form_responses (form_id, answers_json, user_ip, submitted_at)
    VALUES (?, ?, ?, ?)
    """, (f1_id, json.dumps(resp1), "127.0.0.1", now))

    cursor.execute("""
    INSERT INTO form_responses (form_id, answers_json, user_ip, submitted_at)
    VALUES (?, ?, ?, ?)
    """, (f1_id, json.dumps(resp2), "127.0.0.1", now))

    conn.commit()
    conn.close()
    print("[Database OK] forms.db criada e populada com formulários e respostas iniciais.")

if __name__ == '__main__':
    init_db()
