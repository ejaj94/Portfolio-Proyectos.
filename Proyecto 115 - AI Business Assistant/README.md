# Proyecto 115 - AI Business Assistant 🤖
**Nexa AI Enterprise Copilot** — Assistente Corporativo de Inteligência Artificial para Estratégia, Vendas, CRM & Decisão Executiva

---

## 🌟 Funcionalidades Principais

1. **Chat Copilot com Modos Especializados**:
   - Modos executivos dedicados: *Estratégia Empresarial*, *Vendas & Fecho B2B*, *Finanças & MRR*, *Suporte & Atendimento SLA*.
   - Respostas inteligentes com estrutura acionável, cálculo de tokens e sugestões de prompts de um clique.

2. **Clientes (CRM Inteligente)**:
   - Base de clientes com faturação mensal (MRR), setor de atividade e estado de ciclo de vida (`Lead`, `Em Negociação`, `Ativo`, `Risco Churn`).
   - Botão de **Diagnóstico IA** que analisa o perfil da conta e gera recomendações de retenção ou expansão.

3. **Resúmenes (Executive Summaries & Atas)**:
   - Síntese automática de atas de reunião, relatórios financeiros e transcrições com extração de itens de ação e análise de sentimento (`Positivo`, `Neutro`, `Requer Atenção`).

4. **Generación de Emails Comerciais**:
   - Redator corporativo por IA com ajuste de tom de voz (*Profissional*, *Persuasivo*, *Conciso*, *Empático*) e propósito (*Proposta Comercial*, *Follow-up*, *Cobrança Amigável*, *Apresentação*).
   - Botão de cópia imediata com um clique para a área de transferência.

5. **Análisis de Datos & Métricas Financeiras**:
   - Indicadores executivos de MRR ativo, valor médio por conta e volume de tokens processados.
   - Gráficos em Chart.js da composição da carteira de clientes e projeção de crescimento de receita, acompanhados de diagnósticos textuais de IA.

6. **Tareas (Action Tracker)**:
   - Gestão de entregáveis e compromissos operacionais por prioridade (*Alta*, *Média*, *Baixa*) e data limite, vinculados a contas de clientes.

7. **Historial de Auditoria**:
   - Linha temporal completa com todas as interações da IA, emails redigidos e tarefas concluídas com registo de tokens consumidos.

---

## 🛠️ Stack Tecnológica

- **Backend**: Python 3 / Flask
- **Motor de IA**: Nexa Neural Business Engine com lógica de síntese e diagnóstico contextual
- **Base de Dados**: SQLite3 com integridade referencial
- **Frontend**: HTML5, Tailwind CSS, FontAwesome 6, Chart.js
- **Design System**: Luminous Emerald/Teal (`#0d9488`, `#14b8a6`) & Deep Obsidian/Slate com suporte a Modo Escuro/Claro

---

## 🚀 Como Executar

```bash
# Navegar até à pasta do projeto
cd "Proyecto 115 - AI Business Assistant"

# Iniciar o servidor Flask
python app.py
```

Aceda através do browser: `http://localhost:6968`
