# Proyecto 113 - Plataforma de Servicios Locales 📍
**LocalPro Marketplace** — Plataforma Full-Stack de Conexão entre Clientes e Profissionais de Serviços Locais

---

## 🌟 Funcionalidades Principais

1. **Gestão de Profissionais**:
   - Diretório de técnicos e especialistas com categorias (*Electricidade*, *Canalização*, *Limpeza*, *Pintura*, *Climatização*, *Carpintaria*).
   - Selo de verificação de identidade e competências, anos de experiência e tarifas horárias.
   - Controlo dinâmico de disponibilidade de agenda (`Disponível` / `Ocupado`).

2. **Catálogo de Serviços**:
   - Serviços tabelados com preço fixo ou por hora e estimativa de duração.
   - Associação direta ao profissional responsável e botão de contratação imediata.

3. **Geolocalização & Cobertura (Ubicación)**:
   - Filtro e pesquisa por cidades de atuação (Lisboa, Porto, Braga, Faro, Cascais, etc.).
   - Raio de cobertura operacional por região.

4. **Motor de Búsqueda & Filtros**:
   - Filtro multidimensional por especialidade, cidade, avaliação mínima por estrelas (4.5+, 4.8+, 5.0) e disponibilidade imediata.

5. **Sistema de Reservas & Agendamentos**:
   - Fluxo completo de agendamento: seleção de serviço, morada, data e janela horária (manhã, almoço, tarde, fim de tarde).
   - Ciclo de estados operacionais: `Pendente` $\rightarrow$ `Confirmada` $\rightarrow$ `Em Andamento` $\rightarrow$ `Concluída` $\rightarrow$ `Cancelada`.

6. **Sistema de Avaliações & Reputação (Valoraciones)**:
   - Comentários e classificação de 1 a 5 estrelas por clientes verificados.
   - Recálculo automático da média de satisfação do profissional em tempo real.

7. **Mensagens & Chat em Tempo Real**:
   - Canal de comunicação direta entre clientes e profissionais para esclarecimento de dúvidas e envio de detalhes prévios à visita técnica.

8. **Dashboard & Métricas do Marketplace**:
   - KPIs de profissionais ativos, serviços agendados, volume financeiro transacionado e índice médio de satisfação.
   - Gráficos em Chart.js de distribuição por especialidade e evolução de pedidos.

---

## 🛠️ Stack Tecnológica

- **Backend**: Python 3 / Flask
- **Base de Dados**: SQLite3 com integridade referencial
- **Frontend**: HTML5, Tailwind CSS, FontAwesome 6, Chart.js
- **Design System**: Sunset Coral (`#f43f5e`) & Radiant Tangerine (`#f97316`), suporte para modo escuro/claro e design responsivo

---

## 🚀 Como Executar

```bash
# Navegar até à pasta do projeto
cd "Proyecto 113 - Plataforma de Servicios Locales"

# Iniciar o servidor Flask
python app.py
```

Aceda através do browser: `http://localhost:6966`
