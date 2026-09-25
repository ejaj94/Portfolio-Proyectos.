# Proyecto 114 - Sistema de Automatizaciones ⚡
**AutoFlow OS** — Mini Plataforma Full-Stack de Automações, Triggers, Ações & Workflows em Tempo Real

---

## 🌟 Funcionalidades Principais

1. **Triggers (Disparadores de Eventos)**:
   - Captura de eventos assíncronos: pagamentos Stripe, webhooks HTTP de entrada, novos emails Gmail e agendadores temporizados (Cron).
   - Armazenamento de esquemas de payload JSON de exemplo para inspeção.

2. **Acciones (Executores de Tarefas)**:
   - Despacho automático de notificações no Slack (canais ou DMs) e Discord.
   - Envio de emails transacionais, gravação de linhas em folhas de cálculo Google Sheets e processamento de texto com modelos de IA.

3. **Flujos (Pipelines de Automatização)**:
   - Construtor visual de fluxos conectando `[Trigger] -> [Condição de Filtro] -> [Ação]`.
   - Modos de controlo: ativação/pausa de fluxo, execução sob demanda ("Executar Agora") e contadores de execuções com taxa de sucesso.

4. **Condiciones (Lógica IF-THEN & Filtros)**:
   - Motor de regras inteligente com operadores numéricos e de texto (`>`, `>=`, `<`, `<=`, `==`, `!=`, `contains`).
   - Simulador interativo em tempo real para testar regras contra payloads JSON antes de disparar automações de produção.

5. **Historial (Logs de Auditoria)**:
   - Registo detalhado de cada disparo com latência em milissegundos, carimbo de data/hora e classificação de estado (`Sucesso`, `Filtrado`, `Erro`).
   - Inspetor modal de payloads JSON de entrada e saída.

6. **Integraciones**:
   - Gestão de conexões com serviços externos (Stripe, Slack, Gmail, Google Sheets, Discord, OpenAI, Webhooks genéricos).
   - Teste instantâneo de conexão e validação de tokens.

7. **Dashboard & Métricas**:
   - KPIs de automações ativas, volume de execuções orquestradas, taxa de sucesso global e latência média.
   - Gráficos em Chart.js com distribuição de estados e monitorização de tráfego por hora.

---

## 🛠️ Stack Tecnológica

- **Backend**: Python 3 / Flask
- **Motor de Regras**: AutoFlow Engine com validação condicional dinâmica
- **Base de Dados**: SQLite3 com integridade referencial
- **Frontend**: HTML5, Tailwind CSS, FontAwesome 6, Chart.js
- **Design System**: Electric Violet (`#8b5cf6`) & Laser Cyan (`#06b6d4`) com estética dark moderna inspirada em n8n e Zapier

---

## 🚀 Como Executar

```bash
# Navegar até à pasta do projeto
cd "Proyecto 114 - Sistema de Automatizaciones"

# Iniciar o servidor Flask
python app.py
```

Aceda através do browser: `http://localhost:6967`
