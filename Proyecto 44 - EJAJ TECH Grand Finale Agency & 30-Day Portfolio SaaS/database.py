import os
import sqlite3

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'agency.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Projects Table (29-day challenge)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day INTEGER UNIQUE NOT NULL,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            short_desc TEXT NOT NULL,
            full_desc TEXT NOT NULL,
            tech_stack TEXT NOT NULL,
            features TEXT NOT NULL,
            image_url TEXT NOT NULL,
            port INTEGER,
            script_pt TEXT NOT NULL,
            views INTEGER DEFAULT 0
        )
    ''')

    # Services Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            icon TEXT NOT NULL,
            title TEXT NOT NULL,
            tagline TEXT NOT NULL,
            description TEXT NOT NULL,
            deliverables TEXT NOT NULL,
            badge TEXT NOT NULL
        )
    ''')

    # Contacts & Quotes Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            service TEXT NOT NULL,
            budget TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()

    # Seed Projects if empty
    cursor.execute('SELECT COUNT(*) FROM projects')
    if cursor.fetchone()[0] == 0:
        seed_projects(cursor)

    # Seed Services if empty
    cursor.execute('SELECT COUNT(*) FROM services')
    if cursor.fetchone()[0] == 0:
        seed_services(cursor)

    conn.commit()
    conn.close()

def seed_services(cursor):
    services = [
        (
            'bi-code-slash',
            'Desenvolvimento Web',
            'Sistemas Web Modernos e Responsivos',
            'Criamos aplicações web personalizadas de alta velocidade com arquiteturas escaláveis em Python, Flask, Node.js e Tailwind CSS, otimizadas para motores de busca e conversão.',
            'Landings de alta conversão, Portais empresariais, PWAs responsivos, SEO técnico avançado',
            'Mais Requisitado'
        ),
        (
            'bi-phone-vibrate',
            'Aplicações Mobile & Desktop',
            'Experiências Nativas e Multiplataforma',
            'Desenvolvemos aplicações com interfaces fluidas e intuitivas adaptadas para iOS, Android e ambientes de trabalho empresariais, integradas com APIs em tempo real.',
            'Apps iOS/Android, Dashboards interativos, Notificações push, Modo offline inteligente',
            'Alta Performance'
        ),
        (
            'bi-building-gear',
            'Sistemas Empresariais & ERP',
            'Gestão Operacional de Elite',
            'Plataformas customizadas de gestão de stocks, faturação homologada, RH, CRM e automação de fluxos financeiros para empresas em expansão.',
            'Gestão de inventários, Faturação eletrónica, Relatórios telemétricos, Controlo de acessos',
            'Enterprise'
        ),
        (
            'bi-cpu-fill',
            'Automatizações & Inteligência Artificial',
            'Otimização de Processos Repetitivos',
            'Implementação de robôs de scraping, conectores de API, chatbots inteligentes e fluxos automatizados que poupam centenas de horas de trabalho operacional.',
            'Web scraping avançado, Integrações de APIs, Automação de marketing, Bots de apoio ao cliente',
            'Inovação IA'
        ),
        (
            'bi-cart-check-fill',
            'E-Commerce & Plataformas SaaS',
            'Lojas Online e Soluções Multi-Vendedor',
            'Construção de ecossistemas completos de venda online com integração de pagamentos MB WAY, Stripe, gateways bancárias e dashboards analíticos de faturação.',
            'Lojas digitais personalizadas, Marketplaces C2C/B2C, Integração MB WAY/Multibanco, Checkout em 1-clique',
            'Pronto a Faturar'
        )
    ]
    cursor.executemany('''
        INSERT INTO services (icon, title, tagline, description, deliverables, badge)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', services)

def seed_projects(cursor):
    projects = [
        (
            1,
            'Fast Food Burger & Crunch',
            'E-commerce & Restauração',
            'Plataforma interativa de pedidos e menu digital para hamburguerias gourmet.',
            'Sistema completo de gestão de menus, carrinho de compras express, personalização de hambúrgueres e acompanhamento de entregas em tempo real.',
            'Python, Flask, SQLite, Bootstrap 5, JS',
            'Menu Interativo, Personalização de Ingredientes, Carrinho Express, Checkout Rápido',
            'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80',
            5000,
            'Procura uma solução de pedidos para o seu restaurante com visual moderno? Conheça o Fast Food Burger & Crunch da EJAJ TECH! Personalize hambúrgueres e faça gerir pedidos num instante. Envie a palavra AJUDA para uma assessoria gratuita!'
        ),
        (
            2,
            'Barbearia Executive Studio',
            'Web & Reservas',
            'Portal premium de agendamento online para barbearias de luxo.',
            'Interface elegante em tom dark gold com seleção de barbeiro, escolha de horário, catálogo de serviços e confirmação automática via SMS/Email.',
            'Python, Flask, SQLite, CSS Custom, JS',
            'Agendamento Online, Seleção de Profissional, Catálogo de Serviços, Gestão de Clientes',
            'https://images.unsplash.com/photo-1503951914875-452162b0f3f1?auto=format&fit=crop&w=800&q=80',
            5100,
            'Quer automatizar a agenda da sua barbearia com estilo executivo? O Executive Studio permite aos seus clientes agendarem em segundos. Fale connosco e envie a palavra AJUDA para transformar o seu negócio!'
        ),
        (
            3,
            'Restaurante Gourmet Elegante',
            'Web & Gastronomia',
            'Website de luxo para restauração com reserva de mesas e menu degustação.',
            'Design refinado com reservas de mesas por sala, carta de vinhos interativa, apresentações em vídeo e gestão de experiência do cliente.',
            'Python, Flask, SQLite, CSS3, JS',
            'Reserva de Mesas, Carta de Vinhos Digital, Galeria de Pratos, Avaliações de Clientes',
            'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80',
            5200,
            'Eleve a presença online do seu restaurante de topo! Apresente menus degustação e gira reservas com elegância. Envie a palavra AJUDA para agendar a sua consultoria gratuita com a EJAJ TECH.'
        ),
        (
            4,
            'App Móvil Gimnasio Fitness',
            'Aplicações & Saúde',
            'Aplicação web responsiva para acompanhamento de treinos e nutrição.',
            'Dashboard de atleta com rotinas personalizadas, cronómetro de descanso, gráfico de evolução de carga e calculadora de macros diários.',
            'Python, Flask, Chart.js, SQLite, Mobile First UI',
            'Planos de Treino, Cronómetro de Séries, Gráficos de Progresso, Calculadora Nutricional',
            'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80',
            5300,
            'Revolucione a experiência dos seus alunos no ginásio! A nossa App Fitness oferece planos de treino e nutrição no telemóvel. Quer uma app assim? Envie a palavra AJUDA!'
        ),
        (
            5,
            'Portal Inmobiliario Lujo Vale do Lobo',
            'Imobiliário & Luxo',
            'Portal imobiliário de elite para propriedades exclusivas no Algarve.',
            'Filtros de pesquisa por zona e caraterísticas de luxo, visitas virtuais, agendamento de visita presencial e calculadora de investimento imobiliário.',
            'Python, Flask, SQLite, Lightgallery.js, CSS Grid',
            'Filtro Avançado de Imóveis, Galeria HD, Formulário de Agendamento, Calculadora Hipotecária',
            'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80',
            5400,
            'Apresente propriedades de luxo com um portal de alto impacto visual! O portal Vale do Lobo oferece galerias HD e filtros precisos. Precisa de apoio? Envie a palavra AJUDA para a EJAJ TECH!'
        ),
        (
            6,
            'Stand Concessionário Autos Lujo Supercars',
            'Automóvel & Luxo',
            'Showroom digital para venda e aluguer de viaturas desportivas e de prestígio.',
            'Ficha técnica detalhada com áudio de motor, simulador de financiamento automóvel, reserva de test-drive e comparador de modelos.',
            'Python, Flask, SQLite, FontAwesome, JS',
            'Showroom 360°, Simulador de Crédito, Agendamento Test-Drive, Especificações Técnicas',
            'https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=800&q=80',
            5500,
            'Venda supercarros com um showroom digital à altura dos seus veículos! Ficha técnica interativa e simulação de crédito imediata. Fale connosco e envie a palavra AJUDA!'
        ),
        (
            7,
            'Clínica Dentária Estética Quinta do Lago',
            'Saúde & Estética',
            'Plataforma médica para marcações de estomatologia e medicina estética.',
            'Triagem virtual de sintomas, apresentação da equipa médica, simulador de sorriso antes/depois e marcação de consultas prioritárias.',
            'Python, Flask, SQLite, Custom UI, JS',
            'Triagem Virtual, Marcação de Consulta, Galeria Antes/Depois, Perfil do Corpo Clínico',
            'https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=800&q=80',
            5600,
            'Transmita confiança máxima aos seus pacientes! A nossa plataforma médica simplifica agendamentos e demonstra tratamentos. Envie a palavra AJUDA para desenvolver a sua clínica digital!'
        ),
        (
            8,
            'Marina de Albufeira Luxury Resort Hotel',
            'Hotelaria & Turismo',
            'Sistema de reservas de suites e alojamento resort com motor de reservas.',
            'Seleção de datas, verificação de disponibilidade em tempo real, pacotes VIP com experiências de iate e navegação intuitiva.',
            'Python, Flask, SQLite, Datepicker.js, CSS3',
            'Motor de Reservas, Calendário de Disponibilidade, Pacotes VIP, Avaliações de Hóspedes',
            'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80',
            5700,
            'Aumente as reservas diretas do seu hotel ou alojamento de luxo! Motor de reservas rápido sem comissões de terceiros. Envie a palavra AJUDA para saber mais com a EJAJ TECH!'
        ),
        (
            9,
            'Sistema de Reservas y Gestión SaaS',
            'SaaS & Gestão',
            'Plataforma SaaS multi-inquilino para gestão de serviços e agendamentos.',
            'Painel administrativo para prestadores de serviços, bloqueio de horários, emissão de comprovativos e lembretes automáticos.',
            'Python, Flask, SQLite, Bootstrap 5, Chart.js',
            'Multi-tenant, Gestão de Calendário, Lembretes Automáticos, Relatórios de Receita',
            'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=800&q=80',
            5710,
            'Gerencie compromissos e equipas sem complicações! O nosso SaaS de Reservas otimiza a sua agenda diária. Quer uma plataforma SaaS? Envie a palavra AJUDA para uma mentoria gratuita!'
        ),
        (
            10,
            'CRM de Ventas y Gestión de Leads SaaS',
            'SaaS & Vendas',
            'Sistema CRM com funil Kanban para acompanhamento de equipas comerciais.',
            'Arrastar e largar cartões de potenciais clientes, pipeline de vendas por fases, métricas de conversão e histórico de comunicações.',
            'Python, Flask, Dragula.js, SQLite, Chart.js',
            'Funil Kanban, Gestão de Oportunidades, Histórico de Contacto, Métricas Comerciais',
            'https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=800&q=80',
            5720,
            'Feche mais negócios e controle o seu funil de vendas com o CRM da EJAJ TECH! Arraste oportunidades no pipeline Kanban e meça resultados. Envie a palavra AJUDA!'
        ),
        (
            11,
            'Sistema de Inventario Enterprise Peças Auto',
            'Enterprise & Peças',
            'Software de gestão de stock e armazenamento para distribuição automóvel.',
            'Controlo de referências OEM, alertas de stock mínimo, leitor de código de barras e gestão de localização no armazém.',
            'Python, Flask, SQLite, DataTables, JS',
            'Códigos OEM, Alerta de Stock Mínimo, Controlo de Armazém, Faturação de Saída',
            'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=800&q=80',
            5730,
            'Elimine erros de stock no seu armazém de peças automóveis! Controlo total de referências e código de barras. Contacte a EJAJ TECH enviando a palavra AJUDA!'
        ),
        (
            12,
            'Sistema de Facturación Profesional SaaS',
            'SaaS & Finanças',
            'Plataforma de emissão de orçamentos e faturas em formato PDF oficial.',
            'Cálculo automático de IVA (23%), retenção na fonte, geração instantânea de PDF e envio direto por e-mail ao cliente.',
            'Python, Flask, ReportLab, SQLite, Custom CSS',
            'Emissão de PDF, Cálculo de IVA 23%, Envio por E-mail, Relatório Mensal de Faturação',
            'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=800&q=80',
            5740,
            'Emita faturas e orçamentos profissionais em segundos! Formatos elegantes em PDF e taxas de IVA configuradas. Precisa de automatizar a sua faturação? Envie a palavra AJUDA!'
        ),
        (
            13,
            'EJAJ TECH Analytics Dashboard SaaS',
            'Telemetria & Analytics',
            'Painel de controlo telemétrico com gráficos em tempo real e métricas de servidores.',
            'Monitorização de CPU, memória RAM, taxa de conversão de tráfego, mapa de calor de utilizadores e alertas de inatividade.',
            'Python, Flask, Chart.js, WebSockets, SQLite',
            'Métricas em Tempo Real, Gráficos Interativos, Alertas de Servidor, Exportação de Dados',
            'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80',
            5800,
            'Tome decisões baseadas em dados em tempo real! O nosso Analytics Dashboard monitoriza servidores e métricas de negócio. Fale com a EJAJ TECH enviando a palavra AJUDA!'
        ),
        (
            14,
            'Gestor de Gastos Veterinaria de Luxo SaaS',
            'SaaS & Clínica',
            'Sistema financeiro especializado para hospitais veterinários e pet shops.',
            'Categorização de despesas médicas, fornecedores de medicamentos, controlo de fluxo de caixa diário e relatórios de rentabilidade.',
            'Python, Flask, SQLite, Chart.js, Bootstrap',
            'Fluxo de Caixa, Categorização de Despesas, Gestão de Fornecedores, Relatórios Anuais',
            'https://images.unsplash.com/photo-1532938911079-1b06ac7ceec7?auto=format&fit=crop&w=800&q=80',
            5880,
            'Mantenha as finanças da sua clínica veterinária sob controlo rigoroso! Gestão de fornecedores e lucros num só local. Envie a palavra AJUDA para uma consultoria gratuita!'
        ),
        (
            15,
            'Gestor de Tarefas Social Media SaaS',
            'SaaS & Produtividade',
            'Plataforma de gestão de conteúdos e publicações para agências de marketing.',
            'Calendário de conteúdos interativo, estados de aprovação de cliente, banco de hashtags e atribuição de equipa.',
            'Python, Flask, FullCalendar.js, SQLite',
            'Calendário Editorial, Banco de Hashtags, Fluxo de Aprovação, Atribuição de Tarefas',
            'https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?auto=format&fit=crop&w=800&q=80',
            5980,
            'Organize as suas campanhas de redes sociais como uma agência de topo! Planeie posts e aprove conteúdos com clientes. Envie a palavra AJUDA para impulsionar a sua agência!'
        ),
        (
            16,
            'Taller Mecánico Supercars SaaS',
            'Enterprise & Automóvel',
            'Gestão integral de ordens de reparação para oficinas mecânicas de alta performance.',
            'Check-in de viatura com fotos de inspeção, orçamentação de peças, histórico do veículo por matrícula e aviso de pronto a recolher.',
            'Python, Flask, SQLite, Mobile Camera Upload',
            'Ordens de Trabalho, Inspeção Fotográfica, Histórico por Matrícula, SMS de Notificação',
            'https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=800&q=80',
            5990,
            'Gerencie a sua oficina mecânica de supercarros com precisão digital! Ordens de trabalho e avisos automáticos para os clientes. Envie a palavra AJUDA para saber como implementar!'
        ),
        (
            17,
            'Gestión Clínica Veterinaria SaaS',
            'SaaS & Saúde',
            'Ficha clínica digital de animais de estimação com histórico de vacinação e consultas.',
            'Registo de vacinas, microchips, agendamento de cirurgias, emissão de receitas médicas veterinárias e dados do tutor.',
            'Python, Flask, SQLite, Custom CSS, JS',
            'Ficha Clínica Animal, Lembrete de Vacinas, Receitas Médicas, Histórico de Cirurgias',
            'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?auto=format&fit=crop&w=800&q=80',
            6050,
            'Digitalize as fichas clínicas dos seus pacientes de quatro patas! Notificações de vacinas e receitas num clique. Fale com a EJAJ TECH enviando a palavra AJUDA!'
        ),
        (
            18,
            'Plataforma Academia Educativa SaaS',
            'EdTech & E-Learning',
            'LMS corporativo e plataforma de cursos online com reprodução de vídeos HD.',
            'Módulos de aulas, questionários de avaliação, acompanhamento de percentagem de progresso e certificados digitais automáticos.',
            'Python, Flask, Video.js, SQLite, Custom UI',
            'Player de Vídeo HD, Certificados PDF, Quizzes Interativos, Progresso do Aluno',
            'https://images.unsplash.com/photo-1501504905252-473c47e087f8?auto=format&fit=crop&w=800&q=80',
            6100,
            'Crie a sua própria academia online de formação profissional! Cursos em vídeo HD e emissão de certificados automáticos. Envie a palavra AJUDA para iniciar o seu projeto!'
        ),
        (
            19,
            'Gestor de Propriedades Inmobiliarias SaaS',
            'SaaS & Imobiliário',
            'Software para gestão de arrendamentos, contratos e cobranças de senhorios.',
            'Controlo de rendas recebidas, emissão de recibos, contratos de arrendamento e alertas de pagamentos em atraso.',
            'Python, Flask, SQLite, DataTables, JS',
            'Gestão de Rendas, Alertas de Incumprimento, Emissão de Recibos, Ficha do Inquilino',
            'https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=800&q=80',
            6150,
            'Gerencie o seu portfólio de imóveis arrendados sem stress! Controlo de cobranças e contratos organizados. Quer uma solução assim? Envie a palavra AJUDA!'
        ),
        (
            20,
            'Sistema de Tickets y Soporte Técnico SaaS',
            'Enterprise & Suporte',
            'Helpdesk para gestão de incidentes tecnológicos com SLA e prioridades.',
            'Abertura de tickets por cliente, atribuição a técnicos, indicador visual de urgência e estatísticas de tempo médio de resposta.',
            'Python, Flask, SQLite, Bootstrap 5, JS',
            'Gestão de Tickets, SLA em Tempo Real, Atribuição por Área, Histórico de Resolução',
            'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=800&q=80',
            6200,
            'Preste um suporte ao cliente impecável! O nosso Helpdesk com SLAs garante respostas rápidas aos problemas da sua equipa. Envie a palavra AJUDA para a EJAJ TECH!'
        ),
        (
            21,
            'CONNECT-CHAT Web SaaS',
            'Comunicação & Real-Time',
            'Plataforma de mensagens instantâneas e videochamadas HD estilo Messenger.',
            'Salas de conversação, chamadas de voz e vídeo encriptadas no navegador, barra de reações com emojis flutuantes e estado de presença.',
            'Python, Flask, WebRTC, Socket.IO, SQLite',
            'Videochamadas HD, Chat em Tempo Real, Reações com Emojis, Indicador de Presença',
            'https://images.unsplash.com/photo-1611606063065-ee7946f0787a?auto=format&fit=crop&w=800&q=80',
            6280,
            'Quer a sua própria plataforma de mensagens corporativa com videochamadas HD encriptadas? Conheça o CONNECT-CHAT SaaS da EJAJ TECH! Envie a palavra AJUDA para o seu projeto!'
        ),
        (
            22,
            'Acortador de Links y Analítica Telemétrica SaaS',
            'Telemetria & Marketing',
            'Plataforma de encurtamento de URLs com rastreio de geolocalização e cliques.',
            'Geração de links curtos personalizados, códigos QR de alta resolução, gráficos de cliques por país e sistema de domínios customizados.',
            'Python, Flask, QRCode.py, SQLite, Chart.js',
            'Encurtador Personalizado, Códigos QR, Telemétrica por País, Gráficos de Tráfego',
            'https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80',
            6300,
            'Encurte links e meça o alcance exato das suas campanhas de marketing! Códigos QR e estatísticas geográficas completas. Envie a palavra AJUDA para desenvolver a sua ferramenta!'
        ),
        (
            23,
            'Planificador de Viajes e Itinerarios SaaS',
            'Turismo & IA',
            'Gerador inteligente de roteiros de férias personalizados por destino.',
            'Seleção de cidade, número de dias e orçamento, gerando recomendações de pontos turísticos, restaurantes e estimativa de custos.',
            'Python, Flask, Leaflet.js, SQLite, API Weather',
            'Roteiros Automáticos, Mapas Interativos, Estimativa de Custos, Recomendações Locais',
            'https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=800&q=80',
            6350,
            'Planeie itinerários de viagem inesquecíveis em poucos cliques! Algoritmo inteligente que recomenda os melhores locais. Envie a palavra AJUDA para construir a sua app!'
        ),
        (
            24,
            'Tienda Online E-Commerce Completo SaaS',
            'E-commerce & Retalho',
            'Loja virtual de vestuário e tecnologia com integração de pagamentos e envios.',
            'Catálogo com variações de tamanho e cor, favoritos, carrinho deslizante e pagamento rápido com MB WAY e referência Multibanco.',
            'Python, Flask, SQLite, Custom E-commerce UI',
            'Carrinho Lateral, Variações de Produto, Pagamentos MB WAY, Gestão de Portes',
            'https://images.unsplash.com/photo-1472851294608-062f824d29cc?auto=format&fit=crop&w=800&q=80',
            6400,
            'Venda os seus produtos online 24 horas por dia com uma loja virtual de alto rendimento! Integração total MB WAY e CTT. Fale connosco e envie a palavra AJUDA!'
        ),
        (
            25,
            'App de Hábitos y Neuro-Performance SaaS',
            'Produtividade & Saúde',
            'Plataforma de otimização de rotinas diárias com rastreador de hábitos e streaks.',
            'Rastreio diário de metas, sequências ininterruptas (streaks), vista de calendário mensal e estatísticas visuais de neuro-performance.',
            'Python, Flask, SQLite, Canvas Confetti, Chart.js',
            'Rastreio de Streaks, Calendário Visual, Estatísticas de Foco, Sistema de Recompensas',
            'https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?auto=format&fit=crop&w=800&q=80',
            6450,
            'Alcance a máxima produtividade e disciplina diária! Rastreie hábitos e visualize o seu progresso com gráficos intuitivos. Envie a palavra AJUDA para a EJAJ TECH!'
        ),
        (
            26,
            'Generador de Posts y Social Media SaaS',
            'Marketing & Automação',
            'Ferramenta de criação de copys e hashtags personalizadas por rede social.',
            'Gerador inteligente de textos para Instagram, LinkedIn e Facebook, banco de hashtags otimizadas e agendador visual de conteúdos.',
            'Python, Flask, SQLite, Instagram Theme Palette',
            'Gerador de Copy, Seleção de Hashtags, Visualizador de Post, Calendário Semanal',
            'https://images.unsplash.com/photo-1611162616475-46b635cb6868?auto=format&fit=crop&w=800&q=80',
            6460,
            'Crie conteúdos envolventes para as suas redes sociais em segundos! Textos estratégicos e hashtags otimizadas. Quer automatizar o seu marketing? Envie a palavra AJUDA!'
        ),
        (
            27,
            'Sistema de Presupuestos y Gestor de Orçamentos SaaS',
            'Enterprise & Finanças',
            'Software profissional para elaboração de propostas comerciais de serviços.',
            'Cálculo de margem de lucro, catálogo de serviços por hora ou projeto, aplicação de taxas de IVA e exportação instantânea em PDF.',
            'Python, Flask, ReportLab PDF, SQLite',
            'Elaboração de Propostas, Exportação PDF Profissional, Controlo de Clientes, Cálculo Margem',
            'https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&w=800&q=80',
            6470,
            'Apresente orçamentos comerciais irresistíveis aos seus clientes! Formato PDF de nível empresarial com calculadoras de IVA. Envie a palavra AJUDA para implementar no seu negócio!'
        ),
        (
            28,
            'Delivery App LOGLEVE Plataforma de Entregas',
            'Logística & Entregas',
            'Sistema completo de distribuição de encomendas e estafetas locais.',
            'Acompanhamento de estado de entrega, atribuição ao estafeta, geolocalização da rota e comprovativo de entrega com assinatura digital.',
            'Python, Flask, Leaflet Maps, SQLite',
            'Rastreio de Entregas, Portal do Estafeta, Notificações SMS, Assinatura Digital',
            'https://images.unsplash.com/photo-1526367790999-0150786686a2?auto=format&fit=crop&w=800&q=80',
            6480,
            'Otimize a operação de entregas da sua frota ou restaurante com a plataforma LOGLEVE da EJAJ TECH! Rastreio de estafetas em tempo real. Fale connosco e envie a palavra AJUDA!'
        ),
        (
            29,
            'OLX-MARKETPLACE SaaS Mini Amazon',
            'E-commerce & Marketplace',
            'Plataforma de compra e venda multi-vendedor com a paleta oficial OLX.',
            'Catálogo C2C/B2C, portal de vendedor com métricas de anúncios, carrinho unificado, pagamentos MB WAY e acompanhamento de encomendas.',
            'Python, Flask, SQLite, OLX Custom Palette, JS',
            'Multi-Vendedor, MB WAY Checkout, Painel do Vendedor, Acompanhamento de Encomenda',
            'https://images.unsplash.com/photo-1472851294608-062f824d29cc?auto=format&fit=crop&w=800&q=80',
            6500,
            'Lance o seu próprio marketplace no estilo OLX e Amazon! Plataforma robusta multi-vendedor com pagamentos seguros MB WAY. Envie a palavra AJUDA para transformar a sua ideia em realidade!'
        )
    ]

    cursor.executemany('''
        INSERT INTO projects (day, title, category, short_desc, full_desc, tech_stack, features, image_url, port, script_pt)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', projects)

if __name__ == '__main__':
    init_db()
    print("[OK] Base de dados agency.db inicializada com sucesso para Proyecto 44 (EJAJ TECH Grand Finale)!")
