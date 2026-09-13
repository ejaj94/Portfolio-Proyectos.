import os
import json

PROJECTS_DATA = [
    {
        "id": 84,
        "number": "Proyecto 84",
        "title": "Crowdfunding & Mecenato SaaS",
        "name": "FundCraft AI",
        "icon": "fa-solid fa-hand-holding-heart",
        "tagline": "Plataforma de Financiamento Coletivo, Angariação de Fundos & Recompensas",
        "features": [
            "Gestão de Campanhas de Crowdfunding",
            "Níveis de Recompensas & Donativos",
            "Barra de Progresso & Metas Financeiras",
            "Painel de Apoiadores (Backers)",
            "Disparo Automático de Notificações"
        ],
        "technologies": ["Python Flask", "SQLite3", "JavaScript ES6", "HTML5 & CSS Grid", "FontAwesome 6"],
        "gradient": "linear-gradient(135deg, #1e3a8a, #0284c7)"
    },
    {
        "id": 85,
        "number": "Proyecto 85",
        "title": "Sistema de Donações ❤️",
        "name": "Donatio SaaS",
        "icon": "fa-solid fa-heart",
        "tagline": "Gestão de Causas Sociais, Doadores Rcorrentes & Objetivos de Impacto",
        "features": [
            "Registo & Gestão de Doadores VIP",
            "Campanhas de Arrecadação com Metas",
            "Histórico Transacional & Recibos",
            "Dashboard de Progresso Financeiro",
            "Filtros de Causas & Categorias"
        ],
        "technologies": ["Python 3.11", "Flask RESTful", "SQLite Database", "CSS Flexbox & Variables", "Animate.css"],
        "gradient": "linear-gradient(135deg, #0284c7, #38bdf8)"
    },
    {
        "id": 86,
        "number": "Proyecto 86",
        "title": "Generador de Contratos 📑",
        "name": "ContractCraft AI",
        "icon": "fa-solid fa-file-signature",
        "tagline": "Automação de Contratos Legais, Modelos Dinâmicos & Assinatura Digital",
        "features": [
            "Catálogo de Plantilhas Jurídicas",
            "Substituição Dinâmica de Variáveis",
            "Gestão de Clientes & Partes",
            "Exportação em Formato PDF & HTML",
            "Histórico & Registo de Assinaturas"
        ],
        "technologies": ["Python Flask", "Jinja2 Templates", "ReportLab / PDF Gen", "SQLite3", "Bootstrap & Custom CSS"],
        "gradient": "linear-gradient(135deg, #1d4ed8, #60a5fa)"
    },
    {
        "id": 87,
        "number": "Proyecto 87",
        "title": "Calculadora de Preços & Margens 💶",
        "name": "PriceMaster AI",
        "icon": "fa-solid fa-calculator",
        "tagline": "Simulação de Custos, Margem de Lucro, Cálculo de IVA & Exportação",
        "features": [
            "Cálculo de Custos Diretos e Indiretos",
            "Definição de Margem de Lucro Alvo",
            "Aplicação Automática de IVA & Descontos",
            "Preço Final Recomendado & Benefício",
            "Relatórios de Rentabilidade em CSV"
        ],
        "technologies": ["Python", "Flask", "SQLite3 Data Ledger", "Chart.js", "Vanilla JS Real-time Engine"],
        "gradient": "linear-gradient(135deg, #2563eb, #93c5fd)"
    },
    {
        "id": 88,
        "number": "Proyecto 88",
        "title": "Sistema de Comissões & Vendas 💰",
        "name": "ComissõesPro AI",
        "icon": "fa-solid fa-money-bill-trend-up",
        "tagline": "Gestão de Vendedores, Cálculo de Comissões, Hierarquias & Rankings",
        "features": [
            "Cadastro de Equipa de Vendedores",
            "Registo de Vendas por Período",
            "Cálculo de Escalões de Percentagem",
            "Leaderboard & Ranking de Performance",
            "Relatórios de Pagamento de Comissões"
        ],
        "technologies": ["Python Flask", "SQLite3", "CSS Grid Layout", "JavaScript ES6", "FontAwesome"],
        "gradient": "linear-gradient(135deg, #1e40af, #3b82f6)"
    },
    {
        "id": 89,
        "number": "Proyecto 89",
        "title": "Lead Generator & Landing Page 🚀",
        "name": "LeadPulse AI",
        "icon": "fa-solid fa-rocket",
        "tagline": "Captura de Leads, Formulários Inteligentes & Funil de Conversão",
        "features": [
            "Landing Page de Alta Conversão",
            "Formulários Dinâmicos de Captura",
            "Gestão de Estados de Lead (Funil)",
            "Seguimento & Automação de E-mails",
            "Dashboard de Taxa de Conversão"
        ],
        "technologies": ["Python", "Flask REST API", "SQLite3", "CSS Glassmorphism", "ChartJS Visuals"],
        "gradient": "linear-gradient(135deg, #0369a1, #38bdf8)"
    },
    {
        "id": 90,
        "number": "Proyecto 90",
        "title": "Email Marketing SaaS 📧",
        "name": "MailCraft AI",
        "icon": "fa-solid fa-envelope-open-text",
        "tagline": "Plataforma de E-mail Marketing, Listas de Distribuição & Campanhas",
        "features": [
            "Gestão de Subscritores & Tags",
            "Listas Segmentadas por Perfil",
            "Disparo & Agendamento de Campanhas",
            "Catálogo de Modelos Responsivos",
            "Métricas de Abertura & CTR"
        ],
        "technologies": ["Python Flask", "SQLite Database", "CSS Variables (Coral & Cyan)", "JavaScript Engine"],
        "gradient": "linear-gradient(135deg, #1e3a8a, #06b6d4)"
    },
    {
        "id": 91,
        "number": "Proyecto 91",
        "title": "Sistema de Newsletter Editorial 📰",
        "name": "Subscribed AI",
        "icon": "fa-solid fa-newspaper",
        "tagline": "Publicação Editorial, Tiers de Leitor, Redator Visual & Timeline",
        "features": [
            "Redator Visual em 3 Painéis + Preview",
            "Subscritores por Tiers (Gratuito, Premium, VIP)",
            "Linha do Tempo Cronológica de Edições",
            "Editorial Ledger Tables com Avatars",
            "Relatórios de Entregabilidade & Export"
        ],
        "technologies": ["Python 3.11", "Flask", "SQLite3", "Google Fonts Playfair Display", "Sidebar UI Design"],
        "gradient": "linear-gradient(135deg, #1b4332, #c85a32)"
    },
    {
        "id": 92,
        "number": "Proyecto 92",
        "title": "Web Analytics & Métricas 📈",
        "name": "PulseAnalytics AI",
        "icon": "fa-solid fa-chart-line",
        "tagline": "Monitorização de Tráfego Web em Tempo Real & Métricas de Audiência",
        "features": [
            "Ticker Ativo de Visitantes Online em Direto",
            "Gráficos Temporais SVG de Sessões",
            "Distribuição Geográfica por Países",
            "Desempenho por URL Path & Dispositivos",
            "Exportação Auditável CSV & JSON"
        ],
        "technologies": ["Python Flask", "SQLite3 Data Warehouse", "SVG Chart Engine", "Dark Cyber Glass UI", "Vanilla JS"],
        "gradient": "linear-gradient(135deg, #090d16, #06b6d4)"
    },
    {
        "id": 93,
        "number": "Proyecto 93",
        "title": "Heatmap Web & Behavior Analytics 🔥",
        "name": "HotTrace AI",
        "icon": "fa-solid fa-fire",
        "tagline": "Mapas de Calor Espaciais, Profundidade de Scroll & Zonas Calientes",
        "features": [
            "Mapa Espacial de Coordenadas de Clique (X/Y)",
            "Profundidade de Scroll (25%, 50%, 75%, 100%)",
            "Matriz de Zonas Calientes (Hotspot Score)",
            "Gravações de Sessões de Utilizadores",
            "Canvas Térmico Interativo com Overlay"
        ],
        "technologies": ["Python Flask", "SQLite3 Spatial Store", "Thermal CSS Glow Canvas", "JetBrains Mono Font", "REST API"],
        "gradient": "linear-gradient(135deg, #0c0a09, #ef4444)"
    }
]

def get_projects():
    return PROJECTS_DATA
