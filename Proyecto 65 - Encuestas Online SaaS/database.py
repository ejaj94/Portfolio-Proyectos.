import sqlite3
import os
import json
from datetime import datetime

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'surveys.db')

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table for Surveys
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS surveys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        slug TEXT UNIQUE NOT NULL,
        questions_json TEXT NOT NULL,
        theme_color TEXT DEFAULT '#10B981',
        created_at TEXT NOT NULL
    )
    """)

    # Table for Survey Responses
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS survey_responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        survey_id INTEGER NOT NULL,
        answers_json TEXT NOT NULL,
        user_ip TEXT,
        submitted_at TEXT NOT NULL,
        FOREIGN KEY (survey_id) REFERENCES surveys (id) ON DELETE CASCADE
    )
    """)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Seed Survey 1: NPS & Satisfação de Cliente
    questions_s1 = [
        {
            "id": "q_1",
            "type": "nps",
            "title": "Numa escala de 0 a 10, qual a probabilidade de recomendar os serviços da EJAJ TECH a um amigo ou colega?",
            "subtitle": "0 = Nada Provável, 10 = Extremamente Provável",
            "required": True
        },
        {
            "id": "q_2",
            "type": "likert",
            "title": "O tempo de resposta do suporte técnico foi rápido e eficiente.",
            "options": ["Discordo Totalmente", "Discordo", "Neutro", "Concordo", "Concordo Totalmente"],
            "required": True
        },
        {
            "id": "q_3",
            "type": "yesno",
            "title": "A nossa plataforma resolveu o problema principal da sua empresa?",
            "required": True
        },
        {
            "id": "q_4",
            "type": "choice",
            "title": "Qual a funcionalidade que mais utiliza no nosso software?",
            "options": ["Dashboards em Tempo Real", "Automação de Relatórios", "Integração de APIs", "Gestão de Utilizadores"],
            "required": True
        },
        {
            "id": "q_5",
            "type": "text",
            "title": "Que novas melhorias ou funcionalidades gostaria de ver implementadas?",
            "subtitle": "Escreva a sua sugestão em texto livre",
            "required": False
        }
    ]

    # Seed Survey 2: Clima Organizacional
    questions_s2 = [
        {
            "id": "q_201",
            "type": "likert",
            "title": "Sinto-me valorizado e reconhecido pelo meu trabalho diário.",
            "options": ["Discordo Totalmente", "Discordo", "Neutro", "Concordo", "Concordo Totalmente"],
            "required": True
        },
        {
            "id": "q_202",
            "type": "nps",
            "title": "Como avalia o seu nível geral de satisfação com o ambiente de trabalho?",
            "subtitle": "0 = Muito Insatisfeito, 10 = Totalmente Satisfeito",
            "required": True
        },
        {
            "id": "q_203",
            "type": "yesno",
            "title": "Considera que dispõe de todas as ferramentas necessárias para desempenhar a sua função?",
            "required": True
        }
    ]

    # Insert seed surveys
    cursor.execute("""
    INSERT INTO surveys (title, description, slug, questions_json, theme_color, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "Medição de NPS & Satisfação de Cliente 📈",
        "Inquérito oficial de avaliação da qualidade e recomendação dos nossos serviços empresariais.",
        "medicao-nps-satisfacao-cliente",
        json.dumps(questions_s1),
        "#10B981",
        now
    ))
    s1_id = cursor.lastrowid

    cursor.execute("""
    INSERT INTO surveys (title, description, slug, questions_json, theme_color, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "Inquérito de Clima Organizacional & RH 👥",
        "Avaliação do ambiente de trabalho, satisfação interna e motivação das equipas.",
        "clima-organizacional-rh",
        json.dumps(questions_s2),
        "#6366F1",
        now
    ))

    # Insert sample seed responses for Survey 1
    resp1 = {
        "q_1": "10",
        "q_2": "Concordo Totalmente",
        "q_3": "Sim",
        "q_4": "Dashboards em Tempo Real",
        "q_5": "Integração nativa com mais ferramentas de pagamentos."
    }
    resp2 = {
        "q_1": "9",
        "q_2": "Concordo",
        "q_3": "Sim",
        "q_4": "Automação de Relatórios",
        "q_5": "Exportação em PDF com templates personalizados."
    }
    resp3 = {
        "q_1": "6",
        "q_2": "Neutro",
        "q_3": "Não",
        "q_4": "Gestão de Utilizadores",
        "q_5": "Melhorar os tempos de carregamento nas horas de ponta."
    }

    cursor.execute("""
    INSERT INTO survey_responses (survey_id, answers_json, user_ip, submitted_at)
    VALUES (?, ?, ?, ?)
    """, (s1_id, json.dumps(resp1), "127.0.0.1", now))

    cursor.execute("""
    INSERT INTO survey_responses (survey_id, answers_json, user_ip, submitted_at)
    VALUES (?, ?, ?, ?)
    """, (s1_id, json.dumps(resp2), "127.0.0.1", now))

    cursor.execute("""
    INSERT INTO survey_responses (survey_id, answers_json, user_ip, submitted_at)
    VALUES (?, ?, ?, ?)
    """, (s1_id, json.dumps(resp3), "127.0.0.1", now))

    conn.commit()
    conn.close()
    print("[Database OK] surveys.db criada e populada com inquéritos e respostas iniciais.")

if __name__ == '__main__':
    init_db()
