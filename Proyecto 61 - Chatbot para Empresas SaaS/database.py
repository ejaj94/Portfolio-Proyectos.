import os
import sqlite3
from datetime import datetime

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'chatbot.db')

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("[DB] Removida base de dados antiga para recriação limpa.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Tabela de Perguntas Frequentes (FAQs)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            category TEXT NOT NULL,
            keywords TEXT NOT NULL,
            is_active INTEGER DEFAULT 1
        );
    """)

    # 2. Tabela de Base de Conhecimento (KB Articles)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            content TEXT NOT NULL,
            views_count INTEGER DEFAULT 0,
            updated_at TEXT NOT NULL
        );
    """)

    # 3. Tabela de Conversas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_token TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            customer_email TEXT,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
    """)

    # 4. Tabela de Mensagens do Chat
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            sender TEXT NOT NULL,
            message_text TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id)
        );
    """)

    # 5. Tabela de Configurações do Bot
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bot_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bot_name TEXT NOT NULL,
            welcome_message TEXT NOT NULL,
            fallback_message TEXT NOT NULL,
            trigger_word TEXT NOT NULL
        );
    """)

    # --- POPULAR BASE DE DADOS COM DADOS DE EXEMPLO (Pt-PT) ---

    # 1. FAQs Seed
    faqs_seed = [
        ("Quais são os horários de atendimento da empresa?",
         "O nosso atendimento presencial e digital funciona de Segunda a Sexta-feira, das 09:00 às 19:00, e aos Sábados das 09:00 às 13:00.",
         "Horários", "horario, funcionamento, abertura, fecho, atendimento", 1),
        
        ("Quais os métodos de pagamento aceites?",
         "Aceitamos pagamentos por MBWay, Referência Multibanco, Cartão de Crédito/Débito (Visa/Mastercard), Transferência Bancária e PayPal.",
         "Faturação", "pagamento, mbway, multibanco, cartao, transferencia, paypal", 1),

        ("Como posso emitir uma fatura com NIF corporativo?",
         "Pode introduzir o seu NIF e razão social durante o checkout. Caso necessite de alteração posterior, envie o seu pedido para suporte@ejajtech.com.",
         "Faturação", "fatura, nif, contribuinte, recibo, imposto", 1),

        ("Qual é o prazo médio de entrega ou implementação de um software?",
         "O prazo varia consoante o projeto. Aplicações SaaS pré-configuradas ficam ativas em 24h. Projetos personalizados têm um prazo médio de 5 a 15 dias úteis.",
         "Serviços", "prazo, entrega, tempo, instalacao, desenvolvimento", 1),

        ("Como solicitar suporte técnico urgente ou humano?",
         "Se o nosso assistente virtual não resolver a sua dúvida, digite a palavra 'AJUDA' ou clique no botão de suporte WhatsApp (+351 911 151 993).",
         "Suporte Técnico", "suporte, ajuda, humano, urgente, whatsapp, contacto", 1),

        ("A empresa realiza integrações de software com APIs personalizadas?",
         "Sim! A EJAJ TECH é especializada no desenvolvimento de REST APIs, WebSockets e integrações com sistemas ERP, CRM e e-commerce.",
         "Serviços", "api, integracao, erp, crm, conexao, sistema", 1),

        ("Como agendar uma demonstração gratuita de um projeto?",
         "Pode agendar diretamente pelo nosso WhatsApp (+351 911 151 993) ou através do formulário de agendamento no nosso portal.",
         "Vendas", "demo, demonstracao, agendar, reuniao, teste", 1)
    ]

    cursor.executemany("""
        INSERT INTO faqs (question, answer, category, keywords, is_active)
        VALUES (?, ?, ?, ?, ?)
    """, faqs_seed)

    # 2. Knowledge Base Seed
    kb_seed = [
        ("Guia de Integração do BotCorp AI com Websites", "Integração & API",
         "Para integrar o BotCorp AI no seu site, adicione o script fornecido no painel de administração antes do fecho da tag </body>. O robô carregará automaticamente com as suas FAQs e base de conhecimento.",
         142, datetime.now().strftime("%Y-%m-%d")),
        
        ("Manual de Configuração de Palavras-Chave e Respostas", "Configuração",
         "As palavras-chave permitem que o bot identifique a intenção do cliente. Adicione sinónimos separados por vírgulas para maximizar a taxa de correspondência automática.",
         98, datetime.now().strftime("%Y-%m-%d")),

        ("Política de Privacidade e Proteção de Dados (RGPD)", "Legal & Segurança",
         "Todas as conversas mantidas no BotCorp AI são encriptadas. Os dados de clientes não são partilhados com terceiros e estão protegidos em conformidade com o RGPD europeu.",
         215, datetime.now().strftime("%Y-%m-%d"))
    ]

    cursor.executemany("""
        INSERT INTO knowledge_base (title, category, content, views_count, updated_at)
        VALUES (?, ?, ?, ?, ?)
    """, kb_seed)

    # 3. Settings Seed
    cursor.execute("""
        INSERT INTO bot_settings (bot_name, welcome_message, fallback_message, trigger_word)
        VALUES (?, ?, ?, ?)
    """, ("BotCorp AI 🤖", 
          "Olá! Sou o assistente virtual da EJAJ TECH. Como posso ajudar a sua empresa hoje?", 
          "Não consegui compreender a sua pergunta com exatidão. Pode reformular ou digitar 'AJUDA' para falar com o nosso suporte humano via WhatsApp (+351 911 151 993).", 
          "AJUDA"))

    # 4. Conversations & Messages Seed
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("""
        INSERT INTO conversations (session_token, customer_name, customer_email, status, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, ("sess_001_demo", "Eng. Carlos Silva", "carlos.silva@empresa.pt", "Ativa", now_str))
    
    conv_id = cursor.lastrowid

    cursor.executemany("""
        INSERT INTO chat_messages (conversation_id, sender, message_text, timestamp)
        VALUES (?, ?, ?, ?)
    """, [
        (conv_id, "bot", "Olá! Sou o assistente virtual da EJAJ TECH. Como posso ajudar a sua empresa hoje?", now_str),
        (conv_id, "user", "Quais os métodos de pagamento aceites?", now_str),
        (conv_id, "bot", "Aceitamos pagamentos por MBWay, Referência Multibanco, Cartão de Crédito/Débito, Transferência Bancária e PayPal.", now_str)
    ])

    conn.commit()
    conn.close()
    print("[DB] Base de dados do Chatbot Robótico (chatbot.db) inicializada com sucesso!")

if __name__ == '__main__':
    init_db()
