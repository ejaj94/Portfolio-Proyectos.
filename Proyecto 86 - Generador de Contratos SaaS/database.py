import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'contracts_system.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Create Templates Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            variable_tags TEXT NOT NULL,
            content_text TEXT NOT NULL
        )
    ''')

    # Create Clients Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            nif_tax TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            company_name TEXT
        )
    ''')

    # Create Contracts Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_code TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            template_id INTEGER NOT NULL,
            client_id INTEGER NOT NULL,
            status TEXT DEFAULT 'Assinado & Válido',
            hash_signature TEXT NOT NULL,
            created_at TEXT NOT NULL,
            pdf_url TEXT,
            FOREIGN KEY (template_id) REFERENCES templates (id),
            FOREIGN KEY (client_id) REFERENCES clients (id)
        )
    ''')

    # Seed Data if empty
    cursor.execute('SELECT COUNT(*) FROM templates')
    if cursor.fetchone()[0] == 0:
        sample_templates = [
            ("Contrato de Prestação de Serviços de TI & Software", "Tecnologia & Consultoria", "Minuta legal padrão para desenvolvimento de plataformas web, aplicações móveis, manutenção de servidores e consultoria tecnológica.", "{{NOME_CLIENTE}}, {{NIF}}, {{VALOR_TOTAL}}, {{PRAZO_MESES}}", "Pelo presente instrumento de Contrato de Prestação de Serviços, a empresa EJAJ TECH compromete-se a prestar serviços de engenharia de software ao Cliente {{NOME_CLIENTE}}, detentor do NIF {{NIF}}, pelo valor global de {{VALOR_TOTAL}} EUR, a ser executado no prazo de {{PRAZO_MESES}} meses."),
            ("Contrato de Arrendamento Habitacional / Comercial", "Imobiliário & Património", "Minuta contratual de arrendamento para habitação própria ou instalações comerciais sob a legislação portuguesa de arrendamento urbano.", "{{NOME_INQUILINO}}, {{NIF_INQUILINO}}, {{VALOR_RENDA}}, {{MORADA_IMOVEIS}}", "Entre o Senhorio e o Inquilino {{NOME_INQUILINO}}, portador do NIF {{NIF_INQUILINO}}, acorda-se o arrendamento do imóvel situado na morada {{MORADA_IMOVEIS}}, mediante a renda mensal ajustada de {{VALOR_RENDA}} EUR."),
            ("Acordo de Confidencialidade (NDA) & RGPD", "Proteção de Dados & Segredos Industriais", "Acordo jurídico para salvaguarda de segredos comerciais, propriedade intelectual e tratamento de dados pessoais em conformidade com o RGPD.", "{{NOME_PARCEIRO}}, {{NIF_PARCEIRO}}, {{DURACAO_ANOS}}", "As partes acordam proteger rigorosamente todas as informações confidenciais trocadas com {{NOME_PARCEIRO}} (NIF {{NIF_PARCEIRO}}), pelo período mínimo de {{DURACAO_ANOS}} anos a contar da data de assinatura."),
            ("Contrato de Trabalho a Termo Certo", "Recursos Humanos & Trabalho", "Modelo contratual de trabalho temporário com cláusulas de período de experiência, vencimento base e direitos laborais.", "{{NOME_TRABALHADOR}}, {{NIF_TRABALHADOR}}, {{CARGO}}, {{VENCIMENTO_BASE}}", "Admite-se o trabalhador {{NOME_TRABALHADOR}}, NIF {{NIF_TRABALHADOR}}, para desempenhar as funções de {{CARGO}}, auferindo o vencimento mensal base de {{VENCIMENTO_BASE}} EUR.")
        ]
        cursor.executemany('INSERT INTO templates (title, category, description, variable_tags, content_text) VALUES (?, ?, ?, ?, ?)', sample_templates)

        sample_clients = [
            ("Lia Mendonça", "509123456", "lia.mendonca@ecotech.pt", "+351 912 345 678", "Av. da Liberdade, 105, Lisboa", "EcoTech Solutions Lda"),
            ("Dr. Gonçalo Neves", "508765432", "goncalo.neves@lawfirm.pt", "+351 934 567 890", "Rua de Santa Catarina, 420, Porto", "Neves & Associados Sociedade de Advogados"),
            ("Sofia Carvalho", "239876543", "sofia.carvalho@designstudio.pt", "+351 965 432 109", "Praça do Município, 12, Faro", "Sofia Carvalho Studio"),
            ("Mário Silva", "507654321", "mario.silva@cinema.pt", "+351 927 890 123", "Av. dos Aliados, 88, Porto", "Douro Film Productions Lda")
        ]
        cursor.executemany('INSERT INTO clients (name, nif_tax, email, phone, address, company_name) VALUES (?, ?, ?, ?, ?, ?)', sample_clients)

        sample_contracts = [
            ("CTR-2026-8801", "Contrato de Prestação de Serviços de TI — EcoTech", 1, 1, "Assinado & Válido", "HASH-SHA256-99A82B71F3", "2026-09-08 11:30", "/export/pdf/CTR-2026-8801"),
            ("CTR-2026-8802", "Acordo de Confidencialidade NDA — Neves & Associados", 3, 2, "Assinado & Válido", "HASH-SHA256-44F10C88D2", "2026-09-10 15:45", "/export/pdf/CTR-2026-8802"),
            ("CTR-2026-8803", "Contrato de Arrendamento Comercial — Sofia Studio", 2, 3, "Pendente Assinatura", "HASH-SHA256-11E92A44B6", "2026-09-12 09:20", "/export/pdf/CTR-2026-8803")
        ]
        cursor.executemany('INSERT INTO contracts (contract_code, title, template_id, client_id, status, hash_signature, created_at, pdf_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', sample_contracts)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Banco de Dados contracts_system.db inicializado com sucesso!")
