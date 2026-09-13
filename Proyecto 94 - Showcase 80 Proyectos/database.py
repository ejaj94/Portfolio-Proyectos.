import os
import json

PROJECTS_DATA = [
    {
        "id": 71,
        "number": "Projeto 71",
        "title": "Crowdfunding & Mecenato SaaS",
        "name": "Fund Craft AI",
        "icon": "fa-solid fa-hand-holding-heart",
        "tagline": "Plataforma de Financiamento Coletivo, Angariação de Fundos & Recompensas",
        "features": [
            "Gestão de Campanhas de Crowdfunding",
            "Níveis de Recompensas & Doações",
            "Barra de Progresso & Metas Financeiras",
            "Painel de Apoiantes (Backers)",
            "Disparo Automático de Notificações"
        ],
        "technologies": ["Python Flask", "SQLite3", "JavaScript ES6", "HTML5 & CSS Grid", "FontAwesome 6"]
    },
    {
        "id": 72,
        "number": "Projeto 72",
        "title": "Sistema de Doações ❤️",
        "name": "Donation Craft AI",
        "icon": "fa-solid fa-heart",
        "tagline": "Gestão de Causas Sociais, Doadores Recorrentes & Objetivos de Impacto",
        "features": [
            "Registo & Gestão de Doadores VIP",
            "Campanhas de Angariação com Metas",
            "Histórico Transacional & Recibos",
            "Dashboard de Progresso Financeiro",
            "Filtros de Causas & Categorias"
        ],
        "technologies": ["Python 3.11", "Flask RESTful", "SQLite Database", "CSS Flexbox & Variables", "Animate.css"]
    },
    {
        "id": 73,
        "number": "Projeto 73",
        "title": "Gerador de Contratos 📑",
        "name": "Contract Craft AI",
        "icon": "fa-solid fa-file-signature",
        "tagline": "Automação de Contratos Legais, Modelos Dinâmicos & Assinatura Digital",
        "features": [
            "Catálogo de Modelos Jurídicos",
            "Substituição Dinâmica de Variáveis",
            "Gestão de Clientes & Partes",
            "Exportação em Formato PDF & HTML",
            "Histórico & Registo de Assinaturas"
        ],
        "technologies": ["Python Flask", "Jinja2 Templates", "ReportLab / PDF Gen", "SQLite3", "Bootstrap & Custom CSS"]
    },
    {
        "id": 74,
        "number": "Projeto 74",
        "title": "Calculadora de Preços & Margens 💶",
        "name": "Price Master AI",
        "icon": "fa-solid fa-calculator",
        "tagline": "Simulação de Custos, Margem de Lucro, Cálculo de IVA & Exportação",
        "features": [
            "Cálculo de Custos Diretos e Indiretos",
            "Definição de Margem de Lucro Alvo",
            "Aplicação Automática de IVA & Descontos",
            "Preço Final Recomendado & Benefício",
            "Relatórios de Rentabilidade em CSV"
        ],
        "technologies": ["Python", "Flask", "SQLite3 Data Ledger", "Chart.js", "Vanilla JS Real-time Engine"]
    },
    {
        "id": 75,
        "number": "Projeto 75",
        "title": "Sistema de Comissões & Vendas 💰",
        "name": "Comissões Pro AI",
        "icon": "fa-solid fa-money-bill-trend-up",
        "tagline": "Gestão de Vendedores, Cálculo de Comissões, Hierarquias & Rankings",
        "features": [
            "Registo de Equipa de Vendedores",
            "Registo de Vendas por Período",
            "Cálculo de Escalões de Percentagem",
            "Tabela de Classificação & Ranking de Desempenho",
            "Relatórios de Pagamento de Comissões"
        ],
        "technologies": ["Python Flask", "SQLite3", "CSS Grid Layout", "JavaScript ES6", "FontAwesome"]
    },
    {
        "id": 76,
        "number": "Projeto 76",
        "title": "Gerador de Leads & Landing Page 🚀",
        "name": "Lead Pulse AI",
        "icon": "fa-solid fa-rocket",
        "tagline": "Captura de Leads, Formulários Inteligentes & Funil de Conversão",
        "features": [
            "Landing Page de Alta Conversão",
            "Formulários Dinâmicos de Captura",
            "Gestão de Etapas de Lead (Funil)",
            "Acompanhamento & Automação de E-mails",
            "Dashboard de Taxa de Conversão"
        ],
        "technologies": ["Python", "Flask REST API", "SQLite3", "CSS Glassmorphism", "ChartJS Visuals"]
    },
    {
        "id": 77,
        "number": "Projeto 77",
        "title": "Email Marketing SaaS 📧",
        "name": "Mail Craft AI",
        "icon": "fa-solid fa-envelope-open-text",
        "tagline": "Plataforma de E-mail Marketing, Listas de Distribuição & Campanhas",
        "features": [
            "Gestão de Subscritores & Etiquetas",
            "Listas Segmentadas por Perfil",
            "Disparo & Agendamento de Campanhas",
            "Catálogo de Modelos Responsivos",
            "Métricas de Abertura & CTR"
        ],
        "technologies": ["Python Flask", "SQLite Database", "CSS Variables (Coral & Cyan)", "JavaScript Engine"]
    },
    {
        "id": 78,
        "number": "Projeto 78",
        "title": "Sistema de Newsletter Editorial 📰",
        "name": "Subscribed AI",
        "icon": "fa-solid fa-newspaper",
        "tagline": "Publicação Editorial, Níveis de Leitor, Redator Visual & Cronologia",
        "features": [
            "Redator Visual em 3 Painéis + Pré-visualização",
            "Subscritores por Níveis (Gratuito, Premium, VIP)",
            "Linha do Tempo Cronológica de Edições",
            "Tabelas Editoriais com Avatares",
            "Relatórios de Entregabilidade & Exportação"
        ],
        "technologies": ["Python 3.11", "Flask", "SQLite3", "Google Fonts Playfair Display", "Sidebar UI Design"]
    },
    {
        "id": 79,
        "number": "Projeto 79",
        "title": "Web Analytics & Métricas 📈",
        "name": "Pulse Analytics AI",
        "icon": "fa-solid fa-chart-line",
        "tagline": "Monitorização de Tráfego Web em Tempo Real & Métricas de Audiência",
        "features": [
            "Indicador Ativo de Visitantes Online em Direto",
            "Gráficos Temporais SVG de Sessões",
            "Distribuição Geográfica por Países",
            "Desempenho por URL Path & Dispositivos",
            "Exportação Auditável CSV & JSON"
        ],
        "technologies": ["Python Flask", "SQLite3 Data Warehouse", "SVG Chart Engine", "Dark Cyber Glass UI", "Vanilla JS"]
    },
    {
        "id": 80,
        "number": "Projeto 80",
        "title": "Heatmap Web & Analytics de Comportamento 🔥",
        "name": "Hot Trace AI",
        "icon": "fa-solid fa-fire",
        "tagline": "Mapas de Calor Espaciais, Profundidade de Scroll & Zonas Quentes",
        "features": [
            "Mapa Espacial de Coordenadas de Clique (X/Y)",
            "Profundidade de Scroll (25%, 50%, 75%, 100%)",
            "Matriz de Zonas Quentes (Hotspot Score)",
            "Gravações de Sessões de Utilizadores",
            "Canvas Térmico Interativo com Camada Sobreposta"
        ],
        "technologies": ["Python Flask", "SQLite3 Spatial Store", "Thermal CSS Glow Canvas", "JetBrains Mono Font", "REST API"]
    }
]

def get_projects():
    return PROJECTS_DATA
