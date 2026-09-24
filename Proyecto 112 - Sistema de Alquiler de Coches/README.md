# Proyecto 112 - Sistema de Alquiler de Coches 🚗
**DrivePulse Rent-a-Car OS** — Plataforma Full-Stack Profissional de Gestão de Frotas, Reservas, Vistorias Digitais & Faturação

---

## 🌟 Funcionalidades Principais

1. **Gestão de Frota (Vehículos)**:
   - Controlo completo de viaturas por categoria (Premium, SUV, Desportivo, Elétrico, Compacto, Sedán).
   - Especificações detalhadas: quilometragem, nível de combustível/bateria, lugares, tipo de caixa (automático/manual).
   - Gestão de ciclo de estados: `Disponível`, `Alugado`, `Lavagem`, `Manutenção`.

2. **Diretório de Clientes (CRM Condutores)**:
   - Fichas completas de condutores com validação de carta de condução e data de validade.
   - Segmentação de clientes: `Particular`, `VIP`, `Empresa`.
   - Histórico acumulado de alugueres e notas operacionais.

3. **Motor de Disponibilidade em Tempo Real**:
   - Algoritmo de verificação de conflitos de datas de levantamento e devolução.
   - Filtro por categoria com cálculo automático de orçamento estimado e caução exigida.

4. **Ciclo de Reservas & Alugueres**:
   - Check-in e entrega de chaves com transição automática de estado do veículo.
   - Check-out e vistoria de retorno com registo de odómetro final e combustível.
   - Encaminhamento automático de viatura para lavagem/higienização após devolução.

5. **Contratos Digitais & Vistorias**:
   - Geração automática de contratos com identificador único (`CONT-2026-XXX`).
   - Apólices de seguro selecionáveis (Básico, Cobertura Total CDW VIP, Proteção Pneus & Vidros).
   - Registo inicial e final de quilometragem e depósito.

6. **Matriz de Tarifas & Preços Dinâmicos**:
   - Regras sazonais com multiplicadores dinâmicos (Época Alta, Fim de Semana, Longa Duração).
   - Simulador interativo de orçamentos no painel.

7. **Gestão Financeira & Pagamentos**:
   - Registo de pagamentos e cauções com referência única (`PAY-CAR-XXXX`).
   - Distinção entre faturação de aluguer e cauções retidas para segurança de franquia.

8. **Dashboard & KPIs Executivos**:
   - Indicadores de utilização de frota, receita faturada e cauções ativas.
   - Gráficos interativos em Chart.js (distribuição da frota e faturação semestral).
   - Alertas operacionais diários de entregas e devoluções.

---

## 🛠️ Stack Tecnológica

- **Backend**: Python 3 / Flask
- **Base de Dados**: SQLite3 com integridade referencial e chaves estrangeiras
- **Frontend**: HTML5, Tailwind CSS, FontAwesome 6, Chart.js
- **Design**: Cyber Blue (`#0284c7`) & Amber Gold (`#f59e0b`), suporte para modo escuro/claro e glassmorphism

---

## 🚀 Como Executar

```bash
# Navegar até à pasta do projeto
cd "Proyecto 112 - Sistema de Alquiler de Coches"

# Iniciar o servidor Flask
python app.py
```

Aceda através do browser: `http://localhost:6965`
